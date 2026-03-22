# Python Automation API

API REST desarrollada con FastAPI para automatización de procesos con integración a Oracle Database.

## ⚠️ Nota sobre Escáneres de Seguridad

**Marzo 2026**: Este proyecto usa **Grype** como escáner de vulnerabilidades en lugar de Trivy, debido al ataque a la cadena de suministro de Trivy (2° ataque en Marzo 2026).

## Versión 2.1 - Seguridad y Testing Mejorados

Esta versión incluye implementaciones de seguridad robustas y tests completos:

### 🔒 Características de Seguridad

| Feature | Implementación |
|---------|----------------|
| **Helmet-style Headers** | X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, HSTS |
| **Rate Limiting** | slowapi con límites por endpoint |
| **CORS Restringido** | Orígenes configurables via entorno |
| **SQL Injection Prevention** | Parameterized queries siempre |
| **Input Validation** | Pydantic con validación estricta |
| **Request Size Limits** | Validación de campos |
| **XSS Protection** | Sanitización de entrada |
| **GitHub Actions** | CI/CD con Grype para escaneo |

## 🤖 GitHub Actions

El proyecto incluye workflows de CI/CD con seguridad automatizada:

### Workflows Incluidos

| Workflow | Descripción | Frecuencia |
|----------|-------------|------------|
| `security.yml` | Escaneo de vulnerabilidades (Grype) | Push + Daily |
| | Verifica dependencias (pip-audit) | |
| | Escaneo de imágenes Docker | |
| | Tests automatizados | |

### Ver Resultados de Seguridad

Los resultados están disponibles en:
- **GitHub Security** > **Vulnerability alerts**
- **Actions** > **Security Scan**

## 🚀 Inicio Rápido

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

## 📡 Endpoints

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

## 🧪 Testing

```bash
# Instalar dependencias de test
pip install pytest pytest-asyncio httpx

# Ejecutar tests
pytest test_api.py -v

# Con coverage
pytest test_api.py --cov=. --cov-report=html
```

### Tests Incluidos

- ✅ **Security Headers** - Verificación de headers de seguridad
- ✅ **Input Validation** - Pruebas de validación de entrada
- ✅ **SQL Injection Prevention** - Pruebas de sanitización
- ✅ **Rate Limiting** - Verificación de límites
- ✅ **Error Handling** - Pruebas de manejo de errores

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

## 📁 Estructura

```
python-automation-20260321/
├── main.py                   # Aplicación principal
├── advanced_utils.py         # Utilidades avanzadas
├── test_api.py              # Tests de API (v2.1)
├── requirements.txt          # Dependencias
├── Dockerfile                # Imagen Docker
├── SECURITY.md               # Políticas de seguridad
├── .github/
│   └── workflows/
│       └── security.yml      # CI/CD con Grype
└── README.md                 # Este archivo
```

## 🛡️ Validación de Entrada

### Protecciones Implementadas

1. **SQL Injection Prevention**
   - Validación de caracteres sospechosos (`<`, `>`, `;`, `--`, `/*`, `*/`)
   - Parameterized queries en todas las consultas
   - Sanitización de entrada

2. **XSS Prevention**
   - Rechazo de contenido con `<script>` tags
   - Validación de longitud de strings

3. **Business Logic Validation**
   - Amount debe ser positivo y menor a 1,000,000
   - Customer name: 1-100 caracteres
   - Description: máximo 500 caracteres

## ⚠️ Notas de Seguridad para Producción

1. ✅ Cambiar `ALLOWED_ORIGINS` a dominios específicos
2. ✅ Usar credenciales fuertes para Oracle
3. ✅ Habilitar SSL/TLS
4. ✅ Configurar rate limits apropiados
5. ✅ Revisar logs regularmente
6. ✅ Ejecutar tests antes de deploy
7. ✅ Usar environment variables para secrets

## 📝 Changelog

### v2.1.0 (2026-03-22)
- ✅ Suite completa de tests (test_api.py)
- ✅ Tests de security headers
- ✅ Tests de SQL injection prevention
- ✅ Tests de validación de entrada
- ✅ Tests de rate limiting

### v2.0.0 (2026-03-21)
- ✅ Headers de seguridad Helmet-style
- ✅ Rate limiting con slowapi
- ✅ CORS restringido
- ✅ Validación estricta con Pydantic

## Tech Stack

- FastAPI
- Pydantic
- slowapi (rate limiting)
- oracledb
- uvicorn
- pytest (testing)

## 📄 Licencia

MIT - Alejandro Kore

## 🤖 Actualizado por

OpenClaw AI Assistant - 2026-03-22
*Mejoras: GitHub Actions con Grype, Suite completa de tests v2.1*