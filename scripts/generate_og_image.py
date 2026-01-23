#!/usr/bin/env python3
"""Generate Open Graph image for social sharing."""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_PATH = PROJECT_ROOT / "docs" / "images" / "og-image.png"

# Berliner Phil colors
PRIMARY_COLOR = (0, 35, 75)  # #00234B
GOLD_COLOR = (201, 162, 39)  # #C9A227
WHITE_COLOR = (255, 255, 255)

def main():
    # OG image standard size: 1200x630
    width, height = 1200, 630
    img = Image.new('RGB', (width, height), PRIMARY_COLOR)
    draw = ImageDraw.Draw(img)

    # Draw gold accent line at top
    draw.rectangle([0, 0, width, 8], fill=GOLD_COLOR)

    # Draw gold accent line at bottom
    draw.rectangle([0, height - 8, width, height], fill=GOLD_COLOR)

    # Try to use a system font, fallback to default
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 72)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
    except OSError:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()

    # Draw title
    title = "Concert Librettos"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 220), title, font=title_font, fill=WHITE_COLOR)

    # Draw gold underline
    line_y = 310
    line_width = 120
    draw.rectangle([(width - line_width) // 2, line_y, (width + line_width) // 2, line_y + 4], fill=GOLD_COLOR)

    # Draw subtitle
    subtitle = "Free Program Notes for Berliner Philharmonie"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    draw.text((subtitle_x, 350), subtitle, font=subtitle_font, fill=(200, 200, 200))

    # Draw musical note emoji/symbol area
    note_text = "🎶"
    try:
        emoji_font = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", 60)
        draw.text((width // 2 - 40, 420), note_text, font=emoji_font, fill=GOLD_COLOR)
    except OSError:
        pass

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUTPUT_PATH, 'PNG', quality=95)
    print(f"OG image saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
