# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/circonus/collectd/interface.py
# Compiled at: 2015-01-26 19:30:15
__doc__ = '\n\ncirconus.collectd.interface\n~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nCreate graph data from a ``collectd`` check bundle containing\n`interface <https://collectd.org/wiki/index.php/Plugin:Interface>`_ metrics.\n\nTransmitted metrics will be on the top of the graph and received metrics will be on the bottom.\n\n'
from circonus.graph import get_graph_data
from circonus.metric import get_datapoints
from circonus.util import get_check_id_from_cid
DATA_FORMULA_TRANSMITTER = '=8*VAL'
DATA_FORMULA_RECEIVER = '=-8*VAL'

def get_interface_metrics(metrics, interface_name='eth0', kind=None):
    """Get metrics for interface ``interface_name`` and ``kind``.

    :param list metrics: The metrics.
    :param str interface_name: (optional) The interface name, e.g., "eth0".
    :param str kind: (optional) The kind of interface metrics to get, e.g., "octets".
    :rtype: :py:class:`list`

    """
    if kind:
        interface_metrics = [ m for m in metrics if m['name'].startswith('interface`%s' % interface_name) and kind in m['name'] ]
    else:
        interface_metrics = [ m for m in metrics if m['name'].startswith('interface`%s' % interface_name) ]
    interface_metrics.sort(reverse=True)
    return interface_metrics


def is_transmitter(metric):
    """Is interface ``metric`` a transmitter?

    :param dict metric: The metric.
    :rtype: :py:class:`bool`

    """
    return metric.get('name', '').endswith('tx')


def is_receiver(metric):
    """Is interface ``metric`` a receiver?

    :param dict metric: The metric.
    :rtype: :py:class:`bool`

    """
    return metric.get('name', '').endswith('rx')


def get_interface_datapoints(check_bundle, interface_name='eth0'):
    """Get a list of datapoints for ``check_bundle`` and ``interface_name``.

    :param list check_bundle: The check bundle.
    :param str interface_name: (optional) The interface name, e.g., "eth0".
    :rtype: :py:class:`list`

    ``octets`` and ``errors`` will be returned.  ``octets`` datapoints have data formulas added to them which makes
    them render as bits per second.  Transmitted ``octets`` will be on the top and received ``octets`` will be on the
    bottom of the graph due to the data formulas.

    """
    datapoints = []
    for cid in check_bundle.get('_checks', []):
        check_id = get_check_id_from_cid(cid)
        metrics = check_bundle['metrics']
        octets = get_interface_metrics(metrics, interface_name, 'octets')
        for m in octets:
            if is_transmitter(m):
                m['data_formula'] = DATA_FORMULA_TRANSMITTER
            elif is_receiver(m):
                m['data_formula'] = DATA_FORMULA_RECEIVER

        datapoints.extend(get_datapoints(check_id, octets, {'derive': 'counter'}))
        errors = get_interface_metrics(metrics, interface_name, 'errors')
        datapoints.extend(get_datapoints(check_id, errors, {'derive': 'counter', 'axis': 'r'}))

    return datapoints


def get_interface_graph_data(check_bundle, interface_name='eth0', title=None):
    """Get graph data for ``check_bundle``.

    :param dict check_bundle: The check bundle to create graph data with.
    :param str title: (optional) The title to use for the graph.
    :param str interface_name: (optional) The interface name, e.g., "eth0".
    :rtype: :py:class:`dict`

    ``title`` defaults to using ``check_bundle["target"]``.  ``interface_name`` and ``bit/s`` will be appended to
    ``title``.

    The returned data :py:class:`dict` can be used to :meth:`~circonus.CirconusClient.create` a `graph
    <https://login.circonus.com/resources/api/calls/graph>`_.

    """
    datapoints = get_interface_datapoints(check_bundle, interface_name)
    graph_title = title if title else '%s interface' % check_bundle['target']
    graph_title = '%s %s bit/s' % (graph_title, interface_name)
    custom_data = {'title': graph_title}
    return get_graph_data(check_bundle, datapoints, custom_data)