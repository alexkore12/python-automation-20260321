# Python Automation API

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com)
[![Oracle](https://img.shields.io/badge/Oracle-Database- red.svg)](https://www.oracle.com/database/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Grype](https://img.shields.io/badge/Security-Grype-orange.svg)](.grype.yaml)

API REST de automatización con FastAPI y Oracle Database. Automatiza procesos empresariales con seguridad integrada y manejo robusto de errores.

## 📋 Descripción

Sistema de automatización de procesos empresariales construido con FastAPI, diseñado para:
- Gestión de órdenes y procesos de negocio
- Integración con Oracle Database
- APIs RESTful con validación estricta
- Rate limiting y seguridad empresarial
- Despliegue containerizado con Docker

## ✨ Características

- ⚡ **FastAPI** - API de alto rendimiento con validación Pydantic
- 🗄️ **Oracle Database** - Conexión pool de conexiones asíncrono
- 🔒 **Seguridad** - Helmet headers, rate limiting, CORS restringido
- ✅ **Validación** - Validación de entrada estricta anti-inyección SQL
- 📊 **Testing** - Suite completa de tests con pytest
- 🐳 **Docker Ready** - Imagen multi-stage optimizada
- 🔍 **Security Scanning** - Grype para vulnerabilidades

## 🚀 Instalación

### Prerequisites

- Python 3.11+
- Oracle Database 19c+ (o docker-compose para desarrollo)
- Oracle Instant Client (para conexión a BD)

### Instalación Local

```bash
# Clonar repositorio
git clone https://github.com/alexkore12/python-automation-20260321.git
cd python-automation-20260321

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con credenciales de Oracle

# Ejecutar
python main.py
```

### Docker Compose

```bash
# Iniciar con Oracle Database local
docker-compose up -d

# Ver logs
docker-compose logs -f api

# La API estará disponible en http://localhost:8080
# Swagger docs: http://localhost:8080/docs
```

## ⚙️ Configuración

### Variables de Entorno

| Variable | Descripción | Requerido |
|----------|-------------|-----------|
| `ORACLE_USER` | Usuario de Oracle | ✅ |
| `ORACLE_PASSWORD` | Password de Oracle | ✅ |
| `ORACLE_DSN` | Data Source Name | ✅ |
| `ALLOWED_ORIGINS` | Orígenes CORS (separados por coma) | No |
| `RATE_LIMIT` | Límite de requests | No |
| `LOG_LEVEL` | Nivel de logging | No |

### Ejemplo .env

```env
ORACLE_USER=automation_user
ORACLE_PASSWORD=SecurePassword123
ORACLE_DSN=localhost:1521/orclpdb1
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
RATE_LIMIT=100/minute
LOG_LEVEL=INFO
```

## 📖 API Endpoints

Una vez ejecutando, visita **http://localhost:8080/docs** para Swagger UI.

### Health Check

```bash
GET /health
# Response: {"status": "healthy", "timestamp": "...", "database": "connected"}
```

### Órdenes

```bash
GET /orders
# Lista todas las órdenes

GET /orders/{order_id}
# Obtiene orden específica

POST /orders
# Crea nueva orden
{
  "customer": "Empresa ABC",
  "amount": 1500.50,
  "description": "Pedido de marzo"
}

PUT /orders/{order_id}
# Actualiza orden existente

DELETE /orders/{order_id}
# Elimina orden
```

### Raíz

```bash
GET /
# Response: {"message": "...", "version": "2.0.0"}
```

## 🔐 Seguridad

### Headers de Seguridad

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000`

### Rate Limiting

Límite global: 100 requests por minuto (configurable)

### Validación de Entrada

- Sanitización de todos los inputs
- Bind variables para queries SQL (previene SQL injection)
- Validación de tipos y rangos con Pydantic
- Límite de longitud en campos de texto

### Escaneo de Vulnerabilidades

```bash
# Instalar Grype
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh

# Escanear imagen Docker
grype image python-automation:latest

# Escanear código fuente
grype fs .
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest -v

# Con coverage
pytest --cov=. --cov-report=html

# Tests específicos
pytest test_api.py::TestSecurityHeaders -v
pytest test_api.py::TestOrderValidation -v
```

### Cobertura de Tests

- **Security Headers** - Verifica headers de seguridad
- **Input Validation** - SQL injection, XSS, límites
- **Rate Limiting** - Verificación de límites
- **Endpoints** - Todos los endpoints
- **Order Validation** - Validación de órdenes
- **Error Handling** - Manejo de errores

## 🐳 Docker

### Build

```bash
docker build -t python-automation .
```

### Run

```bash
docker run -d \
  --name automation-api \
  -p 8080:8080 \
  --env-file .env \
  python-automation
```

### Multi-stage Build

El Dockerfile usa multi-stage build para:
1. Builder stage: instala dependencias
2. Production stage: imagen optimizada con solo runtime

## 📁 Estructura del Proyecto

```
python-automation-20260321/
├── .dockerignore
├── .env.example              # Variables de entorno
├── .gitattributes
├── .gitignore
├── .grype.yaml              # Configuración Grype
├── advanced_utils.py         # Utilidades para BD Oracle
├── CODE_OF_CONDUCT.md
├── CODEOWNERS
├── CONTRIBUTING.md
├── deploy.sh                 # Script de despliegue
├── docker-compose.yaml       # Oracle + API
├── Dockerfile                # Multi-stage build
├── health_check.py          # Verificación de salud
├── LICENSE
├── main.py                   # Aplicación FastAPI
├── README.md
├── requirements.txt
├── SECURITY.md
├── setup.sh                  # Inicialización
└── test_api.py              # Suite de tests
```

## 📈 Monitoreo

### Health Check

```bash
python health_check.py
```

### Verificar Estado

```bash
curl http://localhost:8080/health | jq
```

## 🤝 Contribuir

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Asegúrate que los tests pasan (`pytest`)
4. Commit tus cambios
5. Push y abre Pull Request

## 📝 Licencia

MIT - ver [LICENSE](LICENSE) para detalles.

---

⭐️ Dale una estrella si te fue útil!

⌨️ with ❤️ by [@alexkore12](https://github.com/alexkore12)
