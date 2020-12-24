# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bacpypes/service/device.py
# Compiled at: 2020-04-20 14:21:21
from ..debugging import bacpypes_debugging, ModuleLogger
from ..capability import Capability
from ..pdu import GlobalBroadcast
from ..apdu import WhoIsRequest, IAmRequest, IHaveRequest, SimpleAckPDU
from ..errors import ExecutionError, InconsistentParameters, MissingRequiredParameter, ParameterOutOfRange
from ..task import FunctionTask
_debug = 0
_log = ModuleLogger(globals())

@bacpypes_debugging
class WhoIsIAmServices(Capability):

    def __init__(self):
        if _debug:
            WhoIsIAmServices._debug('__init__')
        Capability.__init__(self)

    def startup(self):
        if _debug:
            WhoIsIAmServices._debug('startup')
        self.i_am()

    def who_is(self, low_limit=None, high_limit=None, address=None):
        if _debug:
            WhoIsIAmServices._debug('who_is')
        whoIs = WhoIsRequest()
        if not address:
            address = GlobalBroadcast()
        whoIs.pduDestination = address
        if low_limit is not None:
            if high_limit is None:
                raise MissingRequiredParameter('high_limit required')
            if low_limit < 0 or low_limit > 4194303:
                raise ParameterOutOfRange('low_limit out of range')
            whoIs.deviceInstanceRangeLowLimit = low_limit
        if high_limit is not None:
            if low_limit is None:
                raise MissingRequiredParameter('low_limit required')
            if high_limit < 0 or high_limit > 4194303:
                raise ParameterOutOfRange('high_limit out of range')
            whoIs.deviceInstanceRangeHighLimit = high_limit
        if _debug:
            WhoIsIAmServices._debug('    - whoIs: %r', whoIs)
        self.request(whoIs)
        return

    def do_WhoIsRequest(self, apdu):
        """Respond to a Who-Is request."""
        if _debug:
            WhoIsIAmServices._debug('do_WhoIsRequest %r', apdu)
        if not self.localDevice:
            if _debug:
                WhoIsIAmServices._debug('    - no local device')
            return
        low_limit = apdu.deviceInstanceRangeLowLimit
        high_limit = apdu.deviceInstanceRangeHighLimit
        if low_limit is not None:
            if high_limit is None:
                raise MissingRequiredParameter('deviceInstanceRangeHighLimit required')
            if low_limit < 0 or low_limit > 4194303:
                raise ParameterOutOfRange('deviceInstanceRangeLowLimit out of range')
        if high_limit is not None:
            if low_limit is None:
                raise MissingRequiredParameter('deviceInstanceRangeLowLimit required')
            if high_limit < 0 or high_limit > 4194303:
                raise ParameterOutOfRange('deviceInstanceRangeHighLimit out of range')
        if low_limit is not None:
            if self.localDevice.objectIdentifier[1] < low_limit:
                return
        if high_limit is not None:
            if self.localDevice.objectIdentifier[1] > high_limit:
                return
        self.i_am(address=apdu.pduSource)
        return

    def i_am(self, address=None):
        if _debug:
            WhoIsIAmServices._debug('i_am')
        if not self.localDevice:
            if _debug:
                WhoIsIAmServices._debug('    - no local device')
            return
        iAm = IAmRequest(iAmDeviceIdentifier=self.localDevice.objectIdentifier, maxAPDULengthAccepted=self.localDevice.maxApduLengthAccepted, segmentationSupported=self.localDevice.segmentationSupported, vendorID=self.localDevice.vendorIdentifier)
        if not address:
            address = GlobalBroadcast()
        iAm.pduDestination = address
        if _debug:
            WhoIsIAmServices._debug('    - iAm: %r', iAm)
        self.request(iAm)

    def do_IAmRequest(self, apdu):
        """Respond to an I-Am request."""
        if _debug:
            WhoIsIAmServices._debug('do_IAmRequest %r', apdu)
        if apdu.iAmDeviceIdentifier is None:
            raise MissingRequiredParameter('iAmDeviceIdentifier required')
        if apdu.maxAPDULengthAccepted is None:
            raise MissingRequiredParameter('maxAPDULengthAccepted required')
        if apdu.segmentationSupported is None:
            raise MissingRequiredParameter('segmentationSupported required')
        if apdu.vendorID is None:
            raise MissingRequiredParameter('vendorID required')
        device_instance = apdu.iAmDeviceIdentifier[1]
        if _debug:
            WhoIsIAmServices._debug('    - device_instance: %r', device_instance)
        device_address = apdu.pduSource
        if _debug:
            WhoIsIAmServices._debug('    - device_address: %r', device_address)
        return


