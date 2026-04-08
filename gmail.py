from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import os

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_service():
    creds = None

    # Load saved token
    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token:
            creds = pickle.load(token)

    # If not authenticated → login
    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open('token.pkl', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

def get_emails(max_results=5):
    service = get_service()

    results = service.users().messages().list(
        userId='me',
        maxResults=max_results
    ).execute()

    messages = results.get('messages', [])

    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(
            userId='me',
            id=msg['id']
        ).execute()

        try:
            payload = msg_data.get('payload', {})
            headers = payload.get('headers', [])

            subject = None

            for h in headers:
                if h['name'] == 'Subject':
                    subject = h['value']
                    break

            # fallback if subject missing
            if not subject:
                subject = "No Subject Email"

            emails.append(subject)

        except Exception as e:
            print("Error parsing email:", e)
            continue

    return emails