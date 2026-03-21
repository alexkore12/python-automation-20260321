# 🐍 Python Automation API

API REST con FastAPI para automatización de procesos, integrada con Oracle Database.

## 📋 Descripción

API RESTful de alto rendimiento construida con FastAPI que proporciona endpoints para gestión de pedidos (orders) con persistencia en Oracle Database. Ideal para sistemas de automatización empresarial.

## 🛠️ Características

- ✅ **FastAPI** - Framework moderno y rápido
- ✅ **Oracle Database** - Persistencia robusta con connection pooling
- ✅ **Pydantic** - Validación de datos
- ✅ **CORS** - Soporte para cross-origin configurable
- ✅ **Connection Pool** - Optimización de conexiones
- ✅ **Logging** - Registro estructurado
- ✅ **Health Checks** - Monitoreo de estado
- ✅ **Paginación** - Soporte para paginar resultados
- ✅ **Documentación Auto** - OpenAPI/Swagger

## 🚀 Instalación Local

### Prerrequisitos

- Python 3.9+
- Oracle Database (local o remoto)

### Pasos

```bash
# 1. Clonar
git clone https://github.com/alexkore12/python-automation-20260321.git
cd python-automation-20260321

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Edita .env con tus credenciales

# 5. Ejecutar
python main.py
```

La API estará disponible en:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🐳 Docker

### Build

```bash
docker build -t python-automation-api .
```

### Ejecutar con Oracle

```bash
docker run -d \
  -p 8000:8000 \
  -e ORACLE_USER=system \
  -e ORACLE_PASSWORD=password \
  -e ORACLE_DSN=oracle:1521/orclpdb1 \
  python-automation-api
```

### Docker Compose

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
    depends_on:
      - oracle

  oracle:
    image: container-registry.oracle.com/database/express:latest
    ports:
      - "1521:1521"
    environment:
      - ORACLE_PWD=password
```

## 📡 Endpoints

### Health & Status

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Información base de la API |
| GET | `/health` | Health check con estado de DB |

### Orders

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/orders` | Listar pedidos (con paginación) |
| GET | `/orders/{id}` | Obtener pedido por ID |
| POST | `/orders` | Crear nuevo pedido |
| PUT | `/orders/{id}` | Actualizar pedido |
| DELETE | `/orders/{id}` | Eliminar pedido |

### Stats

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/stats` | Estadísticas de pedidos |

## 📝 Modelos de Datos

### OrderCreate
```json
{
  "customer": "Juan Pérez",
  "amount": 150.50,
  "description": "Pedido de ejemplo"
}
```

### OrderUpdate
```json
{
  "customer": "Juan Actualizado",
  "amount": 200.00
}
```

### Response Example
```json
{
  "id": 1,
  "customer": "Juan Pérez",
  "amount": 150.50,
  "description": "Pedido de ejemplo",
  "message": "Order created successfully"
}
```

## ⚙️ Configuración

### Variables de Entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| `ORACLE_USER` | Usuario de Oracle | (requerido) |
| `ORACLE_PASSWORD` | Password de Oracle | (requerido) |
| `ORACLE_DSN` | Data Source Name | localhost:1521/orclpdb1 |
| `HOST` | Host del servidor | 0.0.0.0 |
| `PORT` | Puerto del servidor | 8000 |
| `CORS_ORIGINS` | Orígenes CORS permitidos | * |
| `LOG_LEVEL` | Nivel de logging | INFO |

### Paginación

```bash
# Obtener primeros 10 pedidos
curl "http://localhost:8000/orders?skip=0&limit=10"

# Obtener siguientes 10
curl "http://localhost:8000/orders?skip=10&limit=10"
```

## 📁 Estructura

```
python-automation-20260321/
├── main.py              # Aplicación principal
├── requirements.txt     # Dependencias
├── Dockerfile          # Imagen Docker
├── docker-compose.yaml  # Orquestación
├── .env.example        # Ejemplo de configuración
├── .gitignore         # Archivos ignorados
└── README.md          # Este archivo
```

## 📊 Respuestas

### Health Check

```json
{
  "status": "healthy",
  "database": "connected",
  "service": "python-automation",
  "timestamp": "2026-03-21T12:00:00"
}
```

### Stats

```json
{
  "total_orders": 42,
  "total_amount": 15000.00,
  "average_amount": 357.14,
  "timestamp": "2026-03-21T12:00:00"
}
```

## 🔨 Desarrollo

### Ejecutar con hot-reload

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Ejecutar tests

```bash
pytest tests/
```

## ☁️ Deploy

### Render/Railway

1. Conecta tu repositorio
2. Configura las variables de entorno:
   - `ORACLE_USER`
   - `ORACLE_PASSWORD`
   - `ORACLE_DSN`
3. Comando: `python main.py`

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: python-automation
spec:
  replicas: 2
  selector:
    matchLabels:
      app: python-automation
  template:
    spec:
      containers:
      - name: api
        image: python-automation-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: ORACLE_USER
          valueFrom:
            secretKeyRef:
              name: oracle-credentials
              key: user
```

## 🐛 Troubleshooting

### Error de conexión a Oracle

1. Verificar que Oracle esté corriendo
2. Verificar credenciales en .env
3. Verificar DSN (host:puerto/service)

### Puerto en uso

```bash
lsof -i :8000
kill -9 <PID>
```

## 🤝 Contribuir

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios
4. Push a la rama
5. Crea un Pull Request

## 📝 Changelog

- **v1.1.0** - Mejoras de seguridad, paginación, logging
- **v1.0.1** - Mejoras en validación y logging
- **v1.0.0** - API básica con CRUD de pedidos

## 📄 Licencia

MIT License

---

## 🇬🇧 English

REST API with FastAPI for process automation, integrated with Oracle Database. Features include CRUD operations, pagination, connection pooling, and automatic documentation.
