import sys
import os

import datetime
from dateutil.parser import parse
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

sys.path.insert(0, os.path.realpath('./'))
from display.image_processing import UIProc

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

WIDGET_WIDTH = 180
WIDGET_HEIGHT = 384

class AgendaWidget:

    def __init__(self, language="en", calendarId='primary', nr_of_events=10):
        self._calendar_id = calendarId
        self._nr_of_events = nr_of_events
        self._language = language
        self._width = WIDGET_WIDTH
        self._height = WIDGET_HEIGHT

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(host='localhost', port=8088)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self._service = build('calendar', 'v3', credentials=creds)


    def get_data(self):
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = self._service.events().list(calendarId=self._calendar_id, timeMin=now,
                                            maxResults=self._nr_of_events, singleEvents=True,
                                            orderBy='startTime').execute()
        self._events = events_result.get('items', [])


    def get_widget_image(self):
        uiwriter = UIProc(self._language, self._width, self._height)
        h_line_size = 18

        if not self._events:
            uiwriter.write_text('No upcoming events found.', (0, 0))
        idx = 0
        for event in self._events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            get_date_obj = parse(start)

            uiwriter.write_text(get_date_obj.strftime("%b %d %Y %H:%M"), (0, h_line_size*idx), colour="red")
            
            event_summary = (uiwriter.multiline_text(event['summary'], self._height - 130))
            if (len(event_summary) > 1):
                for event_line in event_summary:
                    uiwriter.write_text(event_line, (130, h_line_size*idx))
                    idx = idx + 1
            else:
                uiwriter.write_text(event_summary[0], (130, h_line_size*idx))
                idx = idx + 1

            #print(start, event['summary'])

        return uiwriter.get_image()
