# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/path/guipathenum.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 3415 bytes
"""
**Pathname dialog option** (i.e., member of the Qt-specific
:attr:`QFileDialog.Option` enumeration type conveniently reduced to
integer-based bit masks to be passed as the optionally OR-ed values of the
``dialog_options`` parameter of the
:func:`betsee.util.path.guipath.select_path` function by callers) constants.
"""
from PySide2.QtWidgets import QFileDialog
SHOW_DIRS_ONLY = int(QFileDialog.ShowDirsOnly)
DONT_RESOLVE_SYMLINKS = int(QFileDialog.DontResolveSymlinks)
DONT_CONFIRM_OVERWRITE = int(QFileDialog.DontConfirmOverwrite)
DONT_USE_NATIVE_DIALOG = int(QFileDialog.DontUseNativeDialog)
READ_ONLY = int(QFileDialog.ReadOnly)
HIDE_NAME_FILTER_DETAILS = int(QFileDialog.HideNameFilterDetails)
DONT_USE_CUSTOM_DIRECTORY_ICONS = int(QFileDialog.DontUseCustomDirectoryIcons)