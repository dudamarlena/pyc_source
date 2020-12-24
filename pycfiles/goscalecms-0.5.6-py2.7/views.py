# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/goscale/views.py
# Compiled at: 2013-03-04 06:55:06
import urllib2, urllib
from django import http
from django.utils.translation import ugettext as _

def form(request):
    """ Ajax handler for Google Form submition
    """
    if request.method == 'POST':
        url = request.POST['url']
        submit_url = '%s%shl=%s' % (
         url,
         '&' if '?' in url else '?',
         request.LANGUAGE_CODE)
        params = urllib.urlencode(request.POST)
        f = urllib2.urlopen(submit_url, params)
        text = f.read()
    else:
        text = _('Error: request type has to be POST')
    response = http.HttpResponse(text, mimetype='text/plain')
    return response