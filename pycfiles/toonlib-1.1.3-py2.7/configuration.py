# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/toonlib/configuration.py
# Compiled at: 2018-11-03 13:01:06
"""A place to store the configuration."""
STATE_CACHING_SECONDS = 30
DAY_CACHING_SECONDS = 86400
REQUEST_TIMEOUT = 9
STATES = {0: 'Comfort', 1: 'Home', 
   2: 'Sleep', 
   3: 'Away', 
   4: 'Unknown', 
   5: 'Unknown'}
AUTHENTICATION_ERROR_STRINGS = 'Could not validate clientId based on checksum'
DEFAULT_STATE = {'deviceConfigInfo': {'device': []}, 'deviceStatusInfo': {'device': [], 'inSwitchAllTotal': {'avgUsage': 0.0, 'currentState': 0, 
                                             'currentUsage': 0.0, 
                                             'dayUsage': 0.0}}, 
   'gasUsage': {'avgDayValue': 0.0, 'avgValue': 0.0, 
                'dayCost': 0.0, 
                'dayUsage': 0, 
                'isSmart': 0, 
                'meterReading': 0, 
                'value': 0}, 
   'powerUsage': {'avgDayValue': 0.0, 'avgProduValue': 0, 
                  'avgValue': 0.0, 
                  'dayCost': 0.0, 
                  'dayCostProduced': 0.0, 
                  'dayLowUsage': 0, 
                  'dayUsage': 0, 
                  'isSmart': 0, 
                  'maxSolar': 0, 
                  'meterReading': 0, 
                  'meterReadingLow': 0, 
                  'meterReadingLowProdu': 0, 
                  'meterReadingProdu': 0, 
                  'value': 0, 
                  'valueProduced': 0, 
                  'valueSolar': 0}, 
   'smokeDetectors': {'device': []}, 'thermostatInfo': {'activeState': 0, 'boilerModuleConnected': 0, 
                      'burnerInfo': '0', 
                      'currentDisplayTemp': 0, 
                      'currentModulationLevel': 0, 
                      'currentSetpoint': 0, 
                      'currentTemp': 0, 
                      'errorFound': 0, 
                      'haveOTBoiler': 0, 
                      'nextProgram': 0, 
                      'nextSetpoint': 0, 
                      'nextState': 0, 
                      'nextTime': 0, 
                      'otCommError': '0', 
                      'programState': 0, 
                      'randomConfigId': 0, 
                      'realSetpoint': 0}, 
   'thermostatStates': {'state': [
                                {'dhw': 1, 'id': 0, 
                                   'tempValue': 0},
                                {'dhw': 1, 'id': 1, 
                                   'tempValue': 0},
                                {'dhw': 1, 'id': 2, 
                                   'tempValue': 0},
                                {'dhw': 1, 'id': 3, 
                                   'tempValue': 0},
                                {'dhw': 1, 'id': 4, 
                                   'tempValue': 0}]}}