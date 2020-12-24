# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/hid/osx.py
# Compiled at: 2010-09-10 09:00:00
"""
The OS X HID interface module.
Dynamically loaded on OS X.
Refer to the hid module for available functions
"""
from ctypes import *
from ctypes.util import find_library
import logging, struct
from hid import HIDDevice
from hid.cparser import define, parse
mach_port_t = define('mach_port_t', 'void*')
io_object_t = define('io_object_t', 'void*')
io_iterator_t = define('io_iterator_t', 'void*')
io_service_t = define('io_service_t', 'void*')
io_registry_entry_t = define('io_registry_entry_t', io_object_t)
LPVOID = define('LPVOID', 'void*')
Boolean = define('Boolean', c_ubyte)
UInt8 = define('UInt8', c_uint8)
UInt16 = define('UInt16', c_uint16)
SInt32 = define('SInt32', c_int32)
UInt32 = define('UInt32', c_uint32)
uint32_t = define('uint32_t', c_uint32)
UInt64 = define('UInt64', c_uint64)
ULONG = define('ULONG', c_ulong)
IOReturn = define('IOReturn', c_int)
IOOptionBits = define('IOOptionBits', 'UInt32')
kern_return_t = define('kern_return_t', c_int)
CFDictionaryRef = define('CFDictionaryRef', 'void*')
CFArrayRef = define('CFArrayRef', 'void*')
AbsoluteTime = define('AbsoluteTime', 'UInt64')
CFTimeInterval = define('CFTimeInterval', 'double')
CFTypeRef = define('CFTypeRef', 'void*')
define('__CFString', 'void*')
CFStringRef = define('CFStringRef', '__CFString*')
define('__CFAllocator', 'void*')
CFAllocatorRef = define('CFAllocatorRef', '__CFAllocator*')
CFStringEncoding = define('CFStringEncoding', 'UInt32')
define('__CFNumber', 'void*')
CFNumberRef = define('CFNumberRef', '__CFNumber*')
CFNumberType = define('CFNumberType', c_int)
define('__CFUUID', 'void*')
CFUUIDRef = define('CFUUIDRef', '__CFUUID*')
define('__CFRunLoop', 'void*')
CFRunLoopRef = define('CFRunLoopRef', '__CFRunLoop*')
define('__CFRunLoopSource', 'void*')
CFRunLoopSourceRef = CFRunLoopSourceRef = define('CFRunLoopSourceRef', '__CFRunLoopSource*')
define('__CFDictionary', 'void*')
CFMutableDictionaryRef = define('CFMutableDictionaryRef', '__CFDictionary*')

class CFUUIDBytes(Structure):
    _fields_ = [
     (
      'bytes0_15', c_ubyte * 16)]


define('CFUUIDBytes', CFUUIDBytes)
REFIID = define('REFIID', 'CFUUIDBytes')
IOHIDElementCookie = define('IOHIDElementCookie', 'void*')
IOHIDElementType = define('IOHIDElementType', c_int)
IOHIDQueueInterface = define('IOHIDQueueInterface', 'void*')
IOHIDOutputTransactionInterface = define('IOHIDOutputTransactionInterface', 'void*')
IOHIDReportType = define('IOHIDReportType', c_int)
HRESULT = define('HRESULT', 'SInt32')
IOHIDCallbackFunction = parse('void (*IOHIDCallbackFunction)(void *target, IOReturn result, void *refcon, void *sender)').ctype
define('IOHIDCallbackFunction', IOHIDCallbackFunction)
IOHIDElementCallbackFunction = parse('void (*IOHIDElementCallbackFunction)(void *target, IOReturn result, void *refcon, void *sender, IOHIDElementCookie elementCookie)').ctype
define('IOHIDElementCallbackFunction', IOHIDElementCallbackFunction)
IOHIDReportCallbackFunction = parse('void ( *IOHIDReportCallbackFunction) ( void *target, IOReturn result, void *refcon, void *sender, uint32_t bufferSize)').ctype
define('IOHIDReportCallbackFunction', IOHIDReportCallbackFunction)

