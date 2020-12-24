# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/monitor/views/api/consumer.py
# Compiled at: 2016-06-27 04:20:00
# Size of source mod 2**32: 750 bytes
from pyramid.view import view_config
from xbus.monitor.consumers import get_consumers
from xbus.monitor.consumers import refresh_consumers

@view_config(route_name='consumer_list', request_method='GET', renderer='json', http_cache=0)
def consumer_list(request):
    """List consumers. They are not stored in the database; we instead issue a
    request to Xbus to retrieve them.
    """
    clearing = request.params.get('clearing')
    refresh_consumers(request)
    consumers = get_consumers()
    if clearing:
        consumers = [consumer for consumer in consumers if consumer['clearing']]
    return [{'total_entries': len(consumers)}, consumers]