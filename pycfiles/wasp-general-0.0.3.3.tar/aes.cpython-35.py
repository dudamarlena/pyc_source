# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/crypto/aes.py
# Compiled at: 2017-10-02 11:08:45
# Size of source mod 2**32: 16206 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
import io, re
from Crypto.Cipher import AES as pyAES
from Crypto.Util import Counter
from abc import ABCMeta, abstractmethod
from wasp_general.verify import verify_type, verify_value
from wasp_general.crypto.random import random_int

class WBlockPadding(metaclass=ABCMeta):
    __doc__ = ' Padding/reverse padding class prototype\n\t'

    @abstractmethod
    @verify_type(data=bytes, block_size=int)
    @verify_value(block_size=lambda x: x > 0)
    def pad(self, data, block_size):
        """ Pad given data to given size

                :param data: data to pad
                :param block_size: size to pad
                :return: bytes
                """
        raise NotImplementedError('This method is abstract')

    @abstractmethod
    @verify_type(data=bytes, block_size=int)
    @verify_value(block_size=lambda x: x > 0)
    def reverse_pad(self, data, block_size):
        """ Remove pads and return original data

                :param data: data to remove pads from
                :param block_size: size data aligned to
                :return: bytes
                """
        raise NotImplementedError('This method is abstract')


class WSimplePadding(WBlockPadding):
    __doc__ = ' Class that pads given data with specified ASCII character\n\t'

    @verify_type(padding=(int, None))
    @verify_value(padding=lambda x: x is None or 0 <= x <= 127)
    def __init__(self, padding=None):
        """ Create new padding class

                :param padding: integer code of ASCII character
                """
        if padding is None:
            padding = 0
        self._WSimplePadding__padding_symbol = bytes([padding])

    def padding_symbol(self):
        """ Return character with witch data is padded

                :return: bytes
                """
        return self._WSimplePadding__padding_symbol

    @verify_type(data=bytes, block_size=int)
    @verify_value(block_size=lambda x: x > 0)
    def pad(self, data, block_size):
        """ :meth:`.WBlockPadding.pad` method implementation
                """
        padding_symbol = self.padding_symbol()
        blocks_count = len(data) // block_size
        if len(data) % block_size != 0:
            blocks_count += 1
        total_length = blocks_count * block_size
        return self._fill(data, total_length, padding_symbol)

    @verify_type(data=bytes, block_size=int)
    @verify_value(block_size=lambda x: x > 0)
    def reverse_pad(self, data, block_size):
        """ :meth:`.WBlockPadding.reverse_pad` method implementation
                """
        return data.rstrip(self.padding_symbol())

    @verify_type(data=bytes, total_length=int, padding_symbol=bytes)
    @verify_value(total_length=lambda x: x > 0, padding_symbol=lambda x: len(x) == 1)
    def _fill(self, data, total_length, padding_symbol):
        """ Append padding symbol to the end of data till specified length is reached

                :param data: data to append to
                :param total_length: target length
                :param padding_symbol: symbol to pad
                :return: bytes
                """
        return data.ljust(total_length, padding_symbol)


class WZeroPadding(WSimplePadding):
    __doc__ = ' Zero padding implementation (just alias for WSimplePadding() object)\n\n\tsee also: https://en.wikipedia.org/wiki/Padding_(cryptography)#Zero_padding\n\t'

    def __init__(self):
        """ Create new padding object
                """
        WSimplePadding.__init__(self)


class WShiftPadding(WSimplePadding):
    __doc__ = ' Same as :class:`.WSimplePadding` class, but also randomly shifts original data.\n\t'

    @verify_type(data=bytes, total_length=int, padding_symbol=bytes)
    @verify_value(total_length=lambda x: x > 0, padding_symbol=lambda x: len(x) == 1)
    def _fill(self, data, total_length, padding_symbol):
        """ Overridden :meth:`.WSimplePadding._fill` method. This methods adds padding symbol at the beginning
                and at the end of the specified data.

                :param data: data to append to
                :param total_length: target length
                :param padding_symbol: symbol to pad
                :return: bytes
                """
        delta = total_length - len(data)
        return (padding_symbol * random_int(delta) + data).ljust(total_length, padding_symbol)

    @verify_type(data=bytes, block_size=int)
    @verify_value(block_size=lambda x: x > 0)
    def reverse_pad(self, data, block_size):
        """ :meth:`.WBlockPadding.reverse_pad` method implementation
                """
        padding_symbol = self.padding_symbol()
        return data.lstrip(padding_symbol).rstrip(padding_symbol)


