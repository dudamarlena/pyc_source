# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/siyuan/projects/django-simplemde/testproject/simplemde/widgets.py
# Compiled at: 2018-01-17 09:49:38
# Size of source mod 2**32: 1554 bytes
from __future__ import unicode_literals
import uuid
from django import forms
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.conf import settings
try:
    from django.core.urlresolvers import reverse_lazy
except ImportError:
    from django.urls import reverse_lazy

from .utils import json_dumps
GLOBAL_OPTIONS = getattr(settings, 'SIMPLEMDE_OPTIONS', {})

class SimpleMDEEditor(widgets.Textarea):

    def __init__(self, *args, **kwargs):
        self.custom_options = kwargs.pop('simplemde_options', {})
        (super(SimpleMDEEditor, self).__init__)(*args, **kwargs)

    @property
    def options(self):
        options = GLOBAL_OPTIONS.copy()
        if 'autosave' in options:
            if options['autosave'].get('enabled', False):
                options['autosave']['uniqueId'] = str(uuid.uuid4())
        options.update(self.custom_options)
        return options

    def render(self, name, value, attrs=None):
        if 'class' not in attrs.keys():
            attrs['class'] = ''
        attrs['class'] += ' simplemde-box'
        attrs['data-simplemde-options'] = json_dumps(self.options)
        html = super(SimpleMDEEditor, self).render(name, value, attrs)
        return mark_safe(html)

    def _media(self):
        js = ('simplemde/simplemde.min.js', 'simplemde/simplemde.init.js')
        css = {'all': ('simplemde/simplemde.min.css', )}
        return forms.Media(css=css, js=js)

    media = property(_media)