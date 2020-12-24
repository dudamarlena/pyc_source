# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opengen/tcp/solver_response.py
# Compiled at: 2019-11-25 10:58:56
# Size of source mod 2**32: 1092 bytes
from .solver_status import SolverStatus
from .solver_error import SolverError

class SolverResponse:
    __doc__ = 'Stores a solver response of type SolverStatus or SolverError.'

    def __init__(self, d):
        """Constructs instance of <code>SolverResponse</code>

        Args:
            d: dictionary containing either status or error attributes

        Returns:
            New instance of <code>SolverResponse</code>
        """
        if 'Error' in d.values():
            self._SolverResponse__response = SolverError(d)
        else:
            self._SolverResponse__response = SolverStatus(d)

    def is_ok(self):
        """Determines if response is OK."""
        return isinstance(self._SolverResponse__response, SolverStatus)

    def get(self):
        """
        Returns response, which is an instance of SolverStatus,
        if the call was successful, or an instance of SolverError
        otherwise. It is recommended that you use is_ok() to check
        whether the call has succeeded first
        """
        return self._SolverResponse__response

    def __getitem__(self, key):
        return getattr(self._SolverResponse__response, key)