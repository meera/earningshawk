#!/usr/bin/env python3
"""
YouTube Thumbnail Generator for EarningLens

Creates professional thumbnail images for earnings call videos with:
- Company name
- Event date
- Quarter and Year
- EarningLens branding

Usage:
    python generate_thumbnail.py <data_json_path> <output_path>

Example:
    python generate_thumbnail.py ../studio/data/AAPL-Q4-2024.json output/thumbnail.jpg
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter


def create_gradient_background(width: int, height: int, color1: tuple, color2: tuple) -> Image.Image:
    """Create a gradient background from color1 to color2"""
    base = Image.new('RGB', (width, height), color1)
    top = Image.new('RGB', (width, height), color2)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        for x in range(width):
            # Diagonal gradient
            mask_data.append(int(255 * (y / height)))
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base


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
        # Try to find any TTF font
        return ImageFont.truetype(font_paths[0], size)
    except:
        # Fallback to default
        return ImageFont.load_default()


def draw_text_with_shadow(
    draw: ImageDraw.ImageDraw,
    text: str,
    position: tuple,
    font: ImageFont.FreeTypeFont,
    fill: tuple,
    shadow_offset: int = 3
):
    """Draw text with shadow for better readability"""
    x, y = position
    # Shadow
    draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=(0, 0, 0, 180))
    # Main text
    draw.text((x, y), text, font=font, fill=fill)


def format_date(date_str: str) -> str:
    """Format date string to readable format"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%b %d, %Y')  # e.g., "Nov 01, 2024"
    except:
        return date_str


def generate_thumbnail_variant_a(
    data: dict,
    draw: ImageDraw.ImageDraw,
    width: int,
    height: int
):
    """
    Variant A: Centered Design (Original Style)
    - Company name centered
    - Ticker below
    - Quarter with yellow highlight
    """
    company_name = data.get('company', 'Unknown Company')
    ticker = data.get('ticker', '')
    quarter = data.get('quarter', 'Q4')
    fiscal_year = data.get('fiscal_year', 2024)
    call_date = data.get('call_date', '')
    formatted_date = format_date(call_date) if call_date else ''

    # Fonts
    font_company = get_font(110, bold=True)
    font_ticker = get_font(80, bold=True)
    font_quarter = get_font(70, bold=True)
    font_date = get_font(45)

    # Colors
    white = (255, 255, 255)
    blue = (96, 165, 250)
    yellow = (250, 204, 21)

    # Company Name (centered)
    company_y = 180
    bbox = draw.textbbox((0, 0), company_name, font=font_company)
    company_x = (width - (bbox[2] - bbox[0])) // 2
    draw_text_with_shadow(draw, company_name, (company_x, company_y), font_company, white, 5)

    # Ticker
    ticker_text = f"({ticker})"
    bbox = draw.textbbox((0, 0), ticker_text, font=font_ticker)
    ticker_x = (width - (bbox[2] - bbox[0])) // 2
    ticker_y = company_y + 130
    draw_text_with_shadow(draw, ticker_text, (ticker_x, ticker_y), font_ticker, blue, 4)

    # Quarter with highlight
    quarter_text = f"{quarter} {fiscal_year}"
    bbox = draw.textbbox((0, 0), quarter_text, font=font_quarter)
    quarter_width = bbox[2] - bbox[0]
    quarter_x = (width - quarter_width) // 2
    quarter_y = ticker_y + 110

    draw.rectangle(
        [quarter_x - 20, quarter_y - 10, quarter_x + quarter_width + 20, quarter_y + 80],
        fill=(250, 204, 21, 200),
        outline=(250, 204, 21),
        width=3
    )
    draw.text((quarter_x, quarter_y), quarter_text, font=font_quarter, fill=(15, 23, 42))

    # Date
    if formatted_date:
        date_text = f"Earnings Call • {formatted_date}"
        bbox = draw.textbbox((0, 0), date_text, font=font_date)
        date_x = (width - (bbox[2] - bbox[0])) // 2
        date_y = quarter_y + 110
        draw_text_with_shadow(draw, date_text, (date_x, date_y), font_date, (226, 232, 240), 2)


def generate_thumbnail_variant_b(
    data: dict,
    draw: ImageDraw.ImageDraw,
    width: int,
    height: int
):
    """
    Variant B: Left-Aligned Bold Design
    - Large ticker on left
    - Quarter/year prominent
    - Metrics overlay (if available)
    """
    company_name = data.get('company', 'Unknown Company')
    ticker = data.get('ticker', '')
    quarter = data.get('quarter', 'Q4')
    fiscal_year = data.get('fiscal_year', 2024)

    # Get insights data for metrics
    insights = data.get('insights', {})
    key_metrics = insights.get('key_metrics', {})

    # Fonts
    font_ticker_huge = get_font(180, bold=True)
    font_company = get_font(65, bold=True)
    font_quarter = get_font(90, bold=True)
    font_metric = get_font(50, bold=True)

    # Colors
    white = (255, 255, 255)
    green = (34, 197, 94)  # Green 500
    yellow = (250, 204, 21)

    padding = 80

    # Giant ticker (top left)
    draw_text_with_shadow(draw, ticker, (padding, 100), font_ticker_huge, yellow, 6)

    # Company name (below ticker)
    draw_text_with_shadow(draw, company_name, (padding, 310), font_company, white, 3)

    # Quarter/Year (below company)
    quarter_text = f"{quarter} {fiscal_year} EARNINGS"
    draw_text_with_shadow(draw, quarter_text, (padding, 410), font_quarter, green, 4)

    # Metrics overlay (right side)
    if key_metrics:
        metric_x = width - 500
        metric_y = 150

        for i, (key, value) in enumerate(list(key_metrics.items())[:3]):
            # Metric label
            label = key.replace('_', ' ').upper()
            draw.text((metric_x, metric_y + (i * 120)), label, font=get_font(35), fill=(156, 163, 175))

            # Metric value
            draw_text_with_shadow(
                draw,
                str(value),
                (metric_x, metric_y + (i * 120) + 40),
                font_metric,
                white,
                3
            )


