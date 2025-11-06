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


def generate_thumbnail(
    data: dict,
    output_path: str,
    width: int = 1280,
    height: int = 720
) -> bool:
    """
    Generate YouTube thumbnail image

    Args:
        data: Video data dictionary with company, ticker, quarter, etc.
        output_path: Path to save the thumbnail
        width: Image width (default: 1280 for YouTube)
        height: Image height (default: 720 for YouTube)

    Returns:
        bool: Success status
    """

    try:
        # Create gradient background (dark blue to darker blue)
        img = create_gradient_background(
            width, height,
            (15, 23, 42),   # Slate 900
            (30, 41, 59)    # Slate 800
        )

        draw = ImageDraw.Draw(img, 'RGBA')

        # Add subtle pattern/texture
        for i in range(0, width, 100):
            for j in range(0, height, 100):
                opacity = 10
                draw.ellipse(
                    [i, j, i + 50, j + 50],
                    fill=(255, 255, 255, opacity)
                )

        # Extract data
        company_name = data.get('company', 'Unknown Company')
        ticker = data.get('ticker', '')
        quarter = data.get('quarter', 'Q4')
        fiscal_year = data.get('fiscal_year', 2024)
        call_date = data.get('call_date', '')

        # Format date
        formatted_date = format_date(call_date) if call_date else ''

        # Fonts
        font_company_large = get_font(110, bold=True)
        font_ticker = get_font(80, bold=True)
        font_quarter = get_font(70, bold=True)
        font_date = get_font(45)
        font_logo = get_font(35, bold=True)

        # Colors
        white = (255, 255, 255)
        blue = (96, 165, 250)  # Blue 400
        yellow = (250, 204, 21)  # Yellow 400

        # Layout positions (centered design)
        padding = 80

        # Company Name (centered, top third)
        company_y = 180

        # Get text bounding box for centering
        bbox_company = draw.textbbox((0, 0), company_name, font=font_company_large)
        company_width = bbox_company[2] - bbox_company[0]
        company_x = (width - company_width) // 2

        draw_text_with_shadow(
            draw,
            company_name,
            (company_x, company_y),
            font_company_large,
            white,
            shadow_offset=5
        )

        # Ticker (below company name, centered)
        ticker_text = f"({ticker})"
        bbox_ticker = draw.textbbox((0, 0), ticker_text, font=font_ticker)
        ticker_width = bbox_ticker[2] - bbox_ticker[0]
        ticker_x = (width - ticker_width) // 2
        ticker_y = company_y + 130

        draw_text_with_shadow(
            draw,
            ticker_text,
            (ticker_x, ticker_y),
            font_ticker,
            blue,
            shadow_offset=4
        )

        # Quarter and Year (centered, prominent)
        quarter_text = f"{quarter} {fiscal_year}"
        bbox_quarter = draw.textbbox((0, 0), quarter_text, font=font_quarter)
        quarter_width = bbox_quarter[2] - bbox_quarter[0]
        quarter_x = (width - quarter_width) // 2
        quarter_y = ticker_y + 110

        # Draw quarter with yellow highlight box
        quarter_bg_padding = 20
        draw.rectangle(
            [
                quarter_x - quarter_bg_padding,
                quarter_y - 10,
                quarter_x + quarter_width + quarter_bg_padding,
                quarter_y + 80
            ],
            fill=(250, 204, 21, 200),  # Yellow with transparency
            outline=(250, 204, 21),
            width=3
        )

        draw.text(
            (quarter_x, quarter_y),
            quarter_text,
            font=font_quarter,
            fill=(15, 23, 42)  # Dark text on yellow
        )

        # Event Date (below quarter)
        if formatted_date:
            date_text = f"Earnings Call • {formatted_date}"
            bbox_date = draw.textbbox((0, 0), date_text, font=font_date)
            date_width = bbox_date[2] - bbox_date[0]
            date_x = (width - date_width) // 2
            date_y = quarter_y + 110

            draw_text_with_shadow(
                draw,
                date_text,
                (date_x, date_y),
                font_date,
                (226, 232, 240),  # Slate 200
                shadow_offset=2
            )

        # EarningLens Logo/Badge (bottom right corner)
        logo_padding = 40
        logo_x = width - 350
        logo_y = height - 100

        # Logo background
        draw.rectangle(
            [logo_x - 20, logo_y - 15, logo_x + 290, logo_y + 60],
            fill=(30, 41, 59, 220),  # Semi-transparent dark
            outline=(96, 165, 250),
            width=2
        )

        # Logo text
        logo_text = "📊 EarningLens"
        draw.text(
            (logo_x, logo_y),
            logo_text,
            font=font_logo,
            fill=white
        )

        # Save image
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        img.save(output_path, 'JPEG', quality=95, optimize=True)

        print(f"✅ Thumbnail generated successfully: {output_path}")
        print(f"   Resolution: {width}x{height}")
        print(f"   Company: {company_name} ({ticker})")
        print(f"   Period: {quarter} {fiscal_year}")
        print(f"   Date: {formatted_date}")

        return True

    except Exception as e:
        print(f"❌ Error generating thumbnail: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point"""
    if len(sys.argv) < 3:
        print("Usage: python generate_thumbnail.py <data_json_path> <output_path>")
        print("\nExample:")
        print("  python generate_thumbnail.py ../studio/data/AAPL-Q4-2024.json output/thumbnail.jpg")
        sys.exit(1)

    data_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.exists(data_path):
        print(f"❌ Error: Data file not found: {data_path}")
        sys.exit(1)

    # Load data
    with open(data_path, 'r') as f:
        data = json.load(f)

    # Generate thumbnail
    success = generate_thumbnail(data, output_path)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
