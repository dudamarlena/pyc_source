# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/googleapi/tests/test_spreadsheet.py
# Compiled at: 2019-12-17 00:06:50
# Size of source mod 2**32: 1897 bytes
from googleapiclient.discovery import build
from httplib2 import Http
from foxylib.tools.googleapi.gdoc_tool import USERNAME_GOOGLE_FOXYTRIXY_BOT
from foxylib.tools.googleapi.gsheet_tool import GSSTool

class GSSToolTest:

    def test_04(self):
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        str_SCOPE = 'drive.readonly'
        creds = GSSTool.username_scope2creds(USERNAME_GOOGLE_FOXYTRIXY_BOT, str_SCOPE)
        service = build('drive', 'v3', http=(creds.authorize(Http())))
        h = {'spreadsheetId':'15K2PThxUL6YQhJBoQ5GYEgtNUsH132lUZDGYGxQDn40', 
         'range':'field'}
        result = (service.spreadsheets().values().get)(**h).execute()

    def test_02(self):
        GSSTool.data2test('foxytrixy.bot', GSSTool.SCOPE_READONLY, '1klHQnqtdWWdVavz2ElM_twC9LIez8N-2Wt4Fwob5mOY', 'consumeable')