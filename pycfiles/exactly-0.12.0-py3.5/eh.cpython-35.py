# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case/result/eh.py
# Compiled at: 2019-11-06 08:59:56
# Size of source mod 2**32: 1355 bytes
from typing import Optional
from exactly_lib.test_case.result.failure_details import FailureDetails

class ExitCodeOrHardError(tuple):
    __doc__ = '\n    Represents EITHER success(with exit code) OR hard error.\n    '

    def __new__(cls, exit_code: Optional[int], failure_message: Optional[FailureDetails]):
        return tuple.__new__(cls, (exit_code, failure_message))

    @property
    def is_exit_code(self) -> bool:
        return self[0] is not None

    @property
    def is_hard_error(self) -> bool:
        return self[0] is None

    @property
    def exit_code(self) -> Optional[int]:
        return self[0]

    @property
    def failure_details(self) -> Optional[FailureDetails]:
        """
        :return None iff the object represents SUCCESS.
        """
        return self[1]

    def __str__(self):
        if self.is_exit_code:
            return 'SUCCESS'
        else:
            return 'FAILURE:{}'.format(str(self.failure_details))


def new_eh_exit_code(exit_code: int) -> ExitCodeOrHardError:
    return ExitCodeOrHardError(exit_code, None)


def new_eh_hard_error(failure_details: FailureDetails) -> ExitCodeOrHardError:
    if failure_details is None:
        raise ValueError('A HARD ERROR must have failure details (that is not None)')
    return ExitCodeOrHardError(None, failure_details)