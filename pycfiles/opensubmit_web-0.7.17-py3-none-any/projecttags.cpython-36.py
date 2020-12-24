# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ptroeger/repo/opensubmit/web/opensubmit/templatetags/projecttags.py
# Compiled at: 2018-10-12 02:12:24
# Size of source mod 2**32: 1869 bytes
from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
import os
register = template.Library()

@register.filter(name='basename')
@stringfilter
def basename(value):
    return os.path.basename(value)


@register.filter(name='replace_macros')
@stringfilter
def replace_macros(value, user_dict):
    return value.replace('#FIRSTNAME#', user_dict['first_name'].strip()).replace('#LASTNAME#', user_dict['last_name'].strip())


@register.filter(name='state_label_css')
def state_label_css(subm):
    green_label = 'badge label label-success'
    red_label = 'badge label label-important'
    grey_label = 'badge label label-info'
    if subm.is_closed():
        if subm.grading:
            if subm.grading.means_passed:
                return green_label
            return red_label
    if subm.state in [subm.SUBMITTED_TESTED,
     subm.SUBMITTED,
     subm.TEST_FULL_PENDING,
     subm.GRADED,
     subm.TEST_FULL_FAILED]:
        return green_label
    else:
        if subm.state == subm.TEST_VALIDITY_FAILED:
            return red_label
        return grey_label


@register.assignment_tag
def setting(name):
    return getattr(settings, name, '')


@register.inclusion_tag('inclusion_tags/details_table.html')
def details_table(submission):
    return {'submission': submission}


@register.inclusion_tag('inclusion_tags/deadline.html')
def deadline_timeout(assignment):
    return {'assignment':assignment,  'show_timeout':True}


@register.inclusion_tag('inclusion_tags/deadline.html')
def deadline(assignment):
    return {'assignment':assignment,  'show_timeout':False}


@register.inclusion_tag('inclusion_tags/grading.html')
def grading(submission):
    return {'submission': submission}