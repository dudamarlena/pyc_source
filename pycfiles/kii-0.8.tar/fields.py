# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/base_models/fields.py
# Compiled at: 2014-12-31 04:01:40
from django.db import models
from django.utils.safestring import mark_safe
from django_extensions.db import fields
from django.conf import settings
import markdown

class Markdown(object):

    def __init__(self, instance, field_name):
        self.instance = instance
        self.field_name = field_name

    def _get_raw(self):
        return self.instance.__dict__[self.field_name]

    def _set_raw(self, val):
        setattr(self.instance, self.field_name, val)

    raw = property(_get_raw, _set_raw)
    markup_type = 'markdown'

    def _get_rendered(self):
        if self.instance.__dict__[('{0}_markup_type').format(self.field_name)] == 'markdown':
            return mark_safe(getattr(settings, 'MARKDOWN_FUNCTION', markdown.markdown)(self.raw))
        else:
            return self.raw

    rendered = property(_get_rendered)

    def __unicode__(self):
        return self.raw

    __str__ = __unicode__


class MarkdownDescriptor(object):

    def __init__(self, field):
        self.field = field

    def __get__(self, instance, owner):
        if instance is None:
            raise AttributeError('Can only be accessed via an instance.')
        markup = instance.__dict__[self.field.name]
        if markup is None:
            return
        else:
            return Markdown(instance, self.field.name)

    def __set__(self, obj, value):
        if isinstance(value, Markdown):
            obj.__dict__[self.field.name] = value.raw
        else:
            obj.__dict__[self.field.name] = value


class MarkdownField(models.TextField):
    """Let the user chose among different markup types (ReST, Textile, HTML,
    Markdown). Defaults to markdown.
    """

    def contribute_to_class(self, cls, name):
        super(MarkdownField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, MarkdownDescriptor(self))


class SlugField(fields.AutoSlugField):
    """A custom SlugField that can define his value based on another
    model field.
    """
    pass