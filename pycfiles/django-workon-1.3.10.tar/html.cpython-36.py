# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/DJANGO-WORKON/workon/utils/html.py
# Compiled at: 2018-02-14 05:20:45
# Size of source mod 2**32: 1139 bytes
from django.shortcuts import render
from django.template.loader import get_template
__all__ = [
 'render_content', 'sanitize', 'html2text']

def render_content(request, template, context):
    if request:
        return str(render(request, template, context).content, 'utf-8')
    else:
        html_template = get_template(template)
        return html_template.render(context)


def sanitize(html):
    if not has_bleach:
        logger.warning('Bleach is missing for sanitizing HTML.')
        return html
    else:
        return bleach.clean(html)


def html2text(html):
    try:
        from bs4 import BeautifulSoup
    except:
        raise ImportError('Beautiful Soup is missing to get html2text. Please pip install "beautifulsoup4>=4.6.0"')

    if html:
        soup = BeautifulSoup(html, 'lxml')
        return soup.get_text()
    else:
        return ''