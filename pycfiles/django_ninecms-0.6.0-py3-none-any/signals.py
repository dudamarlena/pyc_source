# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/dev-p5qc/workspace/python/team_reset/ninecms/signals.py
# Compiled at: 2015-03-23 06:16:29
""" Signal definitions for Nine CMS """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'
from django import dispatch
from ninecms.models import TaxonomyTerm, Node
block_signal = dispatch.Signal(providing_args=['view', 'request'])

@dispatch.receiver(block_signal)
def render_view(**kwargs):
    if kwargs['view'] == 'terms':
        return TaxonomyTerm.objects.all()
    if kwargs['view'] == 'random video node':
        return Node.objects.filter(page_type__name='video').prefetch_related('video_set').order_by('?').first()