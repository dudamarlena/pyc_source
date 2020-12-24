# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/i3_agenda/__init__.py
# Compiled at: 2020-04-24 07:36:01
# Size of source mod 2**32: 8750 bytes
from __future__ import print_function
import argparse, datetime, json, os, os.path, pickle, subprocess, time
from os.path import expanduser
from typing import Optional, List
from bidi.algorithm import get_display
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
CONF_DIR = expanduser('~') + os.path.sep + '.i3agenda'
TMP_TOKEN = f"{CONF_DIR}/i3agenda_google_token.pickle"
CACHE_PATH = f"{CONF_DIR}/i3agenda_cache.txt"
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
DEFAULT_CAL_WEBPAGE = 'https://calendar.google.com/calendar/r/day'
button = os.getenv('BLOCK_BUTTON', '')
parser = argparse.ArgumentParser(description='Show next Google Calendar event')
parser.add_argument('--credentials', '-c',
  type=str,
  default='',
  help='path to your credentials.json file')
parser.add_argument('--cachettl', '-ttl',
  type=int,
  default=30,
  help='time for cache to be kept in minutes')
parser.add_argument('--update', '-u',
  action='store_true',
  default=False,
  help='when using this flag it will not load previous results from cache, it will however save new results to cache. You can use this flag to refresh all the cache forcefully')
parser.add_argument('--ids', '-i',
  type=str,
  default=[],
  nargs='+',
  help='list of calendar ids to fetch, space separated. If none is specified all calendars will be fetched')
parser.add_argument('--maxres', '-r',
  type=int,
  default=10,
  help="max number of events to query Google's API for each of your calendars. Increase this number if you have lot of events in your google calendar")
parser.add_argument('--today', '-d',
  action='store_true',
  help='print only today events')
parser.add_argument('--no-event-text', default='No events',
  metavar='TEXT',
  help='text to display when there are no events')

class Event:

    def __init__(self, summary: str, is_allday: bool, unix_time: float, end_time: float):
        self.is_allday = is_allday
        self.summary = summary
        self.unix_time = unix_time
        self.end_time = end_time


class EventEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, Event):
            return o.__dict__
        return json.JSONEncoder.default(self, o)


def main():
    args = parser.parse_args()
    allowed_calendars_ids = args.ids
    if button != '':
        subprocess.Popen(['xdg-open', DEFAULT_CAL_WEBPAGE])
    events = None
    if not args.update:
        events = load_cache(args.cachettl)
    if events == None:
        service = connect(args.credentials)
        events = getEvents(service, allowed_calendars_ids, args.maxres, args.today)
        save_cache(events)
    closest = get_closest(events)
    if closest is None:
        print(args.no_event_text)
        return None
    t = datetime.datetime.fromtimestamp(closest.unix_time)
    print(f"{t:%H:%M} " + get_display(closest.summary))


