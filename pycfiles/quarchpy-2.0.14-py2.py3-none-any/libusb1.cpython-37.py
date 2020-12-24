# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\connection_specific\usb_libs\libusb1.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 50528 bytes
"""
Python ctypes bindings for libusb-1.0.

You should not need to import this if you use usb1 module.

Declares all constants, data structures and exported symbols.
Locates and loads libusb1 dynamic library.
"""
from ctypes import Structure, LittleEndianStructure, CFUNCTYPE, POINTER, addressof, sizeof, cast, c_short, c_int, c_uint, c_size_t, c_long, c_uint8, c_uint16, c_uint32, c_void_p, c_char_p, py_object, pointer, c_char
try:
    from ctypes import c_ssize_t
except ImportError:
    from ctypes import c_longlong
    if sizeof(c_int) == sizeof(c_size_t):
        c_ssize_t = c_int
    else:
        if sizeof(c_long) == sizeof(c_size_t):
            c_ssize_t = c_long
        else:
            if sizeof(c_longlong) == sizeof(c_size_t):
                c_ssize_t = c_longlong
            else:
                raise ValueError('Unsupported arch: sizeof(c_size_t) = %r' % (
                 sizeof(c_size_t),))

import ctypes.util, platform, os.path, sys

class Enum(object):

    def __init__(self, member_dict, scope_dict=None):
        if scope_dict is None:
            scope_dict = sys._getframe(1).f_locals
        forward_dict = {}
        reverse_dict = {}
        next_value = 0
        for name, value in member_dict.items():
            if value is None:
                value = next_value
                next_value += 1
            forward_dict[name] = value
            if value in reverse_dict:
                raise ValueError('Multiple names for value %r: %r, %r' % (
                 value, reverse_dict[value], name))
            reverse_dict[value] = name
            scope_dict[name] = value

        self.forward_dict = forward_dict
        self.reverse_dict = reverse_dict

    def __call__(self, value):
        return self.reverse_dict[value]

    def get(self, value, default=None):
        return self.reverse_dict.get(value, default)


def buffer_at(address, length):
    """
    Simular to ctypes.string_at, but zero-copy and requires an integer address.
    """
    return bytearray((c_char * length).from_address(address))


_desc_type_dict = {'b':c_uint8, 
 'bcd':c_uint16, 
 'bm':c_uint8, 
 'dw':c_uint32, 
 'i':c_uint8, 
 'id':c_uint16, 
 'w':c_uint16}

def newStruct(field_name_list):
    """
    Create a ctype structure class based on USB standard field naming
    (type-prefixed).
    """
    field_list = []
    append = field_list.append
    for field in field_name_list:
        type_prefix = ''
        for char in field:
            if not char.islower():
                break
            type_prefix += char

        append((field, _desc_type_dict[type_prefix]))

    result = type('some_descriptor', (LittleEndianStructure,), {})
    result._pack_ = 1
    result._fields_ = field_list
    return result


def newDescriptor(field_name_list):
    """
    Create a USB descriptor ctype structure, ie starting with bLength and
    bDescriptorType fields.

    See newStruct().
    """
    return newStruct(['bLength', 'bDescriptorType'] + list(field_name_list))


class USBError(Exception):
    value = None

    def __init__(self, value=None):
        Exception.__init__(self)
        if value is not None:
            self.value = value

    def __str__(self):
        return '%s [%s]' % (libusb_error.get(self.value, 'Unknown error'),
         self.value)


if sys.version_info[0] == 3:
    _string_item_to_int = lambda x: x
    _empty_char_p = bytes()
else:
    _string_item_to_int = ord
    _empty_char_p = ''
c_uchar = c_uint8
c_int_p = POINTER(c_int)
LITTLE_ENDIAN = sys.byteorder == 'little'

class timeval(Structure):
    _fields_ = [
     (
      'tv_sec', c_long),
     (
      'tv_usec', c_long)]


timeval_p = POINTER(timeval)

def _loadLibrary():
    system = platform.system()
    if system == 'Windows':
        dll_loader = ctypes.WinDLL
        suffix = '.dll'
    else:
        dll_loader = ctypes.CDLL
        suffix = system == 'Darwin' and '.dylib' or '.so'
    loader_kw = {}
    if sys.version_info[:2] >= (2, 6):
        loader_kw['use_errno'] = True
        loader_kw['use_last_error'] = True
    try:
        return dll_loader(('libusb-1.0' + suffix), **loader_kw)
    except OSError:
        libusb_path = None
        base_name = 'usb-1.0'
        if 'FreeBSD' in system:
            base_name = 'usb'
        else:
            if system == 'Darwin':
                for libusb_path in ('/opt/local/lib/libusb-1.0.dylib', '/sw/lib/libusb-1.0.dylib'):
                    if os.path.exists(libusb_path):
                        break
                else:
                    libusb_path = None

            elif libusb_path is None:
                libusb_path = ctypes.util.find_library(base_name)
                if libusb_path is None:
                    raise
        return dll_loader(libusb_path, **loader_kw)


