#!/bin/bash
# Mac wrapper script to process video on sushi GPU machine
#
# Usage:
#   ./scripts/process-on-sushi.sh <video_file>
#
# Example:
#   ./scripts/process-on-sushi.sh public/videos/PLTR/jUnV3LiN0_k.mp4

set -e

SUSHI_HOST="sushi"  # Update if needed (e.g., user@sushi or sushi.local)
SUSHI_PROJECT_DIR="~/earninglens"

if [ $# -lt 1 ]; then
    echo "Usage: ./scripts/process-on-sushi.sh <video_file>"
    echo ""
    echo "Example:"
    echo "  ./scripts/process-on-sushi.sh public/videos/PLTR/jUnV3LiN0_k.mp4"
    exit 1
fi

VIDEO_FILE="$1"
FILENAME=$(basename "$VIDEO_FILE")
BASE_NAME="${FILENAME%.*}"

echo "=========================================="
echo "EarningLens - Process on Sushi GPU"
echo "=========================================="
echo "Video: $FILENAME"
echo "Host: $SUSHI_HOST"
echo "=========================================="

# Step 1: Upload video to sushi
echo ""
echo "📤 Step 1: Uploading video to sushi..."
scp "$VIDEO_FILE" "$SUSHI_HOST:$SUSHI_PROJECT_DIR/sushi/uploads/"
echo "✅ Upload complete"

# Step 2: Process on sushi
echo ""
echo "🎙️  Step 2: Processing on sushi (transcription + LLM)..."
echo "This may take several minutes..."
ssh -t "$SUSHI_HOST" "cd $SUSHI_PROJECT_DIR && source .venv-sushi/bin/activate && python sushi/process_video.py sushi/uploads/$FILENAME"

# Step 3: Download results
echo ""
echo "📥 Step 3: Downloading results from sushi..."

# Create output directory
OUTPUT_DIR=$(dirname "$VIDEO_FILE")
OUTPUT_DIR="${OUTPUT_DIR/videos/audio}"  # Change videos to audio
mkdir -p "$OUTPUT_DIR"

# Download all generated files
scp "$SUSHI_HOST:$SUSHI_PROJECT_DIR/sushi/uploads/${BASE_NAME}.{json,srt,vtt,txt,paragraphs.json,insights.json}" "$OUTPUT_DIR/" 2>/dev/null || true

echo "✅ Download complete"

# Step 4: Clean up sushi (optional)
echo ""
read -p "Delete files from sushi? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    ssh "$SUSHI_HOST" "rm $SUSHI_PROJECT_DIR/sushi/uploads/${BASE_NAME}.*"
    echo "✅ Cleaned up sushi"
fi

echo ""
echo "=========================================="
echo "✅ Processing Complete!"
echo "=========================================="
echo ""
echo "Generated files in: $OUTPUT_DIR"
echo ""
ls -lh "$OUTPUT_DIR/${BASE_NAME}".* 2>/dev/null || true
echo ""
echo "=========================================="
