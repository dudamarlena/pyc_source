# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgp/packets/user_attribute_subpackets.py
# Compiled at: 2015-08-31 08:17:33
from pgp.packets import constants
from pgp import utils

class UserAttributeSubpacket(object):

    @classmethod
    def from_subpacket_content(cls, sub_type, sub_data):
        return cls(sub_type)

    def __init__(self, sub_type):
        self.sub_type = sub_type

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.sub_type == other.sub_type

    @property
    def content(self):
        return bytearray()

    def __bytes__(self):
        data = self.content
        result = bytearray()
        result.extend(utils.new_packet_length_to_bytes(len(data) + 1, False)[0])
        result.append(self.sub_type)
        result.extend(data)
        return bytes(result)


class ImageAttributeSubpacket(UserAttributeSubpacket):

    @classmethod
    def from_subpacket_content(cls, sub_type, sub_data, parse_unknown=False):
        header_length = sub_data[0] + (sub_data[1] << 8)
        header_version = sub_data[2]
        image_format = None
        if header_version == 1:
            if not header_length == 16:
                raise ValueError
            image_format = sub_data[3]
            if any(sub_data[4:16]):
                raise ValueError
            content_data = sub_data[header_length:]
        else:
            if parse_unknown:
                content_data = sub_data[header_length:]
            else:
                raise ValueError
        return cls(header_version, header_length, image_format, content_data)

    def __init__(self, header_version, header_length, image_format, content_data):
        UserAttributeSubpacket.__init__(self, constants.IMAGE_ATTRIBUTE_SUBPACKET_TYPE)
        self.header_version = header_version
        self.header_length = header_length
        self.image_format = image_format
        self.data = content_data

    def __eq__(self, other):
        return super(ImageAttributeSubpacket, self).__eq__(other) and self.header_version == other.header_version and self.header_length == other.header_length and self.image_format == other.image_format and self.data == other.data

    @property
    def content(self):
        result = bytearray([
         self.header_length & 255,
         self.header_length >> 8 & 255,
         self.header_version])
        if self.image_format is not None:
            result.append(self.image_format)
            result.extend([0] * (self.header_length - 4))
        else:
            result.extend([0] * (self.header_length - 3))
        result.extend(self.data)
        return result


USER_ATTRIBUTE_SUBPACKET_TYPES = {constants.IMAGE_ATTRIBUTE_SUBPACKET_TYPE: ImageAttributeSubpacket}

def user_attribute_subpacket_from_data(data, offset=0):
    sub_data = bytearray()
    offset, sub_len, sub_partial = utils.new_packet_length(data, offset)
    if sub_partial:
        raise ValueError
    sub_type = int(data[offset])
    sub_data_start = offset + 1
    sub_data_end = sub_data_start + sub_len - 1
    sub_data.extend(data[sub_data_start:sub_data_end])
    offset = sub_data_end
    cls = USER_ATTRIBUTE_SUBPACKET_TYPES.get(sub_type, UserAttributeSubpacket)
    return (cls.from_subpacket_content(sub_type, sub_data), offset)