# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/models/EditAreaModel.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 737 bytes
from vaitk import core

class EditAreaModel(core.VObject):
    __doc__ = '\n    Model defining data pertinent to the Edit Area View.\n    '

    def __init__(self):
        super().__init__()
        self._document_pos_at_top = (1, 1)
        self.documentPosAtTopChanged = core.VSignal(self)

    @property
    def document_pos_at_top(self):
        """The document position (in document index) in the top-left corner of the editor"""
        return self._document_pos_at_top

    @document_pos_at_top.setter
    def document_pos_at_top(self, doc_pos):
        if doc_pos[0] < 1 or doc_pos[1] < 1:
            raise ValueError('document pos cannot be < 1')
        self._document_pos_at_top = doc_pos
        self.documentPosAtTopChanged.emit()