# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\ryan\Documents\dev\python\hv-switching-board-firmware\hv_switching_board\__init__.py
# Compiled at: 2016-01-20 22:48:56
from path_helpers import path
from .driver import HVSwitchingBoard

def package_path():
    return path(__file__).parent


def get_sketch_directory():
    """
    Return directory containing the `hv_switching_board` Arduino sketch.
    """
    return package_path().joinpath('Arduino', 'hv_switching_board')


def get_includes():
    """
    Return directories containing the `hv_switching_board` Arduino header
    files.

    Modules that need to compile against `hv_switching_board` should use this
    function to locate the appropriate include directories.

    Notes
    =====

    For example:

        import hv_switching_board
        ...
        print ' '.join(['-I%s' % i for i in hv_switching_board.get_includes()])
        ...

    """
    import base_node
    return [
     get_sketch_directory()] + base_node.get_includes()


def get_sources():
    """
    Return `hv_switching_board` Arduino source file paths.

    Modules that need to compile against `hv_switching_board` should use this
    function to locate the appropriate source files to compile.

    Notes
    =====

    For example:

        import hv_switching_board
        ...
        print ' '.join(hv_switching_board.get_sources())
        ...

    """
    sources = []
    for p in get_includes():
        sources += path(p).files('*.c*')

    return sources


def get_firmwares():
    """
    Return `hv_switching_board` compiled Arduino hex file paths.

    This function may be used to locate firmware binaries that are available
    for flashing to [Arduino Uno][1] boards.

    [1]: http://arduino.cc/en/Main/arduinoBoardUno
    """
    return [ f.abspath() for f in package_path().joinpath('firmware').walkfiles('*.hex')
           ]