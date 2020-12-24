# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/movister/env/src/django-youtube-api/youtube_api/api.py
# Compiled at: 2015-09-09 15:08:25
import logging
from django.conf import settings
from apiclient.discovery import build
from apiclient.errors import HttpError
__all__ = [
 'YoutubeApiError', 'api_call']
log = logging.getLogger('youtube_api')
YOUTUBE_API_ACCESS_KEY = getattr(settings, 'YOUTUBE_API_ACCESS_KEY')
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

class YoutubeApiError(Exception):

    def __init__(self, code, message):
        self.code = code
        self.message = message


def api_call(method, **kwargs):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_ACCESS_KEY)
    try:
        return getattr(youtube, method)().list(**kwargs).execute()
    except HttpError as e:
        raise YoutubeApiError(e.resp.status, e.content)