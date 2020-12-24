# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/tests/test_generators.py
# Compiled at: 2017-06-02 11:17:28
from __future__ import print_function, with_statement, unicode_literals
import os, re, json, shutil, datetime, unittest
from simiki.config import parse_config, get_default_config
from simiki.utils import copytree
from simiki.generators import PageGenerator, CatalogGenerator
from simiki.compat import unicode
test_path = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.dirname(test_path)

class TestPageGenerator(unittest.TestCase):

    def setUp(self):
        self.default_config = get_default_config()
        self.wiki_path = os.path.join(test_path, b'mywiki_for_generator')
        os.chdir(self.wiki_path)
        self.config_file = os.path.join(base_path, b'simiki', b'conf_templates', b'_config.yml.in')
        self.config = parse_config(self.config_file)
        s_themes_path = os.path.join(base_path, b'simiki', self.default_config[b'themes_dir'])
        self.d_themes_path = os.path.join(b'./', self.default_config[b'themes_dir'])
        if os.path.exists(self.d_themes_path):
            shutil.rmtree(self.d_themes_path)
        copytree(s_themes_path, self.d_themes_path)
        self.generator = PageGenerator(self.config, self.wiki_path)

    def test_get_category_and_file(self):
        src_file = os.path.join(self.wiki_path, b'content', b'foo目录', b'foo_page_中文.md')
        self.generator.src_file = src_file
        category, filename = self.generator.get_category_and_file()
        self.assertEqual((
         category, filename), ('foo目录', 'foo_page_中文.md'))

    def test_get_meta_and_content(self):
        src_file = os.path.join(self.wiki_path, b'content', b'foo目录', b'foo_page_中文.md')
        self.generator.src_file = src_file
        meta, content = self.generator.get_meta_and_content()
        expected_meta = {b'date': b'2013-10-17 00:03', b'layout': b'page', b'title': b'Foo Page 2', 
           b'category': b'foo目录', b'filename': b'foo_page_中文.html'}
        self.assertEqual(meta, expected_meta)
        self.assertEqual(content, b'<p>[[simiki]]</p>\n<p>Simiki is a simple wiki framework, written in Python.</p>\n<p>Line 1<br />\nLine 2</p>')
        src_file = os.path.join(self.wiki_path, b'content', b'foo目录', b'foo_page_中文_meta_error_1.md')
        self.generator.src_file = src_file
        self.assertRaises(Exception, self.generator.get_meta_and_content)
        src_file = os.path.join(self.wiki_path, b'content', b'foo目录', b'foo_page_中文_meta_error_2.md')
        self.generator.src_file = src_file
        self.assertRaises(Exception, self.generator.get_meta_and_content)

    def test_get_template_vars(self):
        src_file = os.path.join(self.wiki_path, b'content', b'foo目录', b'foo_page_中文.md')
        self.generator.src_file = src_file
        meta, content = self.generator.get_meta_and_content()
        template_vars = self.generator.get_template_vars(meta, content)
        expected_template_vars = {b'page': {b'category': b'foo目录', 
                     b'content': b'<p>[[simiki]]</p>\n<p>Simiki is a simple wiki framework, written in Python.</p>\n<p>Line 1<br />\nLine 2</p>', 
                     b'filename': b'foo_page_中文.html', 
                     b'date': b'2013-10-17 00:03', 
                     b'layout': b'page', 
                     b'relation': [], b'title': b'Foo Page 2'}, 
           b'site': get_default_config()}
        expected_template_vars[b'site'].update({b'root': b''})
        template_vars[b'site'].pop(b'time')
        expected_template_vars[b'site'].pop(b'time')
        assert template_vars == expected_template_vars

    def test_to_html(self):
        src_file = os.path.join(self.wiki_path, b'content', b'foo目录', b'foo_page_中文.md')
        html_generator_config = self.config
        html_generator_config[b'markdown_ext'] = {b'wikilinks': None}
        html_generator_generator = PageGenerator(html_generator_config, self.wiki_path)
        html = html_generator_generator.to_html(src_file).strip()
        html = re.sub(b'(?sm)\\n\\s*<span class="updated">Page Updated.*?<\\/span>', b'', html)
        html = re.sub(b'(?m)^\\s*<p>Site Generated .*?<\\/p>$\n', b'', html)
        expected_output = os.path.join(self.wiki_path, b'expected_output.html')
        fd = open(expected_output, b'rb')
        year = datetime.date.today().year
        expected_html = unicode(fd.read(), b'utf-8') % year
        assert html.rstrip() == expected_html.rstrip()
        src_file = os.path.join(self.wiki_path, b'content', b'foo目录', b'foo_page_中文.md')
        self.assertRaises(Exception, PageGenerator, self.config, b'wrong_basepath', src_file)
        return

    def test_get_layout(self):
        src_file = os.path.join(self.wiki_path, b'content', b'foo目录', b'foo_page_layout_old_post.md')
        self.generator.src_file = src_file
        meta, _ = self.generator.get_meta_and_content()
        layout = self.generator.get_layout(meta)
        self.assertEqual(layout, b'page')
        src_file = os.path.join(self.wiki_path, b'content', b'foo目录', b'foo_page_layout_without_layout.md')
        self.generator.src_file = src_file
        meta, _ = self.generator.get_meta_and_content()
        layout = self.generator.get_layout(meta)
        self.assertEqual(layout, b'page')

    def test_get_meta(self):
        src_file = os.path.join(self.wiki_path, b'content', b'foo目录', b'foo_page_get_meta_yaml_error.md')
        self.generator.src_file = src_file
        self.assertRaises(Exception, self.generator.get_meta_and_content)
        src_file = os.path.join(self.wiki_path, b'content', b'foo目录', b'foo_page_get_meta_without_title.md')
        self.generator.src_file = src_file
        self.assertRaises(Exception, self.generator.get_meta_and_content)

    def tearDown(self):
        if os.path.exists(self.d_themes_path):
            shutil.rmtree(self.d_themes_path)


