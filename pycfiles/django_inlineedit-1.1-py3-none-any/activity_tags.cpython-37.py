# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\pedro\OneDrive\dev\altimapa\forum-live\activities\templatetags\activity_tags.py
# Compiled at: 2019-11-08 17:28:54
# Size of source mod 2**32: 1934 bytes
from django import template
from django.utils.timezone import now
from datetime import timedelta
from activities.models import Activity
from common.templatetags import acf
register = template.Library()

@register.simple_tag
def task_due_as_style(activity):
    """Return color coding for a task or activity due date (red for overdue, orange for today, yellow for tomorrow)"""
    if not activity.due_on:
        return ''
    t0 = now()
    t1 = t0 + timedelta(days=1)
    t2 = t1 + timedelta(days=1)
    if activity.due_on < t0:
        return 'color:#d9534f'
    if activity.due_on < t1:
        return 'color:#ff6e0d'
    if activity.due_on < t2:
        return 'color:#f0ad4e'
    return 'color:black'


@register.simple_tag
def task_status_as_faicon(activity):
    """Return Font Awesome icon for task status"""
    if activity.status == activity.NOT_STARTED:
        return acf.faicon('circle-o')
    if activity.status == activity.ONGOING:
        return acf.faicon('adjust')
    if activity.status == activity.DONE:
        return acf.faicon('check-circle-o')
    if activity.status == activity.CANCELLED:
        return acf.faicon('times-circle-o')
    if activity.status == activity.PROBLEM:
        return acf.faicon('exclamation-circle')
    return


@register.simple_tag
def get_activities(object, category=None, user=None, exclude=None):
    qs = Activity.get_activities(object).order_by('-updated_on')
    if qs:
        if user:
            qs = qs.filter(user=user)
        if category:
            qs = qs.filter(category=category)
        if exclude:
            qs = qs.exclude(category=exclude)
    return qs


@register.simple_tag
def get_tasks(object, user=None, live_only=True):
    qs = Activity.get_activities(object).filter(categroy=(Activity.TASK))
    if qs:
        if user:
            qs = qs.filter(user=user)
    if qs:
        if live_only:
            qs = qs.exclude(status=(Activity.DONE)).exclude(status=(Activity.CANCELLED))
    return qs