# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/delegates/notedelegate.py
# Compiled at: 2013-04-11 17:47:52
from texteditdelegate import TextEditDelegate, DocumentationMetaclass
from camelot.view.controls.editors.noteeditor import NoteEditor

class NoteDelegate(TextEditDelegate):
    __metaclass__ = DocumentationMetaclass
    editor = NoteEditor