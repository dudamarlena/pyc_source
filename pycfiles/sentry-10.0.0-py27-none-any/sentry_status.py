# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/templatetags/sentry_status.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import, print_function
import itertools
from django import template
from sentry import status_checks
from sentry.status_checks import sort_by_severity
register = template.Library()

@register.inclusion_tag('sentry/partial/system-status.html', takes_context=True)
def show_system_status(context):
    problems = itertools.chain.from_iterable(status_checks.check_all().values())
    return {'problems': sort_by_severity(problems)}