libusb = _loadLibrary()

def bswap16(x):
    return (x & 255) << 8 | x >> 8


if LITTLE_ENDIAN:

    def libusb_cpu_to_le16(x):
        return x


    def libusb_le16_to_cpu(x):
        return x


else:
    libusb_cpu_to_le16 = bswap16
    libusb_le16_to_cpu = bswap16
libusb_class_code = Enum({'LIBUSB_CLASS_PER_INTERFACE':0, 
 'LIBUSB_CLASS_AUDIO':1, 
 'LIBUSB_CLASS_COMM':2, 
 'LIBUSB_CLASS_HID':3, 
 'LIBUSB_CLASS_PHYSICAL':5, 
 'LIBUSB_CLASS_PRINTER':7, 
 'LIBUSB_CLASS_PTP':6, 
 'LIBUSB_CLASS_MASS_STORAGE':8, 
 'LIBUSB_CLASS_HUB':9, 
 'LIBUSB_CLASS_DATA':10, 
 'LIBUSB_CLASS_SMART_CARD':11, 
 'LIBUSB_CLASS_CONTENT_SECURITY':13, 
 'LIBUSB_CLASS_VIDEO':14, 
 'LIBUSB_CLASS_PERSONAL_HEALTHCARE':15, 
 'LIBUSB_CLASS_DIAGNOSTIC_DEVICE':220, 
 'LIBUSB_CLASS_WIRELESS':224, 
 'LIBUSB_CLASS_APPLICATION':254, 
 'LIBUSB_CLASS_VENDOR_SPEC':255})
LIBUSB_CLASS_IMAGE = LIBUSB_CLASS_PTP
libusb_descriptor_type = Enum({'LIBUSB_DT_DEVICE':1, 
 'LIBUSB_DT_CONFIG':2, 
 'LIBUSB_DT_STRING':3, 
 'LIBUSB_DT_INTERFACE':4, 
 'LIBUSB_DT_ENDPOINT':5, 
 'LIBUSB_DT_HID':33, 
 'LIBUSB_DT_REPORT':34, 
 'LIBUSB_DT_PHYSICAL':35, 
 'LIBUSB_DT_HUB':41})
LIBUSB_DT_DEVICE_SIZE = 18
LIBUSB_DT_CONFIG_SIZE = 9
LIBUSB_DT_INTERFACE_SIZE = 9
LIBUSB_DT_ENDPOINT_SIZE = 7
LIBUSB_DT_ENDPOINT_AUDIO_SIZE = 9
LIBUSB_DT_HUB_NONVAR_SIZE = 7
LIBUSB_ENDPOINT_ADDRESS_MASK = 15
LIBUSB_ENDPOINT_DIR_MASK = 128
USB_ENDPOINT_ADDRESS_MASK = LIBUSB_ENDPOINT_ADDRESS_MASK
USB_ENDPOINT_DIR_MASK = LIBUSB_ENDPOINT_DIR_MASK
libusb_endpoint_direction = Enum({'LIBUSB_ENDPOINT_IN':128, 
 'LIBUSB_ENDPOINT_OUT':0})
LIBUSB_TRANSFER_TYPE_MASK = 3
libusb_transfer_type = Enum({'LIBUSB_TRANSFER_TYPE_CONTROL':0, 
 'LIBUSB_TRANSFER_TYPE_ISOCHRONOUS':1, 
 'LIBUSB_TRANSFER_TYPE_BULK':2, 
 'LIBUSB_TRANSFER_TYPE_INTERRUPT':3})
libusb_standard_request = Enum({'LIBUSB_REQUEST_GET_STATUS':0, 
 'LIBUSB_REQUEST_CLEAR_FEATURE':1, 
 'LIBUSB_REQUEST_SET_FEATURE':3, 
 'LIBUSB_REQUEST_SET_ADDRESS':5, 
 'LIBUSB_REQUEST_GET_DESCRIPTOR':6, 
 'LIBUSB_REQUEST_SET_DESCRIPTOR':7, 
 'LIBUSB_REQUEST_GET_CONFIGURATION':8, 
 'LIBUSB_REQUEST_SET_CONFIGURATION':9, 
 'LIBUSB_REQUEST_GET_INTERFACE':10, 
 'LIBUSB_REQUEST_SET_INTERFACE':11, 
 'LIBUSB_REQUEST_SYNCH_FRAME':12})
libusb_request_type = Enum({'LIBUSB_REQUEST_TYPE_STANDARD':0, 
 'LIBUSB_REQUEST_TYPE_CLASS':32, 
 'LIBUSB_REQUEST_TYPE_VENDOR':64, 
 'LIBUSB_REQUEST_TYPE_RESERVED':96})
