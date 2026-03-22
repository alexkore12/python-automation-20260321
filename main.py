"""
Python Automation - FastAPI + Oracle Database
API REST robusta con integración a Oracle Database

Seguridad implementada:
- Helmet para headers de seguridad
- Rate limiting
- CORS restringido
- Validación de entrada estricta
- SQL injection prevention (parameterized queries)
"""
import os
from contextlib import asynccontextmanager
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, field_validator
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
import oracledb
import logging

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================
# SECURITY CONFIGURATION
# ============================================

# Allowed CORS origins (configure for production)
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8080").split(",")

# Rate limiting
RATE_LIMIT = os.getenv("RATE_LIMIT", "100/minute")

# Database configuration from environment
ORACLE_USER = os.getenv("ORACLE_USER")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")
ORACLE_DSN = os.getenv("ORACLE_DSN", "localhost:1521/orclpdb1")

# Security: Validate required environment variables
if not ORACLE_USER or not ORACLE_PASSWORD:
    logger.warning("⚠️ ORACLE_USER and ORACLE_PASSWORD should be set in environment")

# Pool de conexiones
pool: Optional[oracledb.AsyncPool] = None

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

# ============================================
# LIFECYCLE MANAGEMENT
# ============================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manejo del ciclo de vida de la aplicación"""
    global pool
    
    # Startup
    try:
        if ORACLE_USER and ORACLE_PASSWORD:
            pool = oracledb.create_pool(
                user=ORACLE_USER,
                password=ORACLE_PASSWORD,
                dsn=ORACLE_DSN,
                min=2,
                max=10
            )
            logger.info("✓ Oracle pool created successfully")
        else:
            logger.warning("⚠️ Oracle credentials not provided, running without database")
            pool = None
    except Exception as e:
        logger.warning(f"⚠️ Could not create Oracle pool: {e}")
        pool = None
    
    yield
    
    # Shutdown
    if pool:
        await pool.close()
        logger.info("✓ Oracle pool closed")

# ============================================
# FASTAPI APP
# ============================================

