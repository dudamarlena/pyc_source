# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/aegis_model/util/ansi_code.py
# Compiled at: 2020-01-27 21:51:56
# Size of source mod 2**32: 545 bytes


class AnsiEscapeCode:
    HEADER = '\x1b[95m'
    OKBLUE = '\x1b[94m'
    OKGREEN = '\x1b[92m'
    WARNING = '\x1b[93m'
    FAIL = '\x1b[91m'
    ENDC = '\x1b[0m'
    BOLD = '\x1b[1m'
    UNDERLINE = '\x1b[4m'
    PURPLE = '\x1b[95m'
    CYAN = '\x1b[96m'
    DARKCYAN = '\x1b[36m'
    BLUE = '\x1b[94m'
    GREEN = '\x1b[92m'
    YELLOW = '\x1b[93m'
    RED = '\x1b[91m'
    DARKGREEN = '\x1b[32m'


def test_ansi_code():
    print(AnsiEscapeCode.RED + 'This is to test' + AnsiEscapeCode.ENDC)


if __name__ == '__main__':
    test_ansi_code()