class IOHIDEventStruct(Structure):
    _fields_ = [
     parse('IOHIDElementType type').cstruct,
     parse('IOHIDElementCookie elementCookie').cstruct,
     parse('SInt32 value').cstruct,
     parse('AbsoluteTime timestamp').cstruct,
     parse('UInt32 longValueSize').cstruct,
     parse('void * longValue').cstruct]


define('IOHIDEventStruct', IOHIDEventStruct)
kIOHIDReportTypeInput = 0
kIOHIDReportTypeOutput = 1
kIOHIDReportTypeFeature = 2
kIOHIDReportTypeCount = 3
IUNKNOWN_C_GUTS = [
 parse('void *_reserved').cstruct,
 parse('HRESULT (*QueryInterface)(void *thisPointer, REFIID iid, LPVOID *ppv)').cstruct,
 parse('ULONG (*AddRef)(void *thisPointer)').cstruct,
 parse('ULONG (*Release)(void *thisPointer)').cstruct]
IOCFPLUGINBASE = [
 parse('UInt16 version').cstruct,
 parse('UInt16 revision').cstruct,
 parse('IOReturn (*Probe)(void *thisPointer, CFDictionaryRef propertyTable,io_service_t service, SInt32 * order)').cstruct,
 parse('IOReturn (*Start)(void *thisPointer, CFDictionaryRef propertyTable,io_service_t service)').cstruct,
 parse('IOReturn (*Stop)(void *thisPointer)').cstruct]
IOHIDDEVICEINTERFACE_FUNCS_100 = [
 parse('IOReturn (*createAsyncEventSource)(void * self, CFRunLoopSourceRef * source)').cstruct,
 parse('CFRunLoopSourceRef (*getAsyncEventSource)(void * self)').cstruct,
 parse('IOReturn (*createAsyncPort)(void * self, mach_port_t * port)').cstruct,
 parse('mach_port_t (*getAsyncPort)(void * self)').cstruct,
 parse('IOReturn (*open)(void * self, UInt32 flags)').cstruct,
 parse('IOReturn (*close)(void * self)').cstruct,
 parse('IOReturn (*setRemovalCallback)(void * self, IOHIDCallbackFunction removalCallback,void * removalTarget, void * removalRefcon)').cstruct,
 parse('IOReturn (*getElementValue)(void * self, IOHIDElementCookie\telementCookie,IOHIDEventStruct * valueEvent)').cstruct,
 parse('IOReturn (*setElementValue)(void * self, IOHIDElementCookie elementCookie,IOHIDEventStruct * valueEvent, UInt32 timeoutMS,IOHIDElementCallbackFunction callback,void * callbackTarget, void * callbackRefcon)').cstruct,
 parse('IOReturn (*queryElementValue)(void * self, IOHIDElementCookie elementCookie,IOHIDEventStruct * valueEvent, UInt32 timeoutMS,IOHIDElementCallbackFunction callback,void * callbackTarget, void * callbackRefcon)').cstruct,
 parse('IOReturn (*startAllQueues)(void * self)').cstruct,
 parse('IOReturn (*stopAllQueues)(void * self)').cstruct,
 parse('IOHIDQueueInterface ** (*allocQueue) (void *self)').cstruct,
 parse('IOHIDOutputTransactionInterface ** (*allocOutputTransaction) (void *self)').cstruct]
IOHIDDEVICEINTERFACE_FUNCS_121 = [
 parse('IOReturn (*setReport)(void * self, IOHIDReportType reportType, UInt32 reportID,void * reportBuffer, UInt32 reportBufferSize,UInt32 timeoutMS, IOHIDReportCallbackFunction callback,void * callbackTarget, void * callbackRefcon)').cstruct,
 parse('IOReturn (*getReport)(void * self, IOHIDReportType reportType,UInt32 reportID, void * reportBuffer,UInt32 * reportBufferSize, UInt32 timeoutMS,IOHIDReportCallbackFunction callback,void * callbackTarget, void * callbackRefcon)').cstruct]