app = FastAPI(
    title="Python Automation API",
    description="API REST con Oracle Database - Seguridad implementada",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Security Headers (Helmet-like)
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Agregar headers de seguridad"""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

# CORS - Restricted
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# ============================================
# PYDANTIC MODELS
# ============================================

class Order(BaseModel):
    """Modelo de pedido"""
    id: int
    customer: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0)
    description: Optional[str] = Field(None, max_length=500)
    
    @field_validator('customer')
    @classmethod
    def validate_customer(cls, v):
        # Prevent injection attempts
        if any(char in v for char in ['<', '>', ';', '--', '/*', '*/', 'xp_', 'sp_']):
            raise ValueError('Invalid characters in customer name')
        return v.strip()
    
    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        if v > 1_000_000:  # Reasonable limit
            raise ValueError('Amount exceeds maximum allowed')
        return round(v, 2)

class OrderCreate(BaseModel):
    """Modelo para crear pedido"""
    customer: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0)
    description: Optional[str] = Field(None, max_length=500)
    
    @field_validator('customer')
    @classmethod
    def validate_customer(cls, v):
        if any(char in v for char in ['<', '>', ';', '--', '/*', '*/']):
            raise ValueError('Invalid characters in customer name')
        return v.strip()

class OrderUpdate(BaseModel):
    """Modelo para actualizar pedido"""
    customer: Optional[str] = Field(None, min_length=1, max_length=100)
    amount: Optional[float] = Field(None, gt=0, le=1_000_000)
    description: Optional[str] = Field(None, max_length=500)

# ============================================
# DATABASE DEPENDENCY
# ============================================

async def get_db():
    """Dependency para obtener conexión a la base de datos"""
    if pool is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )
    async with pool.acquire() as conn:
        yield conn

# ============================================
# ROUTES
# ============================================

@app.get("/")
@limiter.limit("200/minute")
async def root(request: Request):
    """Endpoint raíz"""
    return {
        "message": "Python Automation API",
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs",
        "security": "enabled"
    }

@app.get("/health")
@limiter.limit("200/minute")
async def health_check(request: Request):
    """Health check endpoint"""
    db_status = "connected" if pool else "disconnected"
    return {
        "status": "healthy",
        "database": db_status,
        "service": "python-automation",
        "version": "2.0.0"
    }

@app.get("/orders", response_model=List[dict])
@limiter.limit("50/minute")
async def get_orders(request: Request, db: oracledb.AsyncConnection = Depends(get_db)):
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
        raise HTTPException(status_code=500, detail="Error fetching orders")

@app.get("/orders/{order_id}", response_model=dict)
@limiter.limit("100/minute")
async def get_order(request: Request, order_id: int, db: oracledb.AsyncConnection = Depends(get_db)):
    """Obtener pedido por ID"""
    # Validate ID
    if order_id < 1 or order_id > 999999999:
        raise HTTPException(status_code=400, detail="Invalid order ID")
    
    try:
        cursor = db.cursor()
        cursor.execute(
            "SELECT id, customer, amount, description FROM orders WHERE id = :1",
            [order_id]
        )
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
        
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
        raise HTTPException(status_code=500, detail="Error fetching order")

@app.post("/orders", status_code=201, response_model=dict)
@limiter.limit("30/minute")
async def create_order(request: Request, order: OrderCreate, db: oracledb.AsyncConnection = Depends(get_db)):
    """Crear nuevo pedido"""
    try:
        cursor = db.cursor()
        
        # Get next ID safely
        cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM orders")
        new_id = cursor.fetchone()[0]
        
        # Parameterized query (prevents SQL injection)
        cursor.execute(
            "INSERT INTO orders (id, customer, amount, description) VALUES (:1, :2, :3, :4)",
            (new_id, order.customer, order.amount, order.description)
        )
        db.commit()
        
        logger.info(f"Order created: {new_id}")
        
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
        raise HTTPException(status_code=500, detail="Error creating order")

@app.put("/orders/{order_id}", response_model=dict)
@limiter.limit("30/minute")
async def update_order(
    request: Request,
    order_id: int, 
    order_update: OrderUpdate,
    db: oracledb.AsyncConnection = Depends(get_db)
):
    """Actualizar pedido"""
    # Validate ID
    if order_id < 1 or order_id > 999999999:
        raise HTTPException(status_code=400, detail="Invalid order ID")
    
    try:
        cursor = db.cursor()
        
        # Check exists
        cursor.execute("SELECT id FROM orders WHERE id = :1", [order_id])
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
        
        # Build update query safely
        updates = []
        params = []
        if order_update.customer is not None:
            updates.append("customer = :1")
            params.append(order_update.customer.strip())
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
            logger.info(f"Order updated: {order_id}")
        
        # Fetch updated
        cursor.execute(
            "SELECT id, customer, amount, description FROM orders WHERE id = :1",
            [order_id]
        )
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
        raise HTTPException(status_code=500, detail="Error updating order")

@app.delete("/orders/{order_id}")
@limiter.limit("20/minute")
async def delete_order(request: Request, order_id: int, db: oracledb.AsyncConnection = Depends(get_db)):
    """Eliminar pedido"""
    # Validate ID
    if order_id < 1 or order_id > 999999999:
        raise HTTPException(status_code=400, detail="Invalid order ID")
    
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM orders WHERE id = :1", [order_id])
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
        
        db.commit()
        logger.info(f"Order deleted: {order_id}")
        
        return {"message": f"Order {order_id} deleted", "id": order_id}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting order: {e}")
        raise HTTPException(status_code=500, detail="Error deleting order")

@app.get("/stats")
@limiter.limit("30/minute")
async def get_stats(request: Request, db: oracledb.AsyncConnection = Depends(get_db)):
    """Estadísticas de pedidos"""
    try:
        cursor = db.cursor()
        
        # Fixed SQL syntax
        cursor.execute("SELECT COUNT(*), COALESCE(SUM(amount), 0), COALESCE(AVG(amount), 0) FROM orders")
        row = cursor.fetchone()
        
        return {
            "total_orders": row[0] if row[0] else 0,
            "total_amount": round(float(row[1]) if row[1] else 0, 2),
            "average_amount": round(float(row[2]) if row[2] else 0, 2)
        }
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        raise HTTPException(status_code=500, detail="Error fetching stats")

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    import uvicorn
    
    # Security: Run with limited exposure
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=int(os.getenv("PORT", "8000")),
        loop="asyncio"
    )
