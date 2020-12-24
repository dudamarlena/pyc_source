# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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