# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Data/Users/steven.skoczen/.virtualenvs/project_tomo/src/heroku-web-autoscale/heroku_web_autoscale/views.py
# Compiled at: 2012-03-05 16:48:30
import tempfile
from django.core.cache import cache
from django.http import HttpResponse
from heroku_web_autoscale.models import HeartbeatTestData

def heartbeat(request):
    rand_number = '%s' % HeartbeatTestData.objects.order_by('?')[0].number
    cached_val = cache.get('heroku_web_autoscale-cached-value')
    if not cached_val:
        cache.set('heroku_web_autoscale-cached-value', '1234')
        cached_val = cache.get('heroku_web_autoscale-cached-value')
    t = tempfile.TemporaryFile()
    t.write('%s %s' % (rand_number, cached_val))
    t.flush()
    t.seek(0)
    assert '%s %s' % (rand_number, cached_val) == t.read()
    return HttpResponse('Beat', content_type='text/plain')