class WPKCS7Padding(WBlockPadding):
    __doc__ = ' PKCS7 Padding implementation\n\n\tsee also: https://en.wikipedia.org/wiki/Padding_(cryptography)#PKCS7\n\t'

    @verify_type(data=bytes, block_size=int)
    @verify_value(block_size=lambda x: x > 0)
    def pad(self, data, block_size):
        """ :meth:`.WBlockPadding.pad` method implementation
                """
        pad_byte = block_size - len(data) % block_size
        return data + bytes([pad_byte] * pad_byte)

    @verify_type(data=bytes, block_size=int)
    @verify_value(data=lambda x: len(x) > 0, block_size=lambda x: x > 0)
    def reverse_pad(self, data, block_size):
        """ :meth:`.WBlockPadding.reverse_pad` method implementation
                """
        pad_byte = data[(-1)]
        if pad_byte > block_size:
            raise ValueError('Invalid padding')
        padding = bytes([pad_byte] * pad_byte)
        if data[-pad_byte:] != padding:
            raise ValueError('Invalid padding')
        return data[:-pad_byte]


class WAESMode:
    __doc__ = " This class specifies modes of AES encryption. It describes secret key (size and value), block cipher mode\n\tof operation, padding object (:class:`.WBlockPadding` instance), required initialization values. Note,\n\tpadding is required if source data isn't aligned to block size.\n\n\tFor byte-sequence generation (that is used as secret key and initialization values) it is possible to use\n\t:class:`wasp_general.crypto.kdf.WPBKDF2`. :class:`wasp_general.crypto.kdf.WPBKDF2` is a wrapper for PBKDF2\n\tfunction (KDF function that safely generates byte-sequence from the given password and salt)\n\n\tCurrently, only two cipher mode of operation are implemented: 'CBC' and 'CTR'\n\n\tsee also: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation\n\t"
    __data_padding_length__ = pyAES.block_size
    __init_vector_length__ = pyAES.block_size
    __counter_size__ = pyAES.block_size
    __mode_re__ = re.compile('AES(\\-|_)(\\d+)(\\-|_)(\\w+)')
    __valid_key_sizes__ = (16, 24, 32)
    __modes_descriptor__ = {'AES-CBC': {'mode_code': pyAES.MODE_CBC, 
                 'requirements': {'initialization_vector': True, 
                                  'counter': False}}, 
     
     'AES-CTR': {'mode_code': pyAES.MODE_CTR, 
                 'requirements': {'initialization_vector': False, 
                                  'counter': True}}}

    class SequenceChopper:
        __doc__ = " Helper, that chops the given byte-sequence into several separate objects (like secret key,\n\t\tinitialization vector or initialization counter values). The exact values depend on AES key size and\n\t\tblock cipher mode of operation.\n\n\t\tIf length of the given byte-sequence is greater then it is required, then extra bytes discard and\n\t\tthis extra-bytes don't take part in any calculation\n\t\t"

        @verify_type('paranoid', block_cipher_mode=str, key_size=int)
        @verify_type(sequence=bytes)
        @verify_value('paranoid', block_cipher_mode=lambda x: x in WAESMode.__modes_descriptor__.keys())
        def __init__(self, key_size, block_cipher_mode, sequence):
            """ Create new chopper

                        :param key_size: AES secret length
                        :param block_cipher_mode: name of block cipher mode of operation
                        :param sequence: byte-sequence to chop
                        """
            required_length = self.required_sequence_length(key_size, block_cipher_mode)
            self._SequenceChopper__key_size = key_size
            self._SequenceChopper__mode = block_cipher_mode
            self._SequenceChopper__sequence = sequence
            if required_length > 0 and len(self._SequenceChopper__sequence) < required_length:
                raise ValueError('Initialization byte-sequence too short. Must be at least %i bytes long' % required_length)

        def secret(self):
            """ Return AES secret generated from the initial byte-sequence

                        :return: bytes
                        """
            return self._SequenceChopper__sequence[:self._SequenceChopper__key_size]

        def initialization_vector(self):
            """ Return initialization vector generated from the initial byte-sequence if it is required
                        by the current block cipher mode of operation. If it doesn't require - then None is returned

                        :return: bytes or None
                        """
            req = self._SequenceChopper__requirements()
            if req['initialization_vector'] is not True:
                return
            start_position = self._SequenceChopper__key_size
            end_position = start_position + WAESMode.__init_vector_length__
            return self._SequenceChopper__sequence[start_position:end_position]

        def initialization_counter_value(self):
            """ Return initialization counter value generated from the initial byte-sequence if it is
                        required by the current block cipher mode of operation. If it doesn't require - then None
                        is returned

                        :return: int or None
                        """
            req = self._SequenceChopper__requirements()
            if req['counter'] is not True:
                return
            start_position = self._SequenceChopper__key_size
            if req['initialization_vector'] is True:
                start_position += WAESMode.__init_vector_length__
            end_position = start_position + WAESMode.__counter_size__
            seq = self._SequenceChopper__sequence[start_position:end_position]
            return int.from_bytes(seq, byteorder='big')

        def __requirements(self):
            """ Return requirements specification (just shortcut to access specific mode requirements from
                        WAESMode.__modes_descriptor__)

                        :return: dict
                        """
            return WAESMode.__modes_descriptor__[self._SequenceChopper__mode]['requirements']

        @classmethod
        @verify_type(key_size=int, block_cipher_mode=str)
        @verify_value(key_size=lambda x: x in WAESMode.__valid_key_sizes__)
        @verify_value(block_cipher_mode=lambda x: x in WAESMode.__modes_descriptor__.keys())
        def required_sequence_length(cls, key_size, block_cipher_mode):
            """ Calculate required byte-sequence length

                        :param key_size: AES secret length
                        :param block_cipher_mode: name of block cipher mode of operation to calculate for

                        :return: int
                        """
            req = WAESMode.__modes_descriptor__[block_cipher_mode]['requirements']
            result = key_size
            if req['initialization_vector'] is True:
                result += WAESMode.__init_vector_length__
            if req['counter'] is True:
                result += WAESMode.__counter_size__
            return result

    @verify_type(key_size=int, block_cipher_mode=str, padding=(None, WBlockPadding), init_sequence=bytes)
    @verify_value(key_size=lambda x: x in WAESMode.__valid_key_sizes__)
    @verify_value(block_cipher_mode=lambda x: x in WAESMode.__modes_descriptor__.keys())
    def __init__(self, key_size, block_cipher_mode, init_sequence, padding=None):
        """ Create new AES-mode.

                :param key_size: secret length
                :param block_cipher_mode: name of block cipher mode of operation
                :param padding: padding object (if required)
                :param init_sequence: AES secret with initialization vector or counter value
                """
        self._WAESMode__key_size = key_size
        self._WAESMode__mode = block_cipher_mode
        self._WAESMode__padding = padding
        self._WAESMode__sequence_chopper = WAESMode.SequenceChopper(key_size, block_cipher_mode, init_sequence)
        self._WAESMode__cipher_args = (self._WAESMode__sequence_chopper.secret(),)
        self._WAESMode__cipher_kwargs = {}
        cipher_descriptor = WAESMode.__modes_descriptor__[block_cipher_mode]
        self._WAESMode__cipher_kwargs['mode'] = cipher_descriptor['mode_code']
        iv = self._WAESMode__sequence_chopper.initialization_vector()
        if iv is not None:
            self._WAESMode__cipher_kwargs['IV'] = iv
        counter = self._WAESMode__sequence_chopper.initialization_counter_value()
        if counter is not None:
            self._WAESMode__cipher_kwargs['counter'] = Counter.new(WAESMode.__counter_size__ * 8, initial_value=counter)

    def key_size(self):
        """ Return cipher secret key size

                :return: int
                """
        return self._WAESMode__key_size

    def mode(self):
        """ Return block cipher mode of operation name

                :return:
                """
        return self._WAESMode__mode

    def padding(self):
        """ Return padding object

                :return: WBlockPadding or None
                """
        return self._WAESMode__padding

    def initialization_vector(self):
        """ Return currently used initialization vector or None if vector is not used

                :return: bytes or None
                """
        return self._WAESMode__sequence_chopper.initialization_vector()

    def initialization_counter_value(self):
        """ Return currently used initialization counter value or None if counter is not used

                :return: int or None
                """
        return self._WAESMode__sequence_chopper.initialization_counter_value()

    def pyaes_args(self):
        """ Generate and return position-dependent arguments, that are used in :meth:`.AES.new` method

                :return: tuple
                """
        return self._WAESMode__cipher_args

    def pyaes_kwargs(self):
        """ Generate and return position-independent (named) arguments, that are used in :meth:`.AES.new` method

                :return: dict
                """
        return self._WAESMode__cipher_kwargs

    @classmethod
    def init_sequence_length(cls, key_size, block_cipher_mode):
        """ Return required byte-sequence length

                :param key_size: secret size
                :param block_cipher_mode: name of block cipher mode of operation

                :return: int
                """
        return WAESMode.SequenceChopper.required_sequence_length(key_size, block_cipher_mode)

    @classmethod
    @verify_type(name=str)
    def parse_cipher_name(cls, name):
        """ Parse cipher name (name like 'aes_256_cbc' or 'AES-128-CTR'). Also this method validates If the
                cipher is supported by this class. If no - exception is raised

                :param name: name to parse

                :return: tuple where the first element is a key size in bytes (int) and the second element - block cipher mode
                of operation (str) (for example: (16, 'AES-CTR') or (24, 'AES-CBC'))
                """
        r = cls.__mode_re__.match(name.upper())
        if r is None:
            raise ValueError('Unable to find suitable cipher for: "%s"' % name)
        key_size = int(int(r.group(2)) / 8)
        block_mode = 'AES-%s' % r.group(4)
        if key_size not in cls.__valid_key_sizes__:
            raise ValueError('Unsupported secret length: "%i"' % key_size)
        if block_mode not in cls.__modes_descriptor__.keys():
            raise ValueError('Unsupported block cipher mode of operation: "%s"' % block_mode)
        return (
         key_size, block_mode)


