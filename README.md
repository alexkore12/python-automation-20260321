# Python Automation - FastAPI + Oracle Database

API REST robusta con integración a Oracle Database.

## 🚀 Características

- **FastAPI** - Framework moderno de alto rendimiento
- **Oracle Database** - Conexión con pool de conexiones
- **Type Safety** - Pydantic models con validación
- **Manejo de errores** - Try-catch con respuestas claras
- **Docker** - Despliegue contenerizado
- **CORS** - Control de accesos cross-origin
- **OAuth2/JWT** - Autenticación segura (preparado)

## 📦 Instalación

```bash
# Clonar repositorio
git clone https://github.com/alexkore12/python-automation-20260321.git
cd python-automation-20260321

# Instalar dependencias
pip install -r requirements.txt
```

## ⚙️ Configuración

Configura las variables de entorno:

```bash
export ORACLE_USER="system"
export ORACLE_PASSWORD="your_password"
export ORACLE_DSN="localhost:1521/orclpdb1"
```

## ▶️ Uso

```bash
# Iniciar servidor
python main.py

# O con uvicorn
uvicorn main:app --reload --port 8000
```

## 📡 Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Estado de la API |
| GET | `/health` | Health check |
| GET | `/orders` | Listar pedidos |
| GET | `/orders/{id}` | Pedido por ID |
| POST | `/orders` | Crear pedido |
| PUT | `/orders/{id}` | Actualizar pedido |
| DELETE | `/orders/{id}` | Eliminar pedido |
| GET | `/stats` | Estadísticas |

## 🗄️ Schema Oracle

```sql
CREATE TABLE orders (
    id NUMBER PRIMARY KEY,
    customer VARCHAR2(100) NOT NULL,
    amount NUMBER(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🧪 Testing

```bash
pytest tests/
```

## 🐳 Docker

```bash
# Build
docker build -t python-automation .

# Run
docker run -p 8000:8000 \
  -e ORACLE_USER=system \
  -e ORACLE_PASSWORD=password \
  -e ORACLE_DSN=localhost:1521/orclpdb1 \
  python-automation
```

## 📁 Estructura

```
├── main.py           # Aplicación principal
├── requirements.txt  # Dependencias
├── Dockerfile        # Contenedor
├── README.md         # Documentación
├── config.py         # Configuración
├── models/           # Modelos de datos
└── tests/           # Pruebas
```

## 🔧 Dependencias

- fastapi
- uvicorn
- oracledb
- python-dotenv

## 🔒 Seguridad

### Recomendaciones para Producción
1. **Usar HTTPS** - Configurar proxy reverso (nginx, traefik)
2. **Variables de entorno** - No hardcodear passwords
3. **Limitar CORS** - Especificar dominios permitidos
4. **Rate Limiting** - Implementar límites de requests
5. **Logs** - Enviar logs a sistema centralizado
6. **Validación Pydantic** - Toda entrada validada

### Oracle Security
- Usar Oracle Wallet para credenciales
- Pool de conexiones con timeouts
- SQL injection prevention (ORM/Pydantic)

## 📝 Licencia

MIT - Alejandro Kore

## 🤖 Actualizado por

OpenClaw AI Assistant - 2026-03-21
*Mejoras: Documentación de seguridad, CORS, OAuth2 preparado*
