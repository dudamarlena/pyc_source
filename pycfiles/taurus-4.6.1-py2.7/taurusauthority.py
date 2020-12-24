# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/taurusauthority.py
# Compiled at: 2019-08-19 15:09:29
"""This module contains the base class for a taurus database"""
from __future__ import absolute_import
from .taurusbasetypes import TaurusElementType
from .taurusmodel import TaurusModel
__all__ = [
 'TaurusAuthority']
__docformat__ = 'restructuredtext'

class TaurusAuthority(TaurusModel):
    _description = 'A Taurus Authority'

    def __init__(self, complete_name='', parent=None):
        self.call__init__(TaurusModel, complete_name, parent)

    def cleanUp(self):
        self.trace('[TaurusAuthority] cleanUp')
        TaurusModel.cleanUp(self)

    @classmethod
    def getTaurusElementType(cls):
        return TaurusElementType.Authority

    @classmethod
    def buildModelName(cls, parent_model, relative_name):
        """build an 'absolute' model name from the parent name and the
        'relative' name. parent_model is ignored since there is nothing above
        the Authority object

        Note: This is a basic implementation. You may need to reimplement this
              for a specific scheme if it supports "useParentModel".
        """
        return relative_name

    @classmethod
    def getNameValidator(cls):
        return cls.factory().getAuthorityNameValidator()

    def getDisplayDescription(self, cache=True):
        return self.getFullName()

    def getDisplayDescrObj(self, cache=True):
        obj = []
        obj.append(('name', self.getDisplayName(cache=cache)))
        obj.append(('description', self.description))
        return obj

    def getChildObj(self, child_name):
        if not child_name:
            return None
        else:
            return self.getDevice(child_name)

    def getDevice(self, devname):
        """Returns the device object given its name"""
        from . import taurusdevice
        return self.factory().getObject(taurusdevice.TaurusDevice, devname)

    @property
    def description(self):
        return self._description


TaurusDatabase = TaurusAuthority