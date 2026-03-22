# Python Automation API

API REST desarrollada con FastAPI para automatización de procesos con integración a Oracle Database.

## Versión 2.0 - Seguridad Mejorada

Esta versión incluye implementaciones de seguridad robustas:

### 🔒 Características de Seguridad

| Feature | Implementación |
|---------|----------------|
| **Helmet-style Headers** | X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, HSTS |
| **Rate Limiting** | slowapi con límites por endpoint |
| **CORS Restringido** | Orígenes configurables via entorno |
| **SQL Injection Prevention** | Parameterized queries siempre |
| **Input Validation** | Pydantic con validación estricta |
| **Request Size Limits** | Validación de campos |

##快速开始

### Requisitos

```bash
pip install -r requirements.txt
```

### Configuración

```bash
# Variables de entorno requeridas
export ORACLE_USER="system"
export ORACLE_PASSWORD="your_secure_password"
export ORACLE_DSN="localhost:1521/orclpdb1"

# Opcional
export ALLOWED_ORIGINS="http://localhost:3000,https://yourdomain.com"
export RATE_LIMIT="100/minute"
export PORT=8000
```

### Ejecutar

```bash
# Desarrollo
python main.py

# Producción
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker

```bash
docker build -t python-automation .
docker run -p 8000:8000 -e ORACLE_USER=system -e ORACLE_PASSWORD=pass -e ORACLE_DSN=host:1521/orclpdb1 python-automation
```

## Endpoints

| Método | Endpoint | Descripción | Rate Limit |
|--------|----------|-------------|------------|
| GET | `/` | Información del API | 200/min |
| GET | `/health` | Health check | 200/min |
| GET | `/orders` | Listar pedidos | 50/min |
| GET | `/orders/{id}` | Obtener pedido | 100/min |
| POST | `/orders` | Crear pedido | 30/min |
| PUT | `/orders/{id}` | Actualizar pedido | 30/min |
| DELETE | `/orders/{id}` | Eliminar pedido | 20/min |
| GET | `/stats` | Estadísticas | 30/min |

## Modelos

### OrderCreate
```json
{
  "customer": "Empresa ABC",
  "amount": 1500.50,
  "description": "Pedido de ejemplo"
}
```

### OrderUpdate
```json
{
  "amount": 2000.00
}
```

## Headers de Seguridad

La API incluye los siguientes headers de seguridad:

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Referrer-Policy: strict-origin-when-cross-origin
```

## Rate Limiting

Por defecto:
- `/` y `/health`: 200/min
- `/orders` (list): 50/min
- `/orders/{id}`: 100/min
- POST `/orders`: 30/min
- PUT `/orders/{id}`: 30/min
- DELETE `/orders/{id}`: 20/min
- `/stats`: 30/min

Personalizar con variable `RATE_LIMIT`.

## Desarrollo

### Estructura

```
python-automation-20260321/
├── main.py          # Aplicación principal
├── requirements.txt # Dependencias
├── Dockerfile       # Imagen Docker
└── README.md        # Este archivo
```

### Tests

```bash
# Test básico
curl http://localhost:8000/health

# Crear pedido
curl -X POST http://localhost:8000/orders \
  -H "Content-Type: application/json" \
  -d '{"customer": "Test", "amount": 100}'
```

## Notas de Seguridad

⚠️ **Producción**:
1. Cambiar `ALLOWED_ORIGINS` a dominios específicos
2. Usar credenciales fuertes para Oracle
3. Habilitar SSL/TLS
4. Configurar rate limits apropiados
5. Revisar logs regularmente

## Logs

```bash
# Ver logs
tail -f uvicorn.log
```

## Tech Stack

- FastAPI
- Pydantic
- slowapi (rate limiting)
- oracledb
- uvicorn
