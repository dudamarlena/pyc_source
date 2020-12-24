# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/swistakm/dev/graceful/build/lib/graceful/errors.py
# Compiled at: 2015-07-14 08:27:35
# Size of source mod 2**32: 1533 bytes
from falcon import HTTPBadRequest

class DeserializationError(ValueError):
    __doc__ = '\n    Raised when error happened during deserialization of object\n    '

    def __init__(self, missing=None, forbidden=None, invalid=None, failed=None):
        self.missing = missing
        self.forbidden = forbidden
        self.invalid = invalid
        self.failed = failed

    def as_bad_request(self):
        return HTTPBadRequest(title='Representation deserialization failed', description=self._get_description())

    def _get_description(self):
        """
        Return human readable description that explains everything that
        went wrong with deserialization.

        """
        return ', '.join([part for part in [
         'missing: {}'.format(self.missing) if self.missing else '',
         'forbidden: {}'.format(self.forbidden) if self.forbidden else '',
         'invalid: {}:'.format(self.invalid) if self.invalid else '',
         'failed to parse: {}'.format(self.failed) if self.failed else ''] if part])


class ValidationError(ValueError):
    __doc__ = 'Raised when validation error occured'

    def as_bad_request(self):
        return HTTPBadRequest(title='Validation failed deserialization failed', description=str(self))