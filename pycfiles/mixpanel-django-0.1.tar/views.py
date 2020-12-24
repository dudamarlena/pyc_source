# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/Aptana_Studio_Workspace/mp_test/mixpanel_django/example/mp_example/views.py
# Compiled at: 2010-12-17 04:04:48
from django.shortcuts import render_to_response
from mixpanel_django.backends import mp_backend

def test_mp_view(request):
    mp_backend.trackMixpanelEvent('index page loaded', {'gender': 'male'}, request)
    mp_backend.trackMixpanelEvent('index page loaded', {'gender': 'female'}, request)
    mp_backend.trackfunnelMixpanelEvent('Signup', 1, 'opened front page', {'gender': 'male'}, request)
    mp_backend.trackfunnelMixpanelEvent('Signup', 2, 'clicked signup button', {'gender': 'male'}, request)
    mp_backend.trackfunnelMixpanelEvent('Signup', 3, 'confirmed email address ', {'gender': 'male'}, request)
    return render_to_response('test_mp.html', {})