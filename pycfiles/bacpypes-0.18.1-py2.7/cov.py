# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bacpypes/service/cov.py
# Compiled at: 2020-04-22 18:27:50
"""
Change Of Value Service
"""
from ..debugging import bacpypes_debugging, DebugContents, ModuleLogger
from ..capability import Capability
from ..core import deferred
from ..task import OneShotTask, RecurringFunctionTask, TaskManager
from ..iocb import IOCB
from ..basetypes import DeviceAddress, COVSubscription, PropertyValue, Recipient, RecipientProcess, ObjectPropertyReference
from ..constructeddata import ListOf, Any
from ..apdu import ConfirmedCOVNotificationRequest, UnconfirmedCOVNotificationRequest, SimpleAckPDU, Error, RejectPDU, AbortPDU
from ..errors import ExecutionError
from ..object import Property
from .detect import DetectionAlgorithm, monitor_filter
_debug = 0
_log = ModuleLogger(globals())

@bacpypes_debugging
class SubscriptionList:

    def __init__(self):
        if _debug:
            SubscriptionList._debug('__init__')
        self.cov_subscriptions = []

    def append(self, cov):
        if _debug:
            SubscriptionList._debug('append %r', cov)
        self.cov_subscriptions.append(cov)

    def remove(self, cov):
        if _debug:
            SubscriptionList._debug('remove %r', cov)
        self.cov_subscriptions.remove(cov)

    def find(self, client_addr, proc_id, obj_id):
        if _debug:
            SubscriptionList._debug('find %r %r %r', client_addr, proc_id, obj_id)
        for cov in self.cov_subscriptions:
            all_equal = cov.client_addr == client_addr and cov.proc_id == proc_id and cov.obj_id == obj_id
            if _debug:
                SubscriptionList._debug('    - cov, all_equal: %r %r', cov, all_equal)
            if all_equal:
                return cov

        return

    def __len__(self):
        if _debug:
            SubscriptionList._debug('__len__')
        return len(self.cov_subscriptions)

    def __iter__(self):
        if _debug:
            SubscriptionList._debug('__iter__')
        for cov in self.cov_subscriptions:
            yield cov


@bacpypes_debugging
class Subscription(OneShotTask, DebugContents):
    _debug_contents = ('obj_ref', 'client_addr', 'proc_id', 'obj_id', 'confirmed',
                       'lifetime')

    def __init__(self, obj_ref, client_addr, proc_id, obj_id, confirmed, lifetime):
        if _debug:
            Subscription._debug('__init__ %r %r %r %r %r %r', obj_ref, client_addr, proc_id, obj_id, confirmed, lifetime)
        OneShotTask.__init__(self)
        self.obj_ref = obj_ref
        self.client_addr = client_addr
        self.proc_id = proc_id
        self.obj_id = obj_id
        self.confirmed = confirmed
        self.lifetime = lifetime
        if lifetime != 0:
            self.install_task(delta=self.lifetime)

    def cancel_subscription(self):
        if _debug:
            Subscription._debug('cancel_subscription')
        self.suspend_task()
        self.obj_ref._app.cancel_subscription(self)
        self.obj_ref = None
        return

    def renew_subscription(self, lifetime):
        if _debug:
            Subscription._debug('renew_subscription')
        if self.isScheduled:
            self.suspend_task()
        if lifetime != 0:
            self.install_task(delta=lifetime)

    def process_task(self):
        if _debug:
            Subscription._debug('process_task')
        self.cancel_subscription()


