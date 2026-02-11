"""Google API client helpers for Slides and Drive."""

from __future__ import annotations

import os
from typing import Any

import google.auth
from dotenv import load_dotenv
from google.api_core.exceptions import GoogleAPIError
from google.auth.exceptions import DefaultCredentialsError
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()

SCOPES = (
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/drive",
)

SERVICE_ACCOUNT_PATH_ENV = "GOOGLE_SERVICE_ACCOUNT_JSON"
DELEGATED_USER_ENV = "GOOGLE_IMPERSONATE_USER"


class CredentialsError(RuntimeError):
    """Raised when Google credentials cannot be loaded."""


class GoogleApiSetupError(RuntimeError):
    """Raised when Google API clients cannot be created."""


def load_credentials() -> Any:
    """Load credentials from service account JSON or ADC."""

    service_account_path = os.getenv(SERVICE_ACCOUNT_PATH_ENV)
    if service_account_path:
        creds = service_account.Credentials.from_service_account_file(
            service_account_path,
            scopes=SCOPES,
        )
        delegated_user = os.getenv(DELEGATED_USER_ENV)
        if delegated_user:
            creds = creds.with_subject(delegated_user)
        return creds

    try:
        creds, _ = google.auth.default(scopes=SCOPES)
    except DefaultCredentialsError as exc:
        raise CredentialsError(
            "No Google credentials found. Set GOOGLE_SERVICE_ACCOUNT_JSON or run "
            "`gcloud auth application-default login --scopes=https://www.googleapis.com/auth/presentations,https://www.googleapis.com/auth/drive`."
        ) from exc

    if creds is None:
        raise CredentialsError(
            "Google credentials were not resolved. Check GOOGLE_SERVICE_ACCOUNT_JSON or ADC setup."
        )

    return creds


def build_slides_service(credentials: Any) -> Any:
    try:
        return build("slides", "v1", credentials=credentials, cache_discovery=False)
    except GoogleAPIError as exc:
        raise GoogleApiSetupError(f"Unable to create Google Slides client: {exc}") from exc


def build_drive_service(credentials: Any) -> Any:
    try:
        return build("drive", "v3", credentials=credentials, cache_discovery=False)
    except GoogleAPIError as exc:
        raise GoogleApiSetupError(f"Unable to create Google Drive client: {exc}") from exc