def getEvents(service, allowed_calendars_ids: List[str], max_results: int, today_only=False) -> List[Event]:
    now = datetime.datetime.utcnow()
    now_rfc3339 = now.isoformat() + 'Z'
    calendar_ids = []
    while True:
        calendar_list = service.calendarList().list().execute()
        for calendar_list_entry in calendar_list['items']:
            if not allowed_calendars_ids or calendar_list_entry['id'] in allowed_calendars_ids:
                calendar_ids.append(calendar_list_entry['id'])
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break

    all = []
    for id in calendar_ids:
        if today_only:
            midnight_rfc3339 = now.replace(hour=23, minute=39, second=59).isoformat() + 'Z'
            events_result = service.events().list(calendarId=id, timeMin=now_rfc3339,
              timeMax=midnight_rfc3339,
              maxResults=max_results,
              singleEvents=True,
              orderBy='startTime').execute()
        else:
            events_result = service.events().list(calendarId=id, timeMin=now_rfc3339,
              maxResults=max_results,
              singleEvents=True,
              orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            pass
        else:
            for event in events:
                end_time = get_event_time(event['end'].get('dateTime', event['end'].get('date')))
                start_time = event['start'].get('dateTime', event['start'].get('date'))
                unix_time = get_event_time(start_time)
                all.append(Event(event['summary'], is_allday(start_time), unix_time, end_time))
            else:
                return all


def is_allday(start_time: str) -> bool:
    return 'T' not in start_time


def get_event_time(full_time: str) -> float:
    if 'T' in full_time:
        format = '%Y-%m-%dT%H:%M:%S%z'
    else:
        format = '%Y-%m-%d'
    if full_time[(-3)] == ':':
        full_time = full_time[:-3] + full_time[-2:]
    return time.mktime(datetime.datetime.strptime(full_time, format).astimezone().timetuple())


def get_closest(events: List[Event]) -> Optional[Event]:
    closest = None
    for event in events:
        if event.is_allday:
            pass
        elif event.end_time < time.time():
            pass
        else:
            if closest is None or event.unix_time < closest.unix_time:
                closest = event
            return closest


def load_cache--- This code section failed: ---

 L. 186         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              exists
                6  LOAD_GLOBAL              CACHE_PATH
                8  CALL_METHOD_1         1  ''
               10  POP_JUMP_IF_TRUE     16  'to 16'

 L. 187        12  LOAD_CONST               None
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L. 189        16  LOAD_GLOBAL              os
               18  LOAD_ATTR                path
               20  LOAD_METHOD              getmtime
               22  LOAD_GLOBAL              CACHE_PATH
               24  CALL_METHOD_1         1  ''
               26  LOAD_GLOBAL              time
               28  LOAD_METHOD              time
               30  CALL_METHOD_0         0  ''
               32  BINARY_SUBTRACT  
               34  LOAD_FAST                'cachettl'
               36  LOAD_CONST               60
               38  BINARY_MULTIPLY  
               40  COMPARE_OP               >
               42  POP_JUMP_IF_FALSE    48  'to 48'

 L. 190        44  LOAD_CONST               None
               46  RETURN_VALUE     
             48_0  COME_FROM            42  '42'

 L. 192        48  BUILD_LIST_0          0 
               50  STORE_FAST               'events'

 L. 194        52  SETUP_FINALLY       142  'to 142'

 L. 195        54  LOAD_GLOBAL              open
               56  LOAD_GLOBAL              CACHE_PATH
               58  LOAD_STR                 'r'
               60  CALL_FUNCTION_2       2  ''
               62  SETUP_WITH          130  'to 130'
               64  STORE_FAST               'f'

 L. 196        66  LOAD_GLOBAL              json
               68  LOAD_METHOD              loads
               70  LOAD_FAST                'f'
               72  LOAD_METHOD              read
               74  CALL_METHOD_0         0  ''
               76  CALL_METHOD_1         1  ''
               78  STORE_FAST               'raw'

 L. 197        80  LOAD_FAST                'raw'
               82  GET_ITER         
               84  FOR_ITER            126  'to 126'
               86  STORE_FAST               'event'

 L. 198        88  LOAD_FAST                'events'
               90  LOAD_METHOD              append

 L. 199        92  LOAD_GLOBAL              Event
               94  LOAD_FAST                'event'
               96  LOAD_STR                 'summary'
               98  BINARY_SUBSCR    
              100  LOAD_FAST                'event'
              102  LOAD_STR                 'is_allday'
              104  BINARY_SUBSCR    
              106  LOAD_FAST                'event'
              108  LOAD_STR                 'unix_time'
              110  BINARY_SUBSCR    
              112  LOAD_FAST                'event'
              114  LOAD_STR                 'end_time'
              116  BINARY_SUBSCR    
              118  CALL_FUNCTION_4       4  ''

 L. 198       120  CALL_METHOD_1         1  ''
              122  POP_TOP          
              124  JUMP_BACK            84  'to 84'
              126  POP_BLOCK        
              128  BEGIN_FINALLY    
            130_0  COME_FROM_WITH       62  '62'
              130  WITH_CLEANUP_START
              132  WITH_CLEANUP_FINISH
              134  END_FINALLY      

 L. 201       136  LOAD_FAST                'events'
              138  POP_BLOCK        
              140  RETURN_VALUE     
            142_0  COME_FROM_FINALLY    52  '52'

 L. 202       142  DUP_TOP          
              144  LOAD_GLOBAL              Exception
              146  COMPARE_OP               exception-match
              148  POP_JUMP_IF_FALSE   162  'to 162'
              150  POP_TOP          
              152  POP_TOP          
              154  POP_TOP          

 L. 204       156  POP_EXCEPT       
              158  LOAD_CONST               None
              160  RETURN_VALUE     
            162_0  COME_FROM           148  '148'
              162  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 152


def save_cache(events: List[Event]) -> None:
    with open(CACHE_PATH, 'w+') as (f):
        f.write(EventEncoder().encode(events))


def connect(credspath: str) -> Resource:
    creds = None
    if not os.path.exists(CONF_DIR):
        os.mkdir(CONF_DIR)
    else:
        if os.path.exists(TMP_TOKEN):
            with open(TMP_TOKEN, 'rb') as (token):
                creds = pickle.load(token)
        elif not (creds and creds.valid):
            if not os.path.exists(credspath):
                print('You need to download your credentials json file from the Google API Console and pass its path to this script')
                exit(1)
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credspath, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TMP_TOKEN, 'wb') as (token):
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)
    return service


if __name__ == '__main__':
    main()