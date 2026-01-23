#!/usr/bin/env python3
"""Generate QR code image for the website."""

import qrcode
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DONATION_URL = "https://buymeacoffee.com/jacopocastellano"
OUTPUT_PATH = PROJECT_ROOT / "docs" / "images" / "qr-donation.png"

def main():
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(DONATION_URL)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#00234B", back_color="white")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUTPUT_PATH)
    print(f"QR code saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
