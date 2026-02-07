# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Single-file eBay listing scraper (`ebay_listing_grabber.py`) that downloads images and videos from eBay product pages. Uses `requests` + `BeautifulSoup` for HTML scraping and `ffmpeg` (external) for HLS video downloads.

## Commands

```bash
# Install dependencies (creates .venv and uv.lock)
uv sync

# Run the scraper
uv run python ebay_listing_grabber.py

# Lint
uv run ruff check ebay_listing_grabber.py
uv run ruff check --fix ebay_listing_grabber.py

# Format
uv run ruff format ebay_listing_grabber.py
uv run ruff format --check ebay_listing_grabber.py
```

## Architecture

All logic lives in `ebay_listing_grabber.py` with two main functions:

- `download_ebay_media(url, folder_name)` — entry point. Fetches the listing page, extracts video via regex on raw HTML (HLS `.m3u8` URL from JSON), then extracts images via BeautifulSoup CSS selectors on the image carousel. Images are downloaded concurrently with `ThreadPoolExecutor`.
- `download_video_ffmpeg(m3u8_url, output_path)` — shells out to `ffmpeg` to download HLS streams.

Images are upscaled to `s-l1600` resolution by rewriting the eBay CDN URL pattern. Video extraction relies on a regex match against the `"HLS"` key in embedded page JSON, not the parsed DOM.

## External Dependencies

- **ffmpeg** must be installed on the system for video downloads (`sudo apt install ffmpeg`)
- Python deps (`requests`, `beautifulsoup4`) are managed via `uv` in `pyproject.toml`

## Ruff Configuration

Configured in `pyproject.toml`: line-length 88, Python 3.12 target, rule sets E/F/I/W/UP/N.

## Commit Conventions

All commits must follow Conventional Commits with a required scope:

```
type(scope): description
```

- **Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`
- **Scopes:** `scraper`, `video`, `deps`, `docs`, `config`, `ci`, `release`
- Description starts lowercase, no trailing period, first line <= 72 chars
- Merge/fixup/squash commits bypass validation

## Git Hooks

Hooks live in `.githooks/` (tracked in git). Activate after cloning:

```bash
git config core.hooksPath .githooks
```

- `pre-commit` — runs `ruff check` and `ruff format --check` on staged `.py` files
- `commit-msg` — validates commit message format against the convention above
