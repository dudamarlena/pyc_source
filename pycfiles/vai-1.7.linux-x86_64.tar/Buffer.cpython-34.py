# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/models/Buffer.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 1789 bytes
import time
from .TextDocument import TextDocument
from .TextDocumentCursor import TextDocumentCursor
from .EditAreaModel import EditAreaModel
from .CommandHistory import CommandHistory
from .Selection import Selection

class Buffer:
    __doc__ = '\n    Represents an editable buffer, and contains the document, the cursor\n    position, the command history, and all the state that is local to a\n    specific buffer.\n    '

    def __init__(self):
        self._document = TextDocument()
        self._document.createDocumentMetaInfo('Modified', False)
        self._document.createDocumentMetaInfo('Filename', None)
        self._document.createDocumentMetaInfo('InitialMD5', None)
        self._document.createDocumentMetaInfo('FileType', 'Text')
        self._document.createLineMetaInfo('LinterResult')
        self._document.createLineMetaInfo('Change')
        self._document.createLineMetaInfo('Bookmark')
        self._document_cursor = TextDocumentCursor(self._document)
        self._edit_area_model = EditAreaModel()
        self._command_history = CommandHistory()
        self._selection = Selection()

    def isEmpty(self):
        """
        Returns True if the document is empty
        """
        return self._document.isEmpty()

    def isModified(self):
        """
        Returns True if the document is modified
        """
        return self._document.documentMetaInfo('Modified').data()

    @property
    def document(self):
        return self._document

    @property
    def cursor(self):
        return self._document_cursor

    @property
    def edit_area_model(self):
        return self._edit_area_model

    @property
    def command_history(self):
        return self._command_history

    @property
    def selection(self):
        return self._selection