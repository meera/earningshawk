#!/bin/bash
# Setup script for sushi GPU machine
# Run this once on sushi after git clone/pull

set -e

echo "=========================================="
echo "EarningLens Sushi GPU Setup"
echo "=========================================="

# Check if we're on the right machine
if [[ $(hostname) != *"sushi"* ]]; then
    echo "⚠️  Warning: This doesn't appear to be the sushi machine"
    echo "Current hostname: $(hostname)"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check for CUDA
echo ""
echo "Checking for CUDA..."
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi
    echo "✅ CUDA is available"
else
    echo "❌ CUDA not found - Whisper will run on CPU (slower)"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check for Python 3
echo ""
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found"
    exit 1
fi

python3 --version
echo "✅ Python 3 found"

# Create virtual environment
echo ""
echo "Creating Python virtual environment..."
python3 -m venv .venv-sushi
echo "✅ Virtual environment created: .venv-sushi"

# Activate venv
source .venv-sushi/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r sushi/requirements.txt
echo "✅ Dependencies installed"

# Create directories
echo ""
echo "Creating working directories..."
mkdir -p sushi/uploads
mkdir -p sushi/downloads
echo "✅ Directories created"

# Check for OpenAI API key
echo ""
echo "Checking for OpenAI API key..."
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY not set"
    echo ""
    echo "To set it permanently, add to ~/.bashrc:"
    echo "  export OPENAI_API_KEY='your-api-key-here'"
    echo ""
    read -p "Enter your OpenAI API key now (or press Enter to skip): " api_key
    if [ -n "$api_key" ]; then
        export OPENAI_API_KEY="$api_key"
        echo "export OPENAI_API_KEY='$api_key'" >> ~/.bashrc
        echo "✅ API key set and added to ~/.bashrc"
    fi
else
    echo "✅ OPENAI_API_KEY is set"
fi

# Download Whisper models (optional but recommended)
echo ""
read -p "Pre-download Whisper models? (recommended, ~3GB) (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Downloading Whisper models..."
    python3 -c "import whisper; whisper.load_model('medium')"
    echo "✅ Whisper models downloaded"
fi

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Activate the environment: source .venv-sushi/bin/activate"
echo "2. Process a video: python sushi/process_video.py sushi/uploads/video.mp4"
echo ""
echo "Or use the Mac wrapper scripts to upload/download via scp"
echo "=========================================="
