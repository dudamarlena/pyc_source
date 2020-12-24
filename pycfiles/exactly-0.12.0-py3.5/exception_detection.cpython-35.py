# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case/exception_detection.py
# Compiled at: 2019-11-06 08:59:56
# Size of source mod 2**32: 1019 bytes
from exactly_lib.test_case.result import sh
from exactly_lib.test_case.result.failure_details import FailureDetails

class DetectedException(Exception):

    def __init__(self, failure_detail: FailureDetails):
        self._failure_detail = failure_detail

    @property
    def failure_details(self) -> FailureDetails:
        return self._failure_detail


def return_success_or_hard_error(callable_block, *args, **kwargs) -> sh.SuccessOrHardError:
    """
    Executes a callable (by invoking its __call__), and returns hard-error iff
    a `DetectedException` is raised, otherwise success.
    :param callable_block: 
    :param args: Arguments given to callable_block
    :param kwargs: Arguments given to callable_block
    :return: success iff callable_block does not raise `DetectedException`, otherwise success
    """
    try:
        callable_block(*args, **kwargs)
        return sh.new_sh_success()
    except DetectedException as ex:
        return sh.new_sh_hard_error(ex.failure_details.failure_message)