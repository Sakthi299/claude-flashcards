# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Daily Motivation Flashcards** web application built with FastAPI. It serves daily motivational quotes with translations, organized by date (day of year).

## Architecture

**Core Stack:**
- **Backend:** FastAPI with uvicorn ASGI server
- **Templates:** Jinja2 for server-side rendering
- **Frontend:** HTML with Tailwind CSS (CDN), vanilla JavaScript for navigation

**Project Structure:**
```
├── main.py              # FastAPI app - API endpoints and routes
├── requirements.txt     # Dependencies (fastapi, uvicorn, jinja2, gunicorn)
├── data/
│   └── daily_motivation.json   # JSON data store with 365 quotes for 2026
├── templates/
│   └── index.html       # Main template with card UI and JS
├── static/
│   ├── style.css        # Custom CSS overrides
│   ├── summer.jpg       # Background image
│   └── istockphoto-...  # Additional image asset
└── venv/                # Python virtual environment
```

**Data Structure:**
The `daily_motivation.json` contains quotes organized by year → month → day:
```json
{
  "2026": {
    "01": { "01": { "text": "...", "translation": "..." } }
  }
}
```

## Key API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | HTML page for today's quote |
| `/api/today` | GET | JSON data for today's quote |
| `/api/date/{month}/{day}` | GET | JSON data for specific date |
| `/api/quote-of-day` | GET | Alias for `/api/today` |

## Common Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Run the development server
python main.py
# or: uvicorn main:app --reload

# View dependencies
pip list
```

## Important Notes

1. The app is configured for **2026** specifically - both in data structure and hardcoded values
2. The main page (`/`) always shows **today's date** but the card content loads from the JSON data file
3. JavaScript navigation allows viewing quotes for other dates without page reload
4. Static files and templates use FastAPI's built-in `StaticFiles` and `Jinja2Templates`
5. The `.gitignore` excludes the `venv/` directory and standard Python build artifacts