LIBUSB_TYPE_STANDARD = LIBUSB_REQUEST_TYPE_STANDARD
LIBUSB_TYPE_CLASS = LIBUSB_REQUEST_TYPE_CLASS
LIBUSB_TYPE_VENDOR = LIBUSB_REQUEST_TYPE_VENDOR
LIBUSB_TYPE_RESERVED = LIBUSB_REQUEST_TYPE_RESERVED
libusb_request_recipient = Enum({'LIBUSB_RECIPIENT_DEVICE':0, 
 'LIBUSB_RECIPIENT_INTERFACE':1, 
 'LIBUSB_RECIPIENT_ENDPOINT':2, 
 'LIBUSB_RECIPIENT_OTHER':3})
LIBUSB_ISO_SYNC_TYPE_MASK = 12
libusb_iso_sync_type = Enum({'LIBUSB_ISO_SYNC_TYPE_NONE':0, 
 'LIBUSB_ISO_SYNC_TYPE_ASYNC':1, 
 'LIBUSB_ISO_SYNC_TYPE_ADAPTIVE':2, 
 'LIBUSB_ISO_SYNC_TYPE_SYNC':3})
LIBUSB_ISO_USAGE_TYPE_MASK = 48
libusb_iso_usage_type = Enum({'LIBUSB_ISO_USAGE_TYPE_DATA':0, 
 'LIBUSB_ISO_USAGE_TYPE_FEEDBACK':1, 
 'LIBUSB_ISO_USAGE_TYPE_IMPLICIT':2})

class libusb_device_descriptor(Structure):
    _fields_ = [
     (
      'bLength', c_uint8),
     (
      'bDescriptorType', c_uint8),
     (
      'bcdUSB', c_uint16),
     (
      'bDeviceClass', c_uint8),
     (
      'bDeviceSubClass', c_uint8),
     (
      'bDeviceProtocol', c_uint8),
     (
      'bMaxPacketSize0', c_uint8),
     (
      'idVendor', c_uint16),
     (
      'idProduct', c_uint16),
     (
      'bcdDevice', c_uint16),
     (
      'iManufacturer', c_uint8),
     (
      'iProduct', c_uint8),
     (
      'iSerialNumber', c_uint8),
     (
      'bNumConfigurations', c_uint8)]


libusb_device_descriptor_p = POINTER(libusb_device_descriptor)

class libusb_endpoint_descriptor(Structure):
    _fields_ = [
     (
      'bLength', c_uint8),
     (
      'bDescriptorType', c_uint8),
     (
      'bEndpointAddress', c_uint8),
     (
      'bmAttributes', c_uint8),
     (
      'wMaxPacketSize', c_uint16),
     (
      'bInterval', c_uint8),
     (
      'bRefresh', c_uint8),
     (
      'bSynchAddress', c_uint8),
     (
      'extra', c_void_p),
     (
      'extra_length', c_int)]


libusb_endpoint_descriptor_p = POINTER(libusb_endpoint_descriptor)

class libusb_interface_descriptor(Structure):
    _fields_ = [
     (
      'bLength', c_uint8),
     (
      'bDescriptorType', c_uint8),
     (
      'bInterfaceNumber', c_uint8),
     (
      'bAlternateSetting', c_uint8),
     (
      'bNumEndpoints', c_uint8),
     (
      'bInterfaceClass', c_uint8),
     (
      'bInterfaceSubClass', c_uint8),
     (
      'bInterfaceProtocol', c_uint8),
     (
      'iInterface', c_uint8),
     (
      'endpoint', libusb_endpoint_descriptor_p),
     (
      'extra', c_void_p),
     (
      'extra_length', c_int)]


libusb_interface_descriptor_p = POINTER(libusb_interface_descriptor)

class libusb_interface(Structure):
    _fields_ = [
     (
      'altsetting', libusb_interface_descriptor_p),
     (
      'num_altsetting', c_int)]


libusb_interface_p = POINTER(libusb_interface)

class libusb_config_descriptor(Structure):
    _fields_ = [
     (
      'bLength', c_uint8),
     (
      'bDescriptorType', c_uint8),
     (
      'wTotalLength', c_uint16),
     (
      'bNumInterfaces', c_uint8),
     (
      'bConfigurationValue', c_uint8),
     (
      'iConfiguration', c_uint8),
     (
      'bmAttributes', c_uint8),
     (
      'MaxPower', c_uint8),
     (
      'interface', libusb_interface_p),
     (
      'extra', c_void_p),
     (
      'extra_length', c_int)]


libusb_config_descriptor_p = POINTER(libusb_config_descriptor)
libusb_config_descriptor_p_p = POINTER(libusb_config_descriptor_p)

class libusb_control_setup(Structure):
    _fields_ = [
     (
      'bmRequestType', c_uint8),
     (
      'bRequest', c_uint8),
     (
      'wValue', c_uint16),
     (
      'wIndex', c_uint16),
     (
      'wLength', c_uint16)]


libusb_control_setup_p = POINTER(libusb_control_setup)
LIBUSB_CONTROL_SETUP_SIZE = sizeof(libusb_control_setup)

class libusb_context(Structure):
    pass


libusb_context_p = POINTER(libusb_context)
libusb_context_p_p = POINTER(libusb_context_p)

class libusb_device(Structure):
    pass


