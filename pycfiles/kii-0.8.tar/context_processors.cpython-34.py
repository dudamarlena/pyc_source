# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/stream/context_processors.py
# Compiled at: 2015-01-18 07:28:37
# Size of source mod 2**32: 823 bytes
from . import models

def streams(request):
    """Add request user streams"""
    context = {}
    if request.user.is_authenticated():
        context['user_streams'] = models.Stream.objects.filter(owner=request.user)
        if request.session.get('selected_stream'):
            selected_stream = models.Stream.objects.get(pk=request.session.get('selected_stream'))
        else:
            selected_stream = models.Stream.objects.get_user_stream(request.user)
        context['selected_stream'] = selected_stream
    return context


def stream_models(request):
    """Add availble stream item subclasses and stream model"""
    return {'item_models': sorted(models.StreamItem.__subclasses__(), key=lambda x: x._meta.verbose_name), 
     'stream_model': models.Stream}