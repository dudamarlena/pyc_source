# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Dean\Documents\Python\python-elgato-streamdeck\src\StreamDeck\DeviceManager.py
# Compiled at: 2020-04-09 21:35:07
# Size of source mod 2**32: 3854 bytes
import Devices.StreamDeckOriginal as StreamDeckOriginal
import Devices.StreamDeckOriginalV2 as StreamDeckOriginalV2
import Devices.StreamDeckMini as StreamDeckMini
import Devices.StreamDeckXL as StreamDeckXL
import Transport.Dummy as Dummy
import Transport.LibUSBHIDAPI as LibUSBHIDAPI

class ProbeError(Exception):
    __doc__ = '\n    Exception thrown when attempting to probe for attached StreamDeck devices,\n    but no suitable valid transport was found.\n    '


class DeviceManager:
    __doc__ = '\n    Central device manager, to enumerate any attached StreamDeck devices. An\n    instance of this class must be created in order to detect and use any\n    StreamDeck devices.\n    '
    USB_VID_ELGATO = 4057
    USB_PID_STREAMDECK_ORIGINAL = 96
    USB_PID_STREAMDECK_ORIGINAL_V2 = 109
    USB_PID_STREAMDECK_MINI = 99
    USB_PID_STREAMDECK_XL = 108

    @staticmethod
    def _get_transport(transport):
        """
        Creates a new HID transport instance from the given transport back-end
        name. If no specific transport is supplied, an attempt to find an
        installed backend will be made.

        :param str transport: Name of a supported HID transport back-end to use, None to autoprobe.

        :rtype: Transport.* instance
        :return: Instance of a HID Transport class
        """
        transports = {'dummy':Dummy, 
         'libusb':LibUSBHIDAPI}
        if transport:
            transport_class = transports.get(transport)
            if transport_class is None:
                raise ProbeError('Unknown HID transport backend "{}".'.format(transport))
            try:
                transport_class.probe()
                return transport_class()
            except Exception as transport_error:
                try:
                    raise ProbeError('Probe failed on HID backend "{}".'.format(transport), transport_error)
                finally:
                    transport_error = None
                    del transport_error

        else:
            probe_errors = {}
            for transport_name, transport_class in transports.items():
                if transport_name == 'dummy':
                    continue
                try:
                    transport_class.probe()
                    return transport_class()
                except Exception as transport_error:
                    try:
                        probe_errors[transport_name] = transport_error
                    finally:
                        transport_error = None
                        del transport_error

            raise ProbeError('Probe failed to find any functional HID backend.', probe_errors)

    def __init__(self, transport=None):
        """
        Creates a new StreamDeck DeviceManager, used to detect attached StreamDeck devices.

        :param str transport: name of the the specific HID transport back-end to use, None to auto-probe.
        """
        self.transport = self._get_transport(transport)

    def enumerate(self):
        """
        Detect attached StreamDeck devices.

        :rtype: list(StreamDeck)
        :return: list of :class:`StreamDeck` instances, one for each detected device.
        """
        products = [
         (
          self.USB_VID_ELGATO, self.USB_PID_STREAMDECK_ORIGINAL, StreamDeckOriginal),
         (
          self.USB_VID_ELGATO, self.USB_PID_STREAMDECK_ORIGINAL_V2, StreamDeckOriginalV2),
         (
          self.USB_VID_ELGATO, self.USB_PID_STREAMDECK_MINI, StreamDeckMini),
         (
          self.USB_VID_ELGATO, self.USB_PID_STREAMDECK_XL, StreamDeckXL)]
        streamdecks = list()
        for vid, pid, class_type in products:
            found_devices = self.transport.enumerate(vid=vid, pid=pid)
            streamdecks.extend([class_type(d) for d in found_devices])

        return streamdecks