IOHIDDEVICEINTERFACE_FUNCS_122 = [
 parse('IOReturn (*copyMatchingElements)(void * self, CFDictionaryRef matchingDict,CFArrayRef * elements)').cstruct,
 parse('IOReturn (*setInterruptReportHandlerCallback)(void * self, void * reportBuffer,UInt32 reportBufferSize,IOHIDReportCallbackFunction callback,void * callbackTarget, void * callbackRefcon)').cstruct]

class IOCFPlugInInterfaceStruct(Structure):
    _fields_ = IUNKNOWN_C_GUTS + IOCFPLUGINBASE


define('IOCFPlugInInterface', IOCFPlugInInterfaceStruct)

class IOHIDDeviceInterface122(Structure):
    _fields_ = IUNKNOWN_C_GUTS + IOHIDDEVICEINTERFACE_FUNCS_100 + IOHIDDEVICEINTERFACE_FUNCS_121 + IOHIDDEVICEINTERFACE_FUNCS_122


class COMObjectRef:

    def __init__(self, ref):
        self.ref = ref
        logging.info('created: %s', self)

    def __del__(self):
        logging.info('releasing: %s', self)
        self.Release()

    def __nonzero__(self):
        return self.ref is not None

    def __str__(self):
        return 'COMObjectRef(%s)' % self.ref

    def __getattr__(self, name):
        """
        return a function on the com object
        (takes care of passing in the ref as the first arg)
        """
        fn = getattr(self.ref.contents.contents, name)
        return lambda *arg: fn(self.ref, *arg)


KERN_SUCCESS = 0
kIOReturnSuccess = 0
kIOHIDDeviceKey = 'IOHIDDevice'
kIOHIDVendorIDKey = 'VendorID'
kIOHIDProductIDKey = 'ProductID'
kIOMasterPortDefault = None
kCFAllocatorDefault = None
kCFStringEncodingASCII = 1536
kCFNumberIntType = 9
kNilOptions = 0
cfLibraryLocation = find_library('CoreFoundation')
logging.info('loading CoreFoundation from: %s', cfLibraryLocation)
cf = CDLL(cfLibraryLocation)
CFDictionaryGetValue = parse('void *CFDictionaryGetValue(CFDictionaryRef theDict, void *key)').from_lib(cf)
CFStringCreateWithCString = parse('CFStringRef CFStringCreateWithCString(CFAllocatorRef alloc, char *cStr, CFStringEncoding encoding)').from_lib(cf)
CFNumberGetValue = parse('Boolean CFNumberGetValue(CFNumberRef number, CFNumberType theType, void *valuePtr)').from_lib(cf)
CFRelease = parse('void CFRelease (CFTypeRef cf)').from_lib(cf)
CFUUIDGetConstantUUIDWithBytes = parse('CFUUIDRef CFUUIDGetConstantUUIDWithBytes(CFAllocatorRef alloc, UInt8 byte0, UInt8 byte1, UInt8 byte2, UInt8 byte3, UInt8 byte4, UInt8 byte5, UInt8 byte6, UInt8 byte7, UInt8 byte8, UInt8 byte9, UInt8 byte10, UInt8 byte11, UInt8 byte12, UInt8 byte13, UInt8 byte14, UInt8 byte15)').from_lib(cf)
CFUUIDGetUUIDBytes = parse('CFUUIDBytes CFUUIDGetUUIDBytes(CFUUIDRef uuid)').from_lib(cf)
CFRunLoopAddSource = parse('void CFRunLoopAddSource(CFRunLoopRef rl, CFRunLoopSourceRef source, CFStringRef mode)').from_lib(cf)
CFRunLoopGetCurrent = parse('CFRunLoopRef CFRunLoopGetCurrent()').from_lib(cf)
CFRunLoopRunInMode = parse('SInt32 CFRunLoopRunInMode(CFStringRef mode, CFTimeInterval seconds, Boolean returnAfterSourceHandled)').from_lib(cf)

