# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/tests/pypokergui/config_builder_test.py
# Compiled at: 2017-04-01 11:23:14
from tests.base_unittest import BaseUnitTest
import os, sys
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import yaml
from pypokergui.config_builder import build_config

class ConfigBuilderTest(BaseUnitTest):

    def setUp(self):
        self.capture = StringIO()
        sys.stdout = self.capture

    def tearDown(self):
        sys.stdout = sys.__stdout__
        teardown_tmp_file()

    def test_build_config(self):
        max_round = 10
        initial_stack = 100
        small_blind = 5
        ante = 1
        blind_structure = None
        build_config(max_round, initial_stack, small_blind, ante, blind_structure)
        with open(tmp_file_path, 'w+') as (f):
            f.write(self.capture.getvalue())
        with open(tmp_file_path, 'rb') as (f):
            data = yaml.load(f)
        self.eq(max_round, data['max_round'])
        self.eq(initial_stack, data['initial_stack'])
        self.eq(small_blind, data['small_blind'])
        self.eq(ante, data['ante'])
        self.eq(blind_structure, data['blind_structure'])
        self.eq('FIXME:your-ai-name', data['ai_players'][0]['name'])
        self.eq('FIXME:your-setup-script-path', data['ai_players'][0]['path'])
        return


tmp_file_path = os.path.join(os.path.dirname(__file__), 'config_builder_test_tmp.yaml')

def teardown_tmp_file():
    if os.path.exists(tmp_file_path):
        os.remove(tmp_file_path)