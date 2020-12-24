# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sss/templatetags/sss_tags.py
# Compiled at: 2010-12-03 16:29:41
import os, datetime
from django import template
from django.db.models import Sum
from django.utils.translation import ugettext as _
from sss.models import BacklogItem
from sss.conf.settings import SPRINT_NORMAL_DURATION, BURNDOWN_GRAPH_DIMENSIONS
from sss.exceptions import EmptyBurndownError
register = template.Library()

@register.simple_tag
def project_summary():
    """Display a simple summary of the project"""
    qs = BacklogItem.current.filter(done=False)
    if qs.count():
        return (' / ').join((
         _('Tasks remaining %d') % qs.count(),
         _('Remaining points %(story_points__sum)d') % qs.aggregate(Sum('story_points'))))
    else:
        return _("Either your project hasn't started, or it's completely done! Next?")


def burndown_compute():
    """Compute every bit of data needed by the Burndown Chart"""
    qs = BacklogItem.current.all()
    if qs.count() == 0:
        raise EmptyBurndownError(_('No backlog, no chart yet'))
    first_date_started = qs.order_by('date_started')[0].date_started
    delta = datetime.datetime.now() - first_date_started
    max_x = SPRINT_NORMAL_DURATION
    if delta.days > SPRINT_NORMAL_DURATION:
        max_x = delta.days
    total_points = qs.aggregate(Sum('story_points'))['story_points__sum']
    x_range = max_x + 1
    ideal_data = []
    current_data = []
    select_date = {'day_done': "strftime('%%Y-%%m-%%d', date_done)"}
    current_points = qs.extra(select=select_date).values('day_done', 'done').annotate(points=Sum('story_points'))
    for x in range(0, x_range):
        points = total_points - total_points * (x / float(SPRINT_NORMAL_DURATION + 1))
        if points > 0:
            ideal_data.append(str(points))
        else:
            ideal_data.append('0')
        current_day = datetime.datetime(first_date_started.year, first_date_started.month, first_date_started.day, 23, 59, 59) + datetime.timedelta(days=x)
        points = sum(item['points'] for item in current_points if item['day_done'] <= str(current_day) if item['done'])
        current_data.append(str(total_points - points))

    ideal_data.append('0')
    today_delta = datetime.datetime.now() - first_date_started
    today_position = today_delta.days * 100 / max_x
    return (
     ideal_data, current_data, max_x, total_points, today_position)


@register.simple_tag
def project_burndown():
    """Display a burndown chart, using JQuery Flot lib.
    """
    (width, height) = BURNDOWN_GRAPH_DIMENSIONS
    FLOT_STRING = '<div id="placeholder" style="width:%(width)dpx;height:%(height)dpx;"></div>\n    <script id="source" language="javascript" type="text/javascript">\n        django.jQuery(function () {\n            var ideal_data = {data: Array(%(ideal_data)s), label: "%(estimated_label)s", color: "#900"};\n            var current_data = {data: Array(%(current_data)s), label: "%(actual_label)s", color: "#090"};\n            django.jQuery.plot(django.jQuery("#placeholder"), [ ideal_data, current_data ]);\n    });</script> '
    try:
        (ideal_data, current_data, max_x, total_points, today_position) = burndown_compute()
    except EmptyBurndownError, e:
        return e

    return FLOT_STRING % {'width': width, 
       'height': height, 
       'ideal_data': (',').join('[ %d, %s ]' % (x, y) for (x, y) in zip(range(0, max_x + 15), ideal_data)), 
       'current_data': (',').join('[ %d, %s ]' % (x, y) for (x, y) in zip(range(0, max_x + 15), current_data)), 
       'estimated_label': _('estimated data'), 
       'actual_label': _('actual data')}


@register.simple_tag
def sss_custom_js():
    """A generic custom JS loader"""
    directory = os.path.dirname(__file__)
    filepath = os.path.join(directory, 'static', 'jquery.flot.js')
    return open(filepath, 'r').read().replace('jQuery', 'django.jQuery')