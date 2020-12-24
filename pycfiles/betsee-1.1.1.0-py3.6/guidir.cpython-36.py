# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/path/guidir.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 4858 bytes
"""
:mod:`PySide2`-based directory functionality.
"""
from PySide2.QtCore import QCoreApplication
from PySide2.QtWidgets import QFileDialog
from betse.util.type.types import type_check, StrOrNoneTypes

@type_check
def select_subdir(init_pathname: str, parent_dirname: str, *args, **kwargs) -> StrOrNoneTypes:
    """
    Display a dialog requesting the user to select an existing subdirectory of
    the parent directory with the passed path, returning the relative pathname
    of this subdirectory with respect to this parent directory if this dialog
    was not cancelled *or* ``None`` otherwise (i.e., if this dialog was
    cancelled).

    Parameters
    ----------
    init_pathname : str
        Absolute or relative pathname of the subdirectory to initially display
        in this dialog. If this pathname is relative, this pathname is
        interpreted as relative to the ``parent_dirname`` parameter.
    parent_dirname : str
        Absolute pathname of the parent directory to select a subdirectory of.

    All remaining paremeters are passed as is to the
    :func:`guipath.select_path` function.

    Returns
    ----------
    StrOrNoneTypes
        Either:

        * If this dialog was confirmed, the absolute pathname of this
          subdirectory.
        * If this dialog was cancelled, ``None``.
    """
    from betsee.util.path import guipath, guipathenum
    if 'dialog_title' not in kwargs:
        kwargs['dialog_title'] = QCoreApplication.translate('select_subdir', 'Select Subdirectory')
    return (guipath.select_path)(args, dialog_callable=QFileDialog.getExistingDirectory, 
     dialog_options=guipathenum.SHOW_DIRS_ONLY, 
     init_pathname=init_pathname, 
     parent_dirname=parent_dirname, 
     is_subpaths=True, **kwargs)