@bacpypes_debugging
class COVDetection(DetectionAlgorithm):
    properties_tracked = ()
    properties_reported = ()
    monitored_property_reference = None

    def __init__(self, obj):
        if _debug:
            COVDetection._debug('__init__ %r', obj)
        DetectionAlgorithm.__init__(self)
        self.obj = obj
        kwargs = {}
        for property_name in self.properties_tracked:
            setattr(self, property_name, None)
            kwargs[property_name] = (obj, property_name)

        self.bind(**kwargs)
        self.cov_subscriptions = SubscriptionList()
        return

    def add_subscription(self, cov):
        if _debug:
            COVDetection._debug('add_subscription %r', cov)
        self.cov_subscriptions.append(cov)

    def cancel_subscription(self, cov):
        if _debug:
            COVDetection._debug('cancel_subscription %r', cov)
        if cov.isScheduled:
            cov.suspend_task()
            if _debug:
                COVDetection._debug('    - task suspended')
        self.cov_subscriptions.remove(cov)

    def execute(self):
        if _debug:
            COVDetection._debug('execute')
        self.send_cov_notifications()

    def send_cov_notifications(self, subscription=None):
        if _debug:
            COVDetection._debug('send_cov_notifications %r', subscription)
        if not len(self.cov_subscriptions):
            return
        else:
            current_time = TaskManager().get_time()
            if _debug:
                COVDetection._debug('    - current_time: %r', current_time)
            list_of_values = []
            for property_name in self.properties_reported:
                if _debug:
                    COVDetection._debug('    - property_name: %r', property_name)
                property_datatype = self.obj.get_datatype(property_name)
                if _debug:
                    COVDetection._debug('        - property_datatype: %r', property_datatype)
                bundle_value = property_datatype(self.obj._values[property_name])
                if _debug:
                    COVDetection._debug('        - bundle_value: %r', bundle_value)
                property_value = PropertyValue(propertyIdentifier=property_name, value=Any(bundle_value))
                list_of_values.append(property_value)

            if _debug:
                COVDetection._debug('    - list_of_values: %r', list_of_values)
            if subscription is not None:
                notification_list = [
                 subscription]
            else:
                notification_list = self.cov_subscriptions
            for cov in notification_list:
                if _debug:
                    COVDetection._debug('    - cov: %s', repr(cov))
                if not cov.lifetime:
                    time_remaining = 0
                else:
                    time_remaining = int(cov.taskTime - current_time)
                    if not time_remaining:
                        time_remaining = 1
                if cov.confirmed:
                    request = ConfirmedCOVNotificationRequest()
                else:
                    request = UnconfirmedCOVNotificationRequest()
                request.pduDestination = cov.client_addr
                request.subscriberProcessIdentifier = cov.proc_id
                request.initiatingDeviceIdentifier = self.obj._app.localDevice.objectIdentifier
                request.monitoredObjectIdentifier = cov.obj_id
                request.timeRemaining = time_remaining
                request.listOfValues = list_of_values
                if _debug:
                    COVDetection._debug('    - request: %s', repr(request))
                self.obj._app.cov_notification(cov, request)

            return

    def __str__(self):
        return '<' + self.__class__.__name__ + '(' + (',').join(self.properties_tracked) + ')' + '>'


class GenericCriteria(COVDetection):
    properties_tracked = ('presentValue', 'statusFlags')
    properties_reported = ('presentValue', 'statusFlags')
    monitored_property_reference = 'presentValue'


@bacpypes_debugging
class COVIncrementCriteria(COVDetection):
    properties_tracked = ('presentValue', 'statusFlags', 'covIncrement')
    properties_reported = ('presentValue', 'statusFlags')
    monitored_property_reference = 'presentValue'

    def __init__(self, obj):
        if _debug:
            COVIncrementCriteria._debug('__init__ %r', obj)
        COVDetection.__init__(self, obj)
        self.previous_reported_value = None
        return

    @monitor_filter('presentValue')
    def present_value_filter(self, old_value, new_value):
        if _debug:
            COVIncrementCriteria._debug('present_value_filter %r %r', old_value, new_value)
        if self.previous_reported_value is None:
            if _debug:
                COVIncrementCriteria._debug('    - first value: %r', old_value)
            self.previous_reported_value = old_value
        value_changed = new_value <= self.previous_reported_value - self.obj.covIncrement or new_value >= self.previous_reported_value + self.obj.covIncrement
        if _debug:
            COVIncrementCriteria._debug('    - value significantly changed: %r', value_changed)
        return value_changed

    def send_cov_notifications(self, subscription=None):
        if _debug:
            COVIncrementCriteria._debug('send_cov_notifications %r', subscription)
        self.previous_reported_value = self.presentValue
        COVDetection.send_cov_notifications(self, subscription)


class AccessDoorCriteria(COVDetection):
    properties_tracked = ('presentValue', 'statusFlags', 'doorAlarmState')
    properties_reported = ('presentValue', 'statusFlags', 'doorAlarmState')


