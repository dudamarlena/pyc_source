# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/googleapi/gdoc_tools.py
# Compiled at: 2019-03-25 20:26:52
# Size of source mod 2**32: 3653 bytes
import pytz
from foxylib.tools.date.pytz_tools import pytz_localize
from foxylib.tools.collections.collections_tools import merge_dicts
from googleapiclient.discovery import build
from httplib2 import Http
from datetime import datetime
import re

class GoogleDocToolkit:

    @classmethod
    def gdoc_id2url(cls, gdoc_id):
        return 'https://docs.google.com/document/d/{0}/'.format(gdoc_id)

    @classmethod
    def creds_gdoc_id2metadata(cls, creds, gdoc_id, options=None):
        str_SCOPE = 'drive.readonly'
        service = build('drive', 'v3', http=(creds.authorize(Http())))
        h = merge_dicts([{'fileId': gdoc_id},
         options])
        b = (service.files().get)(**h).execute()
        return b

    @classmethod
    def creds_gdoc_id2mtime(cls, creds, gdoc_id):
        options = {'fields': 'modifiedTime'}
        h = cls.creds_gdoc_id2metadata(creds, gdoc_id, options)
        s_DATETIME = h['modifiedTime']
        dt_NAIVE = datetime.strptime(s_DATETIME, '%Y-%m-%dT%H:%M:%S.%fZ')
        dt_AWARE = pytz_localize(dt_NAIVE, pytz.utc)
        return dt_AWARE

    @classmethod
    def creds_gdoc_id2utf8(cls, creds, gdoc_id):
        service = build('drive', 'v3', http=(creds.authorize(Http())))
        h = {'fileId':gdoc_id, 
         'mimeType':'text/plain'}
        b = (service.files().export)(**h).execute()
        s_GDOC = b.decode('utf-8')
        s_OUT = re.sub('\r\n', '\n', s_GDOC)
        return s_OUT


gdoc_id2url = GoogleDocToolkit.gdoc_id2url
creds_gdoc_id2metadata = GoogleDocToolkit.creds_gdoc_id2metadata
creds_gdoc_id2mtime = GoogleDocToolkit.creds_gdoc_id2mtime
creds_gdoc_id2utf8 = GoogleDocToolkit.creds_gdoc_id2utf8
USERNAME_GOOGLE_FOXYTRIXY_BOT = 'foxytrixy.bot'