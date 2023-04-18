DEFAULT_GERMAN_OFFSET = 7200

EVENT_ATTRIBUTES_TO_DELETE = ['etag', 'kind', 'id', 'htmlLink', 'creator', 'organizer', 'iCalUID', 'sequence',
                              'reminders',
                              'eventType', "recurrence", "transparency", "extendedProperties", "visibility",
                              "hangoutLink",
                              "conferenceData", "attendees", "location"]


GOOGLE_SCOPES = ["https://www.googleapis.com/auth/calendar"]
GOOGLE_TOKEN_URI = "https://oauth2.googleapis.com/token"