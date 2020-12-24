# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gustavofonseca/prj/github/scielo-django-extensions/scielo_extensions/templatetags/scielo_common.py
# Compiled at: 2012-09-10 13:55:15
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as __
from django.conf import settings
from django import template
register = template.Library()
GLOSSARY_URL = settings.DOCUMENTATION_BASE_URL + '/glossary.html#'

def easy_tag(func):
    """
    Deals with the repetitive parts of parsing template tags
    """

    def inner(parser, token):
        try:
            return func(*token.split_contents())
        except TypeError:
            raise template.TemplateSyntaxError('Bad arguments for tag "%s"' % token.split_contents()[0])

    inner.__name__ = func.__name__
    inner.__doc__ = inner.__doc__
    return inner


def full_path(context, **params):
    url_path = ''
    url_get = context['request'].GET.copy()
    if 'PATH_INFO' in context['request'].META:
        url_path = context['request'].META['PATH_INFO']
    for key, value in params.items():
        url_get[key] = value

    if len(url_get):
        url_path += '?%s' % ('&').join('%s=%s' % (key, value) for key, value in url_get.items() if value)
    return url_path.encode('utf8')


class NamedPagination(template.Node):

    def __init__(self, letters, selected):
        self.letters = template.Variable(letters)
        self.selected = template.Variable(selected)

    def render(self, context):
        letters = self.letters.resolve(context)
        selected = self.selected.resolve(context)
        html_snippet = '<div class="pagination" style="margin:0;padding-top:8px;text-align:center;">\n            <ul><li><a href="?" style="line-height: 20px;padding: 0 5px;">' + str(__('All')) + '</a></li>'
        for letter in letters:
            if letter != selected:
                html_snippet += ('\n                <li><a href="{0}" style="line-height: 20px;padding: 0 5px;">{1}</a></li>').format(full_path(context, letter=letter), letter.encode('utf8'))
            else:
                html_snippet += ('\n                <li class="active"><a href="{0}" style="line-height: 20px;padding: 0 5px;">{1}</a></li>').format(full_path(context, letter=letter), letter.encode('utf8'))

        html_snippet += '\n            </ul></div>'
        return html_snippet


@register.tag()
@easy_tag
def named_pagination(_tag_name, *params):
    return NamedPagination(*params)


class Pagination(template.Node):

    def __init__(self, object_record):
        self.object_record = template.Variable(object_record)

    def render(self, context):
        object_record = self.object_record.resolve(context)
        if not object_record.paginator:
            return ''
        else:
            if object_record.paginator.count > settings.PAGINATION__ITEMS_PER_PAGE:
                class_li_previous = 'disabled' if not object_record.has_previous() else ''
                class_li_next = 'disabled' if not object_record.has_next() else ''
                html_pages = []
                for page in object_record.paginator.page_range:
                    class_li_page = 'active' if object_record.number == page else ''
                    html_pages.append(('<li class="{0}"><a href="{1}">{2}</a></li>').format(class_li_page, full_path(context, page=page), page))

                html_snippet = ('\n                <div class="pagination">\n                <ul>\n                <li class="prev {0}"><a href="{1}">&larr; {2}</a></li>\n                {3}\n                <li class="next {4}"><a href="{5}">{6} &rarr;</a></li>\n                </ul>\n                </div>\n                ').format(class_li_previous, full_path(context, page=object_record.previous_page_number()), _('Previous'), ('').join(html_pages), class_li_next, full_path(context, page=object_record.next_page_number()), _('Next'))
                return html_snippet
            return ''


@register.tag()
@easy_tag
def pagination(_tag_name, params):
    return Pagination(params)


class SimplePagination(template.Node):

    def __init__(self, object_record):
        self.object_record = template.Variable(object_record)

    def render(self, context):
        object_record = self.object_record.resolve(context)
        if not object_record.paginator:
            return ''
        else:
            if object_record.paginator.count > settings.PAGINATION__ITEMS_PER_PAGE:
                class_li_previous = 'disabled' if not object_record.has_previous() else ''
                class_li_next = 'disabled' if not object_record.has_next() else ''
                html_snippet = ('\n                <span style=""><b>{0}-{1}</b> {2} <b>{3}</b></span>\n                <span class="pagination"><ul>\n                <li class="prev {4}">\n                <a href="{5}">&larr;</a></li>\n                <li class="next {6}">\n                <a href="{7}">&rarr;</a></li>\n                </ul></span>\n                ').format(object_record.start_index(), object_record.end_index(), _('of'), object_record.paginator.count, class_li_previous, full_path(context, page=object_record.previous_page_number()), class_li_next, full_path(context, page=object_record.next_page_number()))
                return html_snippet
            return ''


@register.tag()
@easy_tag
def simple_pagination(_tag_name, params):
    return SimplePagination(params)


class FieldHelpText(template.Node):

    def __init__(self, field_name, help_text, glossary_refname):
        self.field_name = template.Variable(field_name)
        self.help_text = template.Variable(help_text)
        self.glossary_refname = glossary_refname

    def render(self, context):
        field_name = self.field_name.resolve(context)
        help_text = self.help_text.resolve(context)
        glossary_refname = self.glossary_refname
        for value in ['field_name', 'help_text', 'glossary_refname']:
            if len(locals().get(value)) < 1:
                return ''

        html_snippet = ('\n            <a class="help-text"\n               target="_blank"\n               rel="popover"\n               data-original-title="{0} {1}"\n               data-content="{2}"\n               href="{3}{4}">\n                <i class="icon-question-sign">&nbsp;</i>\n            </a>\n        ').format(_('Help on:'), field_name, help_text, GLOSSARY_URL, glossary_refname).strip()
        return html_snippet


@register.tag()
@easy_tag
def field_help(_tag_name, *params):
    """
    Renders the help for a given field.

    Usage: {% field_help field_label help_text %}
    """
    return FieldHelpText(*params)