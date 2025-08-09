import pandas as pd
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/documents']
CSV_FILE = 'scored_events_enhanced.csv'
DOC_TITLE = f"Toronto Event Newsletter – {datetime.datetime.now().strftime('%B %d, %Y')}"

def auth_google_docs():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return build('docs', 'v1', credentials=creds)

def format_event_block(event):
    return f"""🎭 {event['title']}
Venue: {event['venue']}
{event['description']}
{event['url']}
++"""

def main():
    df = pd.read_csv(CSV_FILE)

    c.
    df = df[df['PickForNewsletter'].astype(str).str.lower().isin(['true', 'yes', '1'])]

    if df.empty:
        print("No events marked for newsletter. Exiting.")
        return

    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df[df['date'] > datetime.datetime.now()]
        df = df.sort_values('date')
    else:
        df = df.reset_index()

    
    content = "\n\n".join([format_event_block(row) for _, row in df.iterrows()])

    try:
        service = auth_google_docs()
        doc = service.documents().create(body={'title': DOC_TITLE}).execute()
        doc_id = doc['documentId']

        
        service.documents().batchUpdate(
            documentId=doc_id,
            body={
                'requests': [
                    {
                        'insertText': {
                            'location': {'index': 1},
                            'text': content
                        }
                    }
                ]
            }
        ).execute()

        print(f"\n Newsletter created with {len(df)} events:")
        print(f"https://docs.google.com/document/d/{doc_id}/edit")

    except Exception as e:
        print(" Error creating document:", e)

if __name__ == '__main__':
    main()
