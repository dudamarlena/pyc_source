# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/analytics/maintenance.py
# Compiled at: 2011-07-19 07:57:01
from inspect import ismethod, isclass
from django.conf import settings
from analytics.models import Metric
from analytics.settings import ANALYTICS_APP_MODULE
from analytics.basemetric import BaseMetric
from django.utils.translation import ugettext as _

def has_methods(obj, methods):
    """
    Checks whether the specified object has all of the given
    methods (a list of strings holding the names of the methods).
    """
    methods_dict = dict([ (method, False) for method in methods ])
    for attr in dir(obj):
        attr_obj = getattr(obj, attr, None)
        if ismethod(attr_obj):
            if attr in methods_dict:
                methods_dict[attr] = True

    for method, has_method in methods_dict.iteritems():
        if not has_method:
            return False

    return True


def scan_apps_for_metrics():
    """
    Scans the apps in the current project for analytics-related
    definition files.

    Inspired by http://djangosnippets.org/snippets/573/
    """
    required_methods = []
    for attr in dir(BaseMetric):
        obj = getattr(BaseMetric, attr, None)
        if ismethod(obj):
            required_methods.append(attr)

    metric_uids = {}
    for app in settings.INSTALLED_APPS:
        import_app = '%s.%s' % (app, ANALYTICS_APP_MODULE)
        try:
            print _('Scanning %(app)s for metrics...') % {'app': import_app}
            mod = __import__(import_app, globals(), locals(), [ANALYTICS_APP_MODULE])
            for attr in dir(mod):
                obj = getattr(mod, attr, None)
                if isclass(obj) and issubclass(obj, BaseMetric) and obj is not BaseMetric:
                    print _('Found metric class %(metric)s') % {'metric': attr}
                    if not has_methods(obj, required_methods):
                        print _('ERROR: Metric %(metric)s does not include all methods from BaseMetric') % {'metric': attr}
                    elif obj.uid in metric_uids:
                        print _('Duplicate metric "%(metric)s" found! Skipping.') % {'metric': metric.uid}
                    elif not obj.uid or not obj.title:
                        print _('Metric "%(metric)s" is missing a UID or title, skipping.') % {'metric': attr}
                    else:
                        metric, created = Metric.objects.get_or_create(uid=obj.uid)
                        metric.title = obj.title
                        metric.metric_class = '%s.%s' % (import_app, attr)
                        metric.save()
                        print _('Metric "%(metric)s" successfully created.') % {'metric': metric.title}
                        metric_uids[obj.uid] = None

            print ''
        except ImportError:
            print _('Failed to import app %(app)s for analytics inspection, skipping') % {'app': import_app}

    return


def drop_metric(uid):
    """
    Removes the metric with the specified uid.
    """
    if uid == 'ALL':
        Metric.objects.all().delete()
    else:
        Metric.objects.get(uid=uid).delete()


def deactivate_metric(uid):
    """
    Deactivates the specified metric.
    """
    if uid == 'ALL':
        Metric.objects.all().update(active=False)
    else:
        Metric.objects.filter(uid=uid).update(active=False)


def activate_metric(uid):
    """
    Activates the specified metric.
    """
    if uid == 'ALL':
        Metric.objects.all().update(active=True)
    else:
        Metric.objects.filter(uid=uid).update(active=True)


def reset_metric(uid, frequencies):
    """
    Removes all of the statistics associated with each
    of the metrics.

    If frequency is not specified, it will automatically
    remove statistics for all frequencies.
    """
    metrics = Metric.objects.all() if uid == 'ALL' else Metric.objects.filter(uid=uid)
    for m in metrics:
        print _('Deleting statistics for %(metric)s...') % {'metric': m.title}
        m.statistics.filter(frequency__in=frequencies).delete()


def list_metrics():
    """
    Lists all of the metrics, their UIDs and their active status.

    TODO: Make this prettier somehow.
    """
    print ''
    for m in Metric.objects.all():
        print '%s ("%s"): active=%s, statistics=%d' % (m.uid, m.title, m.active, m.statistics.count())

    print ''