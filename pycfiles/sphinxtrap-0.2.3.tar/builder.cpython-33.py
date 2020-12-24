# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jose/Documents/projects/sphinxtrap/repo/tests/builder.py
# Compiled at: 2014-02-15 15:19:13
# Size of source mod 2**32: 1600 bytes
import os
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import tempfile
from shutil import rmtree
from sphinx import cmdline
from .mocking import unittest, mock
cache = {'tmp_file': '/tmp/__sphinxtrap__',  'index_html': None}

class BuildProject(unittest.TestCase):
    index_html = None

    def test_1_build(self):
        global cache
        cache['old_pwd'] = os.getcwd()
        path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(os.path.join(path, 'testprj'))
        cache['tmp_file'] = tempfile.mkdtemp()
        args = [
         'sphinx-build', '-b', 'html', '-d',
         cache['tmp_file'] + '/doctrees', 'source',
         cache['tmp_file'] + '/build/html']
        with mock.patch('sys.stdout', new=StringIO()) as (fake_out):
            retv = cmdline.main(args)
        self.assertEqual(retv, 0)

    def read(self):
        if cache['index_html'] is None:
            fname = cache['tmp_file'] + '/build/html/index.html'
            with open(fname, 'rt') as (fd):
                cache['index_html'] = fd.read()
        return cache['index_html']

    def test_2_icon_role(self):
        btn = '<p><em class="icon-bullhorn icon-holder"></em></p>'
        self.assertIn(btn, self.read())

    def test_2_btn_role(self):
        btn = '<a class="btn reference external" href="http://sphinx-doc.or'
        self.assertIn(btn, self.read())

    def test_3_tear_down(self):
        rmtree(cache['tmp_file'])
        os.chdir(cache['old_pwd'])