class TestCatalogGenerator(unittest.TestCase):

    def setUp(self):
        self.default_config = get_default_config()
        self.wiki_path = os.path.join(test_path, b'mywiki_for_generator')
        os.chdir(self.wiki_path)
        self.config_file = os.path.join(base_path, b'simiki', b'conf_templates', b'_config.yml.in')
        self.config = parse_config(self.config_file)
        s_themes_path = os.path.join(base_path, b'simiki', self.default_config[b'themes_dir'])
        self.d_themes_path = os.path.join(b'./', self.default_config[b'themes_dir'])
        if os.path.exists(self.d_themes_path):
            shutil.rmtree(self.d_themes_path)
        copytree(s_themes_path, self.d_themes_path)
        self.pages = {b'content/other/page1.md': {b'content': b'', b'collection': b'mycoll', 
                                       b'date': b'2016-06-02 00:00', 
                                       b'layout': b'page', 
                                       b'title': b'Page 1'}, 
           b'content/other/page2.md': {b'content': b'', b'date': b'2016-06-02 00:00', 
                                       b'layout': b'page', 
                                       b'title': b'Page 2'}, 
           b'content/other/page3.md': {b'content': b'', b'collection': b'mycoll', 
                                       b'date': b'2016-06-02 00:00', 
                                       b'layout': b'page', 
                                       b'title': b'Page 3'}}
        self.generator = CatalogGenerator(self.config, self.wiki_path, self.pages)

    def test_get_template_vars(self):
        tpl_vars = self.generator.get_template_vars()
        with open(os.path.join(self.wiki_path, b'expected_pages.json'), b'r') as (fd):
            expected_pages = json.load(fd)
            assert tpl_vars[b'pages'] == expected_pages
        with open(os.path.join(self.wiki_path, b'expected_structure.json'), b'r') as (fd):
            expected_structure = json.load(fd)
            assert tpl_vars[b'site'][b'structure'] == expected_structure

    def test_to_catalog(self):
        catalog_html = self.generator.generate_catalog_html()
        catalog_html = re.sub(b'(?m)^\\s*<p>Site Generated .*?<\\/p>$\n', b'', catalog_html)
        fd = open(os.path.join(self.wiki_path, b'expected_catalog.html'), b'rb')
        year = datetime.date.today().year
        expected_html = unicode(fd.read(), b'utf-8') % year
        assert catalog_html.rstrip() == expected_html.rstrip()


if __name__ == b'__main__':
    unittest.main()