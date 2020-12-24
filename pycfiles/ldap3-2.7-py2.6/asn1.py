# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\utils\asn1.py
# Compiled at: 2020-02-23 02:04:04
"""
"""
from pyasn1 import __version__ as pyasn1_version
from pyasn1.codec.ber import decoder
from pyasn1.codec.ber.encoder import Encoder
from ..core.results import RESULT_CODES
from ..utils.conv import to_unicode
from ..protocol.convert import referrals_to_list
CLASSES = {(False, False): 0, (False, True): 1, 
   (True, False): 2, 
   (True, True): 3}
if pyasn1_version == 'xxx0.2.3':
    from pyasn1.codec.ber.encoder import tagMap, BooleanEncoder, encode
    from pyasn1.type.univ import Boolean
    from pyasn1.compat.octets import ints2octs

    class BooleanCEREncoder(BooleanEncoder):
        _true = ints2octs((255, ))


    tagMap[Boolean.tagSet] = BooleanCEREncoder()
else:
    from pyasn1.codec.ber.encoder import tagMap, typeMap, AbstractItemEncoder
    from pyasn1.type.univ import Boolean
    from copy import deepcopy

    class LDAPBooleanEncoder(AbstractItemEncoder):
        supportIndefLenMode = False
        if pyasn1_version <= '0.2.3':
            from pyasn1.compat.octets import ints2octs
            _true = ints2octs((255, ))
            _false = ints2octs((0, ))

            def encodeValue(self, encodeFun, value, defMode, maxChunkSize):
                return (value and self._true or self._false, 0)

        elif pyasn1_version <= '0.3.1':

            def encodeValue(self, encodeFun, value, defMode, maxChunkSize):
                return (
                 value and (255, ) or (0, ), False, False)

        elif pyasn1_version <= '0.3.4':

            def encodeValue(self, encodeFun, value, defMode, maxChunkSize, ifNotEmpty=False):
                return (value and (255, ) or (0, ), False, False)

        elif pyasn1_version <= '0.3.7':

            def encodeValue(self, value, encodeFun, **options):
                return (
                 value and (255, ) or (0, ), False, False)

        else:

            def encodeValue(self, value, asn1Spec, encodeFun, **options):
                return (
                 value and (255, ) or (0, ), False, False)


    customTagMap = deepcopy(tagMap)
    customTypeMap = deepcopy(typeMap)
    customTagMap[Boolean.tagSet] = LDAPBooleanEncoder()
    customTypeMap[Boolean.typeId] = LDAPBooleanEncoder()
    encode = Encoder(customTagMap, customTypeMap)

def compute_ber_size(data):
    """
    Compute size according to BER definite length rules
    Returns size of value and value offset
    """
    if data[1] <= 127:
        return (data[1], 2)
    else:
        bytes_length = data[1] - 128
        value_length = 0
        cont = bytes_length
        for byte in data[2:2 + bytes_length]:
            cont -= 1
            value_length += byte * 256 ** cont

        return (
         value_length, bytes_length + 2)


def decode_message_fast(message):
    (ber_len, ber_value_offset) = compute_ber_size(get_bytes(message[:10]))
    decoded = decode_sequence(message, ber_value_offset, ber_len + ber_value_offset, LDAP_MESSAGE_CONTEXT)
    return {'messageID': decoded[0][3], 
       'protocolOp': decoded[1][2], 
       'payload': decoded[1][3], 
       'controls': decoded[2][3] if len(decoded) == 3 else None}


def decode_sequence(message, start, stop, context_decoders=None):
    decoded = []
    while start < stop:
        octet = get_byte(message[start])
        ber_class = CLASSES[(bool(octet & 128), bool(octet & 64))]
        ber_constructed = bool(octet & 32)
        ber_type = octet & 31
        ber_decoder = DECODERS[(ber_class, octet & 31)] if ber_class < 2 else None
        (ber_len, ber_value_offset) = compute_ber_size(get_bytes(message[start:start + 10]))
        start += ber_value_offset
        if ber_decoder:
            value = ber_decoder(message, start, start + ber_len, context_decoders)
        else:
            value = context_decoders[ber_type](message, start, start + ber_len)
        decoded.append((ber_class, ber_constructed, ber_type, value))
        start += ber_len

    return decoded


def decode_integer(message, start, stop, context_decoders=None):
    first = message[start]
    value = -1 if get_byte(first) & 128 else 0
    for octet in message[start:stop]:
        value = value << 8 | get_byte(octet)

    return value


def decode_octet_string(message, start, stop, context_decoders=None):
    return message[start:stop]


def decode_boolean(message, start, stop, context_decoders=None):
    if message[start:stop] == 0:
        return False
    return True


def decode_bind_response(message, start, stop, context_decoders=None):
    return decode_sequence(message, start, stop, BIND_RESPONSE_CONTEXT)


def decode_extended_response(message, start, stop, context_decoders=None):
    return decode_sequence(message, start, stop, EXTENDED_RESPONSE_CONTEXT)


def decode_intermediate_response(message, start, stop, context_decoders=None):
    return decode_sequence(message, start, stop, INTERMEDIATE_RESPONSE_CONTEXT)


def decode_controls(message, start, stop, context_decoders=None):
    return decode_sequence(message, start, stop, CONTROLS_CONTEXT)


def ldap_result_to_dict_fast(response):
    response_dict = dict()
    response_dict['result'] = int(response[0][3])
    response_dict['description'] = RESULT_CODES[response_dict['result']]
    response_dict['dn'] = to_unicode(response[1][3], from_server=True)
    response_dict['message'] = to_unicode(response[2][3], from_server=True)
    if len(response) == 4:
        response_dict['referrals'] = referrals_to_list([ to_unicode(referral[3], from_server=True) for referral in response[3][3] ])
    else:
        response_dict['referrals'] = None
    return response_dict


if str is not bytes:

    def get_byte(x):
        return x


    def get_bytes(x):
        return x


else:

    def get_byte(x):
        return ord(x)


    def get_bytes(x):
        return bytearray(x)


DECODERS = {(0, 1): decode_boolean, 
   (0, 2): decode_integer, 
   (0, 4): decode_octet_string, 
   (0, 10): decode_integer, 
   (0, 16): decode_sequence, 
   (0, 17): decode_sequence, 
   (1, 1): decode_bind_response, 
   (1, 4): decode_sequence, 
   (1, 5): decode_sequence, 
   (1, 7): decode_sequence, 
   (1, 9): decode_sequence, 
   (1, 11): decode_sequence, 
   (1, 13): decode_sequence, 
   (1, 15): decode_sequence, 
   (1, 19): decode_sequence, 
   (1, 24): decode_extended_response, 
   (1, 25): decode_intermediate_response, 
   (2, 3): decode_octet_string}
BIND_RESPONSE_CONTEXT = {7: decode_octet_string}
EXTENDED_RESPONSE_CONTEXT = {10: decode_octet_string, 
   11: decode_octet_string}
INTERMEDIATE_RESPONSE_CONTEXT = {0: decode_octet_string, 
   1: decode_octet_string}
LDAP_MESSAGE_CONTEXT = {0: decode_controls, 
   3: decode_sequence}
CONTROLS_CONTEXT = {0: decode_sequence}