# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bfnet/util.py
# Compiled at: 2015-11-23 15:02:13
# Size of source mod 2**32: 2151 bytes
__doc__ = '\nMisc utils for deep internal usage of Python.\n'
import struct

def infer_int_pack(arg) -> str:
    """
    Attempt to infer the correct struct format for an int.
    :param arg: The integer argument to infer.
    :return: A character for the struct string.
    """
    if -32768 <= arg <= 32767:
        return 'h'
    if -2147483648 <= arg <= 2147483647:
        return 'i'
    if -18446744073709551616 <= arg <= 18446744073709551615:
        return 'q'
    raise OverflowError('Number {} too big to fit into a struct normally'.format(arg))


def _process_args(*args):
    a = []
    for arg in args:
        if isinstance(arg, str):
            for _ in arg:
                a.append(_)

        elif isinstance(arg, bytes):
            for _ in arg:
                a.append(_.to_bytes(1, 'big'))

        else:
            a.append(arg)

    return tuple(a)


def auto_infer_struct_pack(*args, pack: bool=False) -> str:
    """
    This will automatically attempt to infer the struct pack/unpack format string
    from the types of your arguments.

    All integer values will be set as unsigned by default.

    :param pack: Should we automatically pack your data up?
    :param args: The items to infer from.
    :return: Either the string format string, or the packed bytes data.
    """
    fmt_string = '!'
    for arg in args:
        if type(arg) == int:
            fmt_string += infer_int_pack(arg)
        elif type(arg) == float:
            fmt_string += 'd'
        elif type(arg) == str:
            fmt_string += '{}s'.format(len(arg))
        elif type(arg) == bytes:
            fmt_string += '{}c'.format(len(arg))
        elif type(arg) == bool:
            fmt_string += '?'
        else:
            raise ValueError('Type could not be determined - {}'.format(type(arg)))

    if not pack:
        return fmt_string
    s = struct.pack(fmt_string, *_process_args(*args))
    return s