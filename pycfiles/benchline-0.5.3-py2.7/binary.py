# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/benchline/binary.py
# Compiled at: 2014-05-01 17:17:54
"""
Script for reusable functions that help with freezing python code into binaries.
"""
import os, sys, benchline.args

def validate_args(parser, options, args):
    pass


def abs_res_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller

    >>> p = abs_res_path("binary.py")
    >>> p.endswith("binary.py")
    True
    >>> p.startswith("C") if os.name == 'nt' else p.startswith("/")
    True

    :param relative_path: string
    :return: string
    """
    if frozen_in_pyinstaller():
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


def frozen_in_pyinstaller():
    """Let's you know if the currently executing code is executing out of pyinstaller or not
    :return: boolean
    """
    try:
        sys._MEIPASS
        return True
    except AttributeError:
        return False


def main():
    benchline.args.go(__doc__, validate_args=validate_args)


if __name__ == '__main__':
    main()