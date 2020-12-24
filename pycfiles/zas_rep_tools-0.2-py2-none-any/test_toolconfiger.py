# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/egoruni/Desktop/BA/Code/zas-rep-tools/zas_rep_tools/tests/test_toolconfiger.py
# Compiled at: 2018-10-16 13:31:08
import unittest, os, logging, sure, copy
from collections import defaultdict
from nose.plugins.attrib import attr
from testfixtures import tempdir, TempDirectory
from distutils.dir_util import copy_tree
import json, time, threading
from zas_rep_tools.src.classes.ToolConfiger import ToolConfiger
from zas_rep_tools.src.classes.dbhandler import DBHandler
from zas_rep_tools.src.classes.reader import Reader
from zas_rep_tools.src.utils.debugger import p, wipd, wipdn, wipdl, wipdo
from zas_rep_tools.src.utils.helpers import NestedDictValues, levenstein
from zas_rep_tools.src.utils.basetester import BaseTester
import platform
if platform.uname()[0].lower() != 'windows':
    import colored_traceback
    colored_traceback.add_hook()
else:
    import colorama

class TestZASToolConfigerToolConfiger(BaseTester, unittest.TestCase):
    _multiprocess_shared_ = True

    def setUp(self):
        super(type(self), self).setUp()

    def tearDown(self):
        super(type(self), self).tearDown()

    @attr(status='stable')
    def test_init_configer_000(self):
        self.prj_folder()
        configer = ToolConfiger(mode=self.mode)

    def SendKeys(self, keys):
        if keys == '{ENTER}':
            keys = 'return'
        from os import system
        system('osascript -e \'tell application "System Events" to keystroke ' + keys + "'")

    def test_get_user_data_for_error_tracking_500(self):
        configer = ToolConfiger(mode=self.mode)