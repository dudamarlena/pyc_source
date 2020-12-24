# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opencontainers/digest/exceptions.py
# Compiled at: 2019-11-04 13:56:08
# Size of source mod 2**32: 975 bytes


class ErrDigestInvalidFormat(Exception):
    __doc__ = 'ErrDigestInvalidFormat returned when digest format invalid.\n    '

    def __init__(self, message, errors):
        super().__init__('invalid checksum digest format')
        self.errors = errors


class ErrDigestInvalidLength(Exception):
    __doc__ = 'ErrDigestInvalidLength returned when digest has invalid length.\n    '

    def __init__(self, message, errors):
        super().__init__('invalid checksum digest length')
        self.errors = errors


class ErrDigestUnsupported(Exception):
    __doc__ = 'returned when the digest algorithm is unsupported.\n    '

    def __init__(self, message, errors):
        super().__init__('unsupported digest algorithm')
        self.errors = errors