def CFSTR(cstr):
    return CFStringCreateWithCString(kCFAllocatorDefault, cstr, kCFStringEncodingASCII)


kCFRunLoopDefaultMode = CFStringRef.in_dll(cf, 'kCFRunLoopDefaultMode')
iokitLibraryLocation = find_library('IOKit')
logging.info('loading IOKit from: %s', iokitLibraryLocation)
iokit = CDLL(iokitLibraryLocation)
IOIteratorNext = parse('io_object_t IOIteratorNext(io_iterator_t iterator )').from_lib(iokit)
IOObjectRelease = parse('kern_return_t IOObjectRelease(io_object_t object)').from_lib(iokit)
IOServiceMatching = parse('CFMutableDictionaryRef IOServiceMatching(char* name )').from_lib(iokit)
IOServiceGetMatchingServices = parse('kern_return_t IOServiceGetMatchingServices(mach_port_t masterPort,CFDictionaryRef matching, io_iterator_t * existing )').from_lib(iokit)
IOCreatePlugInInterfaceForService = parse('kern_return_t IOCreatePlugInInterfaceForService(io_service_t service,CFUUIDRef pluginType, CFUUIDRef interfaceType,IOCFPlugInInterface *** theInterface, SInt32 * theScore)').from_lib(iokit)
IORegistryEntryCreateCFProperties = parse('kern_return_t IORegistryEntryCreateCFProperties(io_registry_entry_t entry,CFMutableDictionaryRef * properties,CFAllocatorRef allocator,IOOptionBits options )').from_lib(iokit)
kIOHIDDeviceUserClientTypeID = CFUUIDGetConstantUUIDWithBytes(None, 250, 18, 250, 56, 111, 26, 17, 212, 186, 12, 0, 5, 2, 143, 24, 213)
kIOCFPlugInInterfaceID = CFUUIDGetConstantUUIDWithBytes(None, 194, 68, 232, 88, 16, 156, 17, 212, 145, 212, 0, 80, 228, 198, 66, 111)
kIOHIDDeviceInterfaceID = CFUUIDGetConstantUUIDWithBytes(None, 120, 189, 66, 12, 111, 20, 17, 212, 148, 116, 0, 5, 2, 143, 24, 213)

def find_hid_devices():
    """
    query the host computer for all available USB *HID* devices
    and returns a list of any found
    """
    return find_usb_devices(kIOHIDDeviceKey, kIOHIDVendorIDKey, kIOHIDProductIDKey, OSXHIDDevice)


def find_usb_devices(device_key, vendor_id_key, product_id_key, device_class):
    """
    query the host computer for all available USB devices
    and returns a list of any found
    """
    devices = []
    matchDictionary = IOServiceMatching(device_key)
    objectIterator = io_iterator_t()
    result = IOServiceGetMatchingServices(kIOMasterPortDefault, matchDictionary, byref(objectIterator))
    if result != kIOReturnSuccess or not objectIterator:
        raise RuntimeError("Can't obtain an IO iterator")
    try:
        while True:
            device = IOIteratorNext(objectIterator)
            if not device:
                break
            dev = device_class(device, 0, 0)
            properties = CFMutableDictionaryRef()
            result = IORegistryEntryCreateCFProperties(device, byref(properties), kCFAllocatorDefault, kNilOptions)
            if result == KERN_SUCCESS and properties:
                (vendor, product) = (0, 0)
                vendorRef = CFDictionaryGetValue(properties, CFSTR(vendor_id_key))
                productRef = CFDictionaryGetValue(properties, CFSTR(product_id_key))
                if vendorRef:
                    vendor = c_int()
                    CFNumberGetValue(parse('CFNumberRef').cast(vendorRef), kCFNumberIntType, byref(vendor))
                    CFRelease(vendorRef)
                    vendor = vendor.value
                if productRef:
                    product = c_int()
                    CFNumberGetValue(parse('CFNumberRef').cast(productRef), kCFNumberIntType, byref(product))
                    CFRelease(productRef)
                    product = product.value
                dev.vendor = vendor
                dev.product = product
            logging.info('find_usb_devices: found device vendor=0x%04x product=0x%04x', dev.vendor, dev.product)
            devices.append(dev)

    finally:
        IOObjectRelease(objectIterator)

    return devices


