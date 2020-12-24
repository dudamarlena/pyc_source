# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\connection_specific\usb_libs\usb1.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 83372 bytes
"""
Pythonic wrapper for libusb-1.0.

The first thing you must do is to get an "USB context". To do so, create an
USBContext instance.
Then, you can use it to browse available USB devices and open the one you want
to talk to.
At this point, you should have a USBDeviceHandle instance (as returned by
USBContext or USBDevice instances), and you can start exchanging with the
device.

Features:
- Basic device settings (configuration & interface selection, ...)
- String descriptor lookups (ASCII & unicode), and list supported language
  codes
- Synchronous I/O (control, bulk, interrupt)
- Asynchronous I/O (control, bulk, interrupt, isochronous)
  Note: Isochronous support is not well tested.
  See USBPoller, USBTransfer and USBTransferHelper.

All LIBUSB_* constants are available in this module, without the LIBUSB_
prefix - with one exception: LIBUSB_5GBPS_OPERATION is available as
SUPER_SPEED_OPERATION, so it is a valid python identifier.

All LIBUSB_ERROR_* constants are available in this module as exception classes,
subclassing USBError.
"""
import libusb1
from ctypes import byref, create_string_buffer, c_int, sizeof, POINTER, cast, c_uint8, c_uint16, c_ubyte, string_at, c_void_p, cdll, addressof
import sys, threading
from ctypes.util import find_library
import warnings, weakref, collections, functools
__all__ = [
 'USBContext', 'USBDeviceHandle', 'USBDevice', 'hasCapability',
 'USBPoller', 'USBTransfer', 'USBTransferHelper', 'EVENT_CALLBACK_SET',
 'USBPollerThread', 'USBEndpoint', 'USBInterfaceSetting', 'USBInterface',
 'USBConfiguration', 'DoomedTransferError', 'getVersion', 'USBError']
USBError = libusb1.USBError
STATUS_TO_EXCEPTION_DICT = {}

def __bindConstants():
    global_dict = globals()
    PREFIX = 'LIBUSB_'
    for name, value in libusb1.__dict__.items():
        if name.startswith(PREFIX):
            name = name[len(PREFIX):]
            if name == '5GBPS_OPERATION':
                name = 'SUPER_SPEED_OPERATION'
            assert name not in global_dict
            global_dict[name] = value
            __all__.append(name)

    for name, value in libusb1.libusb_error.forward_dict.items():
        if value:
            if not name.startswith(PREFIX + 'ERROR_'):
                raise AssertionError(name)
            elif name == 'LIBUSB_ERROR_IO':
                name = 'ErrorIO'
            else:
                name = ''.join((x.capitalize() for x in name.split('_')[1:]))
            name = 'USB' + name
            assert name not in global_dict, name
            assert value not in STATUS_TO_EXCEPTION_DICT
            STATUS_TO_EXCEPTION_DICT[value] = global_dict[name] = type(name, (
             USBError,), {'value': value})
            __all__.append(name)


__bindConstants()
del __bindConstants

def raiseUSBError(value):
    raise STATUS_TO_EXCEPTION_DICT.get(value, USBError)(value)


def mayRaiseUSBError(value):
    if value < 0:
        raiseUSBError(value)


try:
    namedtuple = collections.namedtuple
except AttributeError:
    Version = lambda *x: x
else:
    Version = namedtuple('Version', [
     'major', 'minor', 'micro', 'nano', 'rc', 'describe'])
if sys.version_info[0] == 3:
    BYTE = bytes([0])
    xrange = range
    long = int
else:
    BYTE = '\x00'
CONTROL_SETUP = BYTE * CONTROL_SETUP_SIZE
if sys.version_info[:2] >= (2, 6):
    if sys.platform == 'win32':
        from ctypes import get_last_error as get_errno
    else:
        from ctypes import get_errno
else:

    def get_errno():
        raise NotImplementedError('Your python version does not support errno/last_error')


__libc_name = find_library('c')
if __libc_name is None:
    _free = lambda x: None
else:
    _free = getattr(cdll, __libc_name).free
del __libc_name
try:
    WeakSet = weakref.WeakSet
except AttributeError:

    class WeakSet(object):

        def __init__(self):
            self._WeakSet__dict = weakref.WeakKeyDictionary()

        def add(self, item):
            self._WeakSet__dict[item] = None

        def pop(self):
            return self._WeakSet__dict.popitem()[0]


STRING_LENGTH = 255
PATH_MAX_DEPTH = 7
EVENT_CALLBACK_SET = frozenset((
 TRANSFER_COMPLETED,
 TRANSFER_ERROR,
 TRANSFER_TIMED_OUT,
 TRANSFER_CANCELLED,
 TRANSFER_STALL,
 TRANSFER_NO_DEVICE,
 TRANSFER_OVERFLOW))
DEFAULT_ASYNC_TRANSFER_ERROR_CALLBACK = lambda x: False

def create_binary_buffer(init_or_size):
    if isinstance(init_or_size, (int, long)):
        result = create_string_buffer(init_or_size)
    else:
        result = create_string_buffer(init_or_size, len(init_or_size))
    return result


class DoomedTransferError(Exception):
    __doc__ = 'Exception raised when altering/submitting a doomed transfer.'


