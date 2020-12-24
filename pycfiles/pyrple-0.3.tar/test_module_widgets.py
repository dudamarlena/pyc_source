# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/test/test_widgets/test_module_widgets.py
# Compiled at: 2017-08-29 09:44:06
import logging
logger = logging.getLogger(name=__name__)
import time, numpy as np
from pyrpl.async_utils import sleep as async_sleep
from qtpy import QtCore, QtWidgets
from pyrpl.test.test_base import TestPyrpl
from pyrpl import APP
from pyrpl.curvedb import CurveDB

class TestModuleWidgets(TestPyrpl):
    OPEN_ALL_DOCKWIDGETS = True