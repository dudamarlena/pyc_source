# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/community/participation/models/layer_participation_settings.py
# Compiled at: 2015-03-02 10:21:03
from django.db import models
from django.utils.translation import ugettext_lazy as _
from nodeshot.core.layers.models import Layer

class LayerParticipationSettings(models.Model):
    """
    Layer settings regarding participation
    """
    layer = models.OneToOneField(Layer, related_name='layer_participation_settings')
    voting_allowed = models.BooleanField(_('voting allowed?'), default=True)
    rating_allowed = models.BooleanField(_('rating allowed?'), default=True)
    comments_allowed = models.BooleanField(_('comments allowed?'), default=True)

    def __unicode__(self):
        return self.layer.name

    class Meta:
        app_label = 'participation'
        db_table = 'participation_layer_settings'
        verbose_name_plural = 'participation_layer_settings'