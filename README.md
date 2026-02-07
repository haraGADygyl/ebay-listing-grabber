# eBay Listing Grabber

Download high-resolution images and videos from eBay product listings.

## Features

- **Image extraction** — Scrapes all listing photos from the image carousel and automatically upgrades them to the highest available resolution (1600px)
- **Bot detection bypass** — Uses `curl_cffi` with Chrome TLS fingerprint impersonation to avoid 503 blocks
- **Video extraction** — Detects HLS video streams embedded in listing pages and downloads them as MP4
- **Concurrent downloads** — Images are fetched in parallel using a thread pool for faster completion
- **Deduplication** — Filters out duplicate image URLs before downloading

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (package manager)
- [ffmpeg](https://ffmpeg.org/) (only required for video downloads)

### Installing ffmpeg

```bash
# Ubuntu / Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows (via Chocolatey)
choco install ffmpeg
```

## Installation

```bash
git clone https://github.com/manushev/ebay-listing-grabber.git
cd ebay-listing-grabber
uv sync
```

This creates a virtual environment in `.venv/` and installs all dependencies.

## Usage

Edit the `target_url` variable in `ebay_listing_grabber.py` to point to the eBay listing you want to download from, then run:

```bash
uv run python ebay_listing_grabber.py
```

Or import the function directly in your own script:

```python
from ebay_listing_grabber import download_ebay_media

download_ebay_media("https://www.ebay.com/itm/YOUR_ITEM_ID")
```

### Parameters

| Parameter     | Type   | Default        | Description                            |
|---------------|--------|----------------|----------------------------------------|
| `url`         | `str`  | *(required)*   | Full eBay listing URL                  |
| `folder_name` | `str`  | `"ebay_media"` | Directory to save downloaded files to  |

### Output

All media is saved to the output folder (default: `ebay_media/`):

```
ebay_media/
├── image_1.jpg
├── image_2.jpg
├── image_3.jpg
└── listing_video.mp4
```

- Images are saved as `image_1.jpg`, `image_2.jpg`, etc. at 1600px resolution
- Video (if present) is saved as `listing_video.mp4`

## How It Works

1. Fetches the eBay listing page HTML using `curl_cffi` with Chrome TLS fingerprint impersonation to bypass bot detection
2. Searches the raw page source for an HLS stream URL (`"HLS"` key in embedded JSON) and downloads it via ffmpeg
3. Parses the HTML with BeautifulSoup, selects all `<img>` elements inside `div.ux-image-carousel`
4. Rewrites each image URL from eBay's CDN (`i.ebayimg.com`) to request the `s-l1600` size variant
5. Downloads all unique images concurrently using a thread pool (5 workers)

## Development

```bash
# Install dependencies including dev tools
uv sync

# Set up git hooks (required once after cloning)
git config core.hooksPath .githooks

# Lint
uv run ruff check ebay_listing_grabber.py

# Auto-fix lint issues
uv run ruff check --fix ebay_listing_grabber.py

# Format
uv run ruff format ebay_listing_grabber.py

# Check formatting without making changes
uv run ruff format --check ebay_listing_grabber.py
```

### Commit Message Format

This project uses [Conventional Commits](https://www.conventionalcommits.org/) with required scopes, enforced by a git hook.

```
type(scope): description
```

**Types:** `feat` `fix` `docs` `style` `refactor` `perf` `test` `build` `ci` `chore` `revert`

**Scopes:** `scraper` `video` `deps` `docs` `config` `ci` `release`

Description must start lowercase, have no trailing period, and the first line must be 72 characters or fewer.

A `pre-commit` hook also runs `ruff check` and `ruff format --check` on staged Python files, blocking the commit if there are lint or formatting errors.

## License

[MIT](LICENSE)
