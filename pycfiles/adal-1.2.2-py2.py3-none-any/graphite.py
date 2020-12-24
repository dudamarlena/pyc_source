# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /opt/adagios/adagios/../adagios/status/graphite.py
# Compiled at: 2018-05-16 10:07:32
import re, adagios.settings
ILLEGAL_CHAR = re.compile('[^\\w-]')

def _get_graphite_url(base, host, service, metric, from_):
    """ Constructs an URL for Graphite.

    Args:
      - base (str): base URL for Graphite access
      - host (str): hostname
      - service (str): service, e.g. HTTP
      - metric (str): metric, e.g. size, time
      - from_ (str): Graphite time period

    Returns: str
    """
    host_ = _compliant_name(host)
    service_ = _compliant_name(service)
    metric_ = _compliant_name(metric)
    base = base.rstrip('/')
    title = adagios.settings.graphite_title.format(**locals())
    url = '{base}/render?' + adagios.settings.graphite_querystring
    url = url.format(**locals())
    return url


def _compliant_name(name):
    """ Makes the necessary replacements for Graphite. """
    if name == '_HOST_':
        return '__HOST__'
    name = ILLEGAL_CHAR.sub('_', name)
    return name


def get(base, host, service, metrics, units):
    """ Returns a data structure containg URLs for Graphite.

    The structure looks like:
    [{'name': 'One day',
      'css_id' : 'day',
      'metrics': {'size': 'http://url-of-size-metric',
                  'time': 'http://url-of-time-metric'}
     },
     {...}]

    Args:
      - base (str): base URL for Graphite access
      - host (str): hostname
      - service (str): service, e.g. HTTP
      - metrics (list): list of metrics, e.g. ["size", "time"]
      - units (list): a list of <name,css_id,unit>,
        see adagios.settings.GRAPHITE_PERIODS

    Returns: list
    """
    graphs = []
    for name, css_id, unit in units:
        m = {}
        for metric in metrics:
            m[metric] = _get_graphite_url(base, host, service, metric, unit)

        graph = dict(name=name, css_id=css_id, metrics=m)
        graphs.append(graph)

    return graphs