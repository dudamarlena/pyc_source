# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tyrs/shorter/googl.py
# Compiled at: 2011-07-26 04:03:46
import os, sys, httplib2
from urlshorter import UrlShorter
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
FLOW = OAuth2WebServerFlow(client_id='382344260739.apps.googleusercontent.com', client_secret='fJwAFxKWyW4rBmzzm6V3TVsZ', scope='https://www.googleapis.com/auth/urlshortener', user_agent='urlshortener-tyrs/1.0')
googl_token_file = os.environ['HOME'] + '/.config/tyrs/googl.tok'

class GooglUrlShorter(UrlShorter):

    def do_shorter(self, longurl):
        storage = Storage(googl_token_file)
        credentials = storage.get()
        if credentials is None or credentials.invalid:
            return 'need to register to use goog.gl'
        http = httplib2.Http()
        http = credentials.authorize(http)
        service = build('urlshortener', 'v1', http=http)
        try:
            url = service.url()
            body = {'longUrl': longurl}
            resp = url.insert(body=body).execute()
            return resp['id']
        except AccessTokenRefreshError:
            pass

        return

    def register_token(self):
        storage = Storage(googl_token_file)
        credentials = storage.get()
        if credentials is None or credentials.invalid:
            print 'There is no token file found for goo.gl'
            print 'A file will be generated for you'
            credentials = run(FLOW, storage)
        return