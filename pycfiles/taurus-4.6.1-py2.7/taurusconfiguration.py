# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/taurusconfiguration.py
# Compiled at: 2019-08-19 15:09:29
"""[DEPRECATED since taurus v4]
This module contains the base class for a taurus attribute configuration"""
from builtins import object
from .taurusmodel import TaurusModel
from .util.log import taurus4_deprecation
__all__ = [
 'TaurusConfigurationProxy', 'TaurusConfiguration']
__docformat__ = 'restructuredtext'

class TaurusConfigurationProxy(object):
    """
    TaurusAttribute has a reference to TaurusConfiguration and it should also have
    a reference to TaurusAttribute. To solve this cyclic dependency,
    TaurusConfiguration has a weak reference to TaurusAttribute. But then we must
    be sure that no other references to TaurusConfiguration exist so that
    no one tries to use it after its TaurusAttribute has disappeared.
    That's why to the outside world we don't give access to it directly
    but to objects of this new TaurusConfigurationProxy class.
    """

    @taurus4_deprecation(dbg_msg='Do not use this class')
    def __init__(self, parent):
        self.__parent = parent

    def __getattr__(self, name):
        return getattr(self.__parent._getRealConfig(), name)

    def getRealConfigClass(self):
        return self.__parent._getRealConfig().__class__


class TaurusConfiguration(TaurusModel):

    @taurus4_deprecation(alt='TaurusAttribute', dbg_msg='Do not use this class')
    def __init__(self, name, parent, storeCallback=None):
        pass