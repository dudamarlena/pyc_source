# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\cos\PycharmProjects\python_winapi_hook\dllhook\mayhem\mayhem\utilities.py
# Compiled at: 2018-04-24 03:00:55
import ctypes, os, sys, boltons.iterutils

def architecture_is_32bit(arch):
    """
        Check if the architecture specified in *arch* is 32-bit.

        :param str arch: The value to check.
        :rtype: bool
        """
    return bool(arch.lower() in ('i386', 'i686', 'x86'))


def architecture_is_64bit(arch):
    """
        Check if the architecture specified in *arch* is 64-bit.

        :param str arch: The value to check.
        :rtype: bool
        """
    return bool(arch.lower() in ('amd64', 'x86_64'))


def align_down(number, alignment=16):
    """
        Subtract from *number* so it is divisible by *alignment*.

        :param int number: The value to decrease.
        :param int alignment: The value to make *number* divisible by.
        :return: The modified value.
        :rtype: int
        """
    return number - number % alignment


def align_up(number, alignment=16):
    """
        Add to *number* so it is divisible by *alignment*.

        :param int number: The value to increase.
        :param int alignment: The value to make *number* divisible by.
        :return: The modified value.
        :rtype: int
        """
    if number % alignment:
        return number + (alignment - number % alignment)
    else:
        return number


def eval_number(number):
    """
        Evaluate a numerical expressions in different string formats indicating
        base.

        :param str number: The string to evaluate.
        :return: The converted value.
        :rtype: int
        """
    if number.startswith('0b'):
        return int(number[2:], 2)
    if number.startswith('0x'):
        return int(number[2:], 16)
    if number.startswith('0'):
        return int(number, 8)
    if number.isdigit():
        return int(number)
    raise ValueError("unknown numerical value: '" + number + "'")


def print_hexdump(data, address=0, stream=None):
    """
        Print data to stdout in a visually pleasant hex format.

        :param str data: The data to print.
        :param int address: The base address to display for *data*.
        :param stream: The object to write the data to be displayed to.
        """
    stream = stream or sys.stdout
    data = bytearray(data)
    divider = 8
    chunk_size = 16
    for row, chunk in enumerate(boltons.iterutils.chunked(data, chunk_size, fill=-1)):
        offset_col = ('{0:04x}').format(row * chunk_size + address)
        ascii_col = ''
        hex_col = ''
        pos = 0
        for pos, byte in enumerate(chunk):
            hex_col += '   ' if byte == -1 else ('{0:02x} ').format(byte)
            if divider and pos and (pos + 1) % divider == 0:
                hex_col += ' '
            if byte == -1:
                ascii_col += ' '
            elif byte < 32 or byte > 126:
                ascii_col += '.'
            else:
                ascii_col += chr(byte)
            if divider and pos and (pos + 1) % divider == 0:
                ascii_col += ' '

        hex_col = hex_col[:-2 if pos and (pos + 1) % divider == 0 else -1]
        stream.write(('  ').join((offset_col, hex_col, ascii_col)) + os.linesep)

    stream.flush()


def struct_pack(structure):
    """
        Pack a :py:class:`ctypes.Structure` object and convert it to a packed string.

        :param structure: The structure instance to convert
        :type structure: :py:class:`ctypes.Structure`
        :return: The structure instance converted to a string.
        :rtype: str
        """
    return ctypes.string_at(ctypes.byref(structure), ctypes.sizeof(structure))


def struct_unpack(structure, raw_data):
    """
        Convert *raw_data* to an instance of *structure*.

        :param structure: The structure that describes *raw_data*.
        :type structure: :py:class:`ctypes.Structure`
        :param str raw_data: The binary string which contains the structures data.
        :return: A new instance of *structure*.
        :rtype: :py:class:`ctypes.Structure`
        """
    if not isinstance(structure, ctypes.Structure):
        structure = structure()
    ctypes.memmove(ctypes.byref(structure), raw_data, ctypes.sizeof(structure))
    return structure


def bytes_to_ctarray(bytes_):
    """
        Convert a bytes object into a ctypes array.

        :param bytes bytes_: The bytes object to convert.
        :return: The converted byte array.
        """
    ctarray = (ctypes.c_byte * len(bytes_))()
    ctypes.memmove(ctypes.byref(ctarray), bytes_, len(bytes_))
    return ctarray


def ctarray_to_bytes(ctarray):
    """
        Convert ctypes array into a bytes object.

        :param ctarray: The ctypes array to convert.
        :return: The converted ctypes array.
        :rtype: bytes
        """
    if not len(ctarray):
        return bytes()
    bytes_ = buffer(ctarray) if sys.version_info[0] < 3 else bytes(ctarray)
    return bytes_[:]