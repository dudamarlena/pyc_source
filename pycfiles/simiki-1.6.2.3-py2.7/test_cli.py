# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/tests/test_cli.py
# Compiled at: 2017-02-26 00:05:19
from __future__ import print_function, with_statement, unicode_literals
import os, os.path, shutil, unittest, io
from copy import deepcopy
from simiki import cli
from simiki.utils import copytree, emptytree
from simiki.config import get_default_config
test_path = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.dirname(test_path)
INIT_ARGS = {b'--help': False, 
   b'--version': False, 
   b'-c': None, 
   b'-f': None, 
   b'-p': None, 
   b'-t': None, 
   b'--host': None, 
   b'--port': None, 
   b'-w': None, 
   b'--draft': None, 
   b'generate': False, 
   b'g': False, 
   b'init': False, 
   b'new': False, 
   b'n': False, 
   b'preview': False, 
   b'p': False}

class TestCliInit(unittest.TestCase):

    def setUp(self):
        self.default_config = get_default_config()
        self.args = deepcopy(INIT_ARGS)
        self.target_path = b'_build'
        if os.path.exists(self.target_path):
            shutil.rmtree(self.target_path)
        self.files = [b'_config.yml',
         b'fabfile.py',
         os.path.join(self.default_config[b'source'], b'intro', b'gettingstarted.md'),
         os.path.join(self.default_config[b'themes_dir'], self.default_config[b'theme'], b'page.html'),
         os.path.join(self.default_config[b'themes_dir'], self.default_config[b'theme'], b'static', b'css', b'style.css')]
        self.dirs = [
         self.default_config[b'source'],
         self.default_config[b'destination'],
         self.default_config[b'themes_dir'],
         os.path.join(self.default_config[b'themes_dir'], self.default_config[b'theme'])]

    def test_init(self):
        os.chdir(test_path)
        self.args.update({b'init': True, b'-p': self.target_path})
        cli.main(self.args)
        for f in self.files:
            self.assertTrue(os.path.isfile(os.path.join(self.target_path, f)))

        for d in self.dirs:
            self.assertTrue(os.path.isdir(os.path.join(self.target_path, d)))

    def tearDown(self):
        if os.path.exists(self.target_path):
            shutil.rmtree(self.target_path)


class TestCliGenerate(unittest.TestCase):

    def setUp(self):
        self.args = deepcopy(INIT_ARGS)
        self.wiki_path = os.path.join(test_path, b'mywiki_for_cli')
        self.output_path = os.path.join(self.wiki_path, b'output')
        if os.path.exists(self.output_path):
            emptytree(self.output_path)
        config_file_tpl = os.path.join(base_path, b'simiki', b'conf_templates', b'_config.yml.in')
        self.config_file_dst = os.path.join(self.wiki_path, b'_config.yml')
        shutil.copyfile(config_file_tpl, self.config_file_dst)
        s_themes_path = os.path.join(base_path, b'simiki', b'themes')
        self.d_themes_path = os.path.join(self.wiki_path, b'themes')
        if os.path.exists(self.d_themes_path):
            shutil.rmtree(self.d_themes_path)
        copytree(s_themes_path, self.d_themes_path)
        self.drafts = [
         os.path.join(self.output_path, b'intro', b'my_draft.html')]
        self.files = [
         os.path.join(self.output_path, b'index.html'),
         os.path.join(self.output_path, b'intro', b'gettingstarted.html')]
        self.dirs = [
         self.output_path,
         os.path.join(self.output_path, b'intro')]
        self.attach = [
         os.path.join(self.output_path, b'attach', b'images', b'linux', b'opstools.png')]
        self.static = [
         os.path.join(self.output_path, b'static', b'css', b'style.css')]
        os.chdir(self.wiki_path)

    def test_generate(self):
        self.args.update({b'generate': True})
        cli.main(self.args)
        for f in self.drafts:
            self.assertFalse(os.path.isfile(os.path.join(self.wiki_path, f)))

        for f in self.files:
            self.assertTrue(os.path.isfile(os.path.join(self.wiki_path, f)))

        for d in self.dirs:
            self.assertTrue(os.path.isdir(os.path.join(self.wiki_path, d)))

        for f in self.attach:
            self.assertTrue(os.path.isdir(os.path.join(self.wiki_path, d)))

        for f in self.static:
            self.assertTrue(os.path.isdir(os.path.join(self.wiki_path, d)))

    def tearDown(self):
        os.remove(self.config_file_dst)
        if os.path.exists(self.d_themes_path):
            shutil.rmtree(self.d_themes_path)
        if os.path.exists(self.output_path):
            emptytree(self.output_path)


class TestCliNewWiki(unittest.TestCase):

    def setUp(self):
        wiki_path = os.path.join(test_path, b'mywiki_for_others')
        config_file_tpl = os.path.join(base_path, b'simiki', b'conf_templates', b'_config.yml.in')
        self.config_file_dst = os.path.join(wiki_path, b'_config.yml')
        shutil.copyfile(config_file_tpl, self.config_file_dst)
        self.args = deepcopy(INIT_ARGS)
        self.title = b'hello/simiki'
        self.category = os.path.join(b'my目录', b'sub-category')
        self.source_path = os.path.join(wiki_path, b'content')
        self.odir = os.path.join(wiki_path, b'content', self.category)
        self.odir_root = os.path.dirname(self.odir)
        os.chdir(wiki_path)
        if os.path.exists(self.odir_root):
            shutil.rmtree(self.odir_root)

    def test_new_wiki_without_file(self):
        ofile = os.path.join(self.odir, b'hello-slash-simiki.md')
        self.args.update({b'new': True, b'-t': self.title, b'-c': self.category})
        cli.main(self.args)
        self.assertTrue(os.path.isfile(ofile))
        with io.open(ofile, b'rt', encoding=b'utf-8') as (fd):
            lines = fd.read().rstrip().splitlines()
            lines[2] = b''
        expected_lines = [
         b'---', b'title: "hello/simiki"', b'', b'---']
        assert lines == expected_lines

    def tearDown(self):
        os.remove(self.config_file_dst)
        if os.path.exists(self.odir_root):
            shutil.rmtree(self.odir_root)


if __name__ == b'__main__':
    unittest.main()