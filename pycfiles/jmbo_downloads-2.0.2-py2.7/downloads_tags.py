# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/downloads/templatetags/downloads_tags.py
# Compiled at: 2015-04-21 15:31:46
from django import template
from django.template.loader import render_to_string
register = template.Library()

@register.tag
def render_category(parser, token):
    try:
        tag_name, category_dict, first, last = token.split_contents()
        return CategoryNode(category_dict, first, last)
    except ValueError:
        try:
            tag_name, category_dict = token.split_contents()
            return CategoryNode(category_dict)
        except ValueError:
            raise template.TemplateSyntaxError('render_category tag requires argument category_dict')


class CategoryNode(template.Node):

    def __init__(self, category_dict, first=False, last=False):
        self.category_dict = template.Variable(category_dict)
        self.first = first if type(first) == bool else template.Variable(first)
        self.last = last if type(last) == bool else template.Variable(last)

    def render(self, context):
        extra = {'category': self.category_dict.resolve(context), 
           'first': self.first if type(self.first) == bool else self.first.resolve(context), 
           'last': self.last if type(self.last) == bool else self.last.resolve(context)}
        return render_to_string('downloads/inclusion_tags/download_category.html', extra)