class AccessPointCriteria(COVDetection):
    properties_tracked = ('accessEventTime', 'statusFlags')
    properties_reported = ('accessEvent', 'statusFlags', 'accessEventTag', 'accessEventTime',
                           'accessEventCredential', 'accessEventAuthenticationFactor')
    monitored_property_reference = 'accessEvent'


class CredentialDataInputCriteria(COVDetection):
    properties_tracked = ('updateTime', 'statusFlags')
    properties_reported = ('presentValue', 'statusFlags', 'updateTime')


class LoadControlCriteria(COVDetection):
    properties_tracked = ('presentValue', 'statusFlags', 'requestedShedLevel', 'startTime',
                          'shedDuration', 'dutyWindow')
    properties_reported = ('presentValue', 'statusFlags', 'requestedShedLevel', 'startTime',
                           'shedDuration', 'dutyWindow')


@bacpypes_debugging
class PulseConverterCriteria(COVIncrementCriteria):
    properties_tracked = ('presentValue', 'statusFlags', 'covPeriod')
    properties_reported = ('presentValue', 'statusFlags')

    def __init__(self, obj):
        if _debug:
            PulseConverterCriteria._debug('__init__ %r', obj)
        COVIncrementCriteria.__init__(self, obj)
        if self.covPeriod == 0:
            if _debug:
                PulseConverterCriteria._debug('    - no periodic notifications')
            self.cov_period_task = None
        else:
            if _debug:
                PulseConverterCriteria._debug('    - covPeriod: %r', self.covPeriod)
            self.cov_period_task = RecurringFunctionTask(self.covPeriod * 1000, self.send_cov_notifications)
            if _debug:
                PulseConverterCriteria._debug('    - cov period task created')
        return

    def add_subscription(self, cov):
        if _debug:
            PulseConverterCriteria._debug('add_subscription %r', cov)
        COVIncrementCriteria.add_subscription(self, cov)
        if self.cov_period_task:
            self.cov_period_task.install_task()
            if _debug:
                PulseConverterCriteria._debug('    - cov period task installed')

    def cancel_subscription(self, cov):
        if _debug:
            PulseConverterCriteria._debug('cancel_subscription %r', cov)
        COVIncrementCriteria.cancel_subscription(self, cov)
        if not len(self.cov_subscriptions):
            if self.cov_period_task and self.cov_period_task.isScheduled:
                self.cov_period_task.suspend_task()
                if _debug:
                    PulseConverterCriteria._debug('    - cov period task suspended')
                self.cov_period_task = None
        return

    @monitor_filter('covPeriod')
    def cov_period_filter(self, old_value, new_value):
        if _debug:
            PulseConverterCriteria._debug('cov_period_filter %r %r', old_value, new_value)
        if old_value != 0:
            if self.cov_period_task.isScheduled:
                self.cov_period_task.suspend_task()
                if _debug:
                    PulseConverterCriteria._debug('    - canceled old task')
            self.cov_period_task = None
        if new_value != 0:
            self.cov_period_task = RecurringFunctionTask(new_value * 1000, self.cov_period_x)
            self.cov_period_task.install_task()
            if _debug:
                PulseConverterCriteria._debug('    - new task created and installed')
        return False

    def send_cov_notifications(self, subscription=None):
        if _debug:
            PulseConverterCriteria._debug('send_cov_notifications %r', subscription)
        COVIncrementCriteria.send_cov_notifications(self, subscription)


criteria_type_map = {'accessPoint': AccessPointCriteria, 
   'analogInput': COVIncrementCriteria, 
   'analogOutput': COVIncrementCriteria, 
   'analogValue': COVIncrementCriteria, 
   'largeAnalogValue': COVIncrementCriteria, 
   'integerValue': COVIncrementCriteria, 
   'positiveIntegerValue': COVIncrementCriteria, 
   'lightingOutput': COVIncrementCriteria, 
   'binaryInput': GenericCriteria, 
   'binaryOutput': GenericCriteria, 
   'binaryValue': GenericCriteria, 
   'lifeSafetyPoint': GenericCriteria, 
   'lifeSafetyZone': GenericCriteria, 
   'multiStateInput': GenericCriteria, 
   'multiStateOutput': GenericCriteria, 
   'multiStateValue': GenericCriteria, 
   'octetString': GenericCriteria, 
   'characterString': GenericCriteria, 
   'timeValue': GenericCriteria, 
   'dateTimeValue': GenericCriteria, 
   'dateValue': GenericCriteria, 
   'timePatternValue': GenericCriteria, 
   'datePatternValue': GenericCriteria, 
   'dateTimePatternValue': GenericCriteria, 
   'credentialDataInput': CredentialDataInputCriteria, 
   'loadControl': LoadControlCriteria, 
   'loop': GenericCriteria, 
   'pulseConverter': PulseConverterCriteria}