def generate_thumbnail_variant_c(
    data: dict,
    draw: ImageDraw.ImageDraw,
    width: int,
    height: int
):
    """
    Variant C: Split Screen with Speaker Photo
    - Left: Speaker photo (if available)
    - Right: Company info + quarter
    """
    company_name = data.get('company', 'Unknown Company')
    ticker = data.get('ticker', '')
    quarter = data.get('quarter', 'Q4')
    fiscal_year = data.get('fiscal_year', 2024)

    # Try to get speaker photo
    insights = data.get('insights', {})
    people = insights.get('entities', {}).get('people', [])
    speaker_photo_path = None

    if people and len(people) > 0:
        # Get first person (usually CEO)
        speaker = people[0]
        speaker_photo_path = speaker.get('photoLocalPath')

    # Fonts
    font_company = get_font(85, bold=True)
    font_ticker = get_font(70, bold=True)
    font_quarter = get_font(80, bold=True)
    font_speaker = get_font(45)

    # Colors
    white = (255, 255, 255)
    blue = (59, 130, 246)
    yellow = (250, 204, 21)

    # Split screen divider
    divider_x = width // 2

    # Left side: Speaker photo or placeholder
    if speaker_photo_path and os.path.exists(speaker_photo_path):
        try:
            speaker_img = Image.open(speaker_photo_path)
            # Resize to fit left half
            speaker_img = speaker_img.resize((divider_x - 100, height - 100), Image.Resampling.LANCZOS)
            # Paste on left side
            img_temp = draw._image
            img_temp.paste(speaker_img, (50, 50))
        except Exception as e:
            print(f"Warning: Could not load speaker photo: {e}")

    # Right side: Company info
    right_x = divider_x + 80
    y_pos = 150

    # Company name
    draw_text_with_shadow(draw, company_name, (right_x, y_pos), font_company, white, 4)
    y_pos += 120

    # Ticker
    draw_text_with_shadow(draw, f"${ticker}", (right_x, y_pos), font_ticker, blue, 3)
    y_pos += 110

    # Quarter
    quarter_text = f"{quarter}\n{fiscal_year}"
    for line in quarter_text.split('\n'):
        draw_text_with_shadow(draw, line, (right_x, y_pos), font_quarter, yellow, 4)
        y_pos += 90

    # Speaker name (if available)
    if people and len(people) > 0:
        speaker_name = people[0].get('name', '')
        speaker_role = people[0].get('role', '')
        if speaker_name:
            speaker_text = f"{speaker_name}\n{speaker_role}"
            y_pos += 50
            for line in speaker_text.split('\n'):
                draw.text((right_x, y_pos), line, font=font_speaker, fill=(203, 213, 225))
                y_pos += 50


def generate_thumbnail_variant_d(
    data: dict,
    draw: ImageDraw.ImageDraw,
    width: int,
    height: int
):
    """
    Variant D: Minimalist with Large Quarter
    - Huge quarter/year
    - Small company name
    - Clean, bold typography
    """
    company_name = data.get('company', 'Unknown Company')
    ticker = data.get('ticker', '')
    quarter = data.get('quarter', 'Q4')
    fiscal_year = data.get('fiscal_year', 2024)

    # Fonts
    font_quarter_huge = get_font(220, bold=True)
    font_year = get_font(150, bold=True)
    font_company = get_font(60, bold=True)
    font_ticker = get_font(55)

    # Colors
    white = (255, 255, 255)
    gray = (148, 163, 184)
    accent = (139, 92, 246)  # Purple 500

    # Centered layout
    # Quarter (huge, centered)
    bbox = draw.textbbox((0, 0), quarter, font=font_quarter_huge)
    quarter_width = bbox[2] - bbox[0]
    quarter_x = (width - quarter_width) // 2
    quarter_y = 150

    draw_text_with_shadow(draw, quarter, (quarter_x, quarter_y), font_quarter_huge, accent, 6)

    # Year (below quarter)
    year_text = str(fiscal_year)
    bbox = draw.textbbox((0, 0), year_text, font=font_year)
    year_width = bbox[2] - bbox[0]
    year_x = (width - year_width) // 2
    year_y = quarter_y + 230

    draw_text_with_shadow(draw, year_text, (year_x, year_y), font_year, white, 5)

    # Company + Ticker (bottom)
    company_text = f"{company_name} ({ticker})"
    bbox = draw.textbbox((0, 0), company_text, font=font_company)
    company_width = bbox[2] - bbox[0]
    company_x = (width - company_width) // 2
    company_y = year_y + 180

    draw_text_with_shadow(draw, company_text, (company_x, company_y), font_company, gray, 3)

    # Subtitle
    subtitle = "EARNINGS CALL"
    bbox = draw.textbbox((0, 0), subtitle, font=font_ticker)
    subtitle_x = (width - (bbox[2] - bbox[0])) // 2
    subtitle_y = company_y + 80

    draw.text((subtitle_x, subtitle_y), subtitle, font=font_ticker, fill=gray)


