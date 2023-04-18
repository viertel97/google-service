import os
from datetime import datetime, timedelta

from dateutil import parser
from loguru import logger

from core.config import build_calendar_service
from core.constants import EVENT_ATTRIBUTES_TO_DELETE

logger.add(
    os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/logs/" + os.path.basename(__file__) + ".log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)


def get_events(calendars, time_start, time_end):
    calendar_service = build_calendar_service()

    calendar_dict = get_dict(calendar_service)

    event_list = []

    for calendar_name in calendars:
        event_list.extend(
            get_events_from_calendar(calendar_dict[calendar_name], calendar_service, time_start, time_end))

    return event_list


def get_events_from_calendar(calendar_element, calendar_service, time_min=None, time_max=None):
    event_list = []
    page_token = None
    while True:
        events = (
            calendar_service.events()
            .list(
                calendarId=calendar_element["id"],
                pageToken=page_token,
                timeMin=time_min,
                timeMax=time_max,
            )
            .execute()
        )
        for event in events["items"]:
            for attribute in EVENT_ATTRIBUTES_TO_DELETE:
                if attribute in event.keys():
                    del event[attribute]
            event_list.append(event)
        page_token = events.get("nextPageToken")
        if not page_token:
            break
    return event_list


def get_date_or_datetime(event, key):
    date_or_datetime = event[key]
    if "date" in date_or_datetime:
        date_or_datetime = date_or_datetime["date"]
    else:
        date_or_datetime = date_or_datetime["dateTime"]
    return parser.parse(date_or_datetime).replace(tzinfo=None)


def get_events_for_rework():
    events = get_events()
    events = [event for event in events if event["status"] != "cancelled"]
    result = []
    yesterday = (datetime.now() - timedelta(days=1.5))
    tomorrow = (datetime.now() + timedelta(days=1.5))
    for event in events:
        start = get_date_or_datetime(event, "start")
        if yesterday <= start <= tomorrow:
            result.append("{summary}({start})".format(summary=event['summary'], start=start.strftime("%d.%m.%Y %H:%M")))
    sorted_list = sorted(result, key=lambda x: x.split("(")[1])
    return sorted_list


def get_dict(calendar_service):
    calendar_dict = {}
    page_token = None
    while True:
        calendar_list = calendar_service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list["items"]:
            calendar_dict[calendar_list_entry["summary"]] = calendar_list_entry
        page_token = calendar_list.get("nextPageToken")
        if not page_token:
            break
    return calendar_dict
