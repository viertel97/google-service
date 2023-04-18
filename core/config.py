from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from quarter_lib.akeyless import get_secrets
from quarter_lib.logging import setup_logging

from core.constants import GOOGLE_TOKEN_URI, GOOGLE_SCOPES

logger = setup_logging(__file__)


def build_calendar_service():
    token, refresh_token, client_id, client_secret = get_secrets(
        ["google/token", "google/refresh_token", "google/client_id", "google/client_secret"])
    creds = Credentials(token=token, refresh_token=refresh_token, token_uri=GOOGLE_TOKEN_URI,
                        client_id=client_id, client_secret=client_secret, scopes=GOOGLE_SCOPES)
    return build("calendar", "v3", credentials=creds)
