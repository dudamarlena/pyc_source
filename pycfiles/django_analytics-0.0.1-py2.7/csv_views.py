# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/analytics/csv_views.py
# Compiled at: 2011-05-24 10:07:07
import csv, datetime
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from analytics.models import Metric
from analytics import settings

def csv_dump(request, uid):
    """
    Returns a CSV dump of all of the specified metric's counts
    and cumulative counts.
    """
    metric = Metric.objects.get(uid=uid)
    frequency = request.GET.get('frequency', settings.STATISTIC_FREQUENCY_DAILY)
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s%s.csv' % (uid, datetime.datetime.now().strftime('%Y%m%d-%H%M'))
    writer = csv.writer(response)
    writer.writerow([_('Date/time'), _('Count'), _('Cumulative count')])
    for stat in metric.statistics.filter(frequency=frequency).order_by('date_time'):
        writer.writerow([stat.date_time.strftime(settings.CSV_DATETIME_FORMAT), stat.count, stat.cumulative_count])

    return response