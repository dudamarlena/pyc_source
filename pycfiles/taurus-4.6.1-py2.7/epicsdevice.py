# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/epics/epicsdevice.py
# Compiled at: 2019-08-19 15:09:29
"""
epics device. See __init__.py for more detailed documentation
"""
__all__ = [
 'EpicsDevice']
from taurus.core.taurusdevice import TaurusDevice

class EpicsDevice(TaurusDevice):
    """
    Dummy device class for Epics
    (the device concept is not yet used in the Epics scheme)

    .. warning:: In most cases this class should not be instantiated directly.
                 Instead it should be done via the
                    :meth:`EpicsFactory.getDevice`
    """
    _factory = None
    _scheme = 'ca'