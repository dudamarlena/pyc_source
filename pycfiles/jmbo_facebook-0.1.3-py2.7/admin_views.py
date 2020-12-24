# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/jmbo_facebook/admin_views.py
# Compiled at: 2013-05-14 09:27:46
import urllib, urllib2
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.contrib import messages
from django.contrib.sites.models import get_current_site
from django.conf import settings
from jmbo_facebook.models import Page

@staff_member_required
def handler(request):
    redirect = HttpResponseRedirect('/admin/jmbo_facebook/page')
    code = request.REQUEST.get('code')
    if not code:
        return redirect
    site = get_current_site(request)
    protocol = 'http%s' % (request.is_secure() and 's' or '')
    di = dict(redirect_uri=urllib.quote('%s://%s/admin/jmbo_facebook/handler' % (protocol, site.domain)), client_id=settings.JMBO_FACEBOOK['app_id'], client_secret=settings.JMBO_FACEBOOK['app_secret'], code=code)
    url = 'https://graph.facebook.com/oauth/access_token?client_id=%(client_id)s&redirect_uri=%(redirect_uri)s&client_secret=%(client_secret)s&code=%(code)s' % di
    try:
        response = urllib2.urlopen(url)
    except Exception as e:
        msg = 'Something went wrong. Headers: %s' % str(e.headers.items())
        messages.error(request, msg, fail_silently=True)
        return redirect

    access_token = response.read().replace('access_token=', '')
    url = 'https://graph.facebook.com/me/accounts?access_token=' + access_token
    try:
        response = urllib2.urlopen(url)
    except Exception as e:
        msg = 'Something went wrong. Headers: %s' % str(e.headers.items())
        messages.error(request, msg, fail_silently=True)
        return redirect

    json = simplejson.loads(response.read())
    for di in json['data']:
        facebook_id = di['id']
        page, dc = Page.objects.get_or_create(facebook_id=facebook_id)
        page.title = di['name']
        page.access_token = di['access_token']
        page.save()

    msg = 'Created / updated pages. You must publish the relevant pages.'
    messages.success(request, msg, fail_silently=True)
    return redirect