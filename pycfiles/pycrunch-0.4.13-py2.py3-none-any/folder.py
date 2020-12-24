# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pycrud/controllers/folder.py
# Compiled at: 2008-06-20 03:40:59
__doc__ = 'Folder Controller\n\nAUTHOR: Emanuel Gardaya Calso\n\nLast Modified:\n    2008-03-17\n    2008-03-18\n\n'
import logging
from pycrud.lib.base import *
log = logging.getLogger(__name__)

class FolderController(ListController):
    table = model.Folder
    children = dict(message=dict(table=model.Message, columns=('sender', 'recipient',
                                                               'message')))
    properties = ()