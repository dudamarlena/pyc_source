# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/ITTEKV2/MANAGER/app/apps/track/views.py
# Compiled at: 2018-01-10 08:30:56
# Size of source mod 2**32: 1350 bytes
import requests, workon
from django import forms
from django.utils.text import Truncator
from apps.track.models import TrackEvent
app_name = 'track'
__all__ = [
 'List']
route = '^track/events/'
url_name = 'app:track-events'

@workon.route(route + '$', url_name)
class List(workon.List):
    filters = []
    fields = [
     workon.ListCol('action', label='Action', col=1),
     workon.ListCol('object', label='Object', col=2),
     workon.ListCol('field_name', label='Champ', col=1),
     workon.ListCol('old_value', label='old', col=2),
     workon.ListCol('new_value', label='new', col=2),
     workon.ListCol('m2m_repr_set', label='set', col=2),
     workon.ListCol('user', label='user', col=2)]

    def get_update_method(self, obj):
        return 'data-modal'

    def get_queryset(self):
        qs = TrackEvent.objects.all()
        return qs