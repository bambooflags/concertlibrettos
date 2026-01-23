#!/usr/bin/env python3
"""
PDF Converter for Berliner Librettos

Converts markdown libretto files to styled PDFs using pdfkit (wkhtmltopdf).

Usage:
    uv run python converter.py <markdown_file> [output_pdf]

Example:
    uv run python converter.py output/libretto_draft.md
    uv run python converter.py output/libretto_draft.md output/my_concert.pdf
"""

import sys
import base64
from io import BytesIO
from pathlib import Path
from datetime import datetime

import markdown
import pdfkit
import qrcode
from PIL import Image

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"
OUTPUT_DIR = PROJECT_ROOT / "output"
CSS_FILE = TEMPLATES_DIR / "libretto_style.css"

# Donation URL for QR code
DONATION_URL = "https://buymeacoffee.com/jacopocastellano"


def generate_qr_code_base64(url: str, size: int = 80) -> str:
    """Generate a QR code as base64-encoded PNG for embedding in HTML."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=1,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#00234B", back_color="white")

    # Resize to desired size
    img = img.resize((size, size), Image.Resampling.LANCZOS)

    # Convert to base64
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return f"data:image/png;base64,{img_base64}"


def convert_markdown_to_html(md_content: str, css_content: str = "", include_qr: bool = True) -> str:
    """Convert markdown content to HTML with embedded CSS and optional QR code."""
    html_body = markdown.markdown(
        md_content,
        extensions=['extra', 'smarty', 'toc']
    )

    # Generate QR code section if enabled
    qr_section = ""
    if include_qr:
        qr_base64 = generate_qr_code_base64(DONATION_URL)
        qr_section = f'''
    <div class="support-section">
        <img src="{qr_base64}" alt="Support this project" class="qr-code">
        <div class="support-text">
            <span class="support-label">Support this project</span>
            <span class="support-url">buymeacoffee.com/jacopocastellano</span>
        </div>
    </div>'''

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Concert Libretto</title>
    <style>
    {css_content}
    </style>
</head>
<body>
    <div class="libretto">
        {html_body}
    </div>{qr_section}
</body>
</html>"""

    return html_template


def generate_pdf(md_file: Path, output_pdf: Path = None) -> Path:
    """
    Generate PDF from markdown file.

    Args:
        md_file: Path to the markdown file
        output_pdf: Optional output path. If not provided, auto-generates name.

    Returns:
        Path to the generated PDF
    """
    # Read markdown content
    md_content = md_file.read_text(encoding='utf-8')

    # Read CSS
    css_content = ""
    if CSS_FILE.exists():
        css_content = CSS_FILE.read_text(encoding='utf-8')

    # Convert to HTML
    html_content = convert_markdown_to_html(md_content, css_content)

    # Determine output path
    if output_pdf is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_pdf = OUTPUT_DIR / f"libretto_{timestamp}.pdf"

    # Ensure output directory exists
    output_pdf.parent.mkdir(parents=True, exist_ok=True)

    # PDF options for wkhtmltopdf
    options = {
        'page-size': 'A4',
        'margin-top': '25mm',
        'margin-right': '20mm',
        'margin-bottom': '25mm',
        'margin-left': '20mm',
        'encoding': 'UTF-8',
        'enable-local-file-access': None,
        'footer-center': '[page]',
        'footer-font-size': '10',
    }

    # Generate PDF
    pdfkit.from_string(html_content, str(output_pdf), options=options)

    return output_pdf


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: uv run python converter.py <markdown_file> [output_pdf]")
        print("Example: uv run python converter.py output/libretto_draft.md")
        sys.exit(1)

    md_file = Path(sys.argv[1])
    if not md_file.is_absolute():
        md_file = PROJECT_ROOT / md_file

    if not md_file.exists():
        print(f"Error: File not found: {md_file}")
        sys.exit(1)

    output_pdf = None
    if len(sys.argv) >= 3:
        output_pdf = Path(sys.argv[2])
        if not output_pdf.is_absolute():
            output_pdf = PROJECT_ROOT / output_pdf

    print(f"Converting: {md_file}")

    try:
        result = generate_pdf(md_file, output_pdf)
        print(f"PDF generated: {result}")
    except Exception as e:
        print(f"Error generating PDF: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