libusb_device_p = POINTER(libusb_device)
libusb_device_p_p = POINTER(libusb_device_p)
libusb_device_p_p_p = POINTER(libusb_device_p_p)

class libusb_device_handle(Structure):
    pass


libusb_device_handle_p = POINTER(libusb_device_handle)
libusb_device_handle_p_p = POINTER(libusb_device_handle_p)

class libusb_version(Structure):
    _fields_ = [
     (
      'major', c_uint16),
     (
      'minor', c_uint16),
     (
      'micro', c_uint16),
     (
      'nano', c_uint16),
     (
      'rc', c_char_p),
     (
      'describe', c_char_p)]


libusb_speed = Enum({'LIBUSB_SPEED_UNKNOWN':0, 
 'LIBUSB_SPEED_LOW':1, 
 'LIBUSB_SPEED_FULL':2, 
 'LIBUSB_SPEED_HIGH':3, 
 'LIBUSB_SPEED_SUPER':4})
libusb_supported_speed = Enum({'LIBUSB_LOW_SPEED_OPERATION':1, 
 'LIBUSB_FULL_SPEED_OPERATION':2, 
 'LIBUSB_HIGH_SPEED_OPERATION':4, 
 'LIBUSB_5GBPS_OPERATION':8})
libusb_error = Enum({'LIBUSB_SUCCESS':0, 
 'LIBUSB_ERROR_IO':-1, 
 'LIBUSB_ERROR_INVALID_PARAM':-2, 
 'LIBUSB_ERROR_ACCESS':-3, 
 'LIBUSB_ERROR_NO_DEVICE':-4, 
 'LIBUSB_ERROR_NOT_FOUND':-5, 
 'LIBUSB_ERROR_BUSY':-6, 
 'LIBUSB_ERROR_TIMEOUT':-7, 
 'LIBUSB_ERROR_OVERFLOW':-8, 
 'LIBUSB_ERROR_PIPE':-9, 
 'LIBUSB_ERROR_INTERRUPTED':-10, 
 'LIBUSB_ERROR_NO_MEM':-11, 
 'LIBUSB_ERROR_NOT_SUPPORTED':-12, 
 'LIBUSB_ERROR_OTHER':-99})
libusb_transfer_status = Enum({'LIBUSB_TRANSFER_COMPLETED':0, 
 'LIBUSB_TRANSFER_ERROR':1, 
 'LIBUSB_TRANSFER_TIMED_OUT':2, 
 'LIBUSB_TRANSFER_CANCELLED':3, 
 'LIBUSB_TRANSFER_STALL':4, 
 'LIBUSB_TRANSFER_NO_DEVICE':5, 
 'LIBUSB_TRANSFER_OVERFLOW':6})
libusb_transfer_flags = Enum({'LIBUSB_TRANSFER_SHORT_NOT_OK':1, 
 'LIBUSB_TRANSFER_FREE_BUFFER':2, 
 'LIBUSB_TRANSFER_FREE_TRANSFER':4, 
 'LIBUSB_TRANSFER_ADD_ZERO_PACKET':8})

class libusb_iso_packet_descriptor(Structure):
    _fields_ = [
     (
      'length', c_uint),
     (
      'actual_length', c_uint),
     (
      'status', c_int)]


libusb_iso_packet_descriptor_p = POINTER(libusb_iso_packet_descriptor)

class libusb_transfer(Structure):
    pass


libusb_transfer_p = POINTER(libusb_transfer)
libusb_transfer_cb_fn_p = CFUNCTYPE(None, libusb_transfer_p)
_libusb_transfer_fields = [
 (
  'dev_handle', libusb_device_handle_p),
 (
  'flags', c_uint8),
 (
  'endpoint', c_uchar),
 (
  'type', c_uchar),
 (
  'timeout', c_uint),
 (
  'status', c_int),
 (
  'length', c_int),
 (
  'actual_length', c_int),
 (
  'callback', libusb_transfer_cb_fn_p),
 (
  'user_data', c_void_p),
 (
  'buffer', c_void_p),
 (
  'num_iso_packets', c_int),
 (
  'iso_packet_desc', libusb_iso_packet_descriptor)]
if 'FreeBSD' in platform.system():
    if getattr(libusb, 'libusb_get_string_descriptor', None) is None:
        assert _libusb_transfer_fields[2][0] == 'endpoint'
        _libusb_transfer_fields[2] = ('endpoint', c_uint32)
        assert _libusb_transfer_fields[11][0] == 'num_iso_packets'
        _libusb_transfer_fields.insert(11, ('os_priv', c_void_p))
libusb_transfer._fields_ = _libusb_transfer_fields
libusb_capability = Enum({'LIBUSB_CAP_HAS_CAPABILITY':0, 
 'LIBUSB_CAP_HAS_HOTPLUG':1, 
 'LIBUSB_CAP_HAS_HID_ACCESS':256, 
 'LIBUSB_CAP_SUPPORTS_DETACH_KERNEL_DRIVER':257})
