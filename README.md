# Daily Motivation Flashcards

A web application that serves daily motivational quotes with translations, organized by date.

## Overview

This FastAPI-based application displays motivational quotes in a flashcard format. Each day features a unique quote with an English translation and philosophical references.

## Features

- Daily quote display with formatted card UI
- Navigate between dates without page reload
- Responsive design with Tailwind CSS
- RESTful API endpoints for programmatic access
- Background image cycling based on seasons

## Setup

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Application

```bash
# Run the development server
python main.py

# Or use uvicorn directly
uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | HTML page for today's quote |
| `/api/today` | GET | JSON data for today's quote |
| `/api/date/{month}/{day}` | GET | JSON data for specific date |
| `/api/quote-of-day` | GET | Alias for `/api/today` |

## Data Structure

Quotes are stored in `data/daily_motivation.json` with the format:
```json
{
  "2026": {
    "01": {
      "01": {
        "text": "Quote text...",
        "translation": "English translation...",
        "chapter": 12,
        "verse": 13
      }
    }
  }
}
```
