# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case/result/failure_details.py
# Compiled at: 2019-11-06 08:59:56
# Size of source mod 2**32: 2188 bytes
from typing import Optional
from exactly_lib.common.report_rendering import text_docs
from exactly_lib.common.report_rendering.text_doc import TextRenderer

class FailureDetails:
    __doc__ = '\n    An error message, an exception, or both.\n    '

    def __init__(self, failure_message: Optional[TextRenderer], exception: Optional[Exception]):
        self._FailureDetails__failure_message = failure_message
        self._FailureDetails__exception = exception

    @staticmethod
    def new_message(message: TextRenderer, exception: Optional[Exception]=None) -> 'FailureDetails':
        return FailureDetails(message, exception)

    @staticmethod
    def new_constant_message(message: str, exception: Optional[Exception]=None) -> 'FailureDetails':
        return FailureDetails(text_docs.single_pre_formatted_line_object(message), exception)

    @staticmethod
    def new_exception(exception: Exception, message: Optional[str]=None) -> 'FailureDetails':
        if message is None:
            return FailureDetails(None, exception)
        else:
            return FailureDetails(text_docs.single_pre_formatted_line_object(message), exception)

    @property
    def is_only_failure_message(self) -> bool:
        return self._FailureDetails__exception is None

    @property
    def failure_message(self) -> Optional[TextRenderer]:
        return self._FailureDetails__failure_message

    @property
    def has_exception(self) -> bool:
        return self._FailureDetails__exception is not None

    @property
    def exception(self) -> Exception:
        return self._FailureDetails__exception

    def __str__(self) -> str:
        from exactly_lib.util.simple_textstruct.file_printer_output import to_string
        components = []
        if self._FailureDetails__failure_message is not None:
            components += ['message=' + to_string.major_blocks(self._FailureDetails__failure_message.render_sequence())]
        if self._FailureDetails__exception is not None:
            components += ['exception=' + str(self._FailureDetails__exception)]
        return '\n\n'.join(components)