libusb_log_level = Enum({'LIBUSB_LOG_LEVEL_NONE':0, 
 'LIBUSB_LOG_LEVEL_ERROR':1, 
 'LIBUSB_LOG_LEVEL_WARNING':2, 
 'LIBUSB_LOG_LEVEL_INFO':3, 
 'LIBUSB_LOG_LEVEL_DEBUG':4})
libusb_init = libusb.libusb_init
libusb_init.argtypes = [libusb_context_p_p]
libusb_exit = libusb.libusb_exit
libusb_exit.argtypes = [libusb_context_p]
libusb_exit.restype = None
libusb_set_debug = libusb.libusb_set_debug
libusb_set_debug.argtypes = [libusb_context_p, c_int]
libusb_set_debug.restype = None
try:
    libusb_get_version = libusb.libusb_get_version
except AttributeError:
    _dummy_version = libusb_version(0, 0, 0, 0, _empty_char_p, _empty_char_p)
    _dummy_version_p = pointer(_dummy_version)

    def libusb_get_version():
        return _dummy_version_p


else:
    libusb_get_version.argtypes = []
    libusb_get_version.restype = POINTER(libusb_version)
try:
    libusb_has_capability = libusb.libusb_has_capability
except AttributeError:

    def libusb_has_capability(_):
        return 0


else:
    libusb_has_capability.argtypes = [
     c_uint32]
    libusb_has_capability.restype = c_int
try:
    libusb_error_name = libusb.libusb_error_name
except AttributeError:

    def libusb_error_name(errcode):
        pass


else:
    libusb_error_name.argtypes = [
     c_int]
    libusb_error_name.restype = c_char_p

def libusb_strerror(errcode):
    pass


libusb_get_device_list = libusb.libusb_get_device_list
libusb_get_device_list.argtypes = [libusb_context_p, libusb_device_p_p_p]
libusb_get_device_list.restype = c_ssize_t
libusb_free_device_list = libusb.libusb_free_device_list
libusb_free_device_list.argtypes = [libusb_device_p_p, c_int]
libusb_free_device_list.restype = None
libusb_ref_device = libusb.libusb_ref_device
libusb_ref_device.argtypes = [libusb_device_p]
libusb_ref_device.restype = libusb_device_p
libusb_unref_device = libusb.libusb_unref_device
libusb_unref_device.argtypes = [libusb_device_p]
libusb_unref_device.restype = None
libusb_get_configuration = libusb.libusb_get_configuration
libusb_get_configuration.argtypes = [libusb_device_handle_p, c_int_p]
libusb_get_device_descriptor = libusb.libusb_get_device_descriptor
libusb_get_device_descriptor.argtypes = [
 libusb_device_p, libusb_device_descriptor_p]
libusb_get_active_config_descriptor = libusb.libusb_get_active_config_descriptor
libusb_get_active_config_descriptor.argtypes = [
 libusb_device_p, libusb_config_descriptor_p_p]
libusb_get_config_descriptor = libusb.libusb_get_config_descriptor
libusb_get_config_descriptor.argtypes = [
 libusb_device_p, c_uint8, libusb_config_descriptor_p_p]
libusb_get_config_descriptor_by_value = libusb.libusb_get_config_descriptor_by_value
libusb_get_config_descriptor_by_value.argtypes = [
 libusb_device_p, c_uint8, libusb_config_descriptor_p_p]
libusb_free_config_descriptor = libusb.libusb_free_config_descriptor
libusb_free_config_descriptor.argtypes = [libusb_config_descriptor_p]
libusb_free_config_descriptor.restype = None
libusb_get_bus_number = libusb.libusb_get_bus_number
libusb_get_bus_number.argtypes = [libusb_device_p]
libusb_get_bus_number.restype = c_uint8
try:
    libusb_get_port_number = libusb.libusb_get_port_number
except AttributeError:
    pass
else:
    libusb_get_port_number.argtypes = [
     libusb_device_p]
    libusb_get_port_number.restype = c_uint8
try:
    libusb_get_port_numbers = libusb.libusb_get_port_numbers
except AttributeError:
    pass
else:
    libusb_get_port_numbers.argtypes = [libusb_device_p, POINTER(c_uint8), c_int]
    libusb_get_port_numbers.restype = c_int
try:
    libusb_get_parent = libusb.libusb_get_parent
except AttributeError:
    pass
else:
    libusb_get_parent.argtypes = [
     libusb_device_p]
    libusb_get_parent.restype = libusb_device_p
libusb_get_device_address = libusb.libusb_get_device_address
libusb_get_device_address.argtypes = [libusb_device_p]
libusb_get_device_address.restype = c_uint8
try:
    libusb_get_device_speed = libusb.libusb_get_device_speed
except AttributeError:

    def libusb_get_device_speed(_):
        return LIBUSB_SPEED_UNKNOWN


else:
    libusb_get_device_speed.argtypes = [
     libusb_device_p]