class USBTransfer(object):
    __doc__ = '\n    USB asynchronous transfer control & data.\n\n    All modification methods will raise if called on a submitted transfer.\n    Methods noted as "should not be called on a submitted transfer" will not\n    prevent you from reading, but returned value is unspecified.\n\n    Note on user_data: because of pypy\'s current ctype restrictions, user_data\n    is not provided to C level, but is managed purely in python. It should\n    change nothing for you, unless you are looking at underlying C transfer\n    structure - which you should never have to.\n    '
    _USBTransfer__libusb_free_transfer = libusb1.libusb_free_transfer
    _USBTransfer__libusb_cancel_transfer = libusb1.libusb_cancel_transfer
    _USBTransfer__USBError = USBError
    _USBTransfer__USBErrorNotFound = USBErrorNotFound
    _USBTransfer__transfer = None
    _USBTransfer__initialized = False
    _USBTransfer__submitted = False
    _USBTransfer__callback = None
    _USBTransfer__ctypesCallbackWrapper = None
    _USBTransfer__doomed = False
    _USBTransfer__user_data = None
    _USBTransfer__transfer_buffer = None

    def __init__(self, handle, iso_packets, before_submit, after_completion):
        """
        You should not instanciate this class directly.
        Call "getTransfer" method on an USBDeviceHandle instance to get
        instances of this class.
        """
        if iso_packets < 0:
            raise ValueError('Cannot request a negative number of iso packets.')
        self._USBTransfer__handle = handle
        self._USBTransfer__before_submit = before_submit
        self._USBTransfer__after_completion = after_completion
        self._USBTransfer__num_iso_packets = iso_packets
        result = libusb1.libusb_alloc_transfer(iso_packets)
        if not result:
            raise USBErrorNoMem
        self._USBTransfer__transfer = result
        self._USBTransfer__ctypesCallbackWrapper = libusb1.libusb_transfer_cb_fn_p(self._USBTransfer__callbackWrapper)

    def close(self):
        """
        Break reference cycles to allow instance to be garbage-collected.
        Raises if called on a submitted transfer.
        """
        if self._USBTransfer__submitted:
            raise ValueError('Cannot close a submitted transfer')
        self.doom()
        self._USBTransfer__initialized = False
        self._USBTransfer__callback = None
        self._USBTransfer__user_data = None
        self._USBTransfer__ctypesCallbackWrapper = None
        if self._USBTransfer__transfer is not None:
            self._USBTransfer__libusb_free_transfer(self._USBTransfer__transfer)
            self._USBTransfer__transfer = None
        self._USBTransfer__transfer_buffer = None
        self._USBTransfer__before_submit = None
        self._USBTransfer__after_completion = None

    def doom(self):
        """
        Prevent transfer from being submitted again.
        """
        self._USBTransfer__doomed = True

    def __del__(self):
        if self._USBTransfer__transfer is not None:
            try:
                self.cancel()
            except self._USBTransfer__USBErrorNotFound:
                self._USBTransfer__libusb_free_transfer(self._USBTransfer__transfer)

    def __callbackWrapper(self, transfer_p):
        """
        Makes it possible for user-provided callback to alter transfer when
        fired (ie, mark transfer as not submitted upon call).
        """
        self._USBTransfer__submitted = False
        self._USBTransfer__after_completion(self)
        callback = self._USBTransfer__callback
        if callback is not None:
            callback(self)
        if self._USBTransfer__doomed:
            self.close()

    def setCallback(self, callback):
        """
        Change transfer's callback.
        """
        self._USBTransfer__callback = callback

    def getCallback(self):
        """
        Get currently set callback.
        """
        return self._USBTransfer__callback

    def setControl(self, request_type, request, value, index, buffer_or_len, callback=None, user_data=None, timeout=0):
        """
        Setup transfer for control use.

        request_type, request, value, index
            See USBDeviceHandle.controlWrite.
            request_type defines transfer direction (see
            ENDPOINT_OUT and ENDPOINT_IN)).
        buffer_or_len
            Either a string (when sending data), or expected data length (when
            receiving data).
        callback
            Callback function to be invoked on transfer completion.
            Called with transfer as parameter, return value ignored.
        user_data
            User data to pass to callback function.
        timeout
            Transfer timeout in milliseconds. 0 to disable.
        """
        if self._USBTransfer__submitted:
            raise ValueError('Cannot alter a submitted transfer')
        else:
            if self._USBTransfer__doomed:
                raise DoomedTransferError('Cannot reuse a doomed transfer')
            if isinstance(buffer_or_len, (int, long)):
                length = buffer_or_len
                string_buffer = create_binary_buffer(length + CONTROL_SETUP_SIZE)
            else:
                length = len(buffer_or_len)
            string_buffer = create_binary_buffer(CONTROL_SETUP + buffer_or_len)
        self._USBTransfer__initialized = False
        self._USBTransfer__transfer_buffer = string_buffer
        self._USBTransfer__user_data = user_data
        libusb1.libusb_fill_control_setup(string_buffer, request_type, request, value, index, length)
        libusb1.libusb_fill_control_transfer(self._USBTransfer__transfer, self._USBTransfer__handle, string_buffer, self._USBTransfer__ctypesCallbackWrapper, None, timeout)
        self._USBTransfer__callback = callback
        self._USBTransfer__initialized = True

    def setBulk(self, endpoint, buffer_or_len, callback=None, user_data=None, timeout=0):
        """
        Setup transfer for bulk use.

        endpoint
            Endpoint to submit transfer to. Defines transfer direction (see
            ENDPOINT_OUT and ENDPOINT_IN)).
        buffer_or_len
            Either a string (when sending data), or expected data length (when
            receiving data)
        callback
            Callback function to be invoked on transfer completion.
            Called with transfer as parameter, return value ignored.
        user_data
            User data to pass to callback function.
        timeout
            Transfer timeout in milliseconds. 0 to disable.
        """
        if self._USBTransfer__submitted:
            raise ValueError('Cannot alter a submitted transfer')
        if self._USBTransfer__doomed:
            raise DoomedTransferError('Cannot reuse a doomed transfer')
        string_buffer = create_binary_buffer(buffer_or_len)
        self._USBTransfer__initialized = False
        self._USBTransfer__transfer_buffer = string_buffer
        self._USBTransfer__user_data = user_data
        libusb1.libusb_fill_bulk_transfer(self._USBTransfer__transfer, self._USBTransfer__handle, endpoint, string_buffer, sizeof(string_buffer), self._USBTransfer__ctypesCallbackWrapper, None, timeout)
        self._USBTransfer__callback = callback
        self._USBTransfer__initialized = True

    def setInterrupt(self, endpoint, buffer_or_len, callback=None, user_data=None, timeout=0):
        """
        Setup transfer for interrupt use.

        endpoint
            Endpoint to submit transfer to. Defines transfer direction (see
            ENDPOINT_OUT and ENDPOINT_IN)).
        buffer_or_len
            Either a string (when sending data), or expected data length (when
            receiving data)
        callback
            Callback function to be invoked on transfer completion.
            Called with transfer as parameter, return value ignored.
        user_data
            User data to pass to callback function.
        timeout
            Transfer timeout in milliseconds. 0 to disable.
        """
        if self._USBTransfer__submitted:
            raise ValueError('Cannot alter a submitted transfer')
        if self._USBTransfer__doomed:
            raise DoomedTransferError('Cannot reuse a doomed transfer')
        string_buffer = create_binary_buffer(buffer_or_len)
        self._USBTransfer__initialized = False
        self._USBTransfer__transfer_buffer = string_buffer
        self._USBTransfer__user_data = user_data
        libusb1.libusb_fill_interrupt_transfer(self._USBTransfer__transfer, self._USBTransfer__handle, endpoint, string_buffer, sizeof(string_buffer), self._USBTransfer__ctypesCallbackWrapper, None, timeout)
        self._USBTransfer__callback = callback
        self._USBTransfer__initialized = True

    def setIsochronous(self, endpoint, buffer_or_len, callback=None, user_data=None, timeout=0, iso_transfer_length_list=None):
        """
        Setup transfer for isochronous use.

        endpoint
            Endpoint to submit transfer to. Defines transfer direction (see
            ENDPOINT_OUT and ENDPOINT_IN)).
        buffer_or_len
            Either a string (when sending data), or expected data length (when
            receiving data)
        callback
            Callback function to be invoked on transfer completion.
            Called with transfer as parameter, return value ignored.
        user_data
            User data to pass to callback function.
        timeout
            Transfer timeout in milliseconds. 0 to disable.
        iso_transfer_length_list
            List of individual transfer sizes. If not provided, buffer_or_len
            will be divided evenly among available transfers if possible, and
            raise ValueError otherwise.
        """
        if self._USBTransfer__submitted:
            raise ValueError('Cannot alter a submitted transfer')
        num_iso_packets = self._USBTransfer__num_iso_packets
        if num_iso_packets == 0:
            raise TypeError('This transfer canot be used for isochronous I/O. You must get another one with a non-zero iso_packets parameter.')
        if self._USBTransfer__doomed:
            raise DoomedTransferError('Cannot reuse a doomed transfer')
        string_buffer = create_binary_buffer(buffer_or_len)
        buffer_length = sizeof(string_buffer)
        if iso_transfer_length_list is None:
            iso_length, remainder = divmod(buffer_length, num_iso_packets)
            if remainder:
                raise ValueError('Buffer size %i cannot be evenly distributed among %i transfers' % (
                 buffer_length,
                 num_iso_packets))
            iso_transfer_length_list = [
             iso_length] * num_iso_packets
        configured_iso_packets = len(iso_transfer_length_list)
        if configured_iso_packets > num_iso_packets:
            raise ValueError('Too many ISO transfer lengths (%i), there are only %i ISO transfers available' % (
             configured_iso_packets,
             num_iso_packets))
        if sum(iso_transfer_length_list) > buffer_length:
            raise ValueError('ISO transfers too long (%i), there are only %i bytes available' % (
             sum(iso_transfer_length_list),
             buffer_length))
        transfer_p = self._USBTransfer__transfer
        self._USBTransfer__initialized = False
        self._USBTransfer__transfer_buffer = string_buffer
        self._USBTransfer__user_data = user_data
        libusb1.libusb_fill_iso_transfer(transfer_p, self._USBTransfer__handle, endpoint, string_buffer, buffer_length, configured_iso_packets, self._USBTransfer__ctypesCallbackWrapper, None, timeout)
        for length, iso_packet_desc in zip(iso_transfer_length_list, libusb1.get_iso_packet_list(transfer_p)):
            if length <= 0:
                raise ValueError('Negative/null length transfers are not possible.')
            iso_packet_desc.length = length

        self._USBTransfer__callback = callback
        self._USBTransfer__initialized = True

    def getType(self):
        """
        Get transfer type.

        Returns one of:
            TRANSFER_TYPE_CONTROL
            TRANSFER_TYPE_ISOCHRONOUS
            TRANSFER_TYPE_BULK
            TRANSFER_TYPE_INTERRUPT
        """
        return self._USBTransfer__transfer.contents.type

    def getEndpoint(self):
        """
        Get endpoint.
        """
        return self._USBTransfer__transfer.contents.endpoint

    def getStatus(self):
        """
        Get transfer status.
        Should not be called on a submitted transfer.
        """
        return self._USBTransfer__transfer.contents.status

    def getActualLength(self):
        """
        Get actually transfered data length.
        Should not be called on a submitted transfer.
        """
        return self._USBTransfer__transfer.contents.actual_length

    def getBuffer(self):
        """
        Get data buffer content.
        Should not be called on a submitted transfer.
        """
        transfer_p = self._USBTransfer__transfer
        transfer = transfer_p.contents
        if transfer.type == TRANSFER_TYPE_CONTROL:
            result = libusb1.libusb_control_transfer_get_data(transfer_p)
        else:
            result = string_at(transfer.buffer, transfer.length)
        return result

    def getUserData(self):
        """
        Retrieve user data provided on setup.
        """
        return self._USBTransfer__user_data

    def setUserData(self, user_data):
        """
        Change user data.
        """
        self._USBTransfer__user_data = user_data

    def getISOBufferList(self):
        """
        Get individual ISO transfer's buffer.
        Returns a list with one item per ISO transfer, with their
        individually-configured sizes.
        Returned list is consistent with getISOSetupList return value.
        Should not be called on a submitted transfer.

        See also iterISO.
        """
        transfer_p = self._USBTransfer__transfer
        transfer = transfer_p.contents
        if transfer.type != TRANSFER_TYPE_ISOCHRONOUS:
            raise TypeError('This method cannot be called on non-iso transfers.')
        return libusb1.get_iso_packet_buffer_list(transfer_p)

    def getISOSetupList(self):
        """
        Get individual ISO transfer's setup.
        Returns a list of dicts, each containing an individual ISO transfer
        parameters:
        - length
        - actual_length
        - status
        (see libusb1's API documentation for their signification)
        Returned list is consistent with getISOBufferList return value.
        Should not be called on a submitted transfer (except for 'length'
        values).
        """
        transfer_p = self._USBTransfer__transfer
        transfer = transfer_p.contents
        if transfer.type != TRANSFER_TYPE_ISOCHRONOUS:
            raise TypeError('This method cannot be called on non-iso transfers.')
        return [{'length':x.length,  'actual_length':x.actual_length,  'status':x.status} for x in libusb1.get_iso_packet_list(transfer_p)]

    def iterISO(self):
        """
        Generator yielding (status, buffer) for each isochornous transfer.
        buffer is truncated to actual_length.
        This is more efficient than calling both getISOBufferList and
        getISOSetupList when receiving data.
        Should not be called on a submitted transfer.
        """
        transfer_p = self._USBTransfer__transfer
        transfer = transfer_p.contents
        if transfer.type != TRANSFER_TYPE_ISOCHRONOUS:
            raise TypeError('This method cannot be called on non-iso transfers.')
        buffer_position = transfer.buffer
        for iso_transfer in libusb1.get_iso_packet_list(transfer_p):
            yield (iso_transfer.status,
             string_at(buffer_position, iso_transfer.actual_length))
            buffer_position += iso_transfer.length

    def setBuffer(self, buffer_or_len):
        """
        Replace buffer with a new one.
        Allows resizing read buffer and replacing data sent.
        Note: resizing is not allowed for isochronous buffer (use
        setIsochronous).
        Note: disallowed on control transfers (use setControl).
        """
        if self._USBTransfer__submitted:
            raise ValueError('Cannot alter a submitted transfer')
        else:
            transfer = self._USBTransfer__transfer.contents
            if transfer.type == TRANSFER_TYPE_CONTROL:
                raise ValueError('To alter control transfer buffer, use setControl')
            buff = create_binary_buffer(buffer_or_len)
            if transfer.type == TRANSFER_TYPE_ISOCHRONOUS and sizeof(buff) != transfer.length:
                raise ValueError('To alter isochronous transfer buffer length, use setIsochronous')
        self._USBTransfer__transfer_buffer = buff
        transfer.buffer = cast(buff, c_void_p)
        transfer.length = sizeof(buff)

    def isSubmitted(self):
        """
        Tells if this transfer is submitted and still pending.
        """
        return self._USBTransfer__submitted

    def submit(self):
        """
        Submit transfer for asynchronous handling.
        """
        if self._USBTransfer__submitted:
            raise ValueError('Cannot submit a submitted transfer')
        if not self._USBTransfer__initialized:
            raise ValueError('Cannot submit a transfer until it has been initialized')
        if self._USBTransfer__doomed:
            raise DoomedTransferError('Cannot submit doomed transfer')
        self._USBTransfer__before_submit(self)
        self._USBTransfer__submitted = True
        result = libusb1.libusb_submit_transfer(self._USBTransfer__transfer)
        if result:
            self._USBTransfer__after_completion(self)
            self._USBTransfer__submitted = False
            raiseUSBError(result)

    def cancel(self):
        """
        Cancel transfer.
        Note: cancellation happens asynchronously, so you must wait for
        TRANSFER_CANCELLED.
        """
        if not self._USBTransfer__submitted:
            raise self._USBTransfer__USBErrorNotFound
        result = self._USBTransfer__libusb_cancel_transfer(self._USBTransfer__transfer)
        if result:
            raise self._USBTransfer__USBError(result)


