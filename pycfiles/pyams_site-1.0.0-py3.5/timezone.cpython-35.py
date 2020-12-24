# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_site/generations/timezone.py
# Compiled at: 2019-12-15 17:11:01
# Size of source mod 2**32: 1296 bytes
"""PyAMS_*** module

"""
from pyams_site.generations import check_required_utilities
from pyams_site.interfaces import ISiteGenerations
from pyams_utils.interfaces.timezone import IServerTimezone
from pyams_utils.registry import utility_config
from pyams_utils.timezone.utility import ServerTimezoneUtility
__docformat__ = 'restructuredtext'
REQUIRED_UTILITIES = (
 (
  IServerTimezone, '', ServerTimezoneUtility, 'Server timezone'),)

@utility_config(name='PyAMS timezone', provides=ISiteGenerations)
class TimezoneGenerationsChecker:
    __doc__ = 'Site timezone generations checker'
    order = 10
    generation = 1

    @staticmethod
    def evolve(site, current=None):
        """Check for required utilities"""
        check_required_utilities(site, REQUIRED_UTILITIES)