@bacpypes_debugging
class ActiveCOVSubscriptions(Property):

    def __init__(self):
        Property.__init__(self, 'activeCovSubscriptions', ListOf(COVSubscription), default=None, optional=True, mutable=False)
        return

    def ReadProperty(self, obj, arrayIndex=None):
        if _debug:
            ActiveCOVSubscriptions._debug('ReadProperty %s arrayIndex=%r', obj, arrayIndex)
        current_time = TaskManager().get_time()
        if _debug:
            ActiveCOVSubscriptions._debug('    - current_time: %r', current_time)
        cov_subscriptions = []
        for cov in obj._app.subscriptions():
            if not cov.lifetime:
                time_remaining = 0
            else:
                time_remaining = int(cov.taskTime - current_time)
                if not time_remaining:
                    time_remaining = 1
            recipient = Recipient(address=DeviceAddress(networkNumber=cov.client_addr.addrNet or 0, macAddress=cov.client_addr.addrAddr))
            if _debug:
                ActiveCOVSubscriptions._debug('    - recipient: %r', recipient)
            if _debug:
                ActiveCOVSubscriptions._debug('    - client MAC address: %r', cov.client_addr.addrAddr)
            recipient_process = RecipientProcess(recipient=recipient, processIdentifier=cov.proc_id)
            if _debug:
                ActiveCOVSubscriptions._debug('    - recipient_process: %r', recipient_process)
            cov_detection = cov.obj_ref._app.cov_detections[cov.obj_ref]
            if _debug:
                ActiveCOVSubscriptions._debug('    - cov_detection: %r', cov_detection)
            cov_subscription = COVSubscription(recipient=recipient_process, monitoredPropertyReference=ObjectPropertyReference(objectIdentifier=cov.obj_id, propertyIdentifier=cov_detection.monitored_property_reference), issueConfirmedNotifications=cov.confirmed, timeRemaining=time_remaining)
            if hasattr(cov_detection, 'covIncrement'):
                cov_subscription.covIncrement = cov_detection.covIncrement
            if _debug:
                ActiveCOVSubscriptions._debug('    - cov_subscription: %r', cov_subscription)
            cov_subscriptions.append(cov_subscription)

        return cov_subscriptions

    def WriteProperty(self, obj, value, arrayIndex=None, priority=None):
        raise ExecutionError(errorClass='property', errorCode='writeAccessDenied')