class USBTransferHelper(object):
    __doc__ = '\n    Simplifies subscribing to the same transfer over and over, and callback\n    handling:\n    - no need to read event status to execute apropriate code, just setup\n      different functions for each status code\n    - just return True instead of calling submit\n    - no need to check if transfer is doomed before submitting it again,\n      DoomedTransferError is caught.\n\n    Callbacks used in this class must follow the callback API described in\n    USBTransfer, and are expected to return a boolean:\n    - True if transfer is to be submitted again (to receive/send more data)\n    - False otherwise\n\n    Note: as per libusb1 specifications, isochronous transfer global state\n    might be TRANSFER_COMPLETED although some individual packets might\n    have an error status. You can check individual packet status by calling\n    getISOSetupList on transfer object in your callback.\n    '

    def __init__(self, transfer=None):
        """
        Create a transfer callback dispatcher.

        transfer parameter is deprecated. If provided, it will be equivalent
        to:
            helper = USBTransferHelper()
            transfer.setCallback(helper)
        and also allows using deprecated methods on this class (otherwise,
        they raise AttributeError).
        """
        if transfer is not None:
            self._USBTransferHelper__transfer = transfer
            transfer.setCallback(self)
        self._USBTransferHelper__event_callback_dict = {}
        self._USBTransferHelper__errorCallback = DEFAULT_ASYNC_TRANSFER_ERROR_CALLBACK

    def submit(self):
        """
        Submit the asynchronous read request.
        Deprecated. Use submit on transfer.
        """
        self._USBTransferHelper__transfer.submit()

    def cancel(self):
        """
        Cancel a pending read request.
        Deprecated. Use cancel on transfer.
        """
        self._USBTransferHelper__transfer.cancel()

    def setEventCallback(self, event, callback):
        """
        Set a function to call for a given event.
        event must be one of:
            TRANSFER_COMPLETED
            TRANSFER_ERROR
            TRANSFER_TIMED_OUT
            TRANSFER_CANCELLED
            TRANSFER_STALL
            TRANSFER_NO_DEVICE
            TRANSFER_OVERFLOW
        """
        if event not in EVENT_CALLBACK_SET:
            raise ValueError('Unknown event %r.' % (event,))
        self._USBTransferHelper__event_callback_dict[event] = callback

    def setDefaultCallback(self, callback):
        """
        Set the function to call for event which don't have a specific callback
        registered.
        The initial default callback does nothing and returns False.
        """
        self._USBTransferHelper__errorCallback = callback

    def getEventCallback(self, event, default=None):
        """
        Return the function registered to be called for given event identifier.
        """
        return self._USBTransferHelper__event_callback_dict.get(event, default)

    def __call__(self, transfer):
        """
        Callback to set on transfers.
        """
        if self.getEventCallback(transfer.getStatus(), self._USBTransferHelper__errorCallback)(transfer):
            try:
                transfer.submit()
            except DoomedTransferError:
                pass

    def isSubmited(self):
        """
        Returns whether this reader is currently waiting for an event.
        Deprecatd. Use isSubmitted on transfer.
        """
        return self._USBTransferHelper__transfer.isSubmitted()


class USBPollerThread(threading.Thread):
    __doc__ = "\n    Implements libusb1 documentation about threaded, asynchronous\n    applications.\n    In short, instanciate this class once (...per USBContext instance), call\n    start() on the instance, and do whatever you need.\n    This thread will be used to execute transfer completion callbacks, and you\n    are free to use libusb1's synchronous API in another thread, and can forget\n    about libusb1 file descriptors.\n\n    See http://libusb.sourceforge.net/api-1.0/mtasync.html .\n    "

    def __init__(self, context, poller, exc_callback=None):
        """
        Create a poller thread for given context.
        Warning: it will not check if another poller instance was already
        present for that context, and will replace it.

        poller
            (same as USBPoller.__init__ "poller" parameter)

        exc_callback (callable)
          Called with a libusb_error value as single parameter when event
          handling fails.
          If not given, an USBError will be raised, interrupting the thread.
        """
        super(USBPollerThread, self).__init__()
        self.daemon = True
        self._USBPollerThread__context = context
        self._USBPollerThread__poller = poller
        self._USBPollerThread__fd_set = set()
        context.setPollFDNotifiers(self._registerFD, self._unregisterFD)
        for fd, events in context.getPollFDList():
            self._registerFD(fd, events, None)

        if exc_callback is not None:
            self.exceptionHandler = exc_callback

    def __del__(self):
        self._USBPollerThread__context.setPollFDNotifiers(None, None)

    @staticmethod
    def exceptionHandler(exc):
        raise exc

    def run(self):
        context = self._USBPollerThread__context
        poll = self._USBPollerThread__poller.poll
        try_lock_events = context.tryLockEvents
        lock_event_waiters = context.lockEventWaiters
        wait_for_event = context.waitForEvent
        unlock_event_waiters = context.unlockEventWaiters
        event_handling_ok = context.eventHandlingOK
        unlock_events = context.unlockEvents
        handle_events_locked = context.handleEventsLocked
        event_handler_active = context.eventHandlerActive
        getNextTimeout = context.getNextTimeout
        exceptionHandler = self.exceptionHandler
        fd_set = self._USBPollerThread__fd_set
        while fd_set:
            if try_lock_events():
                lock_event_waiters()
                while event_handler_active():
                    wait_for_event()

                unlock_event_waiters()
            else:
                try:
                    while event_handling_ok():
                        if poll(getNextTimeout()):
                            try:
                                handle_events_locked()
                            except USBError:
                                exceptionHandler(sys.exc_info()[1])

                finally:
                    unlock_events()

    def _registerFD(self, fd, events, _):
        self._USBPollerThread__poller.register(fd, events)
        self._USBPollerThread__fd_set.add(fd)

    def _unregisterFD(self, fd, _):
        self._USBPollerThread__fd_set.discard(fd)
        self._USBPollerThread__poller.unregister(fd)


