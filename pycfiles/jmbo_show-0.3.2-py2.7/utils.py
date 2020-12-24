# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/show/utils.py
# Compiled at: 2013-09-27 03:40:37
from django.core.cache import cache
from django.utils import timezone
from show.models import Show

def get_current_next_permitted_show(klass=Show, now=None):
    use_cache = False
    if now is None:
        use_cache = True
        klass_name = klass.__name__
        a = cache.get('jmbo_show_current_show_id_%s' % klass_name)
        b = cache.get('jmbo_show_next_show_id_%s' % klass_name)
        if a and b:
            try:
                return (
                 klass.permitted.get(id=a), klass.permitted.get(id=b))
            except klass.DoesNotExist:
                pass

    if now is None:
        now = timezone.now()
    now_time = now.time()
    today_weekday = now.weekday()
    yesterday_weekday = (today_weekday - 1) % 7
    tomorrow_weekday = (today_weekday + 1) % 7

    def mysort(a, b):
        return cmp(a.start.time(), b.start.time())

    shows = [ o for o in klass.permitted.filter().order_by('start') ]
    shows.sort(mysort)
    slots = {'yesterday': [], 'today': [], 'tomorrow': []}
    for show in shows:
        if show.repeat == 'does_not_repeat':
            if show.start.year == now.year and show.start.month == now.month and show.start.day == now.day:
                slots['today'].append(show)
            yesterday = now - timedelta(days=1)
            if show.start.year == yesterday.year and show.start.month == yesterday.month and show.start.day == yesterday.day:
                slots['yesterday'].append(show)
            tomorrow = now + timedelta(days=1)
            if show.start.year == tomorrow.year and show.start.month == tomorrow.month and show.start.day == tomorrow.day:
                slots['tomorrow'].append(show)
        elif show.repeat == 'weekdays':
            if today_weekday in (0, 1, 2, 3, 4):
                slots['today'].append(show)
            if yesterday_weekday in (0, 1, 2, 3, 4):
                slots['yesterday'].append(show)
            if tomorrow_weekday in (0, 1, 2, 3, 4):
                slots['tomorrow'].append(show)
        elif show.repeat == 'weekends':
            if today_weekday in (5, 6):
                slots['today'].append(show)
            if yesterday_weekday in (5, 6):
                slots['yesterday'].append(show)
            if tomorrow_weekday in (5, 6):
                slots['tomorrow'].append(show)
        elif show.repeat == 'saturdays':
            if today_weekday == 5:
                slots['today'].append(show)
            if yesterday_weekday == 5:
                slots['yesterday'].append(show)
            if tomorrow_weekday == 5:
                slots['tomorrow'].append(show)
        elif show.repeat == 'sundays':
            if today_weekday == 6:
                slots['today'].append(show)
            if yesterday_weekday == 6:
                slots['yesterday'].append(show)
            if tomorrow_weekday == 6:
                slots['tomorrow'].append(show)
        elif show.repeat == 'monthly_by_day_of_month':
            if show.start.day == now.day:
                slots['today'].append(show)
            yesterday = now - timedelta(days=1)
            if show.start.day == yesterday.day:
                slots['yesterday'].append(show)
            tomorrow = now + timedelta(days=1)
            if show.start.day == tomorrow.day:
                slots['tomorrow'].append(show)
        else:
            slots['today'].append(show)
            slots['yesterday'].append(show)
            slots['tomorrow'].append(show)

    current_show = None
    previous_show = None
    next_show = None
    for show in reversed(slots['today']):
        if show.start.time() <= now_time:
            current_show = show
            next_show = previous_show
            break
        previous_show = show

    if current_show is None:
        current_show = slots['yesterday'] and slots['yesterday'][(-1)] or None
        next_show = previous_show
    if next_show is None:
        next_show = slots['tomorrow'] and slots['tomorrow'][0] or None
    if use_cache:
        if current_show:
            cache.set('jmbo_show_current_show_id_%s' % klass_name, current_show.id, 60)
        if next_show:
            cache.set('jmbo_show_next_show_id_%s' % klass_name, next_show.id, 60)
    return (current_show, next_show)


def get_current_permitted_show(klass=Show, now=None):
    result, dc = get_current_next_permitted_show(klass, now)
    return result


def get_next_permitted_show(klass=Show, now=None):
    dc, result = get_current_next_permitted_show(klass, now)
    return result