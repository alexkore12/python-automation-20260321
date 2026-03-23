#!/bin/bash
# Setup script - Install dependencies and configure environment

set -euo pipefail

echo "📦 Installing dependencies..."
if command -v pip &> /dev/null; then
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
elif command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "❌ pip not found"
    exit 1
fi

if [ -f .env.example ]; then
    if [ ! -f .env ]; then
        cp .env.example .env
        echo "✅ Environment file created from .env.example"
    fi
fi

echo "✅ Setup complete!"
