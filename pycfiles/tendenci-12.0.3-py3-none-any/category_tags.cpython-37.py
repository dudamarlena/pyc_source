# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/categories/templatetags/category_tags.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 1909 bytes
from django.template import Library, Node, Variable
from tendenci.apps.categories.models import Category
register = Library()

class GetCategoryForObjectNode(Node):

    def __init__(self, object, context):
        self.object = Variable(object)
        self.context = context

    def render(self, context):
        if not self.context:
            self.context = 'category'
        elif not self.object:
            context[self.context] = ''
            return ''
            object = self.object.resolve(context)
            category = Category.objects.get_for_object(object, 'category')
            if category:
                context[self.context] = category
        else:
            context[self.context] = ''
        return ''


@register.tag
def get_category_for_object(parser, token):
    """
        {% get_category_for_object object %}
    """
    bits = token.split_contents()
    try:
        object = bits[1]
    except:
        object = None

    try:
        context = bits[3]
    except:
        context = None

    return GetCategoryForObjectNode(object, context)


class GetSubCategoryForObjectNode(Node):

    def __init__(self, object, context):
        self.object = Variable(object)
        self.context = context

    def render(self, context):
        if not self.context:
            self.context = 'sub_category'
        elif not self.object:
            context[self.context] = ''
            return ''
            object = self.object.resolve(context)
            category = Category.objects.get_for_object(object, 'sub_category')
            if category:
                context[self.context] = category
        else:
            context[self.context] = ''
        return ''


@register.tag
def get_sub_category_for_object(parser, token):
    """
        {% get_sub_category_for_object object as sub_category %}
    """
    bits = token.split_contents()
    try:
        object = bits[1]
    except:
        object = None

    try:
        context = bits[3]
    except:
        context = None

    return GetSubCategoryForObjectNode(object, context)