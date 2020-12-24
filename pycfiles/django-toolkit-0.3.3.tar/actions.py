# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ahayes/.virtualenvs/roicrm-django1.7/local/lib/python2.7/site-packages/django_toolkit/templatetags/actions.py
# Compiled at: 2014-01-23 22:33:11
from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag
def actions(obj, **kwargs):
    """
    Return actions available for an object
    """
    if 'exclude' in kwargs:
        kwargs['exclude'] = kwargs['exclude'].split(',')
    actions = obj.get_actions(**kwargs)
    if isinstance(actions, dict):
        actions = actions.values()
    buttons = ('').join('%s' % action.render() for action in actions)
    return '<div class="actions">%s</div>' % buttons