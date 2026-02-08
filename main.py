from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import json
import calendar
from datetime import datetime

app = FastAPI(title="Daily Motivation - Flashcards")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")


def load_motivation_data():
    """Load the daily motivation JSON data."""
    with open("data/daily_motivation.json", "r") as f:
        return json.load(f)


def get_day_of_year(date: datetime) -> int:
    """Calculate day of year (1-365)."""
    start_of_year = datetime(date.year, 1, 1)
    return (date - start_of_year).days + 1


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    """Display today's motivation card."""
    today = datetime.now()
    data = load_motivation_data()
    day_of_year = get_day_of_year(today)
    today_date = today.strftime("%A, %B %d, %Y")

    month_str = f"{today.month:02d}"
    day_str = f"{today.day:02d}"

    card = data["2026"].get(month_str, {}).get(day_str)
    if card is None:
        first_month = list(data["2026"].keys())[0]
        first_day = list(data["2026"][first_month].keys())[0]
        card = data["2026"][first_month][first_day]

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "card": card,
            "today": today,
            "today_date": today_date,
            "day_of_year": day_of_year,
        },
    )


class CardResponse(BaseModel):
    date: str
    month: str
    day: str
    text: str
    translation: str
    year: int


@app.get("/api/today", response_model=CardResponse)
async def get_today():
    """API endpoint for today's motivation card."""
    today = datetime.now()
    data = load_motivation_data()

    month_str = f"{today.month:02d}"
    day_str = f"{today.day:02d}"

    card = data["2026"].get(month_str, {}).get(day_str)
    if card is None:
        first_month = list(data["2026"].keys())[0]
        first_day = list(data["2026"][first_month].keys())[0]
        card = data["2026"][first_month][first_day]

    return CardResponse(
        date=today.strftime("%A, %B %d, %Y"),
        month=month_str,
        day=day_str,
        text=card["text"],
        translation=card["translation"],
        year=2026,
    )


@app.get("/api/date/{month}/{day}", response_model=CardResponse)
async def get_date(month: str, day: str):
    """API endpoint for a specific date's motivation card."""
    data = load_motivation_data()

    try:
        month_int = int(month)
        day_int = int(day)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid month or day format")

    if month_int < 1 or month_int > 12:
        raise HTTPException(status_code=400, detail="Month must be between 1 and 12")

    _, last_day = calendar.monthrange(2026, month_int)
    if day_int < 1 or day_int > last_day:
        raise HTTPException(
            status_code=400, detail=f"Day must be between 1 and {last_day}"
        )

    month_str = f"{month_int:02d}"
    day_str = f"{day_int:02d}"

    card = data["2026"].get(month_str, {}).get(day_str)

    if card is None:
        raise HTTPException(
            status_code=404, detail=f"No message found for {month_str}/{day_str}"
        )

    date_obj = datetime(2026, month_int, day_int)
    formatted_date = date_obj.strftime("%A, %B %d, %Y")

    return CardResponse(
        date=formatted_date,
        month=month_str,
        day=day_str,
        text=card["text"],
        translation=card["translation"],
        year=2026,
    )


@app.get("/api/quote-of-day")
async def get_quote_of_day():
    """Alternative endpoint for today's quote."""
    return await get_today()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
