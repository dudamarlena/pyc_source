# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/voice/templatetags/feature_extras.py
# Compiled at: 2011-09-23 18:57:40
from django import template
register = template.Library()

@register.filter
def votes_left(feature):
    return feature.votes_left()


@register.filter
def state(feature):
    return feature.get_state_display()


@register.filter
def votes(feature):
    return feature.total_votes()