@bacpypes_debugging
class ChangeOfValueServices(Capability):

    def __init__(self):
        if _debug:
            ChangeOfValueServices._debug('__init__')
        Capability.__init__(self)
        self.cov_detections = {}
        if self.localDevice and self.localDevice.activeCovSubscriptions is None:
            self.localDevice.add_property(ActiveCOVSubscriptions())
        return

    def add_subscription(self, cov):
        if _debug:
            ChangeOfValueServices._debug('add_subscription %r', cov)
        self.cov_detections[cov.obj_ref].add_subscription(cov)

    def cancel_subscription(self, cov):
        if _debug:
            ChangeOfValueServices._debug('cancel_subscription %r', cov)
        cov_detection = self.cov_detections[cov.obj_ref]
        cov_detection.cancel_subscription(cov)
        if not len(cov_detection.cov_subscriptions):
            if _debug:
                ChangeOfValueServices._debug('    - no more subscriptions')
            cov_detection.unbind()
            del self.cov_detections[cov.obj_ref]

    def subscriptions(self):
        """Generator for the active subscriptions."""
        if _debug:
            ChangeOfValueServices._debug('subscriptions')
        for obj, cov_detection in self.cov_detections.items():
            for cov in cov_detection.cov_subscriptions:
                yield cov

    def cov_notification(self, cov, request):
        if _debug:
            ChangeOfValueServices._debug('cov_notification %s %s', str(cov), str(request))
        iocb = IOCB(request)
        if _debug:
            ChangeOfValueServices._debug('    - iocb: %r', iocb)
        iocb.cov = cov
        iocb.add_callback(self.cov_confirmation)
        self.request_io(iocb)

    def cov_confirmation(self, iocb):
        if _debug:
            ChangeOfValueServices._debug('cov_confirmation %r', iocb)
        if iocb.ioResponse:
            if _debug:
                ChangeOfValueServices._debug('    - ack')
            self.cov_ack(iocb.cov, iocb.args[0], iocb.ioResponse)
        elif isinstance(iocb.ioError, Error):
            if _debug:
                ChangeOfValueServices._debug('    - error: %r', iocb.ioError.errorCode)
            self.cov_error(iocb.cov, iocb.args[0], iocb.ioError)
        elif isinstance(iocb.ioError, RejectPDU):
            if _debug:
                ChangeOfValueServices._debug('    - reject: %r', iocb.ioError.apduAbortRejectReason)
            self.cov_reject(iocb.cov, iocb.args[0], iocb.ioError)
        elif isinstance(iocb.ioError, AbortPDU):
            if _debug:
                ChangeOfValueServices._debug('    - abort: %r', iocb.ioError.apduAbortRejectReason)
            self.cov_abort(iocb.cov, iocb.args[0], iocb.ioError)

    def cov_ack(self, cov, request, response):
        if _debug:
            ChangeOfValueServices._debug('cov_ack %r %r %r', cov, request, response)

    def cov_error(self, cov, request, response):
        if _debug:
            ChangeOfValueServices._debug('cov_error %r %r %r', cov, request, response)

    def cov_reject(self, cov, request, response):
        if _debug:
            ChangeOfValueServices._debug('cov_reject %r %r %r', cov, request, response)

    def cov_abort(self, cov, request, response):
        if _debug:
            ChangeOfValueServices._debug('cov_abort %r %r %r', cov, request, response)

    def do_SubscribeCOVRequest(self, apdu):
        if _debug:
            ChangeOfValueServices._debug('do_SubscribeCOVRequest %r', apdu)
        client_addr = apdu.pduSource
        proc_id = apdu.subscriberProcessIdentifier
        obj_id = apdu.monitoredObjectIdentifier
        confirmed = apdu.issueConfirmedNotifications
        lifetime = apdu.lifetime
        cancel_subscription = confirmed is None and lifetime is None
        obj = self.get_object_id(obj_id)
        if _debug:
            ChangeOfValueServices._debug('    - object: %r', obj)
        if not obj:
            raise ExecutionError(errorClass='object', errorCode='unknownObject')
        if not obj._object_supports_cov:
            raise ExecutionError(errorClass='services', errorCode='covSubscriptionFailed')
        cov_detection = self.cov_detections.get(obj, None)
        if not cov_detection:
            criteria_class = criteria_type_map.get(obj_id[0], None)
            if not criteria_class:
                raise ExecutionError(errorClass='services', errorCode='covSubscriptionFailed')
            cov_detection = criteria_class(obj)
            self.cov_detections[obj] = cov_detection
        if _debug:
            ChangeOfValueServices._debug('    - cov_detection: %r', cov_detection)
        cov = cov_detection.cov_subscriptions.find(client_addr, proc_id, obj_id)
        if _debug:
            ChangeOfValueServices._debug('    - cov: %r', cov)
        if cov:
            if cancel_subscription:
                if _debug:
                    ChangeOfValueServices._debug('    - cancel the subscription')
                self.cancel_subscription(cov)
            else:
                if _debug:
                    ChangeOfValueServices._debug('    - renew the subscription')
                cov.renew_subscription(lifetime)
        elif cancel_subscription:
            if _debug:
                ChangeOfValueServices._debug("    - cancel a subscription that doesn't exist")
        else:
            if _debug:
                ChangeOfValueServices._debug('    - create a subscription')
            cov = Subscription(obj, client_addr, proc_id, obj_id, confirmed, lifetime)
            if _debug:
                ChangeOfValueServices._debug('    - cov: %r', cov)
            self.add_subscription(cov)
        response = SimpleAckPDU(context=apdu)
        self.response(response)
        if not cancel_subscription:
            if _debug:
                ChangeOfValueServices._debug('    - send a notification')
            deferred(cov_detection.send_cov_notifications, cov)
        return