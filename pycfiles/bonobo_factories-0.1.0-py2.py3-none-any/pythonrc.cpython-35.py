# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/bonobo_docker/images/pythonrc.py
# Compiled at: 2018-01-01 16:23:40
# Size of source mod 2**32: 612 bytes


def _enable_syntax_completion():
    try:
        import readline
    except ImportError:
        print('Module readline not available.')
    else:
        import rlcompleter
        readline.parse_and_bind('tab: complete')


def _enable_shell_colors():
    import sys
    from colorama import Fore
    sys.ps1 = Fore.LIGHTWHITE_EX + '🐵 >' + Fore.RESET + ' '
    sys.ps2 = Fore.BLACK + '..' + Fore.LIGHTBLACK_EX + '.' + Fore.RESET + ' '


_enable_syntax_completion()
_enable_shell_colors()
del _enable_syntax_completion
del _enable_shell_colors
bonobo = __import__('bonobo')