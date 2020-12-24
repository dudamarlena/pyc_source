# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/io/image/guiicon.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 1594 bytes
"""
Low-level **icon** (i.e., :class:`QIcon`-based in-memory icon, including both
rasterized and vectorized formats) functionality.
"""
from PySide2.QtGui import QIcon
from betse.util.type.types import type_check

@type_check
def make_icon(resource_name: str) -> QIcon:
    """
    Create and return a new :class:`QIcon` instance encapsulating an in-memory
    icon deserialized from the Qt-specific resource with the passed name.

    Parameters
    ----------
    resource_name : str
        Name of the `Qt-specific resource <resources_>`__ providing this icon.
        For generality, this should typically be a ``:/``- or
        ``qrc:///``-prefixed string (e.g., ``://icon/entypo+/dot-single.svg``).

    .. _resources:
        https://doc.qt.io/qt-5/resources.html

    Returns
    ----------
    QIcon
        In-memory icon deserialized from this resource.
    """
    return QIcon(resource_name)