@bacpypes_debugging
class WhoHasIHaveServices(Capability):

    def __init__(self):
        if _debug:
            WhoHasIHaveServices._debug('__init__')
        Capability.__init__(self)

    def who_has(self, thing, address=None):
        if _debug:
            WhoHasIHaveServices._debug('who_has %r address=%r', thing, address)
        raise NotImplementedError('who_has')

    def do_WhoHasRequest(self, apdu):
        """Respond to a Who-Has request."""
        if _debug:
            WhoHasIHaveServices._debug('do_WhoHasRequest, %r', apdu)
        if not self.localDevice:
            if _debug:
                WhoIsIAmServices._debug('    - no local device')
            return
        if apdu.limits is not None:
            low_limit = apdu.limits.deviceInstanceRangeLowLimit
            high_limit = apdu.limits.deviceInstanceRangeHighLimit
            if low_limit is None:
                raise MissingRequiredParameter('deviceInstanceRangeLowLimit required')
            if low_limit < 0 or low_limit > 4194303:
                raise ParameterOutOfRange('deviceInstanceRangeLowLimit out of range')
            if high_limit is None:
                raise MissingRequiredParameter('deviceInstanceRangeHighLimit required')
            if high_limit < 0 or high_limit > 4194303:
                raise ParameterOutOfRange('deviceInstanceRangeHighLimit out of range')
            if self.localDevice.objectIdentifier[1] < low_limit:
                return
            if self.localDevice.objectIdentifier[1] > high_limit:
                return
        if apdu.object.objectIdentifier is not None:
            obj = self.objectIdentifier.get(apdu.object.objectIdentifier, None)
        elif apdu.object.objectName is not None:
            obj = self.objectName.get(apdu.object.objectName, None)
        else:
            raise InconsistentParameters('object identifier or object name required')
        if not obj:
            return
        else:
            self.i_have(obj, address=apdu.pduSource)
            return

    def i_have(self, thing, address=None):
        if _debug:
            WhoHasIHaveServices._debug('i_have %r address=%r', thing, address)
        if not self.localDevice:
            if _debug:
                WhoIsIAmServices._debug('    - no local device')
            return
        iHave = IHaveRequest(deviceIdentifier=self.localDevice.objectIdentifier, objectIdentifier=thing.objectIdentifier, objectName=thing.objectName)
        if not address:
            address = GlobalBroadcast()
        iHave.pduDestination = address
        if _debug:
            WhoHasIHaveServices._debug('    - iHave: %r', iHave)
        self.request(iHave)

    def do_IHaveRequest(self, apdu):
        """Respond to a I-Have request."""
        if _debug:
            WhoHasIHaveServices._debug('do_IHaveRequest %r', apdu)
        if apdu.deviceIdentifier is None:
            raise MissingRequiredParameter('deviceIdentifier required')
        if apdu.objectIdentifier is None:
            raise MissingRequiredParameter('objectIdentifier required')
        if apdu.objectName is None:
            raise MissingRequiredParameter('objectName required')
        return


@bacpypes_debugging
class DeviceCommunicationControlServices(Capability):

    def __init__(self):
        if _debug:
            DeviceCommunicationControlServices._debug('__init__')
        Capability.__init__(self)
        self._dcc_enable_task = None
        return

    def do_DeviceCommunicationControlRequest(self, apdu):
        if _debug:
            DeviceCommunicationControlServices._debug('do_CommunicationControlRequest, %r', apdu)
        if getattr(self.localDevice, '_dcc_password', None):
            if not apdu.password or apdu.password != getattr(self.localDevice, '_dcc_password'):
                raise ExecutionError(errorClass='security', errorCode='passwordFailure')
        if apdu.enableDisable == 'enable':
            self.enable_communications()
        else:
            self.disable_communications(apdu.enableDisable)
            if apdu.timeDuration:
                self._dcc_enable_task = FunctionTask(self.enable_communications)
                self._dcc_enable_task.install_task(delta=apdu.timeDuration * 60)
                if _debug:
                    DeviceCommunicationControlServices._debug('    - enable scheduled')
        self.response(SimpleAckPDU(context=apdu))
        return

    def enable_communications(self):
        if _debug:
            DeviceCommunicationControlServices._debug('enable_communications')
        self.smap.dccEnableDisable = 'enable'
        if self._dcc_enable_task:
            self._dcc_enable_task.suspend_task()
            self._dcc_enable_task = None
        return

    def disable_communications(self, enable_disable):
        if _debug:
            DeviceCommunicationControlServices._debug('disable_communications %r', enable_disable)
        self.smap.dccEnableDisable = enable_disable
        if self._dcc_enable_task:
            self._dcc_enable_task.suspend_task()
            self._dcc_enable_task = None
        return