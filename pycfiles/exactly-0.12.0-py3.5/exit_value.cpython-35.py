# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/common/exit_value.py
# Compiled at: 2018-05-11 22:50:51
# Size of source mod 2**32: 820 bytes
from exactly_lib.util.ansi_terminal_color import ForegroundColor

class ExitValue(tuple):
    __doc__ = '\n    Result reporting of a process by an exit code together with an\n    corresponding identifier on stdout.\n    '

    def __new__(cls, exit_code: int, exit_identifier: str, color: ForegroundColor):
        return tuple.__new__(cls, (exit_code, exit_identifier, color))

    @property
    def exit_code(self) -> int:
        return self[0]

    @property
    def exit_identifier(self) -> str:
        return self[1]

    @property
    def color(self) -> ForegroundColor:
        return self[2]

    def __hash__(self) -> int:
        return self.exit_code

    def __eq__(self, o: object) -> bool:
        return isinstance(o, ExitValue) and o.exit_code == self.exit_code