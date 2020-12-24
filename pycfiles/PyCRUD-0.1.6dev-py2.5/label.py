# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pycrud/controllers/label.py
# Compiled at: 2008-06-20 03:40:59
"""Folder Controller

AUTHOR: Emanuel Gardaya Calso

Last Modified:
    2008-03-17
    2008-03-18

"""
import logging
from pycrud.lib.base import *
log = logging.getLogger(__name__)

class LabelController(ListController):
    table = model.Label
    children = dict(message=dict(table=model.Message, columns=('sender', 'recipient',
                                                               'message')))