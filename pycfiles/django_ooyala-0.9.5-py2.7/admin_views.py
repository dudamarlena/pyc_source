# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ooyala/admin_views.py
# Compiled at: 2011-01-27 11:10:56
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.http import HttpResponse
from datetime import datetime, date, timedelta
from ooyala.conf import *
from ooyala.library import OoyalaQuery, OoyalaLabelManage, OoyalaChannel, OoyalaAnalytics
from ooyala.constants import OoyalaConstants as O
from ooyala.models import OoyalaItem

@staff_member_required
def backlot_query(request):
    req = OoyalaQuery(page_id=500)
    ooyala_response = req.process()
    print ooyala_response
    print req.url
    if type(ooyala_response) != str:
        items = ooyala_response.getElementsByTagName('item')
        return HttpResponse(ooyala_response.toprettyxml(), mimetype='text/xml')
    print 'got an error back'
    return HttpResponse('tada')