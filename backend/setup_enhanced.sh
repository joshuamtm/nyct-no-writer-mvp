#!/bin/bash

echo "🚀 NYCT No-Writer Enhanced Backend Setup"
echo "========================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo "✅ Created .env file. Please edit it with your API keys:"
    echo "   - OPENAI_API_KEY or ANTHROPIC_API_KEY for AI features"
    echo "   - DATABASE_URL for metrics tracking (optional)"
    echo ""
    echo "To edit: nano .env"
else
    echo "✅ .env file found"
fi

# Check for API keys
if grep -q "your_openai_api_key_here\|your_anthropic_api_key_here" .env; then
    echo ""
    echo "⚠️  WARNING: API keys not configured!"
    echo "The application will run with limited functionality."
    echo "To enable AI features, add your API keys to .env file."
fi

echo ""
echo "Setup complete! To run the enhanced backend:"
echo "  1. Edit .env file with your API keys (if not done)"
echo "  2. Run: source venv/bin/activate"
echo "  3. Run: python main_enhanced.py"
echo ""
echo "Or use the original mock backend:"
echo "  python main.py"