libusb_get_max_packet_size = libusb.libusb_get_max_packet_size
libusb_get_max_packet_size.argtypes = [libusb_device_p, c_uchar]
try:
    libusb_get_max_iso_packet_size = libusb.libusb_get_max_iso_packet_size
except AttributeError:

    def libusb_get_max_iso_packet_size(_, __):
        raise NotImplementedError


else:
    libusb_get_max_iso_packet_size.argtypes = [
     libusb_device_p, c_uchar]
libusb_open = libusb.libusb_open
libusb_open.argtypes = [libusb_device_p, libusb_device_handle_p_p]
libusb_close = libusb.libusb_close
libusb_close.argtypes = [libusb_device_handle_p]
libusb_close.restype = None
libusb_get_device = libusb.libusb_get_device
libusb_get_device.argtypes = [libusb_device_handle_p]
libusb_get_device.restype = libusb_device_p
libusb_set_configuration = libusb.libusb_set_configuration
libusb_set_configuration.argtypes = [libusb_device_handle_p, c_int]
libusb_claim_interface = libusb.libusb_claim_interface
libusb_claim_interface.argtypes = [libusb_device_handle_p, c_int]
libusb_release_interface = libusb.libusb_release_interface
libusb_release_interface.argtypes = [libusb_device_handle_p, c_int]
libusb_open_device_with_vid_pid = libusb.libusb_open_device_with_vid_pid
libusb_open_device_with_vid_pid.argtypes = [
 libusb_context_p, c_uint16, c_uint16]
libusb_open_device_with_vid_pid.restype = libusb_device_handle_p
libusb_set_interface_alt_setting = libusb.libusb_set_interface_alt_setting
libusb_set_interface_alt_setting.argtypes = [
 libusb_device_handle_p, c_int, c_int]
libusb_clear_halt = libusb.libusb_clear_halt
libusb_clear_halt.argtypes = [libusb_device_handle_p, c_uchar]
libusb_reset_device = libusb.libusb_reset_device
libusb_reset_device.argtypes = [libusb_device_handle_p]
libusb_kernel_driver_active = libusb.libusb_kernel_driver_active
libusb_kernel_driver_active.argtypes = [libusb_device_handle_p, c_int]
libusb_detach_kernel_driver = libusb.libusb_detach_kernel_driver
libusb_detach_kernel_driver.argtypes = [libusb_device_handle_p, c_int]
libusb_attach_kernel_driver = libusb.libusb_attach_kernel_driver
libusb_attach_kernel_driver.argtypes = [libusb_device_handle_p, c_int]
try:
    libusb_set_auto_detach_kernel_driver = libusb.libusb_set_auto_detach_kernel_driver
except AttributeError:
    pass
else:
    libusb_set_auto_detach_kernel_driver.argtypes = [libusb_device_handle_p, c_int]
    libusb_set_auto_detach_kernel_driver.restype = c_int

def libusb_control_transfer_get_data(transfer_p):
    transfer = transfer_p.contents
    return buffer_at(transfer.buffer.value, transfer.length)[LIBUSB_CONTROL_SETUP_SIZE:]


def libusb_control_transfer_get_setup(transfer_p):
    return cast(transfer_p.contents.buffer, libusb_control_setup_p)


def libusb_fill_control_setup(setup_p, bmRequestType, bRequest, wValue, wIndex, wLength):
    setup = cast(setup_p, libusb_control_setup_p).contents
    setup.bmRequestType = bmRequestType
    setup.bRequest = bRequest
    setup.wValue = libusb_cpu_to_le16(wValue)
    setup.wIndex = libusb_cpu_to_le16(wIndex)
    setup.wLength = libusb_cpu_to_le16(wLength)


libusb_alloc_transfer = libusb.libusb_alloc_transfer
libusb_alloc_transfer.argtypes = [c_int]
libusb_alloc_transfer.restype = libusb_transfer_p
libusb_submit_transfer = libusb.libusb_submit_transfer
libusb_submit_transfer.argtypes = [libusb_transfer_p]
libusb_cancel_transfer = libusb.libusb_cancel_transfer
libusb_cancel_transfer.argtypes = [libusb_transfer_p]
libusb_free_transfer = libusb.libusb_free_transfer
libusb_free_transfer.argtypes = [libusb_transfer_p]
libusb_free_transfer.restype = None

def libusb_fill_control_transfer(transfer_p, dev_handle, buffer, callback, user_data, timeout):
    transfer = transfer_p.contents
    transfer.dev_handle = dev_handle
    transfer.endpoint = 0
    transfer.type = LIBUSB_TRANSFER_TYPE_CONTROL
    transfer.timeout = timeout
    transfer.buffer = cast(buffer, c_void_p)
    if buffer is not None:
        setup = cast(buffer, libusb_control_setup_p).contents
        transfer.length = LIBUSB_CONTROL_SETUP_SIZE + libusb_le16_to_cpu(setup.wLength)
    transfer.user_data = user_data
    transfer.callback = callback


