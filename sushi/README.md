# Sushi GPU Pipeline

This directory contains scripts for processing earnings call videos on the **sushi** GPU machine.

## Pipeline Overview

```
Mac (Local Development)
    ↓ scp upload
Sushi (GPU Machine)
    ├─ Whisper Transcription (GPU accelerated)
    └─ LLM Insights Extraction (OpenAI API)
    ↓ scp download
Mac (Local Development)
    └─ Remotion Video Generation
```

---

## Setup on Sushi (One-time)

### 1. Clone/Pull Repository

```bash
# SSH into sushi
ssh sushi

# Clone repo (first time)
cd ~
git clone <your-repo-url> earninglens
cd earninglens

# Or pull latest changes
git pull
```

### 2. Run Setup Script

```bash
chmod +x sushi/setup-sushi.sh
./sushi/setup-sushi.sh
```

This will:
- Check for CUDA/GPU
- Create Python virtual environment (`.venv-sushi`)
- Install dependencies (Whisper, OpenAI, etc.)
- Download Whisper models (~3GB)
- Create working directories
- Prompt for OpenAI API key

### 3. Set OpenAI API Key (if not done during setup)

```bash
export OPENAI_API_KEY='your-api-key-here'

# Add to ~/.bashrc for persistence
echo "export OPENAI_API_KEY='your-api-key-here'" >> ~/.bashrc
```

---

## Usage

### Option 1: From Mac (Recommended)

Use the wrapper script on your Mac:

```bash
# From Mac, in earninglens directory
chmod +x scripts/process-on-sushi.sh

./scripts/process-on-sushi.sh public/videos/PLTR/jUnV3LiN0_k.mp4
```

This will automatically:
1. Upload video to sushi
2. Process (transcribe + LLM)
3. Download all results
4. Optionally clean up

### Option 2: Directly on Sushi

SSH into sushi and run manually:

```bash
ssh sushi
cd ~/earninglens
source .venv-sushi/bin/activate

# Process a video
python sushi/process_video.py sushi/uploads/video.mp4

# Or just transcribe (skip LLM)
python sushi/transcribe.py sushi/uploads/video.mp4
```

---

## Generated Files

For each video processed, you'll get:

| File | Description |
|------|-------------|
| `{name}.json` | Full Whisper output (segments, word timestamps) |
| `{name}.srt` | SubRip subtitles (for video editing) |
| `{name}.vtt` | WebVTT subtitles (for web players) |
| `{name}.txt` | Plain text transcript |
| `{name}.paragraphs.json` | Simplified JSON for LLM (speaker-labeled) |
| `{name}.insights.json` | LLM-extracted insights, metadata, entities |

---

## Insights JSON Structure

The `insights.json` file contains:

```json
{
  "metadata": {
    "title": "Palantir Technologies Q3 2024 Earnings Call",
    "description": "Quarterly earnings webcast...",
    "summary": "Palantir discusses Q3 2024 results...",
    "content_type": "call",
    "event_date": "2024-11-04",
    "participants_count": 3
  },

  "speaker_names": {
    "SPEAKER_00": "Alex Karp",
    "SPEAKER_01": "Dave Glazer",
    "SPEAKER_02": "Ryan Taylor"
  },

  "table_of_contents": [
    {"timestamp": 0, "title": "Opening Remarks", "description": "..."},
    {"timestamp": 180, "title": "Q3 Financial Results", "description": "..."}
  ],

  "insights": {
    "key_takeaways": [...],
    "keywords": [{term, explanation}, ...],
    "suggested_questions": [...],
    "notable_quotes": [...]
  },

  "entities": {
    "people": [...],
    "organizations": [...],
    "products": [...],
    "locations": [...]
  }
}
```

---

## Configuration

### Whisper Models

Available models (trade-off: accuracy vs speed):

- `tiny` - Fastest, lowest quality (~1GB VRAM)
- `base` - Fast, decent (~1GB VRAM)
- `small` - Good balance (~2GB VRAM)
- **`medium`** - **Default**, high quality (~5GB VRAM)
- `large` - Best quality, slowest (~10GB VRAM)

Change model:

```bash
python sushi/process_video.py uploads/video.mp4 small
```

### LLM Models

Available OpenAI models:

- **`gpt-4o-mini`** - **Default**, cheap ($0.15/1M tokens)
- `gpt-4o` - More capable ($5/1M tokens)
- `gpt-4-turbo` - Legacy

Change model:

```bash
python sushi/process_video.py uploads/video.mp4 medium gpt-4o
```

---

## Performance

**Whisper Transcription (46 min video):**
- GPU (CUDA): ~10-15 minutes
- CPU: ~1-2 hours

**LLM Insights (46 min video):**
- API call: ~10-30 seconds
- Cost: ~$0.01-0.02 (gpt-4o-mini)

**Total:** ~15-20 minutes per video on GPU

---

## Troubleshooting

### CUDA Out of Memory

Use a smaller Whisper model:

```bash
python sushi/process_video.py uploads/video.mp4 small
```

### OpenAI API Error

Check API key is set:

```bash
echo $OPENAI_API_KEY
```

### SSH Connection Issues

Update hostname in `scripts/process-on-sushi.sh`:

```bash
SUSHI_HOST="user@sushi.local"  # or IP address
```

### Git Pull Conflicts

```bash
# On sushi
cd ~/earninglens
git stash
git pull
git stash pop
```

---

## Development Workflow

1. **On Mac:** Download video with RapidAPI
   ```bash
   source .venv/bin/activate
   python scripts/download-youtube.py jUnV3LiN0_k
   ```

2. **On Mac:** Process on sushi GPU
   ```bash
   ./scripts/process-on-sushi.sh public/videos/PLTR/jUnV3LiN0_k.mp4
   ```

3. **On Mac:** Build Remotion video with transcripts + insights
   ```bash
   npm run remotion
   # Use insights.json for speaker names, metadata, etc.
   ```

4. **On Mac:** Render final video
   ```bash
   npm run render
   ```

---

## Directory Structure

```
sushi/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── setup-sushi.sh           # One-time setup script
├── transcribe.py            # Whisper transcription
├── insights_generator.py    # LLM insights extraction
├── process_video.py         # Full pipeline (transcribe + LLM)
├── uploads/                 # Working directory (uploaded videos)
└── downloads/               # Processed results
```

---

## Cost Estimates

**Per 46-minute earnings call video:**

| Item | Cost |
|------|------|
| RapidAPI YouTube download | Free (quota limit) |
| Whisper transcription | Free (local GPU) |
| OpenAI LLM (gpt-4o-mini) | ~$0.01-0.02 |
| **Total** | **~$0.02** |

**For 100 videos:**
- Total cost: ~$2
- Total time: ~25-30 hours (GPU)
