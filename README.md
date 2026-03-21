# 🐍 Python Automation API

API REST con FastAPI para automatización de procesos, integrada con Oracle Database.

## 📋 Descripción

API RESTful de alto rendimiento construida con FastAPI que proporciona endpoints para gestión de pedidos (orders) con persistencia en Oracle Database. Ideal para sistemas de automatización empresarial.

## 🛠️ Características

- ✅ **FastAPI** - Framework moderno y rápido
- ✅ **Oracle Database** - Persistencia robusta
- ✅ **Pydantic** - Validación de datos
- ✅ **CORS** - Soporte para cross-origin
- ✅ **Connection Pool** - Optimización de conexiones
- ✅ **Logging** - Registro estructurado
- ✅ **Health Checks** - Monitoreo de estado
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
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
export ORACLE_USER="system"
export ORACLE_PASSWORD="tu_password"
export ORACLE_DSN="localhost:1521/orclpdb1"

# 5. Ejecutar
python main.py
```

La API estará disponible en `http://localhost:8000`

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
| GET | `/orders` | Listar todos los pedidos |
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
  "customer": "string (required, 1-100 chars)",
  "amount": "number (required, > 0)",
  "description": "string (optional)"
}
```

### OrderUpdate
```json
{
  "customer": "string (optional)",
  "amount": "number (optional, > 0)",
  "description": "string (optional)"
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

## 🔧 Configuración

### Variables de Entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| `ORACLE_USER` | Usuario de Oracle | system |
| `ORACLE_PASSWORD` | Password de Oracle | password |
| `ORACLE_DSN` | Data Source Name | localhost:1521/orclpdb1 |

## 📁 Estructura

```
python-automation-20260321/
├── main.py              # Aplicación principal
├── requirements.txt     # Dependencias
├── Dockerfile          # Imagen Docker
├── docker-compose.yaml  # Orquestación
└── README.md           # Este archivo
```

## 📊 Health Check Response

```json
{
  "status": "healthy",
  "database": "connected",
  "service": "python-automation"
}
```

## 📈 Stats Response

```json
{
  "total_orders": 42,
  "total_amount": 15000.00,
  "average_amount": 357.14
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
2. Configura las variables de entorno
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

## 📝 Changelog

- **v1.0.0** - API básica con CRUD de pedidos
- **v1.0.1** - Mejoras en validación y logging
- **v1.1.0** - Endpoint de estadísticas

## 🤝 Contribución

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -am 'Agrega nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crea un Pull Request

## 📄 Licencia

MIT License - Uso libre y modificaciones bienvenidas.