class WAES:
    __doc__ = ' PyCrypto AES-encryption wrapper\n\t'

    @verify_type(mode=WAESMode)
    def __init__(self, mode):
        """ Create new AES cipher with specified mode

                :param mode: AES mode
                """
        self._WAES__mode = mode

    def mode(self):
        """ Return AES mode

                :return: WAESMode
                """
        return self._WAES__mode

    def cipher(self):
        """ Generate AES-cipher

                :return: Crypto.Cipher.AES.AESCipher
                """
        cipher = pyAES.new(*self.mode().pyaes_args(), **self.mode().pyaes_kwargs())
        return cipher

    @verify_type(data=(str, bytes))
    def encrypt(self, data):
        """ Encrypt the given data with cipher that is got from AES.cipher call.

                :param data: data to encrypt
                :return: bytes
                """
        padding = self.mode().padding()
        if padding is not None:
            data = padding.pad(data, WAESMode.__data_padding_length__)
        return self.cipher().encrypt(data)

    @verify_type(data=bytes, decode=bool)
    def decrypt(self, data, decode=False):
        """ Decrypt the given data with cipher that is got from AES.cipher call.

                :param data: data to decrypt
                :param decode: whether to decode bytes to str or not
                :return: bytes or str (depends on decode flag)
                """
        result = self.cipher().decrypt(data)
        padding = self.mode().padding()
        if padding is not None:
            result = padding.reverse_pad(result, WAESMode.__data_padding_length__)
        if decode:
            return result.decode()
        return result