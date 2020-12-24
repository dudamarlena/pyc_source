# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/tests/cm_basic/test_configdict.py
# Compiled at: 2017-04-23 10:30:41
""" run with

python setup.py install; nosetests -v --nocapture tests/cm_basic/test_configdict.py:Test_configdict.test_001

nosetests -v --nocapture tests/cm_basic/test_configdict.py

or

nosetests -v tests/cm_basic/test_configdict.py

"""
from __future__ import print_function
import os, shutil
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.util import HEADING

class Test_configdict:
    root_path = os.path.abspath(os.sep)
    cwd_path = os.getcwd()

    def setup(self):
        os.system('cm help')
        self.etc_yaml = os.path.join(self.cwd_path, 'cloudmesh_client', 'etc', 'cloudmesh.yaml')
        self.tmp_yaml = os.path.join(self.root_path, 'tmp', 'cloudmesh.yaml')
        self.tmp_dir = os.path.join(self.root_path, 'tmp')

    def tearDown(self):
        pass

    def test_001_read(self):
        HEADING('test if cloudmesh.yaml is loaded')
        d = ConfigDict('cloudmesh.yaml', verbose=True)
        assert d['cloudmesh']['profile']['firstname'] != ''
        assert len(d['cloudmesh']['clouds']) > 0

    def test_002_set(self):
        HEADING('testing to set a value in the dict')
        shutil.copy(self.etc_yaml, self.tmp_yaml)
        d = ConfigDict('cloudmesh.yaml', load_order=[
         self.tmp_dir], verbose=True)
        d['cloudmesh']['profile']['firstname'] = 'Gregor'
        d.save()
        d = ConfigDict('cloudmesh.yaml', load_order=[
         self.tmp_dir], verbose=True)
        assert d['cloudmesh']['profile']['firstname'] == 'Gregor'

    def test_003_json(self):
        HEADING('test if json is produced')
        d = ConfigDict('cloudmesh.yaml', verbose=True)
        assert d.json.startswith('{')
        try:
            assert not isinstance(d.json, str)
            print('json should be string')
            assert False
        except Exception as e:
            assert isinstance(d.json, str)

    def test_004_yaml(self):
        HEADING('test if yaml is produced')
        d = ConfigDict('cloudmesh.yaml', verbose=True)
        result = d.yaml
        try:
            assert result.startswith('meta')
        except Exception as e:
            print('not valid yaml file.')
            assert False