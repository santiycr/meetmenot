from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = '.secret.json'
APPLICATION_NAME = 'MeetMeNot Robot'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    local_path = os.path.dirname(os.path.realpath(__file__))
    credential_path = os.path.join(local_path, '.auth.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, None)
    return credentials


def list_events(calendar, timeMin, timeMax):
    """ pull event for a user calendar based on a start and end time """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    eventsResult = service.events().list(
        calendarId=calendar, timeMin=timeMin, timeMax=timeMax,
        singleEvents=True, orderBy='startTime').execute()
    return eventsResult.get('items', [])


if __name__ == '__main__':
    now = datetime.datetime.utcnow()
    full_day = datetime.timedelta(days=1)
    events = list_events('primary',
                         now.isoformat() + 'Z',
                         (now + full_day).isoformat() + 'Z')
    if not events:
        print('No events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(event)
