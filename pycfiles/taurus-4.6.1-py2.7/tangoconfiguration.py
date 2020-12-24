# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/tango/tangoconfiguration.py
# Compiled at: 2019-08-19 15:09:29
"""[DEPRECATED SINCE v 4.0]
This module contains all taurus tango attribute configuration"""
__all__ = [
 'TangoConfiguration']
__docformat__ = 'restructuredtext'
from taurus.core.taurusbasetypes import TaurusConfigValue
from taurus.core.taurusconfiguration import TaurusConfiguration

class TangoConfigValue(TaurusConfigValue):
    """A TaurusConfigValue specialization to decode PyTango.AttrInfoEx
    objects"""
    pass


class TangoConfiguration(TaurusConfiguration):
    pass