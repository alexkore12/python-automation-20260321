# ⚙️ Python Automation Scripts

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)

## 📋 Descripción

Colección de scripts de automatización en Python para tareas DevOps y de infraestructura.

## ✨ Características

- 🔄 **Automatización de Tareas**: Scripts reutilizables para operaciones comunes
- 🐳 **Docker Ready**: Ejecuta scripts en contenedores aislados
- 📊 **Logging**: Logging estructurado con rotación de archivos
- ⚙️ **Configurable**: Totalmente configurable via variables de entorno
- 🔒 **Security**: Escaneo automático de vulnerabilidades con Grype
- 📈 **CI/CD**: GitHub Actions para linting, testing y security scanning

## 🚀 Uso

### Prerequisites

- Python 3.11+
- Docker (para ejecución en contenedor)

### Instalación Local

```bash
# Clonar el repositorio
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

# Ejecutar script principal
python main.py
```

### Docker

```bash
# Ejecutar con docker-compose
docker-compose up -d

# O ejecutar una vez
docker-compose run --rm automation
```

## ⚙️ Configuración

Copia `.env.example` a `.env` y configura:

| Variable | Descripción | Default |
|----------|-------------|---------|
| `LOG_LEVEL` | Nivel de logging | INFO |
| `LOG_FILE` | Archivo de log | automation.log |
| `MAX_WORKERS` | Workers máximos | 4 |
| `TIMEOUT` | Timeout en segundos | 300 |

## 📁 Estructura

```
python-automation-20260321/
├── .dockerignore
├── .env.example
├── .github/workflows/
├── .gitignore
├── .grype.yaml
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── Dockerfile
├── LICENSE
├── README.md
├── SECURITY.md
├── advanced_utils.py
├── docker-compose.yaml
├── health_check.py
├── main.py
└── requirements.txt
```

## 🛠️ Scripts Disponibles

| Script | Descripción |
|--------|-------------|
| `main.py` | Punto de entrada principal - orchestration de tareas |
| `advanced_utils.py` | Utilidades avanzadas para automatización |
| `health_check.py` | Script de healthcheck para contenedores |

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor lee [CONTRIBUTING.md](CONTRIBUTING.md) antes de enviar PRs.

## 🧪 Testing

```bash
# Ejecutar tests
pytest

# Con coverage
pytest --cov=. --cov-report=html

# Modo watch (re-ejecuta en cambios)
pytest --watch
```

## 📈 CI/CD

Workflows de GitHub Actions incluidos:
- ✅ Linting con ruff
- ✅ Tests con pytest
- ✅ Security scanning con Grype
- ✅ Docker build

## 🚨 Troubleshooting

### ModuleNotFoundError

**Problema:** `ModuleNotFoundError: No module named '...'`  
**Solución:** Asegúrate de tener el entorno virtual activado y las dependencias instaladas.

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Permisos denegados en Docker

**Problema:** `permission denied while trying to connect to the Docker daemon`  
**Solución:** Verifica que el usuario tenga permisos para usar Docker.

```bash
# Agregar usuario al grupo docker
sudo usermod -aG docker $USER
# O ejecutar con sudo
```

### Errores de conexión

**Problema:** Error de timeout en operaciones de red  
**Solución:** Aumenta el valor de TIMEOUT en .env o verifica tu conexión.

## 🌐 Referencias

- [Python Documentation](https://docs.python.org/3/)
- [Grype Vulnerability Scanner](https://github.com/anchore/grype)
- [Docker Docs](https://docs.docker.com/)
- [Pytest Documentation](https://docs.pytest.org/)

## 📝 Licencia

MIT - véase [LICENSE](LICENSE) para detalles.