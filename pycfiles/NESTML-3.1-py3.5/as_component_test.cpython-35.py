# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/as_component_test.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 3042 bytes
import unittest, os, shutil
from pynestml.frontend.pynestml_frontend import to_nest
from pynestml.frontend.frontend_configuration import FrontendConfiguration

class AsComponentTest(unittest.TestCase):
    __doc__ = '"\n    This test checks whether PyNestML can be executed correctly as a component from a different component.\n    '

    def test_from_string(self):
        input_path = str(os.path.join(os.path.dirname(__file__), 'resources', 'CommentTest.nestml'))
        target_path = 'target'
        logging_level = 'INFO'
        module_name = 'module'
        store_log = False
        suffix = ''
        dev = True
        to_nest(input_path, target_path, logging_level, module_name, store_log, suffix, dev)
        self.assertTrue(os.path.isfile(os.path.join(FrontendConfiguration.get_target_path(), 'CMakeLists.txt')))
        self.assertTrue(os.path.isfile(os.path.join(FrontendConfiguration.get_target_path(), 'commentTest.cpp')))
        self.assertTrue(os.path.isfile(os.path.join(FrontendConfiguration.get_target_path(), 'commentTest.h')))
        self.assertTrue(os.path.isfile(os.path.join(FrontendConfiguration.get_target_path(), 'module.cpp')))
        self.assertTrue(os.path.isfile(os.path.join(FrontendConfiguration.get_target_path(), 'module.h')))

    def test_from_objects(self):
        input_path = os.path.join(os.path.dirname(__file__), 'resources', 'CommentTest.nestml')
        target_path = os.path.join('target')
        logging_level = 'INFO'
        module_name = 'module'
        store_log = False
        suffix = ''
        dev = True
        to_nest(input_path, target_path, logging_level, module_name, store_log, suffix, dev)
        self.assertTrue(os.path.isfile(os.path.join(FrontendConfiguration.get_target_path(), 'CMakeLists.txt')))
        self.assertTrue(os.path.isfile(os.path.join(FrontendConfiguration.get_target_path(), 'commentTest.cpp')))
        self.assertTrue(os.path.isfile(os.path.join(FrontendConfiguration.get_target_path(), 'commentTest.h')))
        self.assertTrue(os.path.isfile(os.path.join(FrontendConfiguration.get_target_path(), 'module.cpp')))
        self.assertTrue(os.path.isfile(os.path.join(FrontendConfiguration.get_target_path(), 'module.h')))

    def tearDown(self):
        shutil.rmtree(FrontendConfiguration.target_path)