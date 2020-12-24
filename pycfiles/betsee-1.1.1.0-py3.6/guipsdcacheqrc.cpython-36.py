# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/lib/pyside2/cache/guipsdcacheqrc.py
# Compiled at: 2019-08-01 01:03:55
# Size of source mod 2**32: 3090 bytes
"""
High-level support facilities for integrating :mod:`PySide2` widget classes
with XML-formatted Qt resource collection (QRC) files exported by the external
Qt Designer application.
"""
from betse.util.io.log import logs
from betse.util.path import files, pathnames, paths
from betse.util.path.command import cmdrun, cmds
from betse.util.type.types import type_check

@type_check
def convert_qrc_to_py_file(qrc_filename: str, py_filename: str) -> None:
    """
    Convert the XML-formatted file with the passed ``.qrc``-suffixed filename
    *and* all binary resources referenced by this file exported by the external
    Qt Designer GUI into the :mod:`PySide2`-based Python module with the passed
    ``.py``-suffixed filename if capable of doing so *or* log a non-fatal
    warning and return otherwise.

    This function requires the optional third-party dependency
    ``pyside2-tools`` distributed by The Qt Company. Specifically, this
    high-level function wraps the low-level ``pyside2-rcc`` command installed
    by that dependency with a human-usable API.

    Parameters
    ----------
    qrc_filename : str
        Absolute or relative filename of the input ``.qrc``-suffixed file.
    py_filename : str
        Absolute or relative filename of the output ``.py``-suffixed file.
    """
    logs.log_info('Synchronizing PySide2 module "%s" from "%s"...', pathnames.get_basename(py_filename), pathnames.get_basename(qrc_filename))
    cmds.die_unless_command(filename='pyside2-rcc',
      reason='(e.g., as package "pyside2-tools" not installed).')
    files.die_unless_file(qrc_filename)
    paths.die_unless_writable(py_filename)
    pathnames.die_unless_filetype_equals(pathname=qrc_filename, filetype='qrc')
    pathnames.die_unless_filetype_equals(pathname=py_filename, filetype='py')
    cmdrun.log_output_or_die(command_words=(
     'pyside2-rcc', '-o', py_filename, qrc_filename))