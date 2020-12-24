# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opengen/tcp/solver_error.py
# Compiled at: 2019-11-25 10:58:56
# Size of source mod 2**32: 1085 bytes


class SolverError:
    __doc__ = 'Class for storing solver status in the event of an error.'

    def __init__(self, error):
        """Constructs instance of <code>SolverError</code>

        Args:
            error: dictionary containing error attributes

        Returns:
            New instance of <code>SolverError</code>
        """
        for k, v in error.items():
            attribute_name = '__{}'.format(k)
            setattr(self, attribute_name, v)

    @property
    def code(self):
        """
        Returns error codes:
        1000: Invalid request: Malformed or invalid JSON
        1600: Initial guess has incomplete dimensions
        1700: Wrong dimension of Lagrange multipliers
        2000: Problem solution failed (solver error)
        3003: Parameter vector has wrong length
        :return: Error code
        """
        return self.__dict__['__code']

    @property
    def message(self):
        """
        Returns an appropriate error message matching the error code
        :return: Error message
        """
        return self.__dict__['__message']