#!/usr/bin/env python3
"""
Artistic YouTube Thumbnail Generator for EarningLens

Creates 4 visually stunning thumbnail variants with actual video frames:
1. Cinematic - Dark overlay with dramatic typography
2. Data Overlay - Metrics overlaid on video frame
3. Magazine Cover - Bold shapes and typography
4. Neon Tech - Futuristic glowing elements

Usage:
    python generate_thumbnail_artistic.py <video_path> <data_json_path> <output_dir>

Example:
    python generate_thumbnail_artistic.py /var/earninglens/PLTR/Q3-2025/take1.mp4 \
        studio/data/PLTR-Q3-2025.json output/thumbnails/
"""

import json
import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import tempfile


def extract_video_frame(video_path: str, timestamp: str = "00:00:15") -> Image.Image:
    """
    Extract a single frame from video at specified timestamp

    Args:
        video_path: Path to video file
        timestamp: Timestamp in HH:MM:SS format (default: 15 seconds in)

    Returns:
        PIL Image object
    """
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
        tmp_path = tmp.name

    try:
        # Use ffmpeg to extract frame
        cmd = [
            'ffmpeg',
            '-ss', timestamp,
            '-i', video_path,
            '-vframes', '1',
            '-q:v', '2',  # High quality
            '-y',
            tmp_path
        ]

        subprocess.run(cmd, check=True, capture_output=True)

        # Load image
        frame = Image.open(tmp_path)
        return frame

    finally:
        # Clean up temp file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Get font, trying system fonts"""
    font_paths = [
        # Linux fonts
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        # Fallback
        None
    ]

    font_path = font_paths[0] if bold else font_paths[1]

    try:
        if font_path and os.path.exists(font_path):
            return ImageFont.truetype(font_path, size)
        return ImageFont.truetype(font_paths[0], size)
    except:
        return ImageFont.load_default()


def create_gradient(width: int, height: int, colors: list, direction: str = 'vertical') -> Image.Image:
    """Create a gradient image"""
    base = Image.new('RGB', (width, height), colors[0])

    if len(colors) < 2:
        return base

    top = Image.new('RGB', (width, height), colors[1])
    mask = Image.new('L', (width, height))
    mask_data = []

    for y in range(height):
        for x in range(width):
            if direction == 'vertical':
                mask_data.append(int(255 * (y / height)))
            elif direction == 'horizontal':
                mask_data.append(int(255 * (x / width)))
            elif direction == 'diagonal':
                mask_data.append(int(255 * ((x + y) / (width + height))))

    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base


