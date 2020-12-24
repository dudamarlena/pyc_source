# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/cachet_url_monitor/status.py
# Compiled at: 2020-01-18 16:59:17
# Size of source mod 2**32: 705 bytes
"""
This file defines all the different status different values.
These are all constants and are coupled to cachet's API configuration.
"""
from enum import Enum

class ComponentStatus(Enum):
    OPERATIONAL = 1
    PERFORMANCE_ISSUES = 2
    PARTIAL_OUTAGE = 3
    MAJOR_OUTAGE = 4


INCIDENT_PARTIAL = 'PARTIAL'
INCIDENT_MAJOR = 'MAJOR'
INCIDENT_PERFORMANCE = 'PERFORMANCE'
INCIDENT_MAP = {INCIDENT_PARTIAL: ComponentStatus.PARTIAL_OUTAGE, 
 INCIDENT_MAJOR: ComponentStatus.MAJOR_OUTAGE, 
 INCIDENT_PERFORMANCE: ComponentStatus.PERFORMANCE_ISSUES}

class IncidentStatus(Enum):
    SCHEDULED = 0
    INVESTIGATING = 1
    IDENTIFIED = 2
    WATCHING = 3
    FIXED = 4