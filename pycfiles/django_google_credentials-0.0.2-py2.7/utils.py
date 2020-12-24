# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/google_credentials/utils.py
# Compiled at: 2013-01-22 03:47:41
from apiclient.discovery import build
from django.conf import settings
import httplib2
from oauth2client.django_orm import Storage
from google_credentials.models import Credentials

def get_service():
    storage = Storage(Credentials, 'client_id', settings.GA_CLIENT_ID, 'credentials')
    credentials = storage.get()
    http = credentials.authorize(httplib2.Http())
    service = build('analytics', 'v3', http=http)
    return service