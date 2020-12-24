# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hermit/errors.py
# Compiled at: 2019-07-11 16:56:25
# Size of source mod 2**32: 438 bytes


class HermitError(Exception):
    __doc__ = 'Generic Hermit Error'


class InvalidSignatureRequest(HermitError):
    __doc__ = 'Signature request was not valid'

    def __init__(self, message: str) -> None:
        """Initialize a new `InvalidSignatureRequest`

        :param message: more details on the error.
        """
        HermitError.__init__(self, 'Invalid signature request: {}.'.format(message))