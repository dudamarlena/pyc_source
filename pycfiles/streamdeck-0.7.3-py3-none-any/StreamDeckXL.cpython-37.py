# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Dean\Documents\Python\python-elgato-streamdeck\src\StreamDeck\Devices\StreamDeckXL.py
# Compiled at: 2020-04-11 03:11:41
# Size of source mod 2**32: 9893 bytes
from .StreamDeck import StreamDeck

class StreamDeckXL(StreamDeck):
    __doc__ = '\n    Represents a physically attached StreamDeck Original device.\n    '
    KEY_COUNT = 32
    KEY_COLS = 8
    KEY_ROWS = 4
    KEY_PIXEL_WIDTH = 96
    KEY_PIXEL_HEIGHT = 96
    KEY_IMAGE_FORMAT = 'JPEG'
    KEY_FLIP = (True, True)
    KEY_ROTATION = 0
    DECK_TYPE = 'Stream Deck XL'
    IMAGE_REPORT_LENGTH = 1024
    IMAGE_REPORT_HEADER_LENGTH = 8
    IMAGE_REPORT_PAYLOAD_LENGTH = IMAGE_REPORT_LENGTH - IMAGE_REPORT_HEADER_LENGTH
    BLANK_KEY_IMAGE = [
     255, 216, 255, 224, 0, 16, 74, 70, 73, 70, 0, 1, 1, 0, 0, 1, 0, 1, 0,
     0, 255, 219, 0, 67, 0, 8, 6, 6, 7, 6, 5, 8, 7, 7, 7, 9, 9, 8,
     10, 12, 20, 13, 12, 11, 11, 12, 25, 18, 19, 15, 20, 29, 26, 31, 30, 29, 26,
     28, 28, 32, 36, 46, 39, 32, 34, 44, 35, 28, 28, 40, 55, 41, 44, 48, 49, 52,
     52, 52, 31, 39, 57, 61, 56, 50, 60, 46, 51, 52, 50, 255, 219, 0, 67, 1, 9,
     9, 9, 12, 11, 12, 24, 13, 13, 24, 50, 33, 28, 33, 50, 50, 50, 50, 50, 50,
     50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50,
     50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50,
     50, 50, 50, 50, 50, 50, 255, 192, 0, 17, 8, 0, 96, 0, 96, 3, 1, 34, 0,
     2, 17, 1, 3, 17, 1, 255, 196, 0, 31, 0, 0, 1, 5, 1, 1, 1, 1, 1,
     1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
     11, 255, 196, 0, 181, 16, 0, 2, 1, 3, 3, 2, 4, 3, 5, 5, 4, 4, 0,
     0, 1, 125, 1, 2, 3, 0, 4, 17, 5, 18, 33, 49, 65, 6, 19, 81, 97, 7,
     34, 113, 20, 50, 129, 145, 161, 8, 35, 66, 177, 193, 21, 82, 209, 240, 36, 51, 98,
     114, 130, 9, 10, 22, 23, 24, 25, 26, 37, 38, 39, 40, 41, 42, 52, 53, 54, 55,
     56, 57, 58, 67, 68, 69, 70, 71, 72, 73, 74, 83, 84, 85, 86, 87, 88, 89, 90,
     99, 100, 101, 102, 103, 104, 105, 106, 115, 116, 117, 118, 119, 120, 121, 122, 131, 132, 133,
     134, 135, 136, 137, 138, 146, 147, 148, 149, 150, 151, 152, 153, 154, 162, 163, 164, 165, 166,
     167, 168, 169, 170, 178, 179, 180, 181, 182, 183, 184, 185, 186, 194, 195, 196, 197, 198, 199,
     200, 201, 202, 210, 211, 212, 213, 214, 215, 216, 217, 218, 225, 226, 227, 228, 229, 230, 231,
     232, 233, 234, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 255, 196, 0, 31, 1, 0,
     3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 2, 3,
     4, 5, 6, 7, 8, 9, 10, 11, 255, 196, 0, 181, 17, 0, 2, 1, 2, 4, 4,
     3, 4, 7, 5, 4, 4, 0, 1, 2, 119, 0, 1, 2, 3, 17, 4, 5, 33, 49,
     6, 18, 65, 81, 7, 97, 113, 19, 34, 50, 129, 8, 20, 66, 145, 161, 177, 193, 9,
     35, 51, 82, 240, 21, 98, 114, 209, 10, 22, 36, 52, 225, 37, 241, 23, 24, 25, 26,
     38, 39, 40, 41, 42, 53, 54, 55, 56, 57, 58, 67, 68, 69, 70, 71, 72, 73, 74,
     83, 84, 85, 86, 87, 88, 89, 90, 99, 100, 101, 102, 103, 104, 105, 106, 115, 116, 117,
     118, 119, 120, 121, 122, 130, 131, 132, 133, 134, 135, 136, 137, 138, 146, 147, 148, 149, 150,
     151, 152, 153, 154, 162, 163, 164, 165, 166, 167, 168, 169, 170, 178, 179, 180, 181, 182, 183,
     184, 185, 186, 194, 195, 196, 197, 198, 199, 200, 201, 202, 210, 211, 212, 213, 214, 215, 216,
     217, 218, 226, 227, 228, 229, 230, 231, 232, 233, 234, 242, 243, 244, 245, 246, 247, 248, 249,
     250, 255, 218, 0, 12, 3, 1, 0, 2, 17, 3, 17, 0, 63, 0, 249, 254, 138, 40,
     160, 2, 138, 40, 160, 2, 138, 40, 160, 2, 138, 40, 160, 2, 138, 40, 160, 2, 138,
     40, 160, 2, 138, 40, 160, 2, 138, 40, 160, 2, 138, 40, 160, 2, 138, 40, 160, 2,
     138, 40, 160, 2, 138, 40, 160, 2, 138, 40, 160, 2, 138, 40, 160, 2, 138, 40, 160,
     2, 138, 40, 160, 2, 138, 40, 160, 2, 138, 40, 160, 2, 138, 40, 160, 2, 138, 40,
     160, 2, 138, 40, 160, 2, 138, 40, 160, 2, 138, 40, 160, 2, 138, 40, 160, 2, 138,
     40, 160, 2, 138, 40, 160, 2, 138, 40, 160, 2, 138, 40, 160, 2, 138, 40, 160, 2,
     138, 40, 160, 2, 138, 40, 160, 2, 138, 40, 160, 2, 138, 40, 160, 2, 138, 40, 160,
     2, 138, 40, 160, 2, 138, 40, 160, 15, 255, 217]

    def _read_key_states(self):
        """
        Reads the key states of the StreamDeck. This is used internally by
        :func:`~StreamDeck._read` to talk to the actual device.

        :rtype: list(bool)
        :return: Button states, with the origin at the top-left of the deck.
        """
        states = self.device.read(4 + self.KEY_COUNT)[4:]
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
        payload = bytearray(32)
        payload[0:2] = [3, 2]
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
        payload = bytearray(32)
        payload[0:2] = [3, 8, percent]
        self.device.write_feature(payload)

    def get_serial_number(self):
        """
        Gets the serial number of the attached StreamDeck.

        :rtype: str
        :return: String containing the serial number of the attached device.
        """
        serial = self.device.read_feature(6, 32)
        return self._extract_string(serial[2:])

    def get_firmware_version(self):
        """
        Gets the firmware version of the attached StreamDeck.

        :rtype: str
        :return: String containing the firmware version of the attached device.
        """
        version = self.device.read_feature(5, 32)
        return self._extract_string(version[6:])

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
             7,
             key,
             1 if this_length == bytes_remaining else 0,
             this_length & 255,
             this_length >> 8,
             page_number & 255,
             page_number >> 8]
            payload = bytes(header) + image[bytes_sent:bytes_sent + this_length]
            padding = bytearray(self.IMAGE_REPORT_LENGTH - len(payload))
            self.device.write(payload + padding)
            bytes_remaining = bytes_remaining - this_length
            page_number = page_number + 1