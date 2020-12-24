# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/google_credentials/views.py
# Compiled at: 2013-01-22 03:47:41
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from google_credentials.models import Credentials
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.django_orm import Storage

@staff_member_required
def authorize(request):
    client_id = settings.GA_CLIENT_ID
    client_secret = settings.GA_CLIENT_SECRET
    redirect_uri = settings.GA_REDIRECT_URI
    scope = settings.GA_SCOPE
    storage = Storage(Credentials, 'client_id', client_id, 'credentials')
    credentials = storage.get()
    if credentials is None or credentials.invalid is True:
        FLOW = OAuth2WebServerFlow(client_id=client_id, client_secret=client_secret, scope=scope, redirect_uri=redirect_uri)
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    else:
        messages.info(request, 'Previously authorized %s.' % client_id)
        return HttpResponseRedirect(reverse('admin:index'))
        return


@staff_member_required
def purge(request):
    client_id = settings.GA_CLIENT_ID
    try:
        Credentials.objects.get(client_id=client_id).delete()
        messages.info(request, 'Purged %s.' % client_id)
    except Credentials.DoesNotExist:
        messages.info(request, 'Nor credentials found for %s, nothing purged.' % client_id)

    return HttpResponseRedirect(reverse('admin:index'))


@staff_member_required
def callback(request):
    client_id = settings.GA_CLIENT_ID
    client_secret = settings.GA_CLIENT_SECRET
    redirect_uri = settings.GA_REDIRECT_URI
    scope = settings.GA_SCOPE
    FLOW = OAuth2WebServerFlow(client_id=client_id, client_secret=client_secret, scope=scope, redirect_uri=redirect_uri)
    credentials = FLOW.step2_exchange(request.REQUEST)
    credentials_obj, created = Credentials.objects.get_or_create(client_id=credentials.client_id)
    credentials_obj.credentials = credentials
    credentials_obj.save()
    messages.info(request, 'Authorized %s.' % client_id)
    return HttpResponseRedirect(reverse('admin:index'))