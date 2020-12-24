# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/data/guidataicon.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 1893 bytes
"""
Application-specific **post-startup icon store** (i.e., abstract container of
all :class:`QIcon`-based in-memory icons required *after* rather than during
application startup) functionality.

By compare, most icons leveraged by this application are required only at
application startup and hence already managed by the pregenerated
:mod:`betsee.data.py.betsee_ui` submodule cached from the Qt Creator-managed
``betsee/data/ui/betsee.ui` file created at application design time. To avoid
redundancy, this submodule intentionally excludes these icons.

Design
----------
Each post-startup icon stored by this submodule is exposed through a
corresponding function decorated by the :func:`func_cached` memoizer,
guaranteeing that:

* The first call to that function creates, caches, and returns a new
  :class:`QIcon` instance encapsulating that icon.
* All subsequent calls to that function return the existing :class:`QIcon`
  instance previously cached by the first call to that function.
"""
from PySide2.QtGui import QIcon
from betse.util.type.decorator.decmemo import func_cached
from betsee.util.io.image import guiicon

@func_cached
def get_icon_dot() -> QIcon:
    """
    **Bullet point** (i.e., icon typically signifying a numberless item of a
    dynamically constructed list, tree, or other data structure).
    """
    return guiicon.make_icon(resource_name='://icon/entypo+/dot-single.svg')