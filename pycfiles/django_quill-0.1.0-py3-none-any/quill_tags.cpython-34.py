# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rsenkbeil/Projects/gs/django-quill/quill/templatetags/quill_tags.py
# Compiled at: 2014-12-16 20:48:34
# Size of source mod 2**32: 1034 bytes
import json
from django import template
from django.apps import apps
register = template.Library()
quill_app = apps.get_app_config('quill')

@register.filter()
def quill_conf(name):
    """Get a value from the configuration app."""
    return getattr(quill_app, name)


quill_conf.is_safe = True

@register.filter()
def quill_conf_json(name):
    """Get a value from the configuration app as JSON."""
    return json.dumps(getattr(quill_app, name))


quill_conf_json.is_safe = True

@register.simple_tag(takes_context=True)
def render_toolbar(context, config):
    """Render the toolbar for the given config."""
    quill_config = getattr(quill_app, config)
    t = template.loader.get_template(quill_config['toolbar_template'])
    return t.render(context)


@register.simple_tag(takes_context=True)
def render_editor(context, config):
    """Render the editor for the given config."""
    quill_config = getattr(quill_app, config)
    t = template.loader.get_template(quill_config['editor_template'])
    return t.render(context)