# ⚙️ Python Automation Scripts

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)

## 📋 Descripción

Colección de scripts de automatización en Python para tareas DevOps y de infraestructura.

## ✨ Características

- 🔄 **Automatización de Tareas**: Scripts reutilizables
- 🐳 **Docker Ready**: Ejecuta scripts en contenedores
- 📊 **Logging**: Logging estructurado
- ⚙️ **Configurable**: Variables de entorno
- 🔒 **Security**: Escaneo con Grype

## 🚀 Uso

### Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar script
python main.py
```

### Docker

```bash
docker-compose run --rm automation
```

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
├── main.py
└── requirements.txt
```

## 🤝 Contribuir

Lee [CONTRIBUTING.md](CONTRIBUTING.md).

## 📝 Licencia

MIT - [LICENSE](LICENSE)