class USBPoller(object):
    __doc__ = '\n    Class allowing integration of USB event polling in a file-descriptor\n    monitoring event loop.\n\n    WARNING: Do not call "poll" from several threads concurently. Do not use\n    synchronous USB transfers in a thread while "poll" is running. Doing so\n    will result in unnecessarily long pauses in some threads. Opening and/or\n    closing devices while polling can cause race conditions to occur.\n    '

    def __init__(self, context, poller):
        """
        Create a poller for given context.
        Warning: it will not check if another poller instance was already
        present for that context, and will replace it.

        poller is a polling instance implementing the following methods:
        - register(fd, event_flags)
          event_flags have the same meaning as in poll API (POLLIN & POLLOUT)
        - unregister(fd)
        - poll(timeout)
          timeout being a float in seconds, or negative/None if there is no
          timeout.
          It must return a list of (descriptor, event) pairs.
        Note: USBPoller is itself a valid poller.
        Note2: select.poll uses a timeout in milliseconds, for some reason
        (all other select.* classes use seconds for timeout), so you should
        wrap it to convert & round/truncate timeout.
        """
        self._USBPoller__context = context
        self._USBPoller__poller = poller
        self._USBPoller__fd_set = set()
        context.setPollFDNotifiers(self._registerFD, self._unregisterFD)
        for fd, events in context.getPollFDList():
            self._registerFD(fd, events)

    def __del__(self):
        self._USBPoller__context.setPollFDNotifiers(None, None)

    def poll(self, timeout=None):
        """
        Poll for events.
        timeout can be a float in seconds, or None for no timeout.
        Returns a list of (descriptor, event) pairs.
        """
        next_usb_timeout = self._USBPoller__context.getNextTimeout()
        if timeout is None or timeout < 0:
            usb_timeout = next_usb_timeout
        else:
            if next_usb_timeout:
                usb_timeout = min(next_usb_timeout, timeout)
            else:
                usb_timeout = timeout
        event_list = self._USBPoller__poller.poll(usb_timeout)
        if event_list:
            fd_set = self._USBPoller__fd_set
            result = [(x, y) for x, y in event_list if x not in fd_set]
            if len(result) != len(event_list):
                self._USBPoller__context.handleEventsTimeout()
        else:
            result = event_list
            self._USBPoller__context.handleEventsTimeout()
        return result

    def register(self, fd, events):
        """
        Register an USB-unrelated fd to poller.
        Convenience method.
        """
        if fd in self._USBPoller__fd_set:
            raise ValueError('This fd is a special USB event fd, it cannot be polled.')
        self._USBPoller__poller.register(fd, events)

    def unregister(self, fd):
        """
        Unregister an USB-unrelated fd from poller.
        Convenience method.
        """
        if fd in self._USBPoller__fd_set:
            raise ValueError('This fd is a special USB event fd, it must stay registered.')
        self._USBPoller__poller.unregister(fd)

    def _registerFD(self, fd, events, user_data=None):
        self.register(fd, events)
        self._USBPoller__fd_set.add(fd)

    def _unregisterFD(self, fd, user_data=None):
        self._USBPoller__fd_set.discard(fd)
        self.unregister(fd)


