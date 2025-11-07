# 🎨 Artistic YouTube Thumbnail Generator

**Visual storytelling requires stunning thumbnails.**

This generator creates **4 eye-catching thumbnail styles** using actual video frames, not just text on gradients.

---

## Why This Matters

❌ **Old approach:** Boring text on gradient background
- Generic
- Doesn't showcase video content
- Looks like every other YouTube thumbnail

✅ **New approach:** Actual video frames with artistic overlays
- **Shows the visual storytelling immediately**
- Unique to each video
- Eye-catching and professional
- 4 different styles to choose from

---

## The 4 Artistic Styles

### 🎬 Style 1: CINEMATIC

**Aesthetic:** Dark, dramatic, film-like

**Visual Elements:**
- Video frame darkened (50% brightness)
- Vignette effect (dark edges, bright center)
- Dark bottom gradient for text readability
- Large white company name (bottom left)
- Yellow highlighted quarter/year
- Yellow ticker badge (top right)
- Gold accent line above text

**Best For:**
- Premium, high-end feel
- Tech companies (Apple, Microsoft, NVIDIA)
- Serious financial content
- Professional investors

**Example Layout:**
```
┌─────────────────────────────────────────┐
│                              [PLTR] ←──┐│  (Yellow badge)
│                                        ││
│  [VIDEO FRAME - Darkened]              ││
│                                        ││
│  [Vignette effect around edges]        ││
│                                        ││
│  ─────────────────  ←─ Gold accent line││
│  Palantir Technologies                 ││  (Large white text)
│  Q3 2025 EARNINGS  ←─ Yellow highlight ││
└─────────────────────────────────────────┘
```

---

### 📊 Style 2: DATA OVERLAY

**Aesthetic:** Clean, professional, data-driven

**Visual Elements:**
- Video frame slightly darkened (80% brightness)
- Black semi-transparent top banner
- Blue accent stripe below banner
- Company name + ticker in banner (white text)
- Metric cards overlaid (bottom right)
  - White cards with colored borders
  - Revenue card (blue border)
  - Growth card (green border)
- EarningLens watermark (bottom left)

**Best For:**
- Financial analysts
- Data-focused companies (Goldman Sachs, Bloomberg)
- Metric-heavy quarters
- Professional tone

**Example Layout:**
```
┌─────────────────────────────────────────┐
│ ████████████████████████████████  ←───┐│  (Black banner)
│ █ Palantir (PLTR)              █      ││
│ █ Q3 2025 Earnings Call        █      ││
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ←───┐││  (Blue accent)
│                                        ││
│  [VIDEO FRAME - Clean]                 ││
│                              ┌──────┐  ││
│                              │REVENUE│ ││  (Metric cards)
│                              │$X.XB  │  ││
│                              └──────┘  ││
│                              ┌──────┐  ││
│  📊 EarningLens              │GROWTH │ ││
│                              │↑ XX% │  ││
│                              └──────┘  ││
└─────────────────────────────────────────┘
```

---

### 📰 Style 3: MAGAZINE COVER

**Aesthetic:** Bold, vibrant, editorial

**Visual Elements:**
- Video frame on LEFT half (full height)
- Gradient background on RIGHT half (yellow/gold diagonal)
- Geometric shapes (circles, rectangles) as design elements
- Large bold typography
- HUGE ticker symbol (white)
- Company name (black, uppercase)
- Quarter + year stacked
- Black earnings badge

**Best For:**
- Consumer brands (Nike, Starbucks, Robinhood)
- Younger audience
- High-energy companies
- Standout thumbnails

**Example Layout:**
```
┌───────────────────┬─────────────────────┐
│                   │  ○ ←─ Geometric     │
│                   │     shapes          │
│  [VIDEO FRAME]    │                     │
│                   │  PALANTIR           │  (Bold uppercase)
│                   │  TECHNOLOGIES       │
│                   │                     │
│  [Full height]    │  PLTR ←─ HUGE ticker│  (White, massive)
│                   │                     │
│                   │  Q3                 │
│                   │  2025               │
│                   │  ▓▓▓▓▓▓▓▓▓          │
│                   │  █EARNINGS█ ←─ Badge│
│                   │  ▓▓▓▓▓▓▓▓▓          │
└───────────────────┴─────────────────────┘
     (Video)          (Yellow gradient)
```

---

### ⚡ Style 4: NEON TECH

**Aesthetic:** Futuristic, cyberpunk, high-tech

