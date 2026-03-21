"""
Python FastAPI - REST API with Oracle Database
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import oracledb

app = FastAPI(title="Python Oracle API")

# Oracle connection
DSN = "localhost:1521/orclpdb1"
POOL = oracledb.create_pool(user="system", password="password", dsn=DSN)

class Order(BaseModel):
    id: int
    customer: str
    amount: float

@app.get("/")
def root():
    return {"message": "Python API running"}

@app.get("/orders")
def get_orders():
    with POOL.acquire() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, customer, amount FROM orders")
        return [{"id": r[0], "customer": r[1], "amount": r[2]} for r in cursor]

@app.post("/orders")
def create_order(order: Order):
    with POOL.acquire() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders VALUES (:1, :2, :3)", 
                      (order.id, order.customer, order.amount))
        conn.commit()
    return {"message": "Order created"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
