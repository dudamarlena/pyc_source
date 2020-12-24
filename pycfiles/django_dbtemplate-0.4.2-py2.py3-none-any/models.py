# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kubus/workspace/django-dbtemplate/dbtemplate/models.py
# Compiled at: 2015-06-08 01:34:17
import yaml
from django.db import models
from django.dispatch import receiver
from django.db.models import signals as model_signals
from django.utils.translation import ugettext_lazy as _
from django.template import loader
try:
    from django.template.backends.django import DjangoTemplates
    TEMPLATE_ENGINE = DjangoTemplates
except ImportError:
    TEMPLATE_ENGINE = None

class Template(models.Model):
    slug = models.CharField(_('slug'), max_length=255, unique=True)
    data = models.TextField(_('content'))
    specs = models.TextField(_('specification'), default='')

    class Meta:
        verbose_name = _('template')
        verbose_name_plural = _('templates')

    def __unicode__(self):
        return self.slug

    def get_context_specs(self):
        return yaml.load(self.specs)['context']


@receiver(model_signals.post_save, sender=Template)
def on_save_template_invalidate_loader_cache(**kwargs):
    if TEMPLATE_ENGINE is None:
        from django.template.loader import template_source_loaders
        if not template_source_loaders:
            return
        loaders = template_source_loaders
    else:
        for engine in loader.engines.all():
            if not isinstance(engine, DjangoTemplates):
                return
            loaders = engine.engine.template_loaders

        for template_loader in loaders:
            template_loader.reset()

    return