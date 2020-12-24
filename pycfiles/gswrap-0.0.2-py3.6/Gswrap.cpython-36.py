# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/gswrap/Gswrap.py
# Compiled at: 2018-06-20 04:55:06
# Size of source mod 2**32: 1625 bytes
"""
Google Sheet REST API wrapper class.
Have a nice day:D
"""
import httplib2
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient import discovery

class Gswrap:
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    DRIVE_API_VER = 'v4'
    APPLICATION_NAME = 'gswrap'
    _credentials = None

    def __init__(self, key_file: str, credential_file: str) -> None:
        store = Storage(credential_file)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(key_file, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            credentials = tools.run_flow(flow, store)
        self._credentials = credentials

    def get_value(self, spreadsheet_id: str, range_name: str) -> dict:
        """
        get value by range
        :param spreadsheet_id:
        :param range_name:
        :return:
        """
        service = self._Gswrap__get_service()
        result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        return result.get('values', [])

    def __get_service(self) -> object:
        credentials = self._credentials
        http = credentials.authorize(httplib2.Http())
        discovery_url = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
        return discovery.build('sheets', (self.DRIVE_API_VER), http=http, discoveryServiceUrl=discovery_url)