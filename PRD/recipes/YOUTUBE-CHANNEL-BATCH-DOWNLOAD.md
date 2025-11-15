# YouTube Channel Batch Download Recipe

How to download all videos from a YouTube channel and process them in batches.

---

## Prerequisites

1. **YouTube API Key** - Get from Google Cloud Console
   - Enable YouTube Data API v3
   - Create API credentials
   - Set environment variable: `export YOUTUBE_API_KEY="your_key"`

2. **Rapid API Key** - For video downloads
   - Already configured in `.env` (RAPIDAPI_KEY)

---

## Step 1: Get Video List from Channel

```bash
cd ~/markethawk
source .venv/bin/activate

# Set YouTube API key
export YOUTUBE_API_KEY="your_api_key_here"

# Get all videos from a channel (using channel ID)
python lens/scripts/list_channel_videos.py UCyCv2FDWlZMyNiILlPr8TCw \
  --output /var/markethawk/EarnMoar.txt

# Or filter only earnings-related videos
python lens/scripts/list_channel_videos.py UCyCv2FDWlZMyNiILlPr8TCw \
  --filter-earnings \
  --output /var/markethawk/EarnMoar_earnings.txt
```

**Output:** Text file with one video ID per line
```
qmx-pkFdDVc
abc123XYZ89
def456UVW78
...
```

---

## Step 2: Download Videos to Cache

```bash
python lens/scripts/download_to_cache_pipeline.py \
  /var/markethawk/EarnMoar.txt \
  --workers 5 \
  --report /var/markethawk/earnmoar_download_report.json
```

**What it does:**
- Downloads all videos from the list using Rapid API
- Saves to `/var/markethawk/_downloads/{video_id}/`
- Automatically skips videos already in cache (default behavior)
- Uses 5 parallel workers (faster)
- Generates JSON report with success/failure stats

**Output structure:**
```
/var/markethawk/_downloads/
├── qmx-pkFdDVc/
│   ├── source.mp4
│   └── metadata.json
├── abc123XYZ89/
│   ├── source.mp4
│   └── metadata.json
└── ...
```

---

## Step 3: Create Batch from Video List

```bash
# Create batches (10 videos per batch)
python lens/batch_setup.py \
  /var/markethawk/EarnMoar.txt \
  earnmoar-batch \
  --batch-size 10 \
  --pipeline-type audio-only
```

**Output:**
```
/var/markethawk/batch_runs/earnmoar-batch/
├── pipeline.yaml
├── batch_001/
│   ├── batch.yaml
│   └── batch.log
├── batch_002/
│   └── batch.yaml
└── ...
```

---

## Step 4: Process Batches

```bash
# Process first batch
python lens/batch_processor.py \
  /var/markethawk/batch_runs/earnmoar-batch/batch_001/batch.yaml

# Process all batches sequentially
for batch in /var/markethawk/batch_runs/earnmoar-batch/batch_*/batch.yaml; do
  python lens/batch_processor.py "$batch"
done
```

**Pipeline steps (per video):**
1. Download (from cache - instant!)
2. Transcribe (WhisperX)
3. Extract Insights (OpenAI GPT-4)
4. Validate (is earnings call?)
5. Fuzzy Match (company lookup)
6. Extract Audio (MP3)
7. Upload R2 (audio)
7.5. Upload Artifacts (transcript, insights JSONs)
8. Update Database (PostgreSQL)

---

## Key Features

### Caching System
- Videos are cached in `/var/markethawk/_downloads/`
- Download script **skips cached videos by default**
- Batch processor **reuses cached videos** (no re-download)
- Saves time and Rapid API quota

### Parallel Downloads
- `--workers N` controls parallelism
- Recommended: 5 workers for balance
- Increase for faster downloads (watch API rate limits)
- Decrease if hitting rate limits

### Error Handling
- Failed downloads are logged
- Report shows: downloaded, cached, failed counts
- Can re-run script to retry only failed videos

---

## Complete Example: NVIDIA Earnings Calls

```bash
cd ~/markethawk
source .venv/bin/activate

# 1. Get all NVIDIA videos, filter earnings only
export YOUTUBE_API_KEY="your_key"
python lens/scripts/list_channel_videos.py UC_BFqGbW5-SqT8U3N_lZIDQ \
  --filter-earnings \
  --output /var/markethawk/nvidia_earnings.txt

# 2. Download to cache (5 parallel workers)
python lens/scripts/download_to_cache_pipeline.py \
  /var/markethawk/nvidia_earnings.txt \
  --workers 5 \
  --report /var/markethawk/nvidia_download_report.json

# 3. Create batches (20 videos per batch)
python lens/batch_setup.py \
  /var/markethawk/nvidia_earnings.txt \
  nvidia-earnings-batch \
  --batch-size 20 \
  --pipeline-type audio-only

# 4. Process all batches
for batch in /var/markethawk/batch_runs/nvidia-earnings-batch/batch_*/batch.yaml; do
  echo "Processing: $batch"
  python lens/batch_processor.py "$batch"
done

# 5. View results in database
PGPASSWORD=postgres psql -h 192.168.86.250 -p 54322 -U postgres -d postgres -c \
  "SELECT id, symbol, quarter, year FROM markethawkeye.earnings_calls WHERE symbol LIKE '%NVDA%' ORDER BY created_at DESC;"
```

---

## Troubleshooting

### Channel ID not found with @username
- Use channel ID instead of @username
- Get ID from: https://www.youtube.com/@channelname/about → Share → Copy channel ID

### Rapid API rate limit errors
- Reduce workers: `--workers 3` or `--workers 1`
- Add delays between batches
- Check Rapid API quota/usage

### Videos already processed
- Batch processor skips completed jobs automatically
- Check `batch.yaml` status field
- To reprocess: delete job entry from batch.yaml or create new batch

### Missing YouTube API key
```bash
# Set in current session
export YOUTUBE_API_KEY="your_key"

# Or add to ~/.bashrc / ~/.zshrc
echo 'export YOUTUBE_API_KEY="your_key"' >> ~/.bashrc
source ~/.bashrc
```

---

## Files Created

### Scripts
- `lens/scripts/list_channel_videos.py` - YouTube channel video scraper
- `lens/scripts/download_to_cache_pipeline.py` - Parallel video downloader

### Configuration
- `lens/download_config.example.yaml` - Download pipeline config template

### Data
- `/var/markethawk/{channel}_videos.txt` - Video ID lists
- `/var/markethawk/_downloads/{video_id}/` - Cached videos
- `/var/markethawk/batch_runs/{batch_name}/` - Batch processing data
- `/var/markethawk/batch_runs/{batch_name}/exports/earnings_calls.jsonl` - Database export

---

## Notes

- **Greenfield project** - No legacy considerations
- **Cache is shared** - All batches use same cache directory
- **Re-downloads are safe** - Script skips cached videos by default
- **Batch size recommendation** - 10-20 videos per batch for parallel processing
- **Cost optimization** - Cache videos once, process multiple times if needed

---

**Last Updated:** 2025-11-14
**Related:** BATCH-VIDEO-PROCESSING.md, AUDIO-ONLY-EARNINGS-RECIPE.md
