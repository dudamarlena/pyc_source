# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/4f/p6rdjlq11nz2jwrtdlm918l40000gn/T/pip-install-o463eux1/django-toolware/toolware/templatetags/highlight.py
# Compiled at: 2018-06-21 10:53:48
# Size of source mod 2**32: 1823 bytes
import re
from django import template
from django.template import Node, TemplateSyntaxError
from django.conf import settings
from django.utils.safestring import mark_safe
from ..utils.query import get_text_tokenizer
register = template.Library()

def highlight_text(needles, haystack, cls_name='highlighted', words=False, case=False):
    """ Applies cls_name to all needles found in haystack. """
    if not needles:
        return haystack
    else:
        if not haystack:
            return ''
        else:
            if words:
                pattern = '(%s)' % '|'.join(['\\b{}\\b'.format(re.escape(n)) for n in needles])
            else:
                pattern = '(%s)' % '|'.join([re.escape(n) for n in needles])
            if case:
                regex = re.compile(pattern)
            else:
                regex = re.compile(pattern, re.I)
        i, out = (0, '')
        for m in regex.finditer(haystack):
            out += ''.join([haystack[i:m.start()], '<span class="%s">' % cls_name,
             haystack[m.start():m.end()], '</span>'])
            i = m.end()

        return mark_safe(out + haystack[i:])


@register.filter
def highlight(string, keywords, cls_name='highlighted'):
    """ Given an list of words, this function highlights the matched text in the given string. """
    if not keywords:
        return string
    else:
        if not string:
            return ''
        include, exclude = get_text_tokenizer(keywords)
        highlighted = highlight_text(include, string, cls_name)
        return highlighted


@register.filter
def highlight_words(string, keywords, cls_name='highlighted'):
    """ Given an list of words, this function highlights the matched words in the given string. """
    if not keywords:
        return string
    else:
        if not string:
            return ''
        include, exclude = get_text_tokenizer(keywords)
        highlighted = highlight_text(include, string, cls_name, words=True)
        return highlighted