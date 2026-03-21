"""
Python Automation - FastAPI + Oracle Database
API REST robusta con integración a Oracle Database
"""
import os
from contextlib import asynccontextmanager
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
import oracledb
import logging

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración desde environment
ORACLE_USER = os.getenv("ORACLE_USER", "system")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD", "password")
ORACLE_DSN = os.getenv("ORACLE_DSN", "localhost:1521/orclpdb1")

# Pool de conexiones
pool: Optional[oracledb.AsyncPool] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manejo del ciclo de vida de la aplicación"""
    global pool
    try:
        pool = oracledb.create_pool(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=ORACLE_DSN,
            min=2,
            max=10
        )
        logger.info("Oracle pool created successfully")
    except Exception as e:
        logger.warning(f"Could not create Oracle pool: {e}")
        pool = None
    
    yield
    
    if pool:
        await pool.close()
        logger.info("Oracle pool closed")

app = FastAPI(
    title="Python Automation API",
    description="API REST con Oracle Database",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class Order(BaseModel):
    id: int
    customer: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0)
    description: Optional[str] = None
    
    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        return round(v, 2)

class OrderCreate(BaseModel):
    customer: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0)
    description: Optional[str] = None

class OrderUpdate(BaseModel):
    customer: Optional[str] = Field(None, min_length=1, max_length=100)
    amount: Optional[float] = Field(None, gt=0)
    description: Optional[str] = None

# Database dependency
async def get_db():
    if pool is None:
        raise HTTPException(503, "Database not available")
    async with pool.acquire() as conn:
        yield conn

# Routes
@app.get("/")
async def root():
    return {
        "message": "Python Automation API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    db_status = "connected" if pool else "disconnected"
    return {
        "status": "healthy",
        "database": db_status,
        "service": "python-automation"
    }

@app.get("/orders", response_model=List[dict])
async def get_orders(db: oracledb.AsyncConnection = Depends(get_db)):
    """Listar todos los pedidos"""
    try:
        cursor = db.cursor()
        cursor.execute("SELECT id, customer, amount, description FROM orders ORDER BY id")
        rows = cursor.fetchall()
        return [
            {
                "id": r[0],
                "customer": r[1],
                "amount": float(r[2]) if r[2] else 0,
                "description": r[3]
            }
            for r in rows
        ]
    except oracledb.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(500, "Error fetching orders")

@app.get("/orders/{order_id}", response_model=dict)
async def get_order(order_id: int, db: oracledb.AsyncConnection = Depends(get_db)):
    """Obtener pedido por ID"""
    try:
        cursor = db.cursor()
        cursor.execute("SELECT id, customer, amount, description FROM orders WHERE id = :1", [order_id])
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(404, f"Order {order_id} not found")
        
        return {
            "id": row[0],
            "customer": row[1],
            "amount": float(row[2]) if row[2] else 0,
            "description": row[3]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(500, "Error fetching order")

@app.post("/orders", status_code=201, response_model=dict)
async def create_order(order: OrderCreate, db: oracledb.AsyncConnection = Depends(get_db)):
    """Crear nuevo pedido"""
    try:
        cursor = db.cursor()
        
        # Get next ID
        cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM orders")
        new_id = cursor.fetchone()[0]
        
        cursor.execute(
            "INSERT INTO orders (id, customer, amount, description) VALUES (:1, :2, :3, :4)",
            (new_id, order.customer, order.amount, order.description)
        )
        db.commit()
        
        return {
            "id": new_id,
            "customer": order.customer,
            "amount": order.amount,
            "description": order.description,
            "message": "Order created successfully"
        }
    except oracledb.Error as e:
        db.rollback()
        logger.error(f"Error creating order: {e}")
        raise HTTPException(500, "Error creating order")

@app.put("/orders/{order_id}", response_model=dict)
async def update_order(
    order_id: int, 
    order_update: OrderUpdate,
    db: oracledb.AsyncConnection = Depends(get_db)
):
    """Actualizar pedido"""
    try:
        cursor = db.cursor()
        
        # Check exists
        cursor.execute("SELECT id FROM orders WHERE id = :1", [order_id])
        if not cursor.fetchone():
            raise HTTPException(404, f"Order {order_id} not found")
        
        # Build update query
        updates = []
        params = []
        if order_update.customer is not None:
            updates.append("customer = :1")
            params.append(order_update.customer)
        if order_update.amount is not None:
            updates.append("amount = :2")
            params.append(order_update.amount)
        if order_update.description is not None:
            updates.append("description = :3")
            params.append(order_update.description)
        
        if updates:
            params.append(order_id)
            query = f"UPDATE orders SET {', '.join(updates)} WHERE id = :{len(params)}"
            cursor.execute(query, params)
            db.commit()
        
        # Fetch updated
        cursor.execute("SELECT id, customer, amount, description FROM orders WHERE id = :1", [order_id])
        row = cursor.fetchone()
        
        return {
            "id": row[0],
            "customer": row[1],
            "amount": float(row[2]) if row[2] else 0,
            "description": row[3]
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating order: {e}")
        raise HTTPException(500, "Error updating order")

@app.delete("/orders/{order_id}")
async def delete_order(order_id: int, db: oracledb.AsyncConnection = Depends(get_db)):
    """Eliminar pedido"""
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM orders WHERE id = :1", [order_id])
        
        if cursor.rowcount == 0:
            raise HTTPException(404, f"Order {order_id} not found")
        
        db.commit()
        return {"message": f"Order {order_id} deleted", "id": order_id}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting order: {e}")
        raise HTTPException(500, "Error deleting order")

@app.get("/stats")
async def get_stats(db: oracledb.AsyncConnection = Depends(get_db)):
    """Estadísticas de pedidos"""
    try:
        cursor = db.cursor()
        
        cursor.execute("SELECT COUNT(*), COALESCE(SUM(amount), 0), COALESCE(AVG(amount), 0) FROM orders")
        row = cursor.fetchone()
        
        return {
            "total_orders": row[0] if row[0] else 0,
            "total_amount": round(float(row[1]) if row[1] else 0, 2),
            "average_amount": round(float(row[2]) if row[2] else 0, 2)
        }
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        raise HTTPException(500, "Error fetching stats")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
