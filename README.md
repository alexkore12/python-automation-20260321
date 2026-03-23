# Python Automation API

API REST desarrollada con FastAPI para automatización de procesos con integración a Oracle Database.

Esta versión incluye implementaciones de seguridad robustas y tests completos.

## Características de Seguridad

| Feature | Implementación |
|---------|----------------|
| Helmet-style Headers | X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, HSTS |
| Rate Limiting | slowapi con límites por endpoint |
| CORS Restringido | Orígenes configurables via entorno |
| SQL Injection Prevention | Parameterized queries siempre |
| Input Validation | Pydantic con validación estricta |
| Request Size Limits | Validación de campos |
| XSS Protection | Sanitización de entrada |

## Instalación

```bash
pip install -r requirements.txt
```

## Configuración

### Variables de Entorno Requeridas

```bash
export ORACLE_USER="system"
export ORACLE_PASSWORD="your_secure_password"
export ORACLE_DSN="localhost:1521/orclpdb1"
```

### Variables de Entorno Opcionales

```bash
export ALLOWED_ORIGINS="http://localhost:3000,https://yourdomain.com"
export RATE_LIMIT="100/minute"
export PORT=8000
```

## Uso

### Desarrollo

```bash
python main.py
```

### Producción

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker

```bash
docker build -t python-automation .
docker run -p 8000:8000 \
  -e ORACLE_USER=system \
  -e ORACLE_PASSWORD=pass \
  -e ORACLE_DSN=host:1521/orclpdb1 \
  python-automation
```

## API Endpoints

### Health & Info

| Método | Endpoint | Descripción | Rate Limit |
|--------|----------|-------------|------------|
| GET | `/` | Información del API | 200/min |
| GET | `/health` | Health check | 200/min |

### Orders (CRUD)

| Método | Endpoint | Descripción | Rate Limit |
|--------|----------|-------------|------------|
| GET | `/orders` | Listar pedidos | 50/min |
| GET | `/orders/{id}` | Obtener pedido | 100/min |
| POST | `/orders` | Crear pedido | 30/min |
| PUT | `/orders/{id}` | Actualizar pedido | 30/min |
| DELETE | `/orders/{id}` | Eliminar pedido | 20/min |

### Statistics

| Método | Endpoint | Descripción | Rate Limit |
|--------|----------|-------------|------------|
| GET | `/stats` | Estadísticas | 30/min |

## Ejemplos

### Crear Pedido

```json
{
  "customer": "Empresa ABC",
  "amount": 1500.50,
  "description": "Pedido de ejemplo"
}
```

### Actualizar Pedido

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

## Estructura del Proyecto

```
python-automation-20260321/
├── main.py                 # Aplicación principal
├── test_api.py             # Suite de tests (v2.1)
├── requirements.txt        # Dependencias
├── Dockerfile              # Imagen Docker
├── .env.example            # Ejemplo de configuración
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions
└── README.md                # Este archivo
```

## Seguridad

### SQL Injection Prevention

- Validación de caracteres sospechosos (, ;, --, /*, */)
- Parameterized queries en todas las consultas
- Sanitización de entrada

### XSS Prevention

- Rechazo de contenido con tags `<script>`
- Validación de longitud de strings

### Business Logic Validation

- Amount debe ser positivo y menor a 1,000,000
- Customer name: 1-100 caracteres
- Description: máximo 500 caracteres

## Mejores Prácticas de Producción

- ✅ Cambiar `ALLOWED_ORIGINS` a dominios específicos
- ✅ Usar credenciales fuertes para Oracle
- ✅ Habilitar SSL/TLS
- ✅ Configurar rate limits apropiados
- ✅ Revisar logs regularmente
- ✅ Ejecutar tests antes de deploy
- ✅ Usar environment variables para secrets

## Tests

###安装依赖

```bash
pip install pytest pytest-asyncio httpx
```

###Ejecutar tests

```bash
pytest test_api.py -v
```

###Con coverage

```bash
pytest test_api.py --cov=. --cov-report=html
```

###Cobertura de Tests

| Categoría | Tests |
|-----------|-------|
| Security Headers | ✅ Verificación de headers de seguridad |
| Input Validation | ✅ Pruebas de validación de entrada |
| SQL Injection Prevention | ✅ Pruebas de sanitización |
| Rate Limiting | ✅ Verificación de límites |
| Error Handling | ✅ Pruebas de manejo de errores |

## GitHub Actions CI/CD

El proyecto incluye workflow automático:

```yaml
# .github/workflows/ci.yml
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest test_api.py -v
```

## Changelog

- ✅ v2.1 - Suite completa de tests, validación mejorada
- ✅ v2.0 - Headers de seguridad, rate limiting
- ✅ v1.0 - Versión inicial

## Dependencias

- FastAPI
- Pydantic
- slowapi (rate limiting)
- oracledb
- uvicorn
- pytest (testing)

## Licencia

MIT - Alejandro Kore

## Autor

OpenClaw AI Assistant - 2026-03-22
