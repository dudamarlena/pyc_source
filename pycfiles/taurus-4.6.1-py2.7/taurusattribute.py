# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/taurusattribute.py
# Compiled at: 2019-08-19 15:09:29
"""This module contains the base class for a taurus attribute"""
__all__ = [
 'TaurusAttribute']
__docformat__ = 'restructuredtext'
import weakref
from .taurusmodel import TaurusModel
from taurus.core.taurusbasetypes import TaurusElementType, DataType
from taurus.core.util.log import deprecation_decorator
from taurus.core.units import Quantity

class TaurusAttribute(TaurusModel):
    DftTimeToLive = 10000
    _description = 'A Taurus Attribute'
    defaultFragmentName = 'rvalue'

    def __init__(self, name='', parent=None, **kwargs):
        self.call__init__(TaurusModel, name, parent)
        self.__enable_polling = kwargs.get('enablePolling', True)
        self.__activate_polling = False
        self.__polled = False
        self.__polling_period = kwargs.get('pollingPeriod', 3000)
        self.__forced_polling = False
        storeCallback = kwargs.get('storeCallback', None)
        if storeCallback is not None:
            storeCallback(self)
        self.writable = None
        self.data_format = None
        self._label = self.getSimpleName()
        self.type = None
        self._range = [None, None]
        self._alarm = [None, None]
        self._warning = [None, None]
        self.precision = None
        return

    def cleanUp(self):
        self.trace('[TaurusAttribute] cleanUp')
        if hasattr(self, '_unsuscribeEvents'):
            self.deprecated(dep='TaurusAttribute._unsuscribeEvents API', alt='If you need it called in cleanUp, re-implement cleanUp')
            self._unsuscribeEvents()
        TaurusModel.cleanUp(self)

    @classmethod
    def getTaurusElementType(cls):
        return TaurusElementType.Attribute

    @classmethod
    def buildModelName(cls, parent_model, relative_name):
        """build an 'absolute' model name from the parent model and the
        'relative' name.
        - If parent_model is a TaurusDevice, the return is a composition of
        the database model name and its device name
        - If parent_model is a TaurusAttribute, the relative name is ignored and
        the parent name is returned

        Note: This is a basic implementation. You may need to reimplement this
              for a specific scheme if it supports "useParentModel".
        """
        if parent_model is None:
            return relative_name
        else:
            parent_name = parent_model.getFullName()
            if not parent_name:
                return relative_name
            if isinstance(parent_model, cls):
                return parent_name
            return '%s%s' % (parent_name, relative_name)

    @classmethod
    def getNameValidator(cls):
        return cls.factory().getAttributeNameValidator()

    def isNumeric(self):
        return self.type in [DataType.Float, DataType.Integer]

    @deprecation_decorator(rel='>4.0.1', alt='.type==DataType.DevState')
    def isState(self):
        return False

    def encode(self, value):
        raise NotImplementedError('Not allowed to call AbstractClass' + ' TaurusAttribute.encode')

    def decode(self, attr_value):
        raise NotImplementedError('Not allowed to call AbstractClass' + ' TaurusAttribute.decode')

    def write(self, value, with_read=True):
        raise NotImplementedError('Not allowed to call AbstractClass' + ' TaurusAttribute.write')

    def read(self, cache=True):
        raise NotImplementedError('Not allowed to call AbstractClass' + ' TaurusAttribute.read')

    def poll(self):
        raise NotImplementedError('Not allowed to call AbstractClass' + ' TaurusAttribute.poll')

    def isUsingEvents(self):
        raise NotImplementedError('Not allowed to call AbstractClass' + ' TaurusAttribute.isUsingEvents')

    def getValueObj(self, cache=True):
        try:
            return self.read(cache=cache)
        except Exception:
            return

        return

    def areStrValuesEqual(self, v1, v2):
        try:
            if 'nan' == str(v1).lower() == str(v2).lower():
                return True
            else:
                return self.encode(v1) == self.encode(v2)

        except:
            return False

    def hasEvents(self):
        self.deprecated("Don't use this anymore. Use isUsingEvents instead")
        return self.isUsingEvents()

    def enablePolling(self, force=False):
        """Enable polling. See :meth:`isPollingEnabled` for clarification of
        what enabled polling means.

        :param force: (bool) True also activates polling
                      (see: :meth:`activatePolling`)
        """
        self.__enable_polling = True
        self.__forced_polling = force
        if force:
            self.__activate_polling = True
        if self.__activate_polling:
            self._activatePolling()

    def disablePolling(self):
        """Disable polling and if polling is active also deactivate it.
        See :meth:`isPollingEnabled` for clarification of
        what enabled polling means.
        """
        self.__enable_polling = False
        self.__forced_polling = False
        if self.__activate_polling:
            self._deactivatePolling()

    def isPollingEnabled(self):
        """Indicate whether polling was activated/deactivated by user.
        Enabled polling does not mean that it is active - periodically poll
        the attribute. By default the attribute creation enables polling.

        :return: (bool) whether polling is enabled

        :see: :meth:`enablePolling`, :meth:`disablePolling`
        """
        return self.__enable_polling

    def _activatePolling(self):
        self.__activate_polling = True
        if not self.isPollingEnabled():
            return
        self.factory().addAttributeToPolling(self, self.getPollingPeriod())
        self.__polled = True

    def _deactivatePolling(self):
        self.__activate_polling = False
        self.factory().removeAttributeFromPolling(self)
        self.__polled = False

    def isPollingActive(self):
        """Indicate whether polling is active. Active polling means that
        a periodic timer poll the attribute. By default the attribute creation
        does not activate polling.

        :return: (bool) whether polling is active

        :see: :meth:`activatePolling`, :meth:`disablePolling`
        """
        return self.__polled

    def isPollingForced(self):
        return self.__forced_polling

    def changePollingPeriod(self, period):
        """change polling period to period miliseconds """
        if self.__polling_period == period and self.__activate_polling:
            return
        self.__polling_period = period
        if self.__activate_polling:
            self._deactivatePolling()
            self._activatePolling()

    def isPolled(self):
        self.deprecated('use isPollingActive()')
        return self.isPollingActive()

    def getPollingPeriod(self):
        """returns the polling period """
        return self.__polling_period

    def activatePolling(self, period, unsubscribe_evts=False, force=False):
        """activate polling for attribute.

           :param period: polling period (in miliseconds)
           :type period: int
        """
        self.changePollingPeriod(period)
        self.enablePolling(force=force)

    def deactivatePolling(self, maintain_enabled=False):
        """unregister attribute from polling"""
        self.deprecated('use disablePolling()')
        self.disablePolling()

    def __str__(self):
        return self.getFullName()

    def getDisplayDescription(self, cache=True):
        return self.description

    def getDisplayDescrObj(self, cache=True):
        name = self.getLabel(cache=cache)
        obj = [('name', name),
         (
          'model', self.getFullName() or '')]
        descr = self.description
        if descr:
            _descr = descr.replace('<', '&lt;').replace('>', '&gt;')
            obj.append(('description', _descr))
        if isinstance(self.rvalue, Quantity):
            _unitless = self.rvalue.unitless
            range = self._range
            alarm = self._alarm
            warning = self._warning
            if range != [None, None]:
                if not _unitless:
                    low = range[0]
                    high = range[1]
                else:
                    low = range[0].magnitude
                    high = range[1].magnitude
                obj.append(('range', '[%s, %s]' % (low, high)))
            if alarm != [None, None]:
                if not _unitless:
                    low = alarm[0]
                    high = alarm[1]
                else:
                    low = alarm[0].magnitude
                    high = alarm[1].magnitude
                obj.append(('alarm', '[%s, %s]' % (low, high)))
            if warning != [None, None]:
                if not _unitless:
                    low = warning[0]
                    high = warning[1]
                else:
                    low = warning[0].magnitude
                    high = warning[1].magnitude
                obj.append(('warning', '[%s, %s]' % (low, high)))
        return obj

    def isWritable(self, cache=True):
        return self.writable

    def getType(self, cache=True):
        return self.type

    def getDataFormat(self, cache=True):
        return self.data_format

    def getLabel(self, cache=True):
        return self._label

    def getMinRange(self, cache=True):
        return self._range[0]

    def getMaxRange(self, cache=True):
        return self._range[1]

    def getRange(self, cache=True):
        return self._range

    def getMinAlarm(self, cache=True):
        return self._alarm[0]

    def getMaxAlarm(self, cache=True):
        return self._alarm[1]

    def getAlarms(self, cache=True):
        return self._alarm

    def getMinWarning(self, cache=True):
        return self._warning[0]

    def getMaxWarning(self, cache=True):
        return self._warning[1]

    def getWarnings(self, cache=True):
        return self._warning

    def setLabel(self, lbl):
        self._label = lbl

    def __assertsValidLimits(self, limits):
        assert len(limits) == 2, 'The limits must be two values, low and high'
        low, high = limits
        assert isinstance(self.rvalue, Quantity), 'rvalue is not a Quantity'
        assert isinstance(low, Quantity), 'low is not a Quantity'
        assert isinstance(high, Quantity), 'high is not a Quantity'
        assert self.rvalue.dimensionality == low.dimensionality, 'low and rvalue have different dimensionality'
        assert self.rvalue.dimensionality == high.dimensionality, 'high and rvalue have different dimensionality'

    def setRange(self, *limits):
        if isinstance(limits[0], list):
            limits = limits[0]
        self.__assertsValidLimits(limits)
        self._range = limits

    def setWarnings(self, *limits):
        if isinstance(limits[0], list):
            limits = limits[0]
        self.__assertsValidLimits(limits)
        self._warning = limits

    def setAlarms(self, *limits):
        if isinstance(limits[0], list):
            limits = limits[0]
        self.__assertsValidLimits(limits)
        self._alarm = limits

    def isBoolean(self, cache=True):
        v = self.read(cache)
        return isinstance(v.rvalue, bool)

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, descr):
        self._description = descr

    @property
    def rvalue(self, cache=True):
        valueObj = self.getValueObj()
        if valueObj is None:
            return
        else:
            return valueObj.rvalue
            return

    @property
    def wvalue(self, cache=True):
        valueObj = self.getValueObj()
        if valueObj is None:
            return
        else:
            return valueObj.wvalue
            return

    @property
    def time(self, cache=True):
        valueObj = self.getValueObj()
        if valueObj is None:
            return
        else:
            return valueObj.time
            return

    @property
    def quality(self, cache=True):
        valueObj = self.getValueObj()
        if valueObj is None:
            return
        else:
            return valueObj.quality
            return

    label = property(getLabel, setLabel)
    range = property(getRange, setRange)
    warnings = property(getWarnings, setWarnings)
    alarms = property(getAlarms, setAlarms)