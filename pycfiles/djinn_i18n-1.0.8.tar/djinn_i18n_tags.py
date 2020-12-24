# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_i18n/djinn_i18n/templatetags/djinn_i18n_tags.py
# Compiled at: 2014-08-22 05:05:49
from django.template import Library
from djinn_i18n.tool import TOOL
register = Library()

@register.filter(name='is_override')
def is_override(msgid, locale):
    return TOOL.is_override(msgid, locale)


@register.filter(name='is_fuzzy')
def is_fuzzy(entry):
    return 'fuzzy' in entry.flags