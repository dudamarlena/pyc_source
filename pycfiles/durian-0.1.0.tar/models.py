# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/devel/durian/durian/models.py
# Compiled at: 2009-09-12 09:43:32
from django.db import models
from django.utils.translation import ugettext_lazy as _
from celery.fields import PickledObjectField
from celery.serialization import pickle

class Listener(models.Model):
    hook = models.CharField(_('hook'), max_length=255, help_text=_('Connects to hook'))
    url = models.URLField(verify_exists=False, help_text=_("The URL I'm listening at."))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    config = PickledObjectField(_('configuration'), default=pickle.dumps({}), help_text=_('Hook specific configuration.'))
    match = PickledObjectField(_('conditions'), default=pickle.dumps({}), help_text=_('Hook specific event filter'))

    class Meta:
        verbose_name = _('listener')
        verbose_name_plural = _('listeners')

    def __unicode__(self):
        return '%s match:%s config:%s' % (
         self.url, self.match, self.config)