class USBDeviceHandle(object):
    __doc__ = '\n    Represents an opened USB device.\n    '
    _USBDeviceHandle__handle = None
    _USBDeviceHandle__libusb_close = libusb1.libusb_close
    _USBDeviceHandle__USBError = USBError
    _USBDeviceHandle__USBErrorNoDevice = USBErrorNoDevice
    _USBDeviceHandle__USBErrorNotFound = USBErrorNotFound
    _USBDeviceHandle__USBErrorInterrupted = USBErrorInterrupted
    _USBDeviceHandle__set = set
    _USBDeviceHandle__KeyError = KeyError
    _USBDeviceHandle__sys = sys

    def __init__(self, context, handle, device):
        """
        You should not instanciate this class directly.
        Call "open" method on an USBDevice instance to get an USBDeviceHandle
        instance.
        """
        self._USBDeviceHandle__context = context
        self._USBDeviceHandle__transfer_set = WeakSet()
        self._USBDeviceHandle__inflight = inflight = set()
        self._USBDeviceHandle__inflight_add = inflight.add
        self._USBDeviceHandle__inflight_remove = inflight.remove
        self._USBDeviceHandle__handle = handle
        self._USBDeviceHandle__device = device

    def __del__(self):
        self.close()

    def close(self):
        """
        Close this handle. If not called explicitely, will be called by
        destructor.

        This method cancels any in-flight transfer when it is called. As
        cancellation is not immediate, this method needs to let libusb handle
        events until transfers are actually cancelled.
        In multi-threaded programs, this can lead to stalls. To avoid this,
        do not close nor let GC collect a USBDeviceHandle which has in-flight
        transfers.
        """
        handle = self._USBDeviceHandle__handle
        if handle is not None:
            weak_transfer_set = self._USBDeviceHandle__transfer_set
            transfer_set = self._USBDeviceHandle__set()
            while True:
                try:
                    transfer = weak_transfer_set.pop()
                except self._USBDeviceHandle__KeyError:
                    break

                transfer_set.add(transfer)
                transfer.doom()

            inflight = self._USBDeviceHandle__inflight
            for transfer in inflight:
                try:
                    transfer.cancel()
                except (self._USBDeviceHandle__USBErrorNotFound, self._USBDeviceHandle__USBErrorNoDevice):
                    pass

            while inflight:
                try:
                    self._USBDeviceHandle__context.handleEvents()
                except self._USBDeviceHandle__USBErrorInterrupted:
                    pass

            for transfer in transfer_set:
                transfer.close()

            self._USBDeviceHandle__libusb_close(handle)
            self._USBDeviceHandle__handle = None

    def getDevice(self):
        """
        Get an USBDevice instance for the device accessed through this handle.
        Useful for example to query its configurations.
        """
        return self._USBDeviceHandle__device

    def getConfiguration(self):
        """
        Get the current configuration number for this device.
        """
        configuration = c_int()
        result = libusb1.libusb_get_configuration(self._USBDeviceHandle__handle, byref(configuration))
        mayRaiseUSBError(result)
        return configuration.value

    def setConfiguration(self, configuration):
        """
        Set the configuration number for this device.
        """
        result = libusb1.libusb_set_configuration(self._USBDeviceHandle__handle, configuration)
        mayRaiseUSBError(result)

    def claimInterface(self, interface):
        """
        Claim (= get exclusive access to) given interface number. Required to
        receive/send data.
        """
        result = libusb1.libusb_claim_interface(self._USBDeviceHandle__handle, interface)
        mayRaiseUSBError(result)

    def releaseInterface(self, interface):
        """
        Release interface, allowing another process to use it.
        """
        result = libusb1.libusb_release_interface(self._USBDeviceHandle__handle, interface)
        mayRaiseUSBError(result)

    def setInterfaceAltSetting(self, interface, alt_setting):
        """
        Set interface's alternative setting (both parameters are integers).
        """
        result = libusb1.libusb_set_interface_alt_setting(self._USBDeviceHandle__handle, interface, alt_setting)
        mayRaiseUSBError(result)

    def clearHalt(self, endpoint):
        """
        Clear a halt state on given endpoint number.
        """
        result = libusb1.libusb_clear_halt(self._USBDeviceHandle__handle, endpoint)
        mayRaiseUSBError(result)

    def resetDevice(self):
        """
        Reinitialise current device.
        Attempts to restore current configuration & alt settings.
        If this fails, will result in a device disconnect & reconnect, so you
        have to close current device and rediscover it (notified by a
        ERROR_NOT_FOUND error code).
        """
        result = libusb1.libusb_reset_device(self._USBDeviceHandle__handle)
        mayRaiseUSBError(result)

    def kernelDriverActive(self, interface):
        """
        Tell whether a kernel driver is active on given interface number.
        """
        result = libusb1.libusb_kernel_driver_active(self._USBDeviceHandle__handle, interface)
        if result == 0:
            return False
        if result == 1:
            return True
        raiseUSBError(result)

    def detachKernelDriver(self, interface):
        """
        Ask kernel driver to detach from given interface number.
        """
        result = libusb1.libusb_detach_kernel_driver(self._USBDeviceHandle__handle, interface)
        mayRaiseUSBError(result)

    def attachKernelDriver(self, interface):
        """
        Ask kernel driver to re-attach to given interface number.
        """
        result = libusb1.libusb_attach_kernel_driver(self._USBDeviceHandle__handle, interface)
        mayRaiseUSBError(result)

    def setAutoDetachKernelDriver(self, enable):
        """
        Control automatic kernel driver detach.
        enable (bool)
            True to enable auto-detach, False to disable it.
        """
        result = libusb1.libusb_set_auto_detach_kernel_driver(self._USBDeviceHandle__handle, bool(enable))
        mayRaiseUSBError(result)

    def getSupportedLanguageList(self):
        """
        Return a list of USB language identifiers (as integers) supported by
        current device for its string descriptors.

        Note: language identifiers seem (I didn't check them all...) very
        similar to windows language identifiers, so you may want to use
        locales.windows_locale to get an rfc3066 representation. The 5 standard
        HID language codes are missing though.
        """
        descriptor_string = create_binary_buffer(STRING_LENGTH)
        result = libusb1.libusb_get_string_descriptor(self._USBDeviceHandle__handle, 0, 0, descriptor_string, sizeof(descriptor_string))
        if result == ERROR_PIPE:
            return []
        mayRaiseUSBError(result)
        length = cast(descriptor_string, POINTER(c_ubyte))[0]
        langid_list = cast(descriptor_string, POINTER(c_uint16))
        result = []
        append = result.append
        for offset in xrange(1, length / 2):
            append(libusb1.libusb_le16_to_cpu(langid_list[offset]))

        return result

    def getStringDescriptor(self, descriptor, lang_id):
        """
        Fetch description string for given descriptor and in given language.
        Use getSupportedLanguageList to know which languages are available.
        Return value is an unicode string.
        Return None if there is no such descriptor on device.
        """
        descriptor_string = create_binary_buffer(STRING_LENGTH)
        result = libusb1.libusb_get_string_descriptor(self._USBDeviceHandle__handle, descriptor, lang_id, descriptor_string, sizeof(descriptor_string))
        if result == ERROR_NOT_FOUND:
            return
        mayRaiseUSBError(result)
        return descriptor_string.value.decode('UTF-16-LE')

    def getASCIIStringDescriptor(self, descriptor):
        """
        Fetch description string for given descriptor in first available
        language.
        Return value is an ASCII string.
        Return None if there is no such descriptor on device.
        """
        descriptor_string = create_binary_buffer(STRING_LENGTH)
        result = libusb1.libusb_get_string_descriptor_ascii(self._USBDeviceHandle__handle, descriptor, descriptor_string, sizeof(descriptor_string))
        if result == ERROR_NOT_FOUND:
            return
        mayRaiseUSBError(result)
        return descriptor_string.value.decode('ASCII')

    def _controlTransfer(self, request_type, request, value, index, data, length, timeout):
        result = libusb1.libusb_control_transfer(self._USBDeviceHandle__handle, request_type, request, value, index, data, length, timeout)
        mayRaiseUSBError(result)
        return result

    def controlWrite(self, request_type, request, value, index, data, timeout=0):
        """
        Synchronous control write.
        request_type: request type bitmask (bmRequestType), see
          constants TYPE_* and RECIPIENT_*.
        request: request id (some values are standard).
        value, index, data: meaning is request-dependent.
        timeout: in milliseconds, how long to wait for device acknowledgement.
          Set to 0 to disable.

        Returns the number of bytes actually sent.
        """
        request_type = request_type & ~ENDPOINT_DIR_MASK | ENDPOINT_OUT
        data = create_binary_buffer(data)
        return self._controlTransfer(request_type, request, value, index, data, sizeof(data), timeout)

    def controlRead(self, request_type, request, value, index, length, timeout=0):
        """
        Synchronous control read.
        timeout: in milliseconds, how long to wait for data. Set to 0 to
          disable.
        See controlWrite for other parameters description.

        Returns received data.
        """
        request_type = request_type & ~ENDPOINT_DIR_MASK | ENDPOINT_IN
        data = create_binary_buffer(length)
        transferred = self._controlTransfer(request_type, request, value, index, data, length, timeout)
        return data.raw[:transferred]

    def _bulkTransfer(self, endpoint, data, length, timeout):
        transferred = c_int()
        result = libusb1.libusb_bulk_transfer(self._USBDeviceHandle__handle, endpoint, data, length, byref(transferred), timeout)
        mayRaiseUSBError(result)
        return transferred.value

    def bulkWrite(self, endpoint, data, timeout=0):
        """
        Synchronous bulk write.
        endpoint: endpoint to send data to.
        data: data to send.
        timeout: in milliseconds, how long to wait for device acknowledgement.
          Set to 0 to disable.

        Returns the number of bytes actually sent.
        """
        endpoint = endpoint & ~ENDPOINT_DIR_MASK | ENDPOINT_OUT
        data = create_binary_buffer(data)
        return self._bulkTransfer(endpoint, data, sizeof(data), timeout)

    def bulkRead(self, endpoint, length, timeout=0):
        """
        Synchronous bulk read.
        timeout: in milliseconds, how long to wait for data. Set to 0 to
          disable.
        See bulkWrite for other parameters description.

        Returns received data.
        """
        endpoint = endpoint & ~ENDPOINT_DIR_MASK | ENDPOINT_IN
        data = create_binary_buffer(length)
        transferred = self._bulkTransfer(endpoint, data, length, timeout)
        return data.raw[:transferred]

    def _interruptTransfer(self, endpoint, data, length, timeout):
        transferred = c_int()
        result = libusb1.libusb_interrupt_transfer(self._USBDeviceHandle__handle, endpoint, data, length, byref(transferred), timeout)
        mayRaiseUSBError(result)
        return transferred.value

    def interruptWrite(self, endpoint, data, timeout=0):
        """
        Synchronous interrupt write.
        endpoint: endpoint to send data to.
        data: data to send.
        timeout: in milliseconds, how long to wait for device acknowledgement.
          Set to 0 to disable.

        Returns the number of bytes actually sent.
        """
        endpoint = endpoint & ~ENDPOINT_DIR_MASK | ENDPOINT_OUT
        data = create_binary_buffer(data)
        return self._interruptTransfer(endpoint, data, sizeof(data), timeout)

    def interruptRead(self, endpoint, length, timeout=0):
        """
        Synchronous interrupt write.
        timeout: in milliseconds, how long to wait for data. Set to 0 to
          disable.
        See interruptRead for other parameters description.

        Returns received data.
        """
        endpoint = endpoint & ~ENDPOINT_DIR_MASK | ENDPOINT_IN
        data = create_binary_buffer(length)
        transferred = self._interruptTransfer(endpoint, data, length, timeout)
        return data.raw[:transferred]

    def getTransfer(self, iso_packets=0):
        """
        Get an USBTransfer instance for asynchronous use.
        iso_packets: the number of isochronous transfer descriptors to
          allocate.
        """
        result = USBTransfer(self._USBDeviceHandle__handle, iso_packets, self._USBDeviceHandle__inflight_add, self._USBDeviceHandle__inflight_remove)
        self._USBDeviceHandle__transfer_set.add(result)
        return result