class OSXHIDDevice(HIDDevice):
    """
    class representing a HID device on the host (OS X) computer
    """

    def __init__(self, hidDevice, vendor, product):
        """
        create the hid device wrapper
        hidDevice is a handle from the OS
        """
        HIDDevice.__init__(self, vendor, product)
        self.IOObjectRelease = IOObjectRelease
        self._hidDevice = hidDevice
        self._hidInterface = None
        return

    def __del__(self):
        HIDDevice.__del__(self)
        if self._hidDevice:
            logging.info('releasing HID device: %s' % self)
            self.IOObjectRelease(self._hidDevice)

    def close(self):
        if self._hidInterface:
            self._hidInterface = None
        HIDDevice.close(self)
        return

    def is_open(self):
        """
        see if the device is open
        """
        return self._hidInterface is not None

    def open(self):
        """
        open the HID device - must be called prior to registering callbacks
        or setting reports
        """
        if not self.is_open():
            logging.info('opening hid device')
            plugInInterface = COMObjectRef(POINTER(POINTER(IOCFPlugInInterfaceStruct))())
            score = SInt32()
            IOCreatePlugInInterfaceForService(self._hidDevice, kIOHIDDeviceUserClientTypeID, kIOCFPlugInInterfaceID, byref(plugInInterface.ref), byref(score))
            hidInterface = POINTER(POINTER(IOHIDDeviceInterface122))()
            plugInInterface.QueryInterface(CFUUIDGetUUIDBytes(kIOHIDDeviceInterfaceID), parse('LPVOID*').cast(byref(hidInterface)))
            self._hidInterface = COMObjectRef(hidInterface)
            self._hidInterface.open(0)
        else:
            loggging.info('device already open')

    def set_report(self, report_data, report_id=0):
        """
        "set" a report - send the data to the device (which must have been opened previously)
        """
        HIDDevice.set_report(self, report_data, report_id)
        report_buffer = (c_ubyte * len(report_data))()
        for (i, c) in enumerate(report_data):
            report_buffer[i] = struct.unpack('B', c)[0]

        self._hidInterface.setReport(kIOHIDReportTypeOutput, report_id, report_buffer, len(report_buffer), 100, IOHIDReportCallbackFunction(), None, None)
        return

    def _run_interrupt_callback_loop(self, report_buffer_size):
        """
        run on a thread to handle reading events from the device
        """
        if not self.is_open():
            raise RuntimeError('device not open')
        logging.info('starting _run_interrupt_callback_loop')
        report_buffer = (c_ubyte * report_buffer_size)()

        def callback(target, result, refcon, sender, size):
            if self._callback is not None:
                report_data = ('').join([ struct.pack('B', b) for b in report_buffer ])
                for i in range(len(report_buffer)):
                    report_buffer[i] = 0

                logging.info('interrupt_report_callback(%r)', report_data)
                self._callback(self, report_data)
            return

        hid_callback = IOHIDReportCallbackFunction(callback)
        port = mach_port_t()
        self._hidInterface.createAsyncPort(byref(port))
        eventSource = CFRunLoopSourceRef()
        self._hidInterface.createAsyncEventSource(byref(eventSource))
        self._hidInterface.setInterruptReportHandlerCallback(byref(report_buffer), len(report_buffer), hid_callback, None, None)
        self._hidInterface.startAllQueues()
        CFRunLoopAddSource(CFRunLoopGetCurrent(), eventSource, kCFRunLoopDefaultMode)
        logging.info('running CFRunLoopRunInMode')
        while self._running and self.is_open():
            CFRunLoopRunInMode(kCFRunLoopDefaultMode, 0.1, False)

        return


__all__ = [
 'find_hid_devices', 'OSXHIDDevice']