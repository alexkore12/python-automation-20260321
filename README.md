# ⚙️ Python Automation API

> API REST completa con FastAPI y Oracle Database — Gestión de pedidos, seguridad JWT, rate limiting y despliegues containerizados.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com)
[![Oracle](https://img.shields.io/badge/Oracle-Database- red.svg)](https://oracle.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![Security: Grype](https://img.shields.io/badge/Security-Grype-orange.svg)](.grype.yaml)

## 📋 Descripción

API REST de producción construida con **FastAPI** e **Oracle Database** para gestión de pedidos (orders). Implementa seguridad robusta incluyendo autenticación JWT, rate limiting, validación de entrada estricta y prevención de SQL injection.

## ✨ Características

- ⚡ **Alto Rendimiento** — FastAPI + Uvicorn con async/await
- 🗄️ **Oracle Database** — Pool de conexiones asíncrono con oracledb
- 🔒 **Seguridad Completa** — Helmet headers, CORS, rate limiting, JWT
- 🛡️ **SQL Injection Prevention** — Parameterized queries y validación de entrada
- 📝 **Documentación Automática** — Swagger UI (`/docs`) y ReDoc (`/redoc`)
- 📊 **API REST Completa** — CRUD de pedidos, estadísticas y health checks
- 🐳 **Docker Ready** — Multi-stage builds con Docker y Docker Compose
- 🔍 **Security Scanning** — Grype para escaneo de vulnerabilidades en CI
- ✅ **Testing** — Suite completa con pytest y tests de seguridad
- 📈 **Rate Limiting** — SlowAPI para proteger endpoints críticos

## 🚀 Instalación

### Prerrequisitos

- Python 3.11+
- Oracle Database (local o remoto)
- Docker (opcional)

### Instalación Local

```bash
# Clonar el repositorio
git clone https://github.com/alexkore12/python-automation-20260321.git
cd python-automation-20260321

# Crear entorno virtual
python -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales de Oracle
```

### Ejecutar

```bash
# Servidor de desarrollo (auto-reload)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Producción
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker

```bash
# Construir imagen
docker build -t python-automation-api .

# Ejecutar
docker run -p 8000:8000 --env-file .env python-automation-api
```

### Docker Compose

```bash
docker-compose up -d
```

## 📖 API Endpoints

### Raíz y Health

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Información de la API |
| GET | `/health` | Health check con estado de BD |

### Pedidos (Orders)

| Método | Endpoint | Descripción | Rate Limit |
|--------|----------|-------------|------------|
| GET | `/orders` | Listar todos los pedidos | 50/min |
| GET | `/orders/{id}` | Obtener pedido por ID | 100/min |
| POST | `/orders` | Crear nuevo pedido | 30/min |
| PUT | `/orders/{id}` | Actualizar pedido | 30/min |
| DELETE | `/orders/{id}` | Eliminar pedido | 20/min |
| GET | `/stats` | Estadísticas de pedidos | 30/min |

### Documentación

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## ⚙️ Configuración

### Variables de Entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| `ORACLE_USER` | Usuario de Oracle | **Requerido** |
| `ORACLE_PASSWORD` | Contraseña de Oracle | **Requerido** |
| `ORACLE_DSN` | Data Source Name | `localhost:1521/orclpdb1` |
| `HOST` | Host del servidor | `0.0.0.0` |
| `PORT` | Puerto del servidor | `8000` |
| `ALLOWED_ORIGINS` | CORS orígenes (comma sep.) | `*` |
| `RATE_LIMIT` | Rate limit global | `100/minute` |
| `LOG_LEVEL` | Nivel de logging | `INFO` |

### Rate Limits por Endpoint

| Endpoint | Límite |
|----------|--------|
| `/` | 200/min |
| `/health` | 200/min |
| `/orders` (GET) | 50/min |
| `/orders/{id}` (GET) | 100/min |
| `/orders` (POST) | 30/min |
| `/orders/{id}` (PUT) | 30/min |
| `/orders/{id}` (DELETE) | 20/min |
| `/stats` | 30/min |

## 🔒 Seguridad

### Headers de Seguridad

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000`
- `Referrer-Policy: strict-origin-when-cross-origin`

### Validación de Entrada

- **Customer name**: 1-100 caracteres, sin caracteres especiales (`<`, `>`, `;`, `--`)
- **Amount**: > 0, <= 1,000,000
- **Order ID**: 1 - 999,999,999
- **Todas las queries usan parameterized queries** (previene SQL injection)

### CORS

Configurable via `ALLOWED_ORIGINS`. Por defecto permite `localhost:3000` y `localhost:8080`.

## 📁 Estructura del Proyecto

```
python-automation-20260321/
├── main.py              # FastAPI app + Oracle DB integration
├── advanced_utils.py    # Utilidades: ConfigManager, TaskScheduler, etc.
├── health_check.py      # Script CLI de health check
├── test_api.py          # Suite de tests con pytest
├── requirements.txt     # Dependencias Python
├── Dockerfile
├── docker-compose.yaml
├── .env.example
├── .grype.yaml         # Config de escaneo Grype
├── .github/workflows/   # GitHub Actions CI/CD
├── SECURITY.md
├── CONTRIBUTING.md
└── README.md
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest -v

# Con coverage
pytest --cov=. --cov-report=html

# Tests específicos
pytest test_api.py::TestSecurityHeaders -v
pytest test_api.py::TestInputValidation -v
```

### Suites de Test

- **TestSecurityHeaders** — Verifica headers de seguridad
- **TestInputValidation** — SQL injection, XSS, límites de validación
- **TestRateLimiting** — Rate limits por endpoint
- **TestEndpoints** — CRUD de pedidos
- **TestErrorHandling** — Casos de error

## 📈 CI/CD

GitHub Actions incluido:

```yaml
- Lint: ruff + flake8
- Tests: pytest con coverage
- Security: Grype vulnerability scan
- Docker: build + push
```

## 🚨 Troubleshooting

### Oracle connection failed

**Problema:** `ORA-...` errors  
**Solución:** Verifica `ORACLE_USER`, `ORACLE_PASSWORD` y `ORACLE_DSN` en `.env`.

### Rate limit exceeded

**Problema:** `429 Too Many Requests`  
**Solución:** Espera o aumenta `RATE_LIMIT` en `.env`.

### CORS errors en el navegador

**Problema:** `Access-Control-Allow-Origin` missing  
**Solución:** Agrega tu dominio a `ALLOWED_ORIGINS` en `.env`.

## 🛠️ Utilidades Incluidas

### Health Check CLI

```bash
python health_check.py
```

Salida:
```
🔍 Python Automation - Health Check
✅ service: healthy
⏭️  database: skipped (no credentials)
✅ environment: healthy
Overall: HEALTHY
```

### Advanced Utils

```python
from advanced_utils import ConfigManager, TaskScheduler, DataProcessor

# Configuración centralizada
config = ConfigManager('config.yaml')
db_host = config.get('database.host', 'localhost')

# Scheduling de tareas
scheduler = TaskScheduler()
scheduler.add_task(backup_function, 'daily')
scheduler.run_continuously()

# Procesamiento de datos
processor = DataProcessor()
batch_results = list(processor.batch_process(items, batch_size=100))
```

## 🤝 Contribuir

1. Fork el repositorio
2. Crear branch: `git checkout -b feature/nueva-caracteristica`
3. Commit: `git commit -am 'Agregar característica'`
4. Push: `git push origin feature/nueva-caracteristica`
5. Abrir Pull Request

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

## 📝 Licencia

MIT License - ver [LICENSE](LICENSE) para detalles.

## 🔗 Enlaces Útiles

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Oracle DB Python Driver](https://oracle.github.io/python-oracledb/)
- [SlowAPI Rate Limiting](https://github.com/laurentS/slowapi)
- [Grype Vulnerability Scanner](https://github.com/anchore/grype)