class USBConfiguration(object):

    def __init__(self, context, config):
        """
        You should not instanciate this class directly.
        Call USBDevice methods to get instances of this class.
        """
        if not isinstance(config, libusb1.libusb_config_descriptor):
            raise TypeError('Unexpected descriptor type.')
        self._USBConfiguration__config = config
        self._USBConfiguration__context = context

    def getNumInterfaces(self):
        return self._USBConfiguration__config.bNumInterfaces

    __len__ = getNumInterfaces

    def getConfigurationValue(self):
        return self._USBConfiguration__config.bConfigurationValue

    def getDescriptor(self):
        return self._USBConfiguration__config.iConfiguration

    def getAttributes(self):
        return self._USBConfiguration__config.bmAttributes

    def getMaxPower(self):
        """
        Returns device's power consumption in mW.
        Beware of unit: USB descriptor uses 2mW increments, this method
        converts it to mW units.
        """
        return self._USBConfiguration__config.MaxPower * 2

    def getExtra(self):
        """
        Returns a list of extra (non-basic) descriptors (DFU, HID, ...).
        """
        return libusb1.get_extra(self._USBConfiguration__config)

    def __iter__(self):
        """
        Iterates over interfaces available in this configuration, yielding
        USBInterface instances.
        """
        context = self._USBConfiguration__context
        interface_list = self._USBConfiguration__config.interface
        for interface_num in xrange(self.getNumInterfaces()):
            yield USBInterface(context, interface_list[interface_num])

    iterInterfaces = __iter__

    def __getitem__(self, interface):
        """
        Returns an USBInterface instance.
        """
        if not isinstance(interface, int):
            raise TypeError('interface parameter must be an integer')
        if not 0 <= interface < self.getNumInterfaces():
            raise IndexError('No such interface: %r' % (interface,))
        return USBInterface(self._USBConfiguration__context, self._USBConfiguration__config.interface[interface])


class USBInterface(object):

    def __init__(self, context, interface):
        """
        You should not instanciate this class directly.
        Call USBConfiguration methods to get instances of this class.
        """
        if not isinstance(interface, libusb1.libusb_interface):
            raise TypeError('Unexpected descriptor type.')
        self._USBInterface__interface = interface
        self._USBInterface__context = context

    def getNumSettings(self):
        return self._USBInterface__interface.num_altsetting

    __len__ = getNumSettings

    def __iter__(self):
        """
        Iterates over settings in this insterface, yielding
        USBInterfaceSetting instances.
        """
        context = self._USBInterface__context
        alt_setting_list = self._USBInterface__interface.altsetting
        for alt_setting_num in xrange(self.getNumSettings()):
            yield USBInterfaceSetting(context, alt_setting_list[alt_setting_num])

    iterSettings = __iter__

    def __getitem__(self, alt_setting):
        """
        Returns an USBInterfaceSetting instance.
        """
        if not isinstance(alt_setting, int):
            raise TypeError('alt_setting parameter must be an integer')
        if not 0 <= alt_setting < self.getNumSettings():
            raise IndexError('No such setting: %r' % (alt_setting,))
        return USBInterfaceSetting(self._USBInterface__context, self._USBInterface__interface.altsetting[alt_setting])


class USBInterfaceSetting(object):

    def __init__(self, context, alt_setting):
        """
        You should not instanciate this class directly.
        Call USBDevice or USBInterface methods to get instances of this class.
        """
        if not isinstance(alt_setting, libusb1.libusb_interface_descriptor):
            raise TypeError('Unexpected descriptor type.')
        self._USBInterfaceSetting__alt_setting = alt_setting
        self._USBInterfaceSetting__context = context

    def getNumber(self):
        return self._USBInterfaceSetting__alt_setting.bInterfaceNumber

    def getAlternateSetting(self):
        return self._USBInterfaceSetting__alt_setting.bAlternateSetting

    def getNumEndpoints(self):
        return self._USBInterfaceSetting__alt_setting.bNumEndpoints

    __len__ = getNumEndpoints

    def getClass(self):
        return self._USBInterfaceSetting__alt_setting.bInterfaceClass

    def getSubClass(self):
        return self._USBInterfaceSetting__alt_setting.bInterfaceSubClass

    def getClassTuple(self):
        """
        For convenience: class and subclass are probably often matched
        simultaneously.
        """
        alt_setting = self._USBInterfaceSetting__alt_setting
        return (alt_setting.bInterfaceClass, alt_setting.bInterfaceSubClass)

    getClassTupple = getClassTuple

    def getProtocol(self):
        return self._USBInterfaceSetting__alt_setting.bInterfaceProtocol

    def getDescriptor(self):
        return self._USBInterfaceSetting__alt_setting.iInterface

    def getExtra(self):
        return libusb1.get_extra(self._USBInterfaceSetting__alt_setting)

    def __iter__(self):
        """
        Iterates over endpoints in this interface setting , yielding
        USBEndpoint instances.
        """
        context = self._USBInterfaceSetting__context
        endpoint_list = self._USBInterfaceSetting__alt_setting.endpoint
        for endpoint_num in xrange(self.getNumEndpoints()):
            yield USBEndpoint(context, endpoint_list[endpoint_num])

    iterEndpoints = __iter__

    def __getitem__(self, endpoint):
        """
        Returns an USBEndpoint instance.
        """
        if not isinstance(endpoint, int):
            raise TypeError('endpoint parameter must be an integer')
        if not 0 <= endpoint < self.getNumEndpoints():
            raise ValueError('No such endpoint: %r' % (endpoint,))
        return USBEndpoint(self._USBInterfaceSetting__context, self._USBInterfaceSetting__alt_setting.endpoint[endpoint])


class USBEndpoint(object):

    def __init__(self, context, endpoint):
        if not isinstance(endpoint, libusb1.libusb_endpoint_descriptor):
            raise TypeError('Unexpected descriptor type.')
        self._USBEndpoint__endpoint = endpoint
        self._USBEndpoint__context = context

    def getAddress(self):
        return self._USBEndpoint__endpoint.bEndpointAddress

    def getAttributes(self):
        return self._USBEndpoint__endpoint.bmAttributes

    def getMaxPacketSize(self):
        return self._USBEndpoint__endpoint.wMaxPacketSize

    def getInterval(self):
        return self._USBEndpoint__endpoint.bInterval

    def getRefresh(self):
        return self._USBEndpoint__endpoint.bRefresh

    def getSyncAddress(self):
        return self._USBEndpoint__endpoint.bSynchAddress

    def getExtra(self):
        return libusb1.get_extra(self._USBEndpoint__endpoint)


