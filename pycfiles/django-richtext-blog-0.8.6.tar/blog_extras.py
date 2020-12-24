# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tim/projects/wholebaked-site/venv/local/lib/python2.7/site-packages/richtext_blog/templatetags/blog_extras.py
# Compiled at: 2012-05-23 10:49:38
import re, calendar
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from pygments import lexers, formatters, highlight
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
register = template.Library()

@register.filter
def month_name(value):
    """
    Returns the name of the month for the number passed in. Number must be
    between 1 and 12
    """
    try:
        value = int(value)
    except ValueError:
        return ''

    if value < 1 or value > 12:
        return ''
    return calendar.month_name[value]


@register.filter
@stringfilter
def pygmentize(value, pre_class=''):
    """
    Expects the raw html content of a post as `value`.
    This function will look through the content for any <pre> tags and update
    their contents to include css classes as per syntax highlighting according
    to pygments.
    Can take an optional argument that dictates what css class the resulting
    'pre' pre tag will have.
    Returns the html passed in with the updated <pre> tags included.
    Loosely based on:
    http://www.ofbrooklyn.com/2010/01/15/syntax-highlighting-django-using-pygments/
    """
    soup = BeautifulSoup(value)
    for pre_tag in soup.findAll('pre'):
        keep_lines = []
        for line in pre_tag.prettify().splitlines():
            if line.startswith('<br />'):
                continue
            keep_lines.append(line.replace('&nbsp;', ' '))

        pre_tag_string = ('\n').join(keep_lines)
        pre_string = BeautifulSoup(pre_tag_string, convertEntities=BeautifulSoup.HTML_ENTITIES).findAll('pre')[0].string
        try:
            pre_tag_class = pre_tag['class']
        except KeyError:
            pre_tag_class = ''

        if pre_tag_class:
            lexer = lexers.get_lexer_by_name(pre_tag_class)
        else:
            try:
                lexer = lexers.guess_lexer(pre_string)
            except ValueError:
                lexer = lexers.TextLexer()

        pre_soup = BeautifulSoup(highlight(pre_string, lexer, formatters.HtmlFormatter()))
        if pre_class:
            for pre_tag in pre_soup('pre'):
                pre_tag['class'] = pre_class

        pre_tag.replaceWith(pre_soup)

    return mark_safe(soup)