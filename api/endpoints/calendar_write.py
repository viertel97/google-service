import json
import os
from datetime import datetime, timedelta

import pytz
from loguru import logger

from core.config import build_calendar_service
from core.constants import DEFAULT_GERMAN_OFFSET

logger.add(
    os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/logs/" + os.path.basename(__file__) + ".log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)


def add_event_to_calendar(summary: str, start: datetime, end: datetime, description: str = None):
    if description is None:
        description = {"start": start.strftime("%Y-%m-%dT%H:%M:%S%z"), "end": end.strftime("%Y-%m-%dT%H:%M:%S%z"),
                       "app": summary}
    event = {
        "summary": summary,
        "description": json.dumps(description, indent=4),
        "start": {
            "dateTime": start.strftime("%Y-%m-%dT%H:%M:%S"),
            "timeZone": timezone_from_datetime(start),
        },
        "end": {
            "dateTime": end.strftime("%Y-%m-%dT%H:%M:%S"),
            "timeZone": timezone_from_datetime(end),
        },
    }
    service = build_calendar_service()
    event = (
        service.events().insert(calendarId="8j088igutfd3bkcant6at54d9g@group.calendar.google.com", body=event).execute()
    )
    logger.info("Event created: %s" % (event.get("htmlLink")))


# TODO: Default Todoist Timezone einbauen
def timezone_from_datetime(dt: datetime):
    if dt.tzinfo is None:
        return "Europe/Berlin"
    offset_in_seconds = dt.tzinfo.utcoffset(dt).seconds
    if offset_in_seconds == DEFAULT_GERMAN_OFFSET:
        return "Europe/Berlin"
    else:
        utc_offset = timedelta(seconds=offset_in_seconds)
        now = datetime.now(pytz.utc)
        return [
            tz.zone for tz in map(pytz.timezone, pytz.all_timezones_set) if
            now.astimezone(tz).utcoffset() == utc_offset
        ][0]