class USBDevice(object):
    __doc__ = '\n    Represents a USB device.\n    '
    _USBDevice__configuration_descriptor_list = ()
    _USBDevice__libusb_unref_device = libusb1.libusb_unref_device
    _USBDevice__libusb_free_config_descriptor = libusb1.libusb_free_config_descriptor
    _USBDevice__byref = byref

    def __init__(self, context, device_p, can_load_configuration=True):
        """
        You should not instanciate this class directly.
        Call USBContext methods to receive instances of this class.
        """
        self._USBDevice__context = context
        libusb1.libusb_ref_device(device_p)
        self.device_p = device_p
        device_descriptor = libusb1.libusb_device_descriptor()
        result = libusb1.libusb_get_device_descriptor(device_p, byref(device_descriptor))
        mayRaiseUSBError(result)
        self.device_descriptor = device_descriptor
        if can_load_configuration:
            self._USBDevice__configuration_descriptor_list = descriptor_list = []
            append = descriptor_list.append
            device_p = self.device_p
            for configuration_id in xrange(self.device_descriptor.bNumConfigurations):
                config = libusb1.libusb_config_descriptor_p()
                result = libusb1.libusb_get_config_descriptor(device_p, configuration_id, byref(config))
                if result == ERROR_NOT_FOUND:
                    continue
                mayRaiseUSBError(result)
                append(config.contents)

    def __del__(self):
        self._USBDevice__libusb_unref_device(self.device_p)
        byref = self._USBDevice__byref
        for config in self._USBDevice__configuration_descriptor_list:
            self._USBDevice__libusb_free_config_descriptor(byref(config))

    def __str__(self):
        return 'Bus %03i Device %03i: ID %04x:%04x' % (
         self.getBusNumber(),
         self.getDeviceAddress(),
         self.getVendorID(),
         self.getProductID())

    def __len__(self):
        return len(self._USBDevice__configuration_descriptor_list)

    def __getitem__(self, index):
        return USBConfiguration(self._USBDevice__context, self._USBDevice__configuration_descriptor_list[index])

    def __key(self):
        return (
         id(self._USBDevice__context), self.getBusNumber(),
         self.getDeviceAddress(), self.getVendorID(),
         self.getProductID())

    def __hash__(self):
        return hash(self._USBDevice__key())

    def __eq__(self, other):
        return type(self) == type(other) and (self.device_p == other.device_p or self._USBDevice__key() == other._USBDevice__key())

    def iterConfigurations(self):
        context = self._USBDevice__context
        for config in self._USBDevice__configuration_descriptor_list:
            yield USBConfiguration(context, config)

    iterConfiguations = iterConfigurations

    def iterSettings(self):
        for config in self.iterConfigurations():
            for interface in config:
                for setting in interface:
                    yield setting

    def getBusNumber(self):
        """
        Get device's bus number.
        """
        return libusb1.libusb_get_bus_number(self.device_p)

    def getPortNumber(self):
        """
        Get device's port number.
        """
        return libusb1.libusb_get_port_number(self.device_p)

    def getPortNumberList(self):
        """
        Get the port number of each hub toward device.
        """
        port_list = (c_uint8 * PATH_MAX_DEPTH)()
        result = libusb1.libusb_get_port_numbers(self.device_p, port_list, len(port_list))
        mayRaiseUSBError(result)
        return list(port_list[:result])

    def getDeviceAddress(self):
        """
        Get device's address on its bus.
        """
        return libusb1.libusb_get_device_address(self.device_p)

    def getbcdUSB(self):
        """
        Get the USB spec version device complies to, in BCD format.
        """
        return self.device_descriptor.bcdUSB

    def getDeviceClass(self):
        """
        Get device's class id.
        """
        return self.device_descriptor.bDeviceClass

    def getDeviceSubClass(self):
        """
        Get device's subclass id.
        """
        return self.device_descriptor.bDeviceSubClass

    def getDeviceProtocol(self):
        """
        Get device's protocol id.
        """
        return self.device_descriptor.bDeviceProtocol

    def getMaxPacketSize0(self):
        """
        Get device's max packet size for endpoint 0 (control).
        """
        return self.device_descriptor.bMaxPacketSize0

    def getMaxPacketSize(self, endpoint):
        """
        Get device's max packet size for given endpoint.

        Warning: this function will not always give you the expected result.
        See https://libusb.org/ticket/77 . You should instead consult the
        endpoint descriptor of current configuration and alternate setting.
        """
        result = libusb1.libusb_get_max_packet_size(self.device_p, endpoint)
        mayRaiseUSBError(result)
        return result

    def getMaxISOPacketSize(self, endpoint):
        """
        Get the maximum size for a single isochronous packet for given
        endpoint.

        Warning: this function will not always give you the expected result.
        See https://libusb.org/ticket/77 . You should instead consult the
        endpoint descriptor of current configuration and alternate setting.
        """
        result = libusb1.libusb_get_max_iso_packet_size(self.device_p, endpoint)
        mayRaiseUSBError(result)
        return result

    def getVendorID(self):
        """
        Get device's vendor id.
        """
        return self.device_descriptor.idVendor

    def getProductID(self):
        """
        Get device's product id.
        """
        return self.device_descriptor.idProduct

    def getbcdDevice(self):
        """
        Get device's release number.
        """
        return self.device_descriptor.bcdDevice

    def getSupportedLanguageList(self):
        """
        Get the list of language ids device has string descriptors for.
        """
        temp_handle = self.open()
        return temp_handle.getSupportedLanguageList()

    def _getStringDescriptor(self, descriptor, lang_id):
        if descriptor == 0:
            result = None
        else:
            temp_handle = self.open()
            result = temp_handle.getStringDescriptor(descriptor, lang_id)
        return result

    def _getASCIIStringDescriptor(self, descriptor):
        if descriptor == 0:
            result = None
        else:
            temp_handle = self.open()
            result = temp_handle.getASCIIStringDescriptor(descriptor)
        return result

    def getManufacturer(self):
        """
        Get device's manufaturer name.
        Note: opens the device temporarily.
        """
        return self._getASCIIStringDescriptor(self.device_descriptor.iManufacturer)

    def getProduct(self):
        """
        Get device's product name.
        Note: opens the device temporarily.
        """
        return self._getASCIIStringDescriptor(self.device_descriptor.iProduct)

    def getSerialNumber(self):
        """
        Get device's serial number.
        Note: opens the device temporarily.
        """
        return self._getASCIIStringDescriptor(self.device_descriptor.iSerialNumber)

    def getNumConfigurations(self):
        """
        Get device's number of possible configurations.
        """
        return self.device_descriptor.bNumConfigurations

    def getDeviceSpeed(self):
        """
        Get device's speed.

        Returns one of:
            SPEED_UNKNOWN
            SPEED_LOW
            SPEED_FULL
            SPEED_HIGH
            SPEED_SUPER
        """
        return libusb1.libusb_get_device_speed(self.device_p)

    def open(self):
        """
        Open device.
        Returns an USBDeviceHandle instance.
        """
        handle = libusb1.libusb_device_handle_p()
        result = libusb1.libusb_open(self.device_p, byref(handle))
        mayRaiseUSBError(result)
        return USBDeviceHandle(self._USBDevice__context, handle, self)


_zero_tv = libusb1.timeval(0, 0)
_zero_tv_p = byref(_zero_tv)