def style_1_cinematic(frame: Image.Image, data: dict, width: int = 1280, height: int = 720) -> Image.Image:
    """
    Style 1: CINEMATIC
    - Dark overlay on video frame
    - Dramatic typography
    - Film grain texture
    """
    # Resize frame to fit
    img = frame.resize((width, height), Image.Resampling.LANCZOS)

    # Darken the image
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.5)

    # Add vignette effect
    vignette = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    vignette_draw = ImageDraw.Draw(vignette)

    for i in range(min(width, height) // 3):
        alpha = int(180 * (i / (min(width, height) // 3)))
        vignette_draw.rectangle(
            [i, i, width - i, height - i],
            outline=(0, 0, 0, alpha)
        )

    img = Image.alpha_composite(img.convert('RGBA'), vignette).convert('RGB')

    # Add dark bottom gradient for text
    bottom_gradient = create_gradient(width, height // 2, [(0, 0, 0, 0), (0, 0, 0, 230)], 'vertical')
    gradient_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    gradient_layer.paste(bottom_gradient.convert('RGBA'), (0, height // 2))

    img = Image.alpha_composite(img.convert('RGBA'), gradient_layer).convert('RGB')

    draw = ImageDraw.Draw(img, 'RGBA')

    # Extract data
    company = data.get('company', 'Company')
    ticker = data.get('ticker', 'TICK')
    quarter = data.get('quarter', 'Q3')
    year = data.get('fiscal_year', 2025)

    # Fonts
    font_company = get_font(100, bold=True)
    font_quarter = get_font(70, bold=True)
    font_ticker = get_font(50, bold=True)

    # Company name at bottom
    company_y = height - 250
    draw.text((60, company_y), company, font=font_company, fill=(255, 255, 255))

    # Quarter below company
    quarter_text = f"{quarter} {year} EARNINGS"
    draw.text((60, company_y + 120), quarter_text, font=font_quarter, fill=(250, 204, 21))

    # Ticker badge in top right
    ticker_bg = Image.new('RGBA', (200, 80), (250, 204, 21, 255))
    img.paste(ticker_bg, (width - 240, 40))
    draw.text((width - 220, 50), ticker, font=font_ticker, fill=(0, 0, 0))

    # Accent line
    draw.rectangle([60, company_y - 20, 400, company_y - 10], fill=(250, 204, 21))

    return img


def style_2_data_overlay(frame: Image.Image, data: dict, width: int = 1280, height: int = 720) -> Image.Image:
    """
    Style 2: DATA OVERLAY
    - Clean video frame
    - Metrics cards overlaid
    - Professional data visualization
    """
    # Resize frame
    img = frame.resize((width, height), Image.Resampling.LANCZOS)

    # Slight brightness adjustment
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.8)

    # Convert to RGBA for overlay
    img = img.convert('RGBA')

    draw = ImageDraw.Draw(img, 'RGBA')

    # Extract data
    company = data.get('company', 'Company')
    ticker = data.get('ticker', 'TICK')
    quarter = data.get('quarter', 'Q3')
    year = data.get('fiscal_year', 2025)

    # Fonts
    font_title = get_font(90, bold=True)
    font_metric_label = get_font(28, bold=False)
    font_metric_value = get_font(50, bold=True)

    # Top banner with company info
    banner_height = 180
    draw.rectangle([0, 0, width, banner_height], fill=(0, 0, 0, 200))
    draw.rectangle([0, banner_height - 8, width, banner_height], fill=(37, 99, 235, 255))  # Blue accent

    # Company name in banner
    draw.text((50, 40), f"{company} ({ticker})", font=font_title, fill=(255, 255, 255))
    draw.text((50, 130), f"{quarter} {year} Earnings Call", font=font_metric_label, fill=(200, 200, 200))

    # Metric cards (bottom right)
    card_width = 300
    card_height = 120
    card_spacing = 20
    card_x = width - card_width - 50
    card_y = height - (card_height * 2 + card_spacing + 50)

    # Card 1: Revenue (example)
    draw.rectangle(
        [card_x, card_y, card_x + card_width, card_y + card_height],
        fill=(255, 255, 255, 240),
        outline=(37, 99, 235, 255),
        width=3
    )
    draw.text((card_x + 20, card_y + 20), "REVENUE", font=font_metric_label, fill=(107, 114, 128))
    draw.text((card_x + 20, card_y + 55), "$X.XB", font=font_metric_value, fill=(17, 24, 39))

    # Card 2: Growth
    card_y2 = card_y + card_height + card_spacing
    draw.rectangle(
        [card_x, card_y2, card_x + card_width, card_y2 + card_height],
        fill=(255, 255, 255, 240),
        outline=(72, 187, 120, 255),
        width=3
    )
    draw.text((card_x + 20, card_y2 + 20), "YoY GROWTH", font=font_metric_label, fill=(107, 114, 128))
    draw.text((card_x + 20, card_y2 + 55), "↑ XX%", font=font_metric_value, fill=(72, 187, 120))

    # EarningLens watermark
    font_logo = get_font(32, bold=True)
    draw.text((50, height - 70), "📊 EarningLens", font=font_logo, fill=(255, 255, 255, 255))

    return img.convert('RGB')


def style_3_magazine_cover(frame: Image.Image, data: dict, width: int = 1280, height: int = 720) -> Image.Image:
    """
    Style 3: MAGAZINE COVER
    - Bold typography
    - Unique geometric shapes
    - Vibrant colors
    """
    # Create base with frame on left side
    img = Image.new('RGB', (width, height), (255, 255, 255))

    # Resize frame to left half
    frame_resized = frame.resize((width // 2, height), Image.Resampling.LANCZOS)
    img.paste(frame_resized, (0, 0))

    draw = ImageDraw.Draw(img, 'RGBA')

    # Extract data
    company = data.get('company', 'Company')
    ticker = data.get('ticker', 'TICK')
    quarter = data.get('quarter', 'Q3')
    year = data.get('fiscal_year', 2025)

    # Right half: Bold design
    right_x = width // 2

    # Gradient background on right
    gradient = create_gradient(width // 2, height, [(250, 204, 21), (245, 158, 11)], 'diagonal')
    img.paste(gradient, (right_x, 0))

    # Geometric shapes
    # Circle
    draw.ellipse([right_x + 50, 50, right_x + 200, 200], fill=(255, 255, 255, 80))
    # Rectangle
    draw.rectangle([right_x + 300, height - 250, right_x + 550, height - 100], fill=(0, 0, 0, 50))

    # Fonts
    font_company = get_font(75, bold=True)
    font_ticker = get_font(120, bold=True)
    font_quarter = get_font(60, bold=True)

    # Company name
    company_y = 220
    draw.text((right_x + 80, company_y), company.upper(), font=font_company, fill=(0, 0, 0))

    # Huge ticker
    ticker_y = 320
    draw.text((right_x + 80, ticker_y), ticker, font=font_ticker, fill=(255, 255, 255))

    # Quarter
    quarter_y = 480
    draw.text((right_x + 80, quarter_y), f"{quarter}", font=font_quarter, fill=(0, 0, 0))
    draw.text((right_x + 80, quarter_y + 80), f"{year}", font=font_quarter, fill=(255, 255, 255))

    # Earnings badge
    badge_y = height - 120
    draw.rectangle([right_x + 80, badge_y, right_x + 350, badge_y + 70], fill=(0, 0, 0, 255))
    font_badge = get_font(40, bold=True)
    draw.text((right_x + 100, badge_y + 15), "EARNINGS", font=font_badge, fill=(250, 204, 21))

    return img


def style_4_neon_tech(frame: Image.Image, data: dict, width: int = 1280, height: int = 720) -> Image.Image:
    """
    Style 4: NEON TECH
    - Dark futuristic background
    - Glowing neon elements
    - Tech-inspired design
    """
    # Darken frame significantly
    img = frame.resize((width, height), Image.Resampling.LANCZOS)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.3)

    # Add blue tint
    blue_tint = Image.new('RGBA', (width, height), (37, 99, 235, 60))
    img = Image.alpha_composite(img.convert('RGBA'), blue_tint)

    draw = ImageDraw.Draw(img, 'RGBA')

    # Extract data
    company = data.get('company', 'Company')
    ticker = data.get('ticker', 'TICK')
    quarter = data.get('quarter', 'Q3')
    year = data.get('fiscal_year', 2025)

    # Neon grid lines
    grid_color = (102, 126, 234, 120)
    for i in range(0, width, 100):
        draw.line([(i, 0), (i, height)], fill=grid_color, width=1)
    for i in range(0, height, 100):
        draw.line([(0, i), (width, i)], fill=grid_color, width=1)

    # Fonts
    font_company = get_font(95, bold=True)
    font_ticker = get_font(140, bold=True)
    font_quarter = get_font(65, bold=True)

    # Neon glow effect function
    def draw_neon_text(text, pos, font, color):
        x, y = pos
        # Outer glow
        for offset in range(8, 0, -2):
            alpha = int(80 * (offset / 8))
            glow_color = (*color[:3], alpha)
            draw.text((x, y), text, font=font, fill=glow_color)
        # Main text
        draw.text((x, y), text, font=font, fill=(*color[:3], 255))

    # Company name with cyan glow
    company_y = height // 2 - 150
    draw_neon_text(company.upper(), (100, company_y), font_company, (96, 165, 250))

    # Ticker with magenta glow (HUGE)
    ticker_y = height // 2
    draw_neon_text(ticker, (100, ticker_y), font_ticker, (236, 72, 153))

    # Quarter with yellow glow
    quarter_text = f"{quarter} {year}"
    quarter_y = height // 2 + 180
    draw_neon_text(quarter_text, (100, quarter_y), font_quarter, (250, 204, 21))

    # Glowing border
    border_width = 8
    border_color = (102, 126, 234, 255)
    draw.rectangle([0, 0, width - 1, height - 1], outline=border_color, width=border_width)
    draw.rectangle([border_width, border_width, width - border_width - 1, height - border_width - 1],
                   outline=(96, 165, 250, 150), width=2)

    # Tech corner elements
    corner_size = 60
    corner_color = (250, 204, 21, 255)
    # Top left
    draw.line([(30, 30), (30 + corner_size, 30)], fill=corner_color, width=4)
    draw.line([(30, 30), (30, 30 + corner_size)], fill=corner_color, width=4)
    # Top right
    draw.line([(width - 30, 30), (width - 30 - corner_size, 30)], fill=corner_color, width=4)
    draw.line([(width - 30, 30), (width - 30, 30 + corner_size)], fill=corner_color, width=4)
    # Bottom left
    draw.line([(30, height - 30), (30 + corner_size, height - 30)], fill=corner_color, width=4)
    draw.line([(30, height - 30), (30, height - 30 - corner_size)], fill=corner_color, width=4)
    # Bottom right
    draw.line([(width - 30, height - 30), (width - 30 - corner_size, height - 30)], fill=corner_color, width=4)
    draw.line([(width - 30, height - 30), (width - 30, height - 30 - corner_size)], fill=corner_color, width=4)

    # EarningLens badge
    badge_x = width - 280
    badge_y = height - 80
    draw.rectangle([badge_x - 10, badge_y - 10, badge_x + 260, badge_y + 60],
                   fill=(0, 0, 0, 200), outline=(96, 165, 250, 255), width=2)
    font_logo = get_font(35, bold=True)
    draw.text((badge_x, badge_y), "⚡ EarningLens", font=font_logo, fill=(250, 204, 21))

    return img.convert('RGB')


def generate_all_thumbnails(video_path: str, data: dict, output_dir: str,
                           width: int = 1280, height: int = 720) -> list:
    """
    Generate all 4 thumbnail styles

    Returns:
        List of generated file paths
    """
    os.makedirs(output_dir, exist_ok=True)

    # Extract frame from video
    print("📹 Extracting frame from video...")
    frame = extract_video_frame(video_path)

    ticker = data.get('ticker', 'TICK')
    quarter = data.get('quarter', 'Q3')
    year = data.get('fiscal_year', 2025)
    base_name = f"{ticker}_{quarter}_{year}"

    generated_files = []

    # Style 1: Cinematic
    print("🎬 Generating Style 1: Cinematic...")
    img1 = style_1_cinematic(frame, data, width, height)
    path1 = os.path.join(output_dir, f"{base_name}_cinematic.jpg")
    img1.save(path1, 'JPEG', quality=95, optimize=True)
    generated_files.append(path1)
    print(f"   ✅ Saved: {path1}")

    # Style 2: Data Overlay
    print("📊 Generating Style 2: Data Overlay...")
    img2 = style_2_data_overlay(frame, data, width, height)
    path2 = os.path.join(output_dir, f"{base_name}_data.jpg")
    img2.save(path2, 'JPEG', quality=95, optimize=True)
    generated_files.append(path2)
    print(f"   ✅ Saved: {path2}")

    # Style 3: Magazine Cover
    print("📰 Generating Style 3: Magazine Cover...")
    img3 = style_3_magazine_cover(frame, data, width, height)
    path3 = os.path.join(output_dir, f"{base_name}_magazine.jpg")
    img3.save(path3, 'JPEG', quality=95, optimize=True)
    generated_files.append(path3)
    print(f"   ✅ Saved: {path3}")

    # Style 4: Neon Tech
    print("⚡ Generating Style 4: Neon Tech...")
    img4 = style_4_neon_tech(frame, data, width, height)
    path4 = os.path.join(output_dir, f"{base_name}_neon.jpg")
    img4.save(path4, 'JPEG', quality=95, optimize=True)
    generated_files.append(path4)
    print(f"   ✅ Saved: {path4}")

    return generated_files


def main():
    """Main entry point"""
    if len(sys.argv) < 4:
        print("Usage: python generate_thumbnail_artistic.py <video_path> <data_json_path> <output_dir>")
        print("\nExample:")
        print("  python generate_thumbnail_artistic.py /var/earninglens/PLTR/Q3-2025/take1.mp4 \\")
        print("      studio/data/PLTR-Q3-2025.json output/thumbnails/")
        sys.exit(1)

    video_path = sys.argv[1]
    data_path = sys.argv[2]
    output_dir = sys.argv[3]

    if not os.path.exists(video_path):
        print(f"❌ Error: Video file not found: {video_path}")
        sys.exit(1)

    if not os.path.exists(data_path):
        print(f"❌ Error: Data file not found: {data_path}")
        sys.exit(1)

    # Load data
    with open(data_path, 'r') as f:
        data = json.load(f)

    print("\n" + "=" * 60)
    print("🎨 EarningLens Artistic Thumbnail Generator")
    print("=" * 60)
    print(f"Video: {video_path}")
    print(f"Company: {data.get('company', 'Unknown')} ({data.get('ticker', 'N/A')})")
    print(f"Period: {data.get('quarter', 'Q?')} {data.get('fiscal_year', '????')}")
    print("=" * 60)
    print()

    # Generate thumbnails
    try:
        files = generate_all_thumbnails(video_path, data, output_dir)

        print()
        print("=" * 60)
        print(f"✅ SUCCESS! Generated {len(files)} thumbnail variants:")
        print("=" * 60)
        for i, file in enumerate(files, 1):
            file_size = os.path.getsize(file) / 1024  # KB
            print(f"{i}. {os.path.basename(file)} ({file_size:.1f} KB)")
        print()
        print("Choose your favorite and upload to YouTube!")
        print("=" * 60)

        sys.exit(0)

    except Exception as e:
        print(f"\n❌ Error generating thumbnails: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
