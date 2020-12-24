# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/analytics/calculator.py
# Compiled at: 2011-05-24 10:06:53
from datetime import datetime, timedelta
from django.utils.translation import ugettext as _
from analytics.models import Metric, Statistic
from analytics.settings import *

def calculate_metric(metric, frequency):
    """
    Invokes the given metric's calculation routine.
    """
    start_datetime = None
    end_datetime = None
    latest_datetime = None
    latest_stat = metric.latest_stat(frequency=frequency)
    mod_parts = metric.metric_class.split('.')
    mod = ('.').join(mod_parts[:-1])
    class_name = mod_parts[(-1)]
    metric_class = getattr(__import__(mod, globals(), locals(), [class_name]), class_name, None)
    metric_calc = metric_class()
    if latest_stat is None:
        start_datetime = metric_calc.get_earliest_timestamp()
        if not start_datetime:
            print _('No data for metric %(metric)s, skipping.') % {'metric': metric.title}
            return False
    else:
        start_datetime = latest_stat.date_time
    if frequency == STATISTIC_FREQUENCY_DAILY:
        start_datetime = datetime.strptime(start_datetime.strftime('%Y %m %d'), '%Y %m %d')
        end_datetime = start_datetime + timedelta(days=1)
    else:
        if frequency == STATISTIC_FREQUENCY_WEEKLY:
            start_datetime = datetime.strptime(start_datetime.strftime('%Y %W 0'), '%Y %W %w') - timedelta(days=7)
            end_datetime = start_datetime + timedelta(days=7)
        elif frequency == STATISTIC_FREQUENCY_MONTHLY:
            start_datetime = datetime.strptime(start_datetime.strftime('%Y %m 1'), '%Y %m %d')
            end_datetime = datetime.strptime((start_datetime + timedelta(days=33)).strftime('%Y %m 1'), '%Y %m %d')
        today = datetime.strptime(datetime.now().strftime('%Y %m %d'), '%Y %m %d')
        earliest_datetime = None
        manually_set_cumulative_count = False
        while start_datetime < today:
            count = metric_calc.calculate(start_datetime, end_datetime)
            cumulative_count = 0
            if isinstance(count, tuple):
                cumulative_count = count[1]
                count = count[0]
                manually_set_cumulative_count = True
            stat, created = Statistic.objects.get_or_create(metric=metric, date_time=start_datetime, frequency=frequency)
            stat.count = count
            stat.cumulative_count = cumulative_count
            stat.save()
            latest_stat = stat
            if earliest_datetime is None:
                earliest_datetime = start_datetime
            start_datetime = end_datetime
            if frequency == STATISTIC_FREQUENCY_DAILY:
                end_datetime += timedelta(days=1)
            elif frequency == STATISTIC_FREQUENCY_WEEKLY:
                end_datetime += timedelta(days=7)
            elif frequency == STATISTIC_FREQUENCY_MONTHLY:
                end_datetime = datetime.strptime((start_datetime + timedelta(days=33)).strftime('%Y %m 1'), '%Y %m %d')

    if not manually_set_cumulative_count:
        metric.update_cumulative_counts(earliest_datetime=earliest_datetime, frequency=frequency)
    return True


def calculate_metric_by_uid(uid, frequencies):
    """
    Calculates the specified metric for the given list of frequencies.
    """
    metric = Metric.objects.get(uid=uid)
    for f in frequencies:
        print _('Calculating %(freq)s statistics for %(metric)s...') % {'freq': STATISTIC_FREQUENCY_DICT[frequency].lower(), 'metric': metric.title}
        calculate_metric(metric, f)


def calculate_all_metrics(frequencies):
    """
    Calculates all metrics for all frequencies.
    """
    for metric in Metric.objects.filter(active=True):
        for frequency in frequencies:
            print _('Calculating %(freq)s statistics for %(metric)s...') % {'freq': STATISTIC_FREQUENCY_DICT[frequency].lower(), 'metric': metric.title}
            calculate_metric(metric, frequency)