# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/baroque/defaults/config.py
# Compiled at: 2017-03-21 13:46:09
# Size of source mod 2**32: 688 bytes
"""Default Baroque configuration"""
DEFAULT_CONFIG = {'eventtypes': {'ignore_unregistered': True, 
                'pre_registered': [
                                   'baroque.defaults.eventtypes.GenericEventType',
                                   'baroque.defaults.eventtypes.StateTransitionEventType',
                                   'baroque.defaults.eventtypes.DataOperationEventType',
                                   'baroque.defaults.eventtypes.MetricEventType']}, 
 
 'events': {'validate_schema': True, 
            'persist': False, 
            'persistence_backend': 'baroque.persistence.inmemory.DictBackend'}, 
 
 'reactors': {'propagate_exceptions': True}, 
 
 'topics': {'register_on_binding': True}}