# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Project configuration with `pyproject.toml` and `uv` package management
- Ruff linter and formatter configuration
- `README.md` with usage instructions and documentation
- `CLAUDE.md` for Claude Code guidance

## [0.1.0] - 2026-02-07

### Added

- Initial release
- High-resolution image extraction from eBay listing carousel (up to 1600px)
- HLS video stream detection and download via ffmpeg
- Concurrent image downloading with thread pool (5 workers)
- Automatic image URL deduplication
- Browser-like User-Agent for reliable page fetching
