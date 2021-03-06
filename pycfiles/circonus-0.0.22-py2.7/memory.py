# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/circonus/collectd/memory.py
# Compiled at: 2015-01-26 19:30:15
"""

circonus.collectd.memory
~~~~~~~~~~~~~~~~~~~~~~~~

Create graph data from a ``collectd`` check bundle.

"""
import re
from circonus.graph import get_graph_data
from circonus.metric import get_datapoints, get_metrics, get_metrics_sorted_by_suffix
from circonus.util import get_check_id_from_cid
MEMORY_METRIC_SUFFIXES = [
 'used', 'buffered', 'cached', 'free']
MEMORY_METRIC_RE = re.compile(('\n^memory                         # Starts with "memory"\n`.*`                            # Anything in between\n({}|{}|{}|{})$                  # Ends with defined suffix\n').format(*MEMORY_METRIC_SUFFIXES), re.X)

def get_sorted_memory_metrics(metrics):
    """Get a sorted list of metrics from ``metrics``.

    :param list metrics: The metrics to sort.

    The metrics are sorted by explicit suffix, i.e., :const:`~circonus.collectd.memory.MEMORY_METRIC_SUFFIXES`.

    """
    return get_metrics_sorted_by_suffix(metrics, MEMORY_METRIC_SUFFIXES)


def get_memory_datapoints(check_bundle, metrics):
    """Get a list of datapoints from *sorted* ``metrics``.

    :param dict check_bundle: The check bundle.
    :param list metrics: The sorted metrics to cerate datapoints with.
    :rtype: :py:class:`list`

    """
    datapoints = []
    for i, cid in enumerate(check_bundle['_checks']):
        check_id = get_check_id_from_cid(cid)
        datapoints.extend(get_datapoints(check_id, metrics, {'derive': 'gauge', 'stack': i}))

    return datapoints


def get_memory_graph_data(check_bundle, title=None):
    """Get graph data for ``check_bundle``.

    :param dict check_bundle: The check bundle to create graph data with.
    :param str title: (optional) The title to use for the graph.
    :rtype: :py:class:`dict`

    ``title`` defaults to using ``check_bundle["target"]``.

    The returned data :py:class:`dict` can be used to :meth:`~circonus.CirconusClient.create` a `graph
    <https://login.circonus.com/resources/api/calls/graph>`_.

    """
    data = {}
    memory_metrics = get_metrics(check_bundle, MEMORY_METRIC_RE)
    if memory_metrics:
        sorted_memory_metrics = get_sorted_memory_metrics(memory_metrics)
        datapoints = get_memory_datapoints(check_bundle, sorted_memory_metrics)
        graph_title = title if title else '%s memory' % check_bundle['target']
        custom_data = {'title': graph_title, 'min_left_y': 0, 'min_right_y': 0}
        data = get_graph_data(check_bundle, datapoints, custom_data)
    return data