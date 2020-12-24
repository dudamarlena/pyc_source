# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case/result/sh.py
# Compiled at: 2019-11-06 08:59:56
# Size of source mod 2**32: 1639 bytes
from typing import Optional
from exactly_lib.common.report_rendering import text_docs
from exactly_lib.common.report_rendering.text_doc import TextRenderer

class SuccessOrHardError(tuple):
    __doc__ = '\n    Represents EITHER success OR hard error.\n    '

    def __new__(cls, failure_message: Optional[TextRenderer]):
        return tuple.__new__(cls, (failure_message,))

    @property
    def failure_message(self) -> Optional[TextRenderer]:
        return self[0]

    @property
    def is_success(self) -> bool:
        return self[0] is None

    @property
    def is_hard_error(self) -> bool:
        return not self.is_success

    def __str__(self):
        from exactly_lib.util.simple_textstruct.file_printer_output import to_string
        if self.is_success:
            return 'SUCCESS'
        else:
            return 'FAILURE:' + to_string.major_blocks(self.failure_message.render())


def new_sh_success() -> SuccessOrHardError:
    return __SH_SUCCESS


def new_sh_hard_error__str(failure_message: str) -> SuccessOrHardError:
    if failure_message is None:
        raise ValueError('A HARD ERROR must have a failure message (that is not None)')
    return SuccessOrHardError(text_docs.single_pre_formatted_line_object(failure_message))


def new_sh_hard_error(failure_message: TextRenderer) -> SuccessOrHardError:
    if failure_message is None:
        raise ValueError('A HARD ERROR must have a failure message (that is not None)')
    return SuccessOrHardError(failure_message)


__SH_SUCCESS = SuccessOrHardError(None)