# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/circonus/collectd/cpu.py
# Compiled at: 2015-01-26 19:30:15
__doc__ = '\n\ncirconus.collectd.cpu\n~~~~~~~~~~~~~~~~~~~~~\n\nCreate graph data from a ``collectd`` check bundle containing `cpu <https://collectd.org/wiki/index.php/Plugin:CPU>`_\nmetrics.\n\n'
from collections import OrderedDict
from copy import deepcopy
from itertools import chain
import re
from circonus.graph import get_graph_data
from circonus.metric import get_datapoints, get_metrics, get_metrics_sorted_by_suffix
from circonus.util import get_check_id_from_cid
CPU_METRIC_SUFFIXES = [
 'steal', 'interrupt', 'softirq', 'system', 'wait', 'user', 'nice', 'idle']
CPU_METRIC_RE = re.compile('\n^cpu                            # Starts with "cpu"\n`.*`                            # Anything in between\n', re.X)
CPU_NUMBER_RE = re.compile('\n^cpu                            # Starts with "cpu"\n`                               # Delimiter\n(?P<number>\\d+)                 # Number\n`                               # Delimiter\n', re.X)

def _get_cpus(metrics):
    """Get a list of strings representing the CPUs available in ``metrics``.

    :param list metrics: The metrics used to look for CPUs.
    :rtype: :py:class:`list`

    The returned strings will begin with the CPU metric name. The list is sorted in ascending order.

    """
    cpus = list({m['name'].rpartition('cpu')[0] for m in metrics})
    cpus.sort()
    return cpus


def get_cpu_metrics(metrics):
    """Get a sorted list of metrics from ``metrics``.

    :param list metrics: The metrics to sort.

    The CPU metrics are sorted by:

    #. Name, ascending
    #. Explicit suffix, i.e., :const:`~circonus.collectd.cpu.CPU_METRIC_SUFFIXES`

    """
    cpus = _get_cpus(metrics)
    cpu_metrics = OrderedDict.fromkeys(cpus)
    for cpu in cpus:
        cpu_metrics[cpu] = get_metrics_sorted_by_suffix((m for m in metrics if m['name'].startswith(cpu)), CPU_METRIC_SUFFIXES)

    return list(chain.from_iterable(cpu_metrics.values()))


def get_stacked_cpu_metrics(metrics, hide_idle=True):
    """Get metrics with the ``stack`` attribute added.

    :param list metrics: The metrics to stack.
    :param bool hide_idle: (optional) Hide CPU idle.
    :rtype: :py:class:`list`

    Each CPU will be added to a stack group equal to that CPU's number.  CPU idle metrics are hidden by default.
    ``metrics`` is not modified by this function.

    """
    stacked_metrics = deepcopy(metrics)
    for m in stacked_metrics:
        match = CPU_NUMBER_RE.match(m['name'])
        m['stack'] = int(match.group('number'))
        if hide_idle and m['name'].endswith('idle'):
            m['hidden'] = True

    return stacked_metrics


def get_cpu_datapoints(check_bundle, metrics):
    """Get a list of datapoints from *sorted* ``metrics``.

    :param dict check_bundle: The check bundle.
    :param list metrics: Sorted CPU metrics.
    :rtype: :py:class`list`

    """
    datapoints = []
    for cid in check_bundle.get('_checks', []):
        check_id = get_check_id_from_cid(cid)
        datapoints.extend(get_datapoints(check_id, metrics, {'derive': 'counter'}))

    return datapoints


def get_cpu_graph_data(check_bundle, title=None):
    """Get graph data for ``check_bundle``.

    :param dict check_bundle: The check bundle to create graph data with.
    :param str title: (optional) The title to use for the graph.
    :rtype: :py:class:`dict`

    ``title`` defaults to using ``check_bundle["target"]``.

    The returned data :py:class:`dict` can be used to :meth:`~circonus.CirconusClient.create` a `graph
    <https://login.circonus.com/resources/api/calls/graph>`_.

    """
    data = {}
    metrics = get_cpu_metrics(get_metrics(check_bundle, CPU_METRIC_RE))
    if metrics:
        stacked_metrics = get_stacked_cpu_metrics(metrics)
        datapoints = get_cpu_datapoints(check_bundle, stacked_metrics)
        graph_title = title if title else '%s cpu' % check_bundle['target']
        custom_data = {'title': graph_title, 'max_left_y': 100}
        data = get_graph_data(check_bundle, datapoints, custom_data)
    return data