class USBContext(object):
    __doc__ = '\n    libusb1 USB context.\n\n    Provides methods to enumerate & look up USB devices.\n    Also provides access to global (device-independent) libusb1 functions.\n    '
    _USBContext__libusb_exit = libusb1.libusb_exit
    _USBContext__context_p = None
    _USBContext__added_cb = None
    _USBContext__removed_cb = None
    _USBContext__libusb_set_pollfd_notifiers = libusb1.libusb_set_pollfd_notifiers

    def _validContext(func):

        @functools.wraps(func)
        def wrapper(self, *args, **kw):
            self._USBContext__context_cond.acquire()
            self._USBContext__context_refcount += 1
            self._USBContext__context_cond.release()
            try:
                if self._USBContext__context_p is not None:
                    return func(self, *args, **kw)
            finally:
                self._USBContext__context_cond.acquire()
                self._USBContext__context_refcount -= 1
                if not self._USBContext__context_refcount:
                    self._USBContext__context_cond.notifyAll()
                self._USBContext__context_cond.release()

        return wrapper

    def __init__(self):
        """
        Create a new USB context.
        """
        self._USBContext__context_refcount = 0
        self._USBContext__context_cond = threading.Condition()
        context_p = libusb1.libusb_context_p()
        result = libusb1.libusb_init(byref(context_p))
        mayRaiseUSBError(result)
        self._USBContext__context_p = context_p
        self._USBContext__hotplug_callback_dict = {}

    def __del__(self):
        self._exit()

    def exit(self):
        """
        Close (destroy) this USB context.

        When this method has been called, methods on its instance will
        become mosty no-ops, returning None.
        """
        self._USBContext__context_cond.acquire()
        try:
            while self._USBContext__context_refcount and self._USBContext__context_p is not None:
                self._USBContext__context_cond.wait()

            self._exit()
        finally:
            self._USBContext__context_cond.notifyAll()
            self._USBContext__context_cond.release()

    def _exit(self):
        context_p = self._USBContext__context_p
        if context_p is not None:
            self._USBContext__libusb_exit(context_p)
            self._USBContext__context_p = None
            self._USBContext__added_cb = None
            self._USBContext__removed_cb = None

    @_validContext
    def getDeviceList(self, skip_on_access_error=False, skip_on_error=False):
        """
        Return a list of all USB devices currently plugged in, as USBDevice
        instances.

        skip_on_error (bool)
            If True, ignore devices which raise USBError.

        skip_on_access_error (bool)
            DEPRECATED. Alias for skip_on_error.
        """
        skip_on_error = skip_on_error or skip_on_access_error
        device_p_p = libusb1.libusb_device_p_p()
        libusb_device_p = libusb1.libusb_device_p
        device_list_len = libusb1.libusb_get_device_list(self._USBContext__context_p, byref(device_p_p))
        mayRaiseUSBError(device_list_len)
        try:
            result = []
            append = result.append
            for device_p in device_p_p[:device_list_len]:
                try:
                    device = USBDevice(self, libusb_device_p(device_p.contents))
                except USBError:
                    if not skip_on_error:
                        raise
                else:
                    append(device)

        finally:
            libusb1.libusb_free_device_list(device_p_p, 1)

        return result

    def getByVendorIDAndProductID(self, vendor_id, product_id, skip_on_access_error=False, skip_on_error=False):
        """
        Get the first USB device matching given vendor and product ids.
        Returns an USBDevice instance, or None if no present device match.
        skip_on_error (bool)
            (see getDeviceList)
        skip_on_access_error (bool)
            (see getDeviceList)
        """
        for device in self.getDeviceList(skip_on_access_error=skip_on_access_error,
          skip_on_error=skip_on_error):
            if device.getVendorID() == vendor_id and device.getProductID() == product_id:
                return device

    def openByVendorIDAndProductID(self, vendor_id, product_id, skip_on_access_error=False, skip_on_error=False):
        """
        Get the first USB device matching given vendor and product ids.
        Returns an USBDeviceHandle instance, or None if no present device
        match.
        skip_on_error (bool)
            (see getDeviceList)
        skip_on_access_error (bool)
            (see getDeviceList)
        """
        result = self.getByVendorIDAndProductID(vendor_id,
          product_id, skip_on_access_error=skip_on_access_error,
          skip_on_error=skip_on_error)
        if result is not None:
            return result.open()

    @_validContext
    def getPollFDList(self):
        """
        Return file descriptors to be used to poll USB events.
        You should not have to call this method, unless you are integrating
        this class with a polling mechanism.
        """
        pollfd_p_p = libusb1.libusb_get_pollfds(self._USBContext__context_p)
        if not pollfd_p_p:
            errno = get_errno()
            if errno:
                raise OSError(errno)
            else:
                raise NotImplementedError('Your libusb does not seem to implement pollable FDs')
        try:
            result = []
            append = result.append
            fd_index = 0
            while pollfd_p_p[fd_index]:
                append((
                 pollfd_p_p[fd_index].contents.fd,
                 pollfd_p_p[fd_index].contents.events))
                fd_index += 1

        finally:
            _free(pollfd_p_p)

        return result

    @_validContext
    def handleEvents(self):
        """
        Handle any pending event (blocking).
        See libusb1 documentation for details (there is a timeout, so it's
        not "really" blocking).
        """
        result = libusb1.libusb_handle_events(self._USBContext__context_p)
        mayRaiseUSBError(result)

    @_validContext
    def handleEventsTimeout(self, tv=0):
        """
        Handle any pending event.
        If tv is 0, will return immediately after handling already-pending
        events.
        Otherwise, defines the maximum amount of time to wait for events, in
        seconds.
        """
        if tv is None:
            tv = 0
        tv_s = int(tv)
        tv = libusb1.timeval(tv_s, int((tv - tv_s) * 1000000))
        result = libusb1.libusb_handle_events_timeout(self._USBContext__context_p, byref(tv))
        mayRaiseUSBError(result)

    @_validContext
    def setPollFDNotifiers(self, added_cb=None, removed_cb=None, user_data=None):
        """
        Give libusb1 methods to call when it should add/remove file descriptor
        for polling.
        You should not have to call this method, unless you are integrating
        this class with a polling mechanism.
        """
        if added_cb is None:
            added_cb = POINTER(None)
        else:
            added_cb = libusb1.libusb_pollfd_added_cb_p(added_cb)
        if removed_cb is None:
            removed_cb = POINTER(None)
        else:
            removed_cb = libusb1.libusb_pollfd_removed_cb_p(removed_cb)
        self._USBContext__added_cb = added_cb
        self._USBContext__removed_cb = removed_cb
        self._USBContext__libusb_set_pollfd_notifiers(self._USBContext__context_p, added_cb, removed_cb, user_data)

    @_validContext
    def getNextTimeout(self):
        """
        Returns the next internal timeout that libusb needs to handle, in
        seconds, or None if no timeout is needed.
        You should not have to call this method, unless you are integrating
        this class with a polling mechanism.
        """
        timeval = libusb1.timeval()
        result = libusb1.libusb_get_next_timeout(self._USBContext__context_p, byref(timeval))
        if result == 0:
            return
        if result == 1:
            return timeval.tv_sec + timeval.tv_usec * 1e-06
        raiseUSBError(result)

    @_validContext
    def setDebug(self, level):
        """
        Set debugging level.
        Note: depending on libusb compilation settings, this might have no
        effect.
        """
        libusb1.libusb_set_debug(self._USBContext__context_p, level)

    @_validContext
    def tryLockEvents(self):
        """
        See libusb_try_lock_events doc.
        """
        return libusb1.libusb_try_lock_events(self._USBContext__context_p)

    @_validContext
    def lockEvents(self):
        """
        See libusb_lock_events doc.
        """
        libusb1.libusb_lock_events(self._USBContext__context_p)

    @_validContext
    def lockEventWaiters(self):
        """
        See libusb_lock_event_waiters doc.
        """
        libusb1.libusb_lock_event_waiters(self._USBContext__context_p)

    @_validContext
    def waitForEvent(self, tv=0):
        """
        See libusb_wait_for_event doc.
        """
        if tv is None:
            tv = 0
        tv_s = int(tv)
        tv = libusb1.timeval(tv_s, int((tv - tv_s) * 1000000))
        libusb1.libusb_wait_for_event(self._USBContext__context_p, byref(tv))

    @_validContext
    def unlockEventWaiters(self):
        """
        See libusb_unlock_event_waiters doc.
        """
        libusb1.libusb_unlock_event_waiters(self._USBContext__context_p)

    @_validContext
    def eventHandlingOK(self):
        """
        See libusb_event_handling_ok doc.
        """
        return libusb1.libusb_event_handling_ok(self._USBContext__context_p)

    @_validContext
    def unlockEvents(self):
        """
        See libusb_unlock_events doc.
        """
        libusb1.libusb_unlock_events(self._USBContext__context_p)

    @_validContext
    def handleEventsLocked(self):
        """
        See libusb_handle_events_locked doc.
        """
        result = libusb1.libusb_handle_events_locked(self._USBContext__context_p, _zero_tv_p)
        mayRaiseUSBError(result)

    @_validContext
    def eventHandlerActive(self):
        """
        See libusb_event_handler_active doc.
        """
        return libusb1.libusb_event_handler_active(self._USBContext__context_p)

    @staticmethod
    def hasCapability(capability):
        """
        Backward-compatibility alias for module-level hasCapability.
        """
        return hasCapability(capability)

    @_validContext
    def hotplugRegisterCallback(self, callback, events=HOTPLUG_EVENT_DEVICE_ARRIVED | HOTPLUG_EVENT_DEVICE_LEFT, flags=HOTPLUG_ENUMERATE, vendor_id=HOTPLUG_MATCH_ANY, product_id=HOTPLUG_MATCH_ANY, dev_class=HOTPLUG_MATCH_ANY):
        """
        Registers an hotplug callback.
        On success, returns an opaque value which can be passed to
        hotplugDeregisterCallback.
        Callback must accept the following positional arguments:
        - this USBContext instance
        - an USBDevice instance
          If device has left, configuration descriptors may not be
          available. Its device descriptor will be available.
        - event type, one of:
            HOTPLUG_EVENT_DEVICE_ARRIVED
            HOTPLUG_EVENT_DEVICE_LEFT
        Callback must return whether it must be unregistered (any true value
        to be unregistered, any false value to be kept registered).
        """

        def wrapped_callback(context_p, device_p, event, _):
            assert addressof(context_p.contents) == addressof(self._USBContext__context_p.contents), (context_p, self._USBContext__context_p)
            unregister = bool(callback(self, USBDevice(self, device_p, event != HOTPLUG_EVENT_DEVICE_LEFT), event))
            if unregister:
                del self._USBContext__hotplug_callback_dict[handle]
            return unregister

        handle = c_int()
        callback_p = libusb1.libusb_hotplug_callback_fn_p(wrapped_callback)
        result = libusb1.libusb_hotplug_register_callback(self._USBContext__context_p, events, flags, vendor_id, product_id, dev_class, callback_p, None, byref(handle))
        mayRaiseUSBError(result)
        handle = handle.value
        assert handle not in self._USBContext__hotplug_callback_dict, (
         handle,
         self._USBContext__hotplug_callback_dict)
        self._USBContext__hotplug_callback_dict[handle] = (
         callback_p, wrapped_callback)
        return handle

    @_validContext
    def hotplugDeregisterCallback(self, handle):
        """
        Deregisters an hotplug callback.
        handle (opaque)
            Return value of a former hotplugRegisterCallback call.
        """
        del self._USBContext__hotplug_callback_dict[handle]
        libusb1.libusb_hotplug_deregister_callback(self._USBContext__context_p, handle)


del USBContext._validContext

def getVersion():
    """
    Returns underlying libusb's version information as a 6-namedtuple (or
    6-tuple if namedtuples are not avaiable):
    - major
    - minor
    - micro
    - nano
    - rc
    - describe
    Returns (0, 0, 0, 0, '', '') if libusb doesn't have required entry point.
    """
    version = libusb1.libusb_get_version().contents
    return Version(version.major, version.minor, version.micro, version.nano, version.rc, version.describe)


def hasCapability(capability):
    """
    Tests feature presence.

    capability should be one of:
        CAP_HAS_CAPABILITY
        CAP_HAS_HOTPLUG
        CAP_HAS_HID_ACCESS
        CAP_SUPPORTS_DETACH_KERNEL_DRIVER
    """
    return libusb1.libusb_has_capability(capability)


class LibUSBContext(USBContext):
    __doc__ = '\n    Backward-compatibility alias for USBContext.\n    '

    def __init__(self):
        warnings.warn('LibUSBContext is being renamed to USBContext', DeprecationWarning)
        super(LibUSBContext, self).__init__()