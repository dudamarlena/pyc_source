# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/doorpi/status/status_lib/event_handler.py
# Compiled at: 2016-08-01 11:57:45
import logging
logger = logging.getLogger(__name__)
logger.debug('%s loaded', __name__)

def get(*args, **kwargs):
    try:
        if len(kwargs['name']) == 0:
            kwargs['name'] = ['']
        if len(kwargs['value']) == 0:
            kwargs['value'] = ['']
        event_handler = kwargs['DoorPiObject'].event_handler
        status = {}
        for name_requested in kwargs['name']:
            if name_requested in 'sources':
                status['sources'] = event_handler.sources
            if name_requested in 'events':
                status['events'] = event_handler.events
            if name_requested in 'events_by_source':
                status['events_by_source'] = event_handler.events_by_source
            if name_requested in 'actions':
                status['actions'] = {}
                for event in event_handler.actions:
                    status['actions'][event] = []
                    for action in event_handler.actions[event]:
                        status['actions'][event].append(str(action))

            if name_requested in 'threads':
                status['threads'] = str(event_handler.threads)
            if name_requested in 'idle':
                status['idle'] = event_handler.idle

        return status
    except Exception as exp:
        logger.exception(exp)
        return {'Error': 'could not create ' + str(__name__) + ' object - ' + str(exp)}


def is_active(doorpi_object):
    if doorpi_object.event_handler:
        return True
    return False