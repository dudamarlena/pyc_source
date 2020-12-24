# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/armoury/trigger/cross_trace.py
# Compiled at: 2016-06-30 06:13:10
"""this module is used to process the cross application/transaction trace with processing the header.
"""
import logging
console = logging.getLogger(__name__)

def process_header(tracker, headers):
    """
    :param tracker:
    :param headers:
    :return:
    """
    action_trace_invoke = 0
    if not tracker.enabled:
        return
    if not tracker.call_tingyun_id:
        return
    tingyun_ids = tracker._tingyun_id.split('|')
    if tingyun_ids < 2:
        console.debug('tingyun id is not satisfied, if this continue please contact us.')
        return
    if tracker.duration >= tracker.settings.action_tracer.action_threshold or tracker._called_traced_data and hasattr(tracker._called_traced_data, 'tr'):
        action_trace_invoke = 1
    services = {'ex': tracker.external_time, 'rds': tracker.redis_time, 'mc': tracker.memcache_time, 'mon': tracker.mongo_time, 
       'db': tracker.db_time}
    duration = tracker.duration
    code_time = duration - sum([ t for t in services.values() if t >= 0 ])
    trace_data = {'id': tingyun_ids[1].encode('utf8'), 
       'action': tracker.path.encode('utf8'), 
       'trId': tracker.generate_trace_guid().encode('utf8'), 
       'time': {'duration': duration, 
                'qu': tracker.queque_time, 
                'code': code_time}}
    for key, value in services.iteritems():
        if value >= 0:
            trace_data['time'][key] = value

    if 0 != action_trace_invoke:
        trace_data['tr'] = action_trace_invoke
    if tracker.call_req_id:
        trace_data['r'] = tracker.call_req_id.encode('utf8')
    headers.append(('X-Tingyun-Tx-Data', '%s' % trace_data))