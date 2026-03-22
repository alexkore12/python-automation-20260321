# Security Hardening Guide

## Python Automation API - Security Best Practices

This document outlines the security measures implemented in this FastAPI application and additional recommendations for production deployments.

## ✅ Implemented Security Features

### 1. Security Headers (Custom Implementation)

The API implements security headers similar to Helmet:

```python
from fastapi import Response

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response
```

**Headers implemented:**
- `X-Content-Type-Options` - Prevents MIME sniffing
- `X-Frame-Options` - Prevents clickjacking
- `X-XSS-Protection` - XSS filter
- `Strict-Transport-Security` - Enforces HTTPS
- `Referrer-Policy` - Controls referrer information

### 2. Rate Limiting (slowapi)

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/items")
@limiter.limit("50/minute")
async def get_items(request: Request):
    return {"items": []}
```

**Default limits:**
| Endpoint | Limit |
|----------|-------|
| `/`, `/health` | 200/min |
| `/orders` (list) | 50/min |
| `/orders/{id}` | 100/min |
| POST `/orders` | 30/min |
| PUT `/orders/{id}` | 30/min |
| DELETE `/orders/{id}` | 20/min |
| `/stats` | 30/min |

### 3. Input Validation (Pydantic)

```python
from pydantic import BaseModel, Field, field_validator

class OrderCreate(BaseModel):
    customer: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0, le=1000000)
    description: str = Field(..., min_length=1, max_length=500)
    
    @field_validator('customer')
    @classmethod
    def validate_customer(cls, v):
        if not v.strip():
            raise ValueError('Customer cannot be empty')
        return v.strip()
```

### 4. CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 5. SQL Injection Prevention

The API uses **parameterized queries** exclusively:

```python
# ✅ Safe - Parameterized query
async def get_order(pool, order_id: int):
    async with pool.acquire() as conn:
        cursor = await conn.cursor()
        await cursor.execute(
            "SELECT * FROM orders WHERE order_id = :1",
            [order_id]
        )
        return await cursor.fetchone()

# ❌ Unsafe - String concatenation (NEVER DO THIS)
# await cursor.execute(f"SELECT * FROM orders WHERE order_id = {order_id}")
```

## 🚀 Production Hardening Checklist

### Environment Variables

```bash
# Required
ORACLE_USER=prod_user
ORACLE_PASSWORD=<strong-password>
ORACLE_DSN=prod-db.example.com:1521/orclpdb1

# Security
ALLOWED_ORIGINS=https://yourdomain.com
RATE_LIMIT=50/minute
PORT=8000
LOG_LEVEL=warning

# Optional
DB_POOL_MIN=2
DB_POOL_MAX=20
REQUEST_TIMEOUT=30
```

### Oracle Database Security

1. **Use connection pooling**
```python
pool = oracledb.create_pool(
    user=ORACLE_USER,
    password=ORACLE_PASSWORD,
    dsn=ORACLE_DSN,
    min=2,
    max=20,
    timeout=30
)
```

2. **Enable SSL/TLS**
```python
pool = oracledb.create_pool(
    user=ORACLE_USER,
    password=ORACLE_PASSWORD,
    dsn=ORACLE_DSN,
    ssl=True,
    ssl_ca="/path/to/ca.pem"
)
```

3. **Use least privilege**
```sql
-- Create user with minimal permissions
CREATE USER api_user IDENTIFIED BY "strong_password";
GRANT CONNECT, RESOURCE TO api_user;
GRANT SELECT ON specific_table TO api_user;
```

### Authentication & Authorization

For production, implement JWT or OAuth2:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### Request Size Limits

```python
from fastapi import Request

@app.middleware("http")
async def limit_request_size(request: Request, call_next):
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > 10000:  # 10KB
        return Response(content="Request too large", status_code=413)
    return await call_next(request)
```

### Logging & Monitoring

```python
import logging
from logging.handlers import RotatingFileHandler

# Secure logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(
            'app.log',
            maxBytes=10485760,  # 10MB
            backupCount=5
        ),
        logging.StreamHandler()
    ]
)

# Don't log sensitive data
logger = logging.getLogger(__name__)
logger.info(f"User {user_id} logged in")  # ✅ Good
logger.info(f"Password: {password}")     # ❌ NEVER
```

### Docker Security

```dockerfile
# Use specific Python version
FROM python:3.11-slim

# Create non-root user
RUN useradd -m -u 1000 appuser

# Set working directory
WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Change ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

### Docker Compose with Security

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ORACLE_USER=${ORACLE_USER}
      - ORACLE_PASSWORD=${ORACLE_PASSWORD}
      - ORACLE_DSN=${ORACLE_DSN}
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
    networks:
      - backend

networks:
  backend:
    driver: bridge
```

## 🛡️ DDoS Protection

### With Nginx

```nginx
# Rate limiting
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

server {
    location / {
        limit_req zone=api_limit burst=20 nodelay;
        proxy_pass http://localhost:8000;
    }
}
```

## 📋 Compliance

For production, ensure:

- **GDPR** - Data protection (EU)
- **CCPA** - Consumer privacy
- **HIPAA** - Healthcare data (if applicable)
- **SOC 2** - Security controls

## 🔒 SSL/TLS Configuration

### Using Uvicorn with SSL

```bash
# Generate self-signed (development only)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365

# Run with SSL
uvicorn main:app --host 0.0.0.0 --port 8000 --ssl-keyfile key.pem --ssl-certfile cert.pem
```

### Production SSL (Nginx)

```nginx
server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🧪 Security Testing

```bash
# Dependency vulnerability scanning
pip audit
safety check

# Static analysis
bandit -r .
pylint --security=enabled .

# Dynamic testing
# Use OWASP ZAP, Burp Suite, or similar
```

## 🚨 Incident Response

1. **Detect** - Monitor for anomalies
2. **Contain** - Isolate affected systems
3. **Eradicate** - Remove threat
4. **Recover** - Restore services
5. **Lessons Learned** - Update security

---

**Last Updated:** March 2026
**Version:** 2.0
