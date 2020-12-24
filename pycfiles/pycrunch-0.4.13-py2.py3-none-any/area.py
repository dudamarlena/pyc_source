# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pycrud/controllers/area.py
# Compiled at: 2008-06-20 02:48:54
import logging
from pycrud.lib.base import *
from pycrud import model
log = logging.getLogger(__name__)

class AreaController(ListController):
    table = model.Area