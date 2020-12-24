# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/quran/templatetags/quran.py
# Compiled at: 2009-12-06 21:51:32
from django import template
from quran.models import *
register = template.Library()

@register.filter(name='translate')
def translate(value, arg=Translation.get(id=1)):
    """
    Display the translation for the given aya
    """
    return TranslatedAya.get(aya=aya, translation=translation)