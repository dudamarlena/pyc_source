# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/models/DocumentMetaInfo.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 1287 bytes
from vaitk import core

class DocumentMetaInfo:
    __doc__ = '\n    Information holder for meta information about the document as a whole.\n    '

    def __init__(self, meta_type, document, data=None):
        """
        Initializes the meta info.
        Not publicly used. There's a factory method on the TextDocument.

        Args:
            meta_type (str) : A descriptive identifier string (e.g. CreationTime)
            document (TextDocument) : the associated TextDocument instance.
            data (Any, default None) : the value of the meta information.
        """
        self._meta_type = meta_type
        self._document = document
        self._data = data
        self.contentChanged = core.VSignal(self)

    def setData(self, data):
        if self._data != data:
            self._data = data
            self.notifyObservers()

    def data(self):
        return self._data

    def clear(self):
        if self._data is not None:
            self._data = None
            self.notifyObservers()

    def notifyObservers(self):
        self.contentChanged.emit(self._data)

    @property
    def meta_type(self):
        return self._meta_type

    @property
    def document(self):
        return self._document

    def __str__(self):
        return str(self._data)