def libusb_fill_bulk_transfer(transfer_p, dev_handle, endpoint, buffer, length, callback, user_data, timeout):
    transfer = transfer_p.contents
    transfer.dev_handle = dev_handle
    transfer.endpoint = endpoint
    transfer.type = LIBUSB_TRANSFER_TYPE_BULK
    transfer.timeout = timeout
    transfer.buffer = cast(buffer, c_void_p)
    transfer.length = length
    transfer.user_data = user_data
    transfer.callback = callback


def libusb_fill_interrupt_transfer(transfer_p, dev_handle, endpoint, buffer, length, callback, user_data, timeout):
    transfer = transfer_p.contents
    transfer.dev_handle = dev_handle
    transfer.endpoint = endpoint
    transfer.type = LIBUSB_TRANSFER_TYPE_INTERRUPT
    transfer.timeout = timeout
    transfer.buffer = cast(buffer, c_void_p)
    transfer.length = length
    transfer.user_data = user_data
    transfer.callback = callback


def libusb_fill_iso_transfer(transfer_p, dev_handle, endpoint, buffer, length, num_iso_packets, callback, user_data, timeout):
    transfer = transfer_p.contents
    transfer.dev_handle = dev_handle
    transfer.endpoint = endpoint
    transfer.type = LIBUSB_TRANSFER_TYPE_ISOCHRONOUS
    transfer.timeout = timeout
    transfer.buffer = cast(buffer, c_void_p)
    transfer.length = length
    transfer.num_iso_packets = num_iso_packets
    transfer.user_data = user_data
    transfer.callback = callback


def _get_iso_packet_list(transfer):
    list_type = libusb_iso_packet_descriptor * transfer.num_iso_packets
    return list_type.from_address(addressof(transfer.iso_packet_desc))


def get_iso_packet_list(transfer_p):
    """
    Python-specific helper extracting a list of iso packet descriptors,
    because it's not as straight-forward as in C.
    """
    return _get_iso_packet_list(transfer_p.contents)


def _get_iso_packet_buffer(transfer, offset, length):
    return buffer_at(transfer.buffer + offset, length)


def get_iso_packet_buffer_list(transfer_p):
    """
    Python-specific helper extracting a list of iso packet buffers.
    """
    transfer = transfer_p.contents
    offset = 0
    result = []
    append = result.append
    for iso_transfer in _get_iso_packet_list(transfer):
        length = iso_transfer.length
        append(_get_iso_packet_buffer(transfer, offset, length))
        offset += length

    return result


def get_extra(descriptor):
    """
    Python-specific helper to access "extra" field of descriptors,
    because it's not as straight-forward as in C.
    Returns a list, where each entry is an individual extra descriptor.
    """
    result = []
    extra_length = descriptor.extra_length
    if extra_length:
        extra = buffer_at(descriptor.extra.value, extra_length)
        append = result.append
        while extra:
            length = _string_item_to_int(extra[0])
            if not 0 < length <= len(extra):
                raise ValueError('Extra descriptor %i is incomplete/invalid' % (
                 len(result),))
            append(extra[:length])
            extra = extra[length:]

    return result


def libusb_set_iso_packet_lengths(transfer_p, length):
    transfer = transfer_p.contents
    for iso_packet_desc in _get_iso_packet_list(transfer):
        iso_packet_desc.length = length


def libusb_get_iso_packet_buffer(transfer_p, packet):
    transfer = transfer_p.contents
    offset = 0
    if packet >= transfer.num_iso_packets:
        return
    iso_packet_desc_list = _get_iso_packet_list(transfer)
    for i in xrange(packet):
        offset += iso_packet_desc_list[i].length

    return _get_iso_packet_buffer(transfer, offset, iso_packet_desc_list[packet].length)


def libusb_get_iso_packet_buffer_simple(transfer_p, packet):
    transfer = transfer_p.contents
    if packet >= transfer.num_iso_packets:
        return
    iso_length = transfer.iso_packet_desc.length
    return _get_iso_packet_buffer(transfer, iso_length * packet, iso_length)


libusb_control_transfer = libusb.libusb_control_transfer
libusb_control_transfer.argtypes = [libusb_device_handle_p, c_uint8, c_uint8,
 c_uint16, c_uint16, c_void_p, c_uint16,
 c_uint]
libusb_bulk_transfer = libusb.libusb_bulk_transfer
libusb_bulk_transfer.argtypes = [libusb_device_handle_p, c_uchar, c_void_p,
 c_int, c_int_p, c_uint]
libusb_interrupt_transfer = libusb.libusb_interrupt_transfer
libusb_interrupt_transfer.argtypes = [libusb_device_handle_p, c_uchar,
 c_void_p, c_int, c_int_p, c_uint]

def libusb_get_descriptor(dev, desc_type, desc_index, data, length):
    return libusb_control_transfer(dev, LIBUSB_ENDPOINT_IN, LIBUSB_REQUEST_GET_DESCRIPTOR, desc_type << 8 | desc_index, 0, data, length, 1000)


