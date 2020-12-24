# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case/result/pfh.py
# Compiled at: 2019-11-06 08:59:56
# Size of source mod 2**32: 2488 bytes
from enum import Enum
from typing import Optional
from exactly_lib.common.report_rendering import text_docs
from exactly_lib.common.report_rendering.text_doc import TextRenderer

class PassOrFailOrHardErrorEnum(Enum):
    __doc__ = '\n    Implementation note: The error-values must correspond to those of PartialControlledFailureEnum\n    '
    PASS = 0
    FAIL = 2
    HARD_ERROR = 99


class PassOrFailOrHardError(tuple):
    __doc__ = '\n    Represents EITHER success OR hard error.\n    '

    def __new__(cls, status: PassOrFailOrHardErrorEnum, failure_message: Optional[TextRenderer]):
        return tuple.__new__(cls, (status, failure_message))

    @property
    def status(self) -> PassOrFailOrHardErrorEnum:
        return self[0]

    @property
    def is_error(self) -> bool:
        return self.status is not PassOrFailOrHardErrorEnum.PASS

    @property
    def failure_message(self) -> Optional[TextRenderer]:
        """
        :return None iff the object represents PASS.
        """
        return self[1]


__PFH_PASS = PassOrFailOrHardError(PassOrFailOrHardErrorEnum.PASS, None)

def new_pfh_pass() -> PassOrFailOrHardError:
    return __PFH_PASS


def new_pfh_non_pass(status: PassOrFailOrHardErrorEnum, failure_message: TextRenderer) -> PassOrFailOrHardError:
    return PassOrFailOrHardError(status, failure_message)


def new_pfh_fail(failure_message: TextRenderer) -> PassOrFailOrHardError:
    return PassOrFailOrHardError(PassOrFailOrHardErrorEnum.FAIL, failure_message)


def new_pfh_fail__str(failure_message: str) -> PassOrFailOrHardError:
    return new_pfh_fail(text_docs.single_pre_formatted_line_object(failure_message))


def new_pfh_fail_if_has_failure_message(failure_message: Optional[TextRenderer]) -> PassOrFailOrHardError:
    if failure_message is None:
        return new_pfh_pass()
    return new_pfh_fail(failure_message)


def new_pfh_hard_error(failure_message: TextRenderer) -> PassOrFailOrHardError:
    return PassOrFailOrHardError(PassOrFailOrHardErrorEnum.HARD_ERROR, failure_message)


def new_pfh_hard_error__str(failure_message: str) -> PassOrFailOrHardError:
    return new_pfh_hard_error(text_docs.single_pre_formatted_line_object(failure_message))