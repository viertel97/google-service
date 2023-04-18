from datetime import datetime, timedelta

from fastapi import APIRouter
from quarter_lib.logging import setup_logging

from api.endpoints.calendar_read import get_events
from api.endpoints.calendar_write import add_event_to_calendar
from core.models.event import Event

logger = setup_logging(__file__)
api_router = APIRouter()


@logger.catch
@api_router.get("/events/{days}")
async def get_events_from_google_calendar(days: int = 365, calendar_names: list = ["Janik's Kalender"]):
    now = datetime.now()
    one_year_ago = now - timedelta(days=days)
    one_year_ahead = now + timedelta(days=days)
    events = get_events(calendar_names, one_year_ago.isoformat() + "Z", one_year_ahead.isoformat() + "Z")
    return list(events)


@logger.catch
@api_router.post("/event", status_code=201)
async def add_event_to_google_calendar(event: Event):
    add_event_to_calendar(event.summary, event.start_datetime, event.end_datetime)