**Visual Elements:**
- Video frame heavily darkened (30% brightness)
- Blue tint overlay (tech feel)
- Neon grid lines (subtle, blue/purple)
- Glowing neon text (cyan, magenta, yellow)
- Company name: Cyan glow
- Ticker: Magenta glow (HUGE)
- Quarter: Yellow glow
- Glowing borders (double-line, blue)
- Tech corner brackets (yellow)
- EarningLens badge with lightning bolt

**Best For:**
- Tech companies (Tesla, NVIDIA, Palantir)
- Crypto/blockchain companies
- AI/ML companies
- Gaming companies
- Futuristic brands

**Example Layout:**
```
┌═══════════════════════════════════════┐
║ ┌┐                            ┌┐      ║  (Corner brackets)
║ └┘                            └┘      ║
║   [GRID LINES]                        ║
║                                       ║
║   PALANTIR TECHNOLOGIES ←─ Cyan glow  ║
║                                       ║
║   PLTR  ←──────── Magenta glow (HUGE) ║
║                                       ║
║   Q3 2025 ←─────────────── Yellow glow║
║                                       ║
║                    ⚡ EarningLens ←──┐║  (Glowing badge)
║ ┌┐                            ┌┐      ║
║ └┘                            └┘      ║
└═══════════════════════════════════════┘
   (Glowing border)
```

---

## Usage

### Prerequisites

```bash
# Install dependencies
pip install Pillow>=10.0.0

# Ensure ffmpeg is installed (for video frame extraction)
ffmpeg -version
```

### Generate All 4 Styles

```bash
python generate_thumbnail_artistic.py <video_path> <data_json> <output_dir>
```

**Example:**
```bash
python generate_thumbnail_artistic.py \
    /var/earninglens/PLTR/Q3-2025/take1.mp4 \
    studio/data/PLTR-Q3-2025.json \
    output/thumbnails/
```

**Output:**
```
📹 Extracting frame from video...
🎬 Generating Style 1: Cinematic...
   ✅ Saved: output/thumbnails/PLTR_Q3_2025_cinematic.jpg
📊 Generating Style 2: Data Overlay...
   ✅ Saved: output/thumbnails/PLTR_Q3_2025_data.jpg
📰 Generating Style 3: Magazine Cover...
   ✅ Saved: output/thumbnails/PLTR_Q3_2025_magazine.jpg
⚡ Generating Style 4: Neon Tech...
   ✅ Saved: output/thumbnails/PLTR_Q3_2025_neon.jpg

✅ SUCCESS! Generated 4 thumbnail variants
```

### Input Data Format

**Required JSON structure:**
```json
{
  "company": "Palantir Technologies",
  "ticker": "PLTR",
  "quarter": "Q3",
  "fiscal_year": 2025
}
```

---

## Choosing the Best Style

### Decision Matrix

| Company Type | Best Style | Reason |
|--------------|------------|--------|
| **Tech (PLTR, NVDA, TSLA)** | Neon Tech | Matches brand identity |
| **Finance (GS, JPM, BLK)** | Data Overlay | Professional, data-focused |
| **Consumer (AAPL, SBUX, NKE)** | Magazine Cover | Bold, accessible |
| **Enterprise (MSFT, ORCL)** | Cinematic | Premium, serious |

### A/B Testing Recommendations

1. **Upload 2 videos with different thumbnails**
   - Test Style 1 vs Style 4 for tech companies
   - Compare CTR (click-through rate) after 48 hours

2. **Rotate thumbnails**
   - Change thumbnail after 1 week if CTR is low
   - YouTube allows thumbnail changes without re-upload

3. **Audience preference**
   - Younger audience (18-34): Magazine Cover, Neon Tech
   - Older audience (35+): Cinematic, Data Overlay

---

## Customization

### Extract Frame at Different Timestamp

Default: 15 seconds into video

Edit `generate_thumbnail_artistic.py`:
```python
# Extract frame at 30 seconds instead
frame = extract_video_frame(video_path, timestamp="00:00:30")
```

### Change Colors

**Cinematic Style:**
```python
# Change yellow accent to blue
draw.text((60, company_y + 120), quarter_text, font=font_quarter, fill=(96, 165, 250))
```

**Neon Tech Style:**
```python
# Change ticker glow from magenta to cyan
draw_neon_text(ticker, (100, ticker_y), font_ticker, (96, 165, 250))  # Cyan instead
```

### Add Real Metrics

Currently shows placeholder text ("$X.XB", "↑ XX%")

**To add real data:**

1. Add metrics to JSON:
```json
{
  "company": "Palantir",
  "ticker": "PLTR",
  "quarter": "Q3",
  "fiscal_year": 2025,
  "metrics": {
    "revenue": "$678M",
    "growth": "+30%"
  }
}
```

