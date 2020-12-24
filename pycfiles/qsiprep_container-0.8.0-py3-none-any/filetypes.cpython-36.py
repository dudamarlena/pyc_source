# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-uunam8sj/pip/pip/_internal/utils/filetypes.py
# Compiled at: 2020-03-25 22:23:37
# Size of source mod 2**32: 571 bytes
"""Filetype information.
"""
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import Tuple
WHEEL_EXTENSION = '.whl'
BZ2_EXTENSIONS = ('.tar.bz2', '.tbz')
XZ_EXTENSIONS = ('.tar.xz', '.txz', '.tlz', '.tar.lz', '.tar.lzma')
ZIP_EXTENSIONS = ('.zip', WHEEL_EXTENSION)
TAR_EXTENSIONS = ('.tar.gz', '.tgz', '.tar')
ARCHIVE_EXTENSIONS = ZIP_EXTENSIONS + BZ2_EXTENSIONS + TAR_EXTENSIONS + XZ_EXTENSIONS