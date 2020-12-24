# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Dean\Documents\Python\python-elgato-streamdeck\src\StreamDeck\Devices\StreamDeckMini.py
# Compiled at: 2019-11-20 04:01:04
# Size of source mod 2**32: 5463 bytes
from .StreamDeck import StreamDeck

class StreamDeckMini(StreamDeck):
    __doc__ = '\n    Represents a physically attached StreamDeck Mini device.\n    '
    KEY_COUNT = 6
    KEY_COLS = 3
    KEY_ROWS = 2
    KEY_PIXEL_WIDTH = 80
    KEY_PIXEL_HEIGHT = 80
    KEY_IMAGE_FORMAT = 'BMP'
    KEY_FLIP = (False, True)
    KEY_ROTATION = 90
    DECK_TYPE = 'Stream Deck Mini'
    IMAGE_REPORT_LENGTH = 1024
    IMAGE_REPORT_HEADER_LENGTH = 16
    IMAGE_REPORT_PAYLOAD_LENGTH = IMAGE_REPORT_LENGTH - IMAGE_REPORT_HEADER_LENGTH
    BLANK_KEY_IMAGE = [
     66, 77, 246, 60, 0, 0, 0, 0,
     0, 0, 54, 0, 0, 0, 40, 0,
     0, 0, 72, 0, 0, 0, 72, 0,
     0, 0, 1, 0, 24, 0, 0, 0,
     0, 0, 192, 60, 0, 0, 196, 14,
     0, 0, 196, 14, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0] + [
     0] * (KEY_PIXEL_WIDTH * KEY_PIXEL_HEIGHT * 3)

    def _read_key_states(self):
        """
        Reads the key states of the StreamDeck. This is used internally by
        :func:`~StreamDeck._read` to talk to the actual device.

        :rtype: list(bool)
        :return: Button states, with the origin at the top-left of the deck.
        """
        states = self.device.read(1 + self.KEY_COUNT)[1:]
        return [bool(s) for s in states]

    def _reset_key_stream(self):
        """
        Sends a blank key report to the StreamDeck, resetting the key image
        streamer in the device. This prevents previously started partial key
        writes that were not completed from corrupting images sent from this
        application.
        """
        payload = bytearray(self.IMAGE_REPORT_LENGTH)
        payload[0] = 2
        self.device.write(payload)

    def reset(self):
        """
        Resets the StreamDeck, clearing all button images and showing the
        standby image.
        """
        payload = bytearray(17)
        payload[0:2] = [11, 99]
        self.device.write_feature(payload)

    def set_brightness(self, percent):
        """
        Sets the global screen brightness of the StreamDeck, across all the
        physical buttons.

        :param int/float percent: brightness percent, from [0-100] as an `int`,
                                  or normalized to [0.0-1.0] as a `float`.
        """
        if isinstance(percent, float):
            percent = int(100.0 * percent)
        percent = min(max(percent, 0), 100)
        payload = bytearray(17)
        payload[0:6] = [5, 85, 170, 209, 1, percent]
        self.device.write_feature(payload)

    def get_serial_number(self):
        """
        Gets the serial number of the attached StreamDeck.

        :rtype: str
        :return: String containing the serial number of the attached device.
        """
        serial = self.device.read_feature(3, 17)
        return self._extract_string(serial[5:])

    def get_firmware_version(self):
        """
        Gets the firmware version of the attached StreamDeck.

        :rtype: str
        :return: String containing the firmware version of the attached device.
        """
        version = self.device.read_feature(4, 17)
        return self._extract_string(version[5:])

    def set_key_image(self, key, image):
        """
        Sets the image of a button on the StreamDeck to the given image. The
        image being set should be in the correct format for the device, as an
        enumerable collection of bytes.

        .. seealso:: See :func:`~StreamDeck.get_key_image_format` method for
                     information on the image format accepted by the device.

        :param int key: Index of the button whose image is to be updated.
        :param enumerable image: Raw data of the image to set on the button.
                                 If `None`, the key will be cleared to a black
                                 color.
        """
        if min(max(key, 0), self.KEY_COUNT) != key:
            raise IndexError('Invalid key index {}.'.format(key))
        image = bytes(image or self.BLANK_KEY_IMAGE)
        page_number = 0
        bytes_remaining = len(image)
        while bytes_remaining > 0:
            this_length = min(bytes_remaining, self.IMAGE_REPORT_PAYLOAD_LENGTH)
            bytes_sent = page_number * self.IMAGE_REPORT_PAYLOAD_LENGTH
            header = [
             2,
             1,
             page_number,
             0,
             1 if this_length == bytes_remaining else 0,
             key + 1,
             0,
             0,
             0,
             0,
             0,
             0,
             0,
             0,
             0,
             0]
            payload = bytes(header) + image[bytes_sent:bytes_sent + this_length]
            padding = bytearray(self.IMAGE_REPORT_LENGTH - len(payload))
            self.device.write(payload + padding)
            bytes_remaining = bytes_remaining - this_length
            page_number = page_number + 1