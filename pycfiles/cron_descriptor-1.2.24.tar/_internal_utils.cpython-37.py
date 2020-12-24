# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-install-65c3rg8f/requests/requests/_internal_utils.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 1096 bytes
__doc__ = '\nrequests._internal_utils\n~~~~~~~~~~~~~~\n\nProvides utility functions that are consumed internally by Requests\nwhich depend on extremely few external helpers (such as compat)\n'
from .compat import is_py2, builtin_str, str

def to_native_string(string, encoding='ascii'):
    """Given a string object, regardless of type, returns a representation of
    that string in the native string type, encoding and decoding where
    necessary. This assumes ASCII unless told otherwise.
    """
    if isinstance(string, builtin_str):
        out = string
    elif is_py2:
        out = string.encode(encoding)
    else:
        out = string.decode(encoding)
    return out


def unicode_is_ascii(u_string):
    """Determine if unicode string only contains ASCII characters.

    :param str u_string: unicode string to check. Must be unicode
        and not Python 2 `str`.
    :rtype: bool
    """
    assert isinstance(u_string, str)
    try:
        u_string.encode('ascii')
        return True
    except UnicodeEncodeError:
        return False