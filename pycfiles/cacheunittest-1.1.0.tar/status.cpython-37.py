# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/cachet_url_monitor/status.py
# Compiled at: 2020-01-18 16:59:17
# Size of source mod 2**32: 705 bytes
__doc__ = "\nThis file defines all the different status different values.\nThese are all constants and are coupled to cachet's API configuration.\n"
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