def libusb_get_string_descriptor(dev, desc_index, langid, data, length):
    return libusb_control_transfer(dev, LIBUSB_ENDPOINT_IN, LIBUSB_REQUEST_GET_DESCRIPTOR, LIBUSB_DT_STRING << 8 | desc_index, langid, data, length, 1000)


libusb_get_string_descriptor_ascii = libusb.libusb_get_string_descriptor_ascii
libusb_get_string_descriptor_ascii.argtypes = [libusb_device_handle_p,
 c_uint8, c_void_p, c_int]
libusb_try_lock_events = libusb.libusb_try_lock_events
libusb_try_lock_events.argtypes = [libusb_context_p]
libusb_lock_events = libusb.libusb_lock_events
libusb_lock_events.argtypes = [libusb_context_p]
libusb_unlock_events = libusb.libusb_unlock_events
libusb_unlock_events.argtypes = [libusb_context_p]
libusb_unlock_events.restype = None
libusb_event_handling_ok = libusb.libusb_event_handling_ok
libusb_event_handling_ok.argtypes = [libusb_context_p]
libusb_event_handler_active = libusb.libusb_event_handler_active
libusb_event_handler_active.argtypes = [libusb_context_p]
libusb_lock_event_waiters = libusb.libusb_lock_event_waiters
libusb_lock_event_waiters.argtypes = [libusb_context_p]
libusb_lock_event_waiters.restype = None
libusb_unlock_event_waiters = libusb.libusb_unlock_event_waiters
libusb_unlock_event_waiters.argtypes = []
libusb_unlock_event_waiters.restype = None
libusb_wait_for_event = libusb.libusb_wait_for_event
libusb_wait_for_event.argtypes = [libusb_context_p, timeval_p]
libusb_handle_events_timeout = libusb.libusb_handle_events_timeout
libusb_handle_events_timeout.argtypes = [libusb_context_p, timeval_p]
try:
    libusb_handle_events_timeout_completed = libusb.libusb_handle_events_timeout_completed
except AttributeError:
    pass
else:
    libusb_handle_events_timeout_completed.argtypes = [libusb_context_p, timeval_p, c_int_p]
libusb_handle_events = libusb.libusb_handle_events
libusb_handle_events.argtypes = [libusb_context_p]
try:
    libusb_handle_events_completed = libusb.libusb_handle_events_completed
except AttributeError:
    pass
else:
    libusb_handle_events_completed.argtypes = [
     libusb_context_p, c_int_p]
libusb_handle_events_locked = libusb.libusb_handle_events_locked
libusb_handle_events_locked.argtypes = [libusb_context_p, timeval_p]
libusb_get_next_timeout = libusb.libusb_get_next_timeout
libusb_get_next_timeout.argtypes = [libusb_context_p, timeval_p]

class libusb_pollfd(Structure):
    _fields_ = [
     (
      'fd', c_int),
     (
      'events', c_short)]


libusb_pollfd_p = POINTER(libusb_pollfd)
libusb_pollfd_p_p = POINTER(libusb_pollfd_p)
libusb_pollfd_added_cb_p = CFUNCTYPE(None, c_int, c_short, py_object)
libusb_pollfd_removed_cb_p = CFUNCTYPE(None, c_int, py_object)
libusb_get_pollfds = libusb.libusb_get_pollfds
libusb_get_pollfds.argtypes = [libusb_context_p]
libusb_get_pollfds.restype = libusb_pollfd_p_p
libusb_set_pollfd_notifiers = libusb.libusb_set_pollfd_notifiers
libusb_set_pollfd_notifiers.argtypes = [libusb_context_p,
 libusb_pollfd_added_cb_p,
 libusb_pollfd_removed_cb_p, py_object]
libusb_set_pollfd_notifiers.restype = None
libusb_hotplug_callback_handle = c_int
libusb_hotplug_flag = Enum({'LIBUSB_HOTPLUG_ENUMERATE': 1})
libusb_hotplug_event = Enum({'LIBUSB_HOTPLUG_EVENT_DEVICE_ARRIVED':1, 
 'LIBUSB_HOTPLUG_EVENT_DEVICE_LEFT':2})
LIBUSB_HOTPLUG_MATCH_ANY = -1
libusb_hotplug_callback_fn_p = CFUNCTYPE(c_int, libusb_context_p, libusb_device_p, c_int, c_void_p)
try:
    libusb_hotplug_register_callback = libusb.libusb_hotplug_register_callback
except AttributeError:
    pass
else:
    libusb_hotplug_register_callback.argtypes = [libusb_context_p,
     c_int, c_int,
     c_int, c_int, c_int,
     libusb_hotplug_callback_fn_p, c_void_p,
     POINTER(libusb_hotplug_callback_handle)]
    libusb_hotplug_register_callback.restype = c_int
try:
    libusb_hotplug_deregister_callback = libusb.libusb_hotplug_deregister_callback
except AttributeError:
    pass
else:
    libusb_hotplug_deregister_callback.argtypes = [libusb_context_p,
     libusb_hotplug_callback_handle]
    libusb_hotplug_deregister_callback.restype = None