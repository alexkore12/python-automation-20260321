#!/bin/bash
# Python Automation - Development Environment Setup
# Usage: ./setup.sh

set -e

echo "🐍 Setting up Python Automation environment..."

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Python version: $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# Create .env from example if it doesn't exist
if [ ! -f .env ] && [ -f .env.example ]; then
    echo "📝 Creating .env from example..."
    cp .env.example .env
fi

echo "✅ Python Automation environment ready!"
echo ""
echo "📝 Next steps:"
echo "   1. Activate: source venv/bin/activate"
echo "   2. Configure .env file"
echo "   3. Run: python main.py"