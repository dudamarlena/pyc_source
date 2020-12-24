# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/movister/env/src/django-email-html/email_html/templatetags/email_html.py
# Compiled at: 2016-02-01 06:42:04
from django import template
from subprocess import Popen, PIPE
from bs4 import BeautifulSoup
try:
    unicode_type = unicode
except NameError:
    unicode_type = str

register = template.Library()

@register.filter
def html2text(value):
    """
    Pipes given HTML string into the text browser W3M, which renders it.
    Rendered text is grabbed from STDOUT and returned.
    """
    try:
        cmd = 'w3m -dump -T text/html -O utf-8'
        proc = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, universal_newlines=True)
        return proc.communicate(str(value))[0]
    except OSError:
        return value


@register.filter
def extract_urllinks(value, template='%(text)s (%(url)s)'):
    """
    Extract urls from links and put it to brackets after links. Useful for generating plain version of email body from html
    """
    html = BeautifulSoup(value)
    for link in html.findAll('a'):
        text = ('').join(map(unicode_type, link.contents)).strip()
        if link.get('href') and link.get('href') != text:
            result = template % {'text': text, 
               'url': link['href'].replace('\n', '')}
        elif text:
            result = text
        link.replaceWith(result)

    return html