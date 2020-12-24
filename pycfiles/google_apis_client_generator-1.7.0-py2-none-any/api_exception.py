# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dsupplee/dev/apis-client-generator/src/googleapis/codegen/api_exception.py
# Compiled at: 2019-01-24 16:56:47
"""The Exceptions we can raise from API parsing."""

class ApiException(Exception):
    """The base class for all API parsing exceptions."""

    def __init__(self, reason, def_dict=None):
        """Create an exception.

    Args:
      reason: (str) The human readable explanation of this exception.
      def_dict: (dict) The discovery dictionary we failed on.
    """
        super(ApiException, self).__init__()
        self._reason = reason
        self._def_dict = def_dict

    def __str__(self):
        if self._def_dict:
            return '%s: %s' % (self._reason, self._def_dict)
        return self._reason