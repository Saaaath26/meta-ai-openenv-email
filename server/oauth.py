from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
import os
import pickle

router = APIRouter()

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

CLIENT_SECRETS_FILE = "credentials.json"

REDIRECT_URI = "http://127.0.0.1:8000/auth/callback"

flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    redirect_uri=REDIRECT_URI
)


@router.get("/login")
def login():
    auth_url, _ = flow.authorization_url(prompt="consent")
    return RedirectResponse(auth_url)


@router.get("/callback")
def callback(request: Request):
    code = request.query_params.get("code")

    flow.fetch_token(code=code)
    creds = flow.credentials

    with open("token.pkl", "wb") as f:
        pickle.dump(creds, f)

    return {"message": "Login successful"}