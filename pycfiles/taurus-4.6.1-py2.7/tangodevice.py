# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/tango/tangodevice.py
# Compiled at: 2019-08-19 15:09:29
"""This module defines the TangoDevice object"""
from builtins import object
import time
from PyTango import DeviceProxy, DevFailed, LockerInfo, DevState
from taurus.core.taurusdevice import TaurusDevice
from taurus.core.taurusbasetypes import TaurusDevState, TaurusLockInfo, LockStatus, TaurusEventType
from taurus.core.util.log import taurus4_deprecation
__all__ = [
 'TangoDevice']
__docformat__ = 'restructuredtext'

class _TangoInfo(object):
    pass


def __init__(self):
    self.dev_class = self.dev_type = 'TangoDevice'
    self.doc_url = 'http://www.esrf.fr/computing/cs/tango/tango_doc/ds_doc/'
    self.server_host = 'Unknown'
    self.server_id = 'Unknown'
    self.server_version = 1


class TangoDevice(TaurusDevice):
    """A Device object representing an abstraction of the PyTango.DeviceProxy
       object in the taurus.core.tango scheme"""
    _factory = None
    _scheme = 'tango'
    _description = 'A Tango Device'

    def __init__(self, name='', **kw):
        """Object initialization."""
        self.call__init__(TaurusDevice, name, **kw)
        self._deviceObj = self._createHWObject()
        self._lock_info = TaurusLockInfo()
        self._deviceStateObj = None
        self._deviceState = TaurusDevState.Undefined
        return

    def __getattr__(self, name):
        if name != '_deviceObj' and self._deviceObj is not None:
            return getattr(self._deviceObj, name)
        else:
            cls_name = self.__class__.__name__
            raise AttributeError("'%s' has no attribute '%s'" % (cls_name, name))
            return

    def __contains__(self, key):
        """delegate the contains interface to the device proxy"""
        hw = self.getDeviceProxy()
        if hw is None:
            return False
        else:
            return hw.__contains__(key)

    def __getitem__(self, key):
        """read attribute value using key-indexing syntax (e.g. as in a dict)
        on the device"""
        attr = self.getAttribute(key)
        return attr.read()

    def __setitem__(self, key, value):
        """set attribute value using key-indexing syntax (e.g. as in a dict)
        on the device"""
        attr = self.getAttribute(key)
        return attr.write(value)

    def getAttribute(self, attrname):
        """Returns the attribute object given its name"""
        slashnb = attrname.count('/')
        if slashnb == 0:
            attrname = '%s/%s' % (self.getFullName(), attrname)
        elif attrname[0] == '/':
            attrname = '%s%s' % (self.getFullName(), attrname)
        return self.factory().getAttribute(attrname)

    @taurus4_deprecation(alt='.stateObj.read().rvalue [Tango] or ' + '.state [agnostic]')
    def getState(self, cache=True):
        stateAttrValue = self.stateObj.read(cache=cache)
        if stateAttrValue is not None:
            state_rvalue = stateAttrValue.rvalue
            return DevState.values[state_rvalue.value]
        else:
            return

    @taurus4_deprecation(alt='.stateObj [Tango] or ' + '.factory.getAttribute(state_full_name) [agnostic]')
    def getStateObj(self):
        return self.stateObj

    @taurus4_deprecation(alt='state')
    def getSWState(self, cache=True):
        raise Exception('getSWState has been removed. Use state instead')

    @property
    def state(self, cache=True):
        """Reimplemented from :class:`TaurusDevice` to use Tango's state
        attribute for diagnosis of the current state. It supports a "cache"
        kwarg

        :param cache: (bool) If True (default), cache will be used when reading
                      the state attribute of this device

        :return: (TaurusDevState)
        """
        self._deviceState = TaurusDevState.NotReady
        try:
            taurus_tango_state = self.stateObj.read(cache).rvalue
        except:
            try:
                if self.getDeviceProxy().import_info().exported:
                    self._deviceState = TaurusDevState.Undefined
                    return self._deviceState
                else:
                    return self._deviceState

            except:
                return self._deviceState

        from taurus.core.tango.enums import DevState as TaurusTangoDevState
        if taurus_tango_state == TaurusTangoDevState.UNKNOWN:
            self._deviceState = TaurusDevState.Undefined
        elif taurus_tango_state not in (TaurusTangoDevState.FAULT,
         TaurusTangoDevState.DISABLE,
         TaurusTangoDevState.INIT):
            self._deviceState = TaurusDevState.Ready
        return self._deviceState

    @taurus4_deprecation(alt='state [agnostic] or stateObj.read [Tango]')
    def getValueObj(self, cache=True):
        """ Deprecated by TEP14.
        ..warning::
            this bck-compat implementation is not perfect because the
            rvalue of the returned TangoAttributeValue is now a member of
            TaurusDevState instead of TaurusSWDevState
        """
        if not cache:
            self.warning('Ignoring argument `cache=False`to getValueObj()')
        from taurus.core.tango.tangoattribute import TangoAttrValue
        ret = TangoAttrValue()
        ret.rvalue = self.state
        return ret

    def getDisplayDescrObj(self, cache=True):
        desc_obj = super(TangoDevice, self).getDisplayDescrObj(cache)
        ret = []
        for name, value in desc_obj:
            if name.lower() == 'device state' and self.stateObj is not None:
                tg_state = self.stateObj.read(cache).rvalue.name
                value = '%s (%s)' % (value, tg_state)
            ret.append((name, value))

        return ret

    def cleanUp(self):
        self.trace('[TangoDevice] cleanUp')
        self._descr = None
        if self._deviceStateObj is not None:
            self._deviceStateObj.removeListener(self)
        self._deviceStateObj = None
        self._deviceObj = None
        TaurusDevice.cleanUp(self)
        return

    @taurus4_deprecation(alt='.state().name')
    def getDisplayValue(self, cache=True):
        return self.state(cache).name

    def _createHWObject(self):
        try:
            return DeviceProxy(self.getFullName())
        except DevFailed as e:
            self.warning('Could not create HW object: %s' % e.args[0].desc)
            self.traceback()

    @taurus4_deprecation(alt='getDeviceProxy()')
    def getHWObj(self):
        return self.getDeviceProxy()

    def getDeviceProxy(self):
        if self._deviceObj is None:
            self._deviceObj = self._createHWObject()
        return self._deviceObj

    @taurus4_deprecation(alt='getDeviceProxy() is not None')
    def isValidDev(self):
        """see: :meth:`TaurusDevice.isValid`"""
        return self._deviceObj is not None

    def lock(self, force=False):
        li = self.getLockInfo()
        if force:
            if self.getLockInfo().status == TaurusLockInfo.Locked:
                self.unlock(force=True)
        return self.getDeviceProxy().lock()

    def unlock(self, force=False):
        return self.getDeviceProxy().unlock(force)

    def getLockInfo(self, cache=False):
        lock_info = self._lock_info
        if cache and lock_info.status != LockStatus.Unknown:
            return lock_info
        else:
            try:
                dev = self.getDeviceProxy()
                li = LockerInfo()
                locked = dev.get_locker(li)
                msg = '%s ' % self.getSimpleName()
                if locked:
                    lock_info.id = pid = li.li
                    lock_info.language = li.ll
                    lock_info.host = host = li.locker_host
                    lock_info.klass = li.locker_class
                    if dev.is_locked_by_me():
                        status = LockStatus.LockedMaster
                        msg += 'is locked by you!'
                    else:
                        status = LockStatus.Locked
                        msg += 'is locked by PID %s on %s' % (pid, host)
                else:
                    lock_info.id = None
                    lock_info.language = None
                    lock_info.host = host = None
                    lock_info.klass = None
                    status = LockStatus.Unlocked
                    msg += 'is not locked'
                lock_info.status = status
                lock_info.status_msg = msg
            except:
                self._lock_info = lock_info = TaurusLockInfo()

            return lock_info

    def removeListener(self, listener):
        ret = TaurusDevice.removeListener(self, listener)
        if not ret or self.hasListeners():
            return ret
        return self.stateObj.removeListener(self)

    def addListener(self, listener):
        weWereListening = self.hasListeners()
        ret = TaurusDevice.addListener(self, listener)
        if not ret:
            return ret
        if weWereListening:
            try:
                evt_value = self.__decode(self.stateObj.read())
            except:
                self.debug('Cannot read state')
                return ret

            listeners = hasattr(listener, '__iter__') and listener or [
             listener]
            self.fireEvent(TaurusEventType.Change, evt_value, listeners)
        else:
            self.stateObj.addListener(self)
        return ret

    def eventReceived(self, event_src, event_type, event_value):
        if event_type == TaurusEventType.Config:
            return
        value = self.__decode(event_value)
        new_state = value.rvalue
        if new_state != self._deviceState:
            msg = 'Device State changed %s -> %s' % (self._deviceState.name,
             new_state.name)
            self.debug(msg)
            self._deviceState = new_state
            self.fireEvent(TaurusEventType.Change, value)

    def __decode(self, event_value):
        """Decode events from the state attribute into TangoAttrValues whose
        rvalue is the Device state"""
        from taurus.core.tango.tangoattribute import TangoAttrValue
        if isinstance(event_value, TangoAttrValue):
            new_state = TaurusDevState.Ready
        elif isinstance(event_value, DevFailed):
            new_state = TaurusDevState.NotReady
        else:
            self.info('Unexpected event value: %r', event_value)
            new_state = TaurusDevState.Undefined
        from taurus.core.taurusbasetypes import TaurusModelValue
        value = TaurusModelValue()
        value.rvalue = new_state
        return value

    def __pollResult(self, attrs, ts, result, error=False):
        if error:
            for attr in attrs.values():
                attr.poll(single=False, value=None, error=result, time=ts)

            return
        for da in result:
            if da.has_failed:
                v, err = None, DevFailed(*da.get_err_stack())
            else:
                v, err = da, None
            attr = attrs[da.name]
            attr.poll(single=False, value=v, error=err, time=ts)

        return

    def __pollAsynch(self, attrs):
        ts = time.time()
        try:
            req_id = self.read_attributes_asynch(list(attrs.keys()))
        except DevFailed as e:
            return (
             False, e, ts)

        return (
         True, req_id, ts)

    def __pollReply(self, attrs, req_id, timeout=None):
        ok, req_id, ts = req_id
        if not ok:
            self.__pollResult(attrs, ts, req_id, error=True)
            return
        else:
            if timeout is None:
                timeout = 0
            timeout = int(timeout * 1000)
            result = self.read_attributes_reply(req_id, timeout)
            self.__pollResult(attrs, ts, result)
            return

    def poll(self, attrs, asynch=False, req_id=None):
        """optimized by reading of multiple attributes in one go"""
        if req_id is not None:
            return self.__pollReply(attrs, req_id)
        else:
            if asynch:
                return self.__pollAsynch(attrs)
            error = False
            ts = time.time()
            try:
                result = self.read_attributes(list(attrs.keys()))
            except DevFailed as e:
                error = True
                result = e

            self.__pollResult(attrs, ts, result, error=error)
            return

    def _repr_html_(self):
        try:
            info = self.getDeviceProxy().info()
        except:
            info = _TangoInfo()

        txt = ('<table>\n    <tr><td>Short name</td><td>{simple_name}</td></tr>\n    <tr><td>Standard name</td><td>{normal_name}</td></tr>\n    <tr><td>Full name</td><td>{full_name}</td></tr>\n    <tr><td>Device class</td><td>{dev_class}</td></tr>\n    <tr><td>Server</td><td>{server_id}</td></tr>\n    <tr><td>Documentation</td><td><a target="_blank" href="{doc_url}">{doc_url}</a></td></tr>\n</table>\n').format(simple_name=self.getSimpleName(), normal_name=self.getNormalName(), full_name=self.getFullName(), dev_class=info.dev_class, server_id=info.server_id, doc_url=info.doc_url)
        return txt

    @taurus4_deprecation(alt='.description')
    def getDescription(self, cache=True):
        return self.description

    @property
    def description(self):
        try:
            self._description = self.getDeviceProxy().description()
        except:
            pass

        return self._description

    @property
    def stateObj(self):
        if self._deviceStateObj is None:
            self._deviceStateObj = self.getAttribute('state')
        return self._deviceStateObj