def generate_thumbnail(
    data: dict,
    output_path: str,
    width: int = 1280,
    height: int = 720,
    variant: str = 'all'
) -> bool:
    """
    Generate YouTube thumbnail image(s)

    Args:
        data: Video data dictionary with company, ticker, quarter, etc.
        output_path: Base path to save thumbnails (will add variant suffix)
        width: Image width (default: 1280 for YouTube)
        height: Image height (default: 720 for YouTube)
        variant: Which variant to generate ('a', 'b', 'c', 'd', or 'all')

    Returns:
        bool: Success status
    """
    try:
        variants_to_generate = []

        if variant == 'all':
            variants_to_generate = ['a', 'b', 'c', 'd']
        else:
            variants_to_generate = [variant.lower()]

        variant_functions = {
            'a': generate_thumbnail_variant_a,
            'b': generate_thumbnail_variant_b,
            'c': generate_thumbnail_variant_c,
            'd': generate_thumbnail_variant_d,
        }

        gradient_colors = {
            'a': ((15, 23, 42), (30, 41, 59)),      # Slate (original)
            'b': ((17, 24, 39), (31, 41, 55)),      # Gray (darker)
            'c': ((30, 58, 138), (29, 78, 216)),    # Blue
            'd': ((88, 28, 135), (107, 33, 168)),   # Purple
        }

        output_paths = []

        for var in variants_to_generate:
            if var not in variant_functions:
                print(f"⚠️  Unknown variant: {var}")
                continue

            # Create gradient background
            color1, color2 = gradient_colors[var]
            img = create_gradient_background(width, height, color1, color2)
            draw = ImageDraw.Draw(img, 'RGBA')

            # Add subtle texture
            for i in range(0, width, 100):
                for j in range(0, height, 100):
                    draw.ellipse([i, j, i + 50, j + 50], fill=(255, 255, 255, 10))

            # Generate variant
            variant_functions[var](data, draw, width, height)

            # Add EarningLens branding (all variants)
            logo_x = width - 350
            logo_y = height - 100
            font_logo = get_font(35, bold=True)

            draw.rectangle(
                [logo_x - 20, logo_y - 15, logo_x + 290, logo_y + 60],
                fill=(30, 41, 59, 220),
                outline=(96, 165, 250),
                width=2
            )
            draw.text((logo_x, logo_y), "📊 EarningLens", font=font_logo, fill=(255, 255, 255))

            # Save variant
            base_name, ext = os.path.splitext(output_path)
            variant_path = f"{base_name}_variant_{var}{ext}"

            output_dir = os.path.dirname(variant_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)

            img.save(variant_path, 'JPEG', quality=95, optimize=True)
            output_paths.append(variant_path)

            print(f"✅ Thumbnail variant {var.upper()} generated: {variant_path}")

        # Summary
        company_name = data.get('company', 'Unknown')
        ticker = data.get('ticker', '')
        quarter = data.get('quarter', '')
        fiscal_year = data.get('fiscal_year', '')

        print(f"\n📊 Thumbnail Generation Complete")
        print(f"   Company: {company_name} ({ticker})")
        print(f"   Period: {quarter} {fiscal_year}")
        print(f"   Variants: {len(output_paths)}")
        print(f"   Resolution: {width}x{height}")

        return True

    except Exception as e:
        print(f"❌ Error generating thumbnail: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Generate YouTube thumbnail variations")
    parser.add_argument("data_path", help="Path to data JSON file")
    parser.add_argument("output_path", help="Base output path for thumbnails")
    parser.add_argument(
        "--variant",
        choices=['a', 'b', 'c', 'd', 'all'],
        default='all',
        help="Which variant to generate (default: all)"
    )
    parser.add_argument("--width", type=int, default=1280, help="Image width (default: 1280)")
    parser.add_argument("--height", type=int, default=720, help="Image height (default: 720)")

    args = parser.parse_args()

    if not os.path.exists(args.data_path):
        print(f"❌ Error: Data file not found: {args.data_path}")
        sys.exit(1)

    # Load data
    with open(args.data_path, 'r') as f:
        data = json.load(f)

    # Generate thumbnail(s)
    success = generate_thumbnail(
        data,
        args.output_path,
        width=args.width,
        height=args.height,
        variant=args.variant
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
