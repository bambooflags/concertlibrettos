# Monthly Workflow for Concert Librettos

This document describes the monthly process for generating new librettos and updating the website.

## Prerequisites

- Python 3.10+ with uv installed
- Git configured
- GitHub repository set up with Pages enabled (source: `/docs` folder)

## Monthly Update Process

### 1. Generate Librettos for the Month

Run the `/librettos_of_the_month` command to generate all librettos for the upcoming month:

```bash
/librettos_of_the_month [month] [year]
```

Example:
```bash
/librettos_of_the_month February 2026
```

This will generate PDFs in the `output/` folder.

### 2. Copy PDFs to the Website

Create the month folder and copy the new PDFs:

```bash
# Create the month folder (format: YYYY-MM)
mkdir -p docs/librettos/2026-02

# Copy the generated PDFs
cp output/libretto_*.pdf docs/librettos/2026-02/
```

### 3. Update index.html

Edit `docs/index.html` to add the new month's concerts. Add a new month section in the `#catalog` section:

```html
<!-- February 2026 -->
<div class="month-section">
    <h3 class="month-header">February 2026</h3>
    <div class="concert-list">
        <div class="concert-card">
            <div class="concert-info">
                <h4>Concert Title</h4>
                <span class="date">February X-X, 2026</span>
                <span class="conductor">Conductor Name</span>
            </div>
            <a href="librettos/2026-02/libretto_filename.pdf" class="download-btn">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                Download PDF
            </a>
        </div>
        <!-- Add more concert-card divs as needed -->
    </div>
</div>
```

### 4. Commit and Push

```bash
git add docs/
git commit -m "Add [Month] [Year] librettos"
git push
```

The site will automatically update on GitHub Pages.

## File Structure

```
docs/
├── index.html              # Main landing page
├── css/
│   └── style.css           # Site styling
├── images/
│   └── qr-donation.png     # Donation QR code
└── librettos/
    ├── 2026-01/            # January 2026
    │   ├── libretto_*.pdf
    │   └── ...
    └── 2026-02/            # February 2026
        └── ...
```

## Regenerating PDFs with QR Codes

If you need to regenerate existing PDFs with the new QR code footer:

```bash
uv run python src/converter.py output/libretto_draft.md output/new_libretto.pdf
```

The QR code will be automatically included in the PDF footer.

## Website URL

Once GitHub Pages is enabled, the site will be available at:

```
https://[username].github.io/concertlibrettos
```

## Support

The Buy Me a Coffee donation link is integrated in:
- The website header and footer
- Each PDF footer via QR code

Donation URL: https://buymeacoffee.com/jacopocastellano
