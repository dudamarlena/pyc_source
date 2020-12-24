# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/widget/stock/guiscrollarea.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 2516 bytes
"""
General-purpose :mod:`QScrollArea` subclasses.
"""
from PySide2.QtWidgets import QScrollArea
from betsee.util.widget.mixin.guiwdgmixin import QBetseeObjectMixin

class QBetseeScrollImage(QBetseeObjectMixin, QScrollArea):
    __doc__ = "\n    General-purpose :mod:`QScrollArea` widget optimized for (pre)viewing\n    exactly one image.\n\n    This widget augments the stock :class:`QScrollArea` widget with:\n\n    * **Image (pre)view.** This widget supports all image filetypes supported\n      by stock Qt widgets. Specifically, all images whose filetypes are in the\n      system-specific set returned by the\n      :func:`betse.util.path.guifiletype.get_image_read_filetypes` function are\n      explicitly supported.\n    * **Horizontal scrollbars,** automatically displaying horizontal scrollbars\n      for all columns whose content exceeds that column's width. For\n      inexplicable reasons, this functionality has been seemingly intentionally\n      omitted from the stock :class:`QScrollArea`.\n\n    Attributes\n    ----------\n    _image_label : QLabel\n        Child label contained with this line edit. To preview the image whose\n        filename is the text displayed by this line edit, this label's pixmap is\n        read from this filename. By convention, this label is typically situated\n        below this line edit.\n    "

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._image_label = None

    def setColumnCount(self, column_count):
        super().setColumnCount(column_count)
        if column_count != 1:
            self.header().setStretchLastSection(True)