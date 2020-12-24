# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/context/missing.py
# Compiled at: 2015-09-01 07:17:44
from __future__ import unicode_literals
from __future__ import print_function
from ..compat import text_type, implements_to_string, implements_bool

def is_missing(obj):
    """Check if an object is missing"""
    return getattr(obj, b'moya_missing', False)


@implements_bool
@implements_to_string
class Missing(object):
    """A value indicating a missing value in the context"""
    moya_missing = True

    def __init__(self, key):
        self.key = text_type(key)

    @classmethod
    def check(cls, obj):
        """Check if an object is missing"""
        return getattr(obj, b'moya_missing', False)

    def __moyajson__(self):
        return

    def __str__(self):
        return b''

    def __int__(self):
        return 0

    def __float__(self):
        return 0.0

    def __repr__(self):
        return b"<missing '%s'>" % self.key

    def __moyaconsole__(self, console):
        console.text((b"<missing '{}'>").format(self.key), italic=True, bold=True, fg=b'yellow')

    def __bool__(self):
        return False

    def __getitem__(self, key):
        return self

    def __setitem__(self, key, value):
        raise ValueError((b'{!r} does not support item assignment').format(self))

    def __iter__(self):
        return iter([])

    def __contains__(self, key):
        return False

    def __len__(self):
        return 0


class MoyaAttributeError(Missing):

    def __init__(self, e):
        self._e = e

    def __repr__(self):
        return (b'<error ({})>').format(self._e)

    def __moyarepr__(self, context):
        return (b'<error ({})>').format(self._e)

    def __moyaconsole__(self, console):
        return console.error((b'<error ({})>').format(self._e))


if __name__ == b'__main__':
    m = Missing(b'foo.bar')
    print(repr(m))
    print(text_type(m))
    print(len(m))