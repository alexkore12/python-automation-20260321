# Python FastAPI REST API

## Descripción
API REST desarrollada con FastAPI y Oracle Database para gestión de órdenes.

## Características
- Endpoints RESTful
- Conexión a Oracle Database
- Pool de conexiones
- CRUD completo

## Instalación
```bash
pip install -r requirements.txt
```

## Ejecución
```bash
uvicorn main:app --reload
```

## Endpoints
- `GET /` - Health check
- `GET /orders` - Listar órdenes
- `POST /orders` - Crear orden

## Configuración
Modificar DSN en main.py para tu base de datos Oracle.

## Tests
```bash
pytest test_api.py
```