2. Update `style_2_data_overlay()`:
```python
# Extract metrics
revenue = data.get('metrics', {}).get('revenue', '$X.XB')
growth = data.get('metrics', {}).get('growth', '↑ XX%')

# Use in cards
draw.text((card_x + 20, card_y + 55), revenue, font=font_metric_value, fill=(17, 24, 39))
draw.text((card_x + 20, card_y2 + 55), growth, font=font_metric_value, fill=(72, 187, 120))
```

---

## Integration with Pipeline

### Automatic Thumbnail Generation

Add to `process_video.py`:

```python
# After rendering video, generate thumbnails
if video_rendered:
    subprocess.run([
        'python', 'generate_thumbnail_artistic.py',
        video_path,
        data_json_path,
        f'/var/earninglens/{ticker}/{quarter}/thumbnails/'
    ])
```

### YouTube Upload Script

Use best-performing thumbnail:

```bash
# Upload video with specific thumbnail
python scripts/upload-youtube.js \
    --video=/var/earninglens/PLTR/Q3-2025/take1.mp4 \
    --thumbnail=/var/earninglens/PLTR/Q3-2025/thumbnails/PLTR_Q3_2025_neon.jpg \
    --title="Palantir (PLTR) Q3 2025 Earnings"
```

---

## Technical Details

### Video Frame Extraction

Uses **ffmpeg** to extract single frame:
```bash
ffmpeg -ss 00:00:15 -i video.mp4 -vframes 1 -q:v 2 output.jpg
```

Parameters:
- `-ss 00:00:15` - Seek to 15 seconds
- `-vframes 1` - Extract 1 frame
- `-q:v 2` - High quality (1-31, lower = better)

### Image Processing

- **Pillow (PIL)** for all image manipulation
- **ImageDraw** for text and shapes
- **ImageFilter** for blur/effects
- **ImageEnhance** for brightness/contrast

### Performance

| Operation | Time |
|-----------|------|
| Extract frame | ~1-2 seconds |
| Generate 1 thumbnail | ~0.5 seconds |
| Total (4 thumbnails) | ~3-4 seconds |

---

## Troubleshooting

### "ffmpeg: command not found"

```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

### Font not found

```bash
# Install DejaVu fonts
sudo apt-get install fonts-dejavu-core

# Verify
ls /usr/share/fonts/truetype/dejavu/
```

### Frame extraction fails

**Check video file:**
```bash
ffmpeg -i video.mp4
# Should show video details without errors
```

**Try different timestamp:**
```python
# If video is short, extract earlier frame
frame = extract_video_frame(video_path, timestamp="00:00:05")
```

---

## Future Enhancements

**Planned features:**

- [ ] **Multi-frame montage** - Use 3-4 frames in one thumbnail
- [ ] **Animated thumbnails** - For tweets/social media
- [ ] **Speaker photos** - Overlay CEO/CFO headshots
- [ ] **Chart integration** - Show actual revenue chart
- [ ] **Company logo** - Auto-download and overlay company logo
- [ ] **Smart frame selection** - Use AI to pick best frame (face detection, action detection)
- [ ] **Brand color extraction** - Auto-detect company brand colors
- [ ] **Template variations** - 10+ styles instead of 4

---

## Examples Gallery

### Cinematic Style

**Best for:** AAPL, MSFT, NVDA, TSLA
- Dark, premium feel
- Film-like aesthetic
- Professional investors

### Data Overlay Style

**Best for:** GS, JPM, BAC, BLK
- Clean, data-focused
- Metric cards prominent
- Financial professionals

### Magazine Cover Style

**Best for:** SBUX, NKE, LULU, HOOD
- Bold, vibrant
- Consumer-friendly
- Younger audience

### Neon Tech Style

**Best for:** PLTR, RBLX, COIN, AI
- Futuristic, high-tech
- Glowing elements
- Tech enthusiasts

---

## Contributing

**Want to add a new style?**

1. Create function: `style_5_your_name()`
2. Follow signature: `(frame: Image.Image, data: dict, width: int, height: int) -> Image.Image`
3. Add to `generate_all_thumbnails()`
4. Test and submit PR

**Example:**
```python
def style_5_minimalist(frame: Image.Image, data: dict, width: int = 1280, height: int = 720) -> Image.Image:
    """
    Style 5: MINIMALIST
    - Clean white space
    - Simple typography
    - Subtle video frame
    """
    # Your implementation here
    pass
```

---

## License

Part of EarningLens project.

**Created:** November 2025
**Author:** Meera
**Status:** Production Ready 🚀
