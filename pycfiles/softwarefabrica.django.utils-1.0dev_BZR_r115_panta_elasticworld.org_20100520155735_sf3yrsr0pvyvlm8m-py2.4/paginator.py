# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/utils/templatetags/paginator.py
# Compiled at: 2009-10-07 03:14:04
from django import template
from django.utils.html import conditional_escape, escape
from django.utils.safestring import mark_safe
from softwarefabrica.django.utils.templates import CachedTemplateLibrary
register = CachedTemplateLibrary()

def paginator(context, url='', adjacent_pages=5, paginator_object_name='paginator', page_object_name='page_obj'):
    """
    To be used in conjunction with the object_list generic view.

    Adds pagination context variables for use in displaying first, adjacent and
    last page links in addition to those created by the object_list generic
    view.

    @see: http://www.djangosnippets.org/snippets/73/
    @see: http://www.djangosnippets.org/snippets/208/
    """
    paginator = None
    page_obj = None
    if context.has_key(paginator_object_name):
        paginator = context[paginator_object_name]
    if context.has_key(page_object_name):
        page_obj = context[page_object_name]
    if not (paginator and page_obj):
        return {'is_paginated': False, 'paginator': None}
    page_numbers = [ n for n in range(page_obj.number - adjacent_pages, page_obj.number + adjacent_pages + 1) if n > 0 if n <= paginator.num_pages ]
    res = {'is_paginated': True, 'paginator': paginator, 'page_obj': page_obj, 'url': url, 'page_numbers': page_numbers, 'show_first': 1 not in page_numbers, 'show_last': paginator.num_pages not in page_numbers}
    keys = (
     'is_paginated', 'hits', 'results_per_page', 'page', 'pages', 'next', 'previous', 'has_next', 'has_previous', 'first_on_page', 'last_on_page', 'page_range', 'paginator', 'page_obj', 'is_popup', 'request', 'q', paginator_object_name, page_object_name)
    for k in keys:
        if k in context:
            res.update({k: context[k]})

    return res


register.inclusion_tag('utils/paginator.html', takes_context=True)(paginator)

class PaginatorPageLinkNode(template.Node):
    __module__ = __name__

    def __init__(self, page_num, page_var='page'):
        self.page_num = template.Variable(page_num)
        self.page_var = page_var

    def render(self, context):
        request = None
        try:
            request = context['request']
        except:
            request = context['pagevars'].request

        try:
            page_num_value = self.page_num.resolve(context)
        except template.VariableDoesNotExist:
            return ''

        get_qd = request.GET.copy()
        get_qd[self.page_var] = page_num_value
        qs = get_qd.urlencode()
        fullpath = '%s%s' % (request.path, qs and '?' + qs or '')
        return mark_safe(fullpath)


def do_paginator_page_link(parser, token):
    """
    Return the link (href) for a paginated page.
    It requires one argument (the page number),
    and also requires that the request object be in the context as 
    directly under the ``request`` name or by putting the standard
    ``pagevars`` object in the context.
    """
    try:
        (tag_name, page_num) = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%r tag requires a single argument' % token.contents.split()[0]

    page_num = page_num.strip('"')
    return PaginatorPageLinkNode(page_num)


register.tag('paginator_page_link', do_paginator_page_link)