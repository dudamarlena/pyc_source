# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/templatetags/survey_extras.py
# Compiled at: 2019-03-02 04:44:34
# Size of source mod 2**32: 739 bytes
from django import template
register = template.Library()

def collapse_form(form, category):
    """ Permit to return the class of the collapsible according to errors in
    the form. """
    categories_with_error = set()
    for field in form:
        if field.errors:
            categories_with_error.add(field.field.widget.attrs['category'])

    if category.name in categories_with_error:
        return 'in'
    return ''


register.filter('collapse_form', collapse_form)

class CounterNode(template.Node):

    def __init__(self):
        self.count = 0

    def render(self, context):
        self.count += 1
        return self.count


@register.tag
def counter(parser, token):
    return CounterNode()