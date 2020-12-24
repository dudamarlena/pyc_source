# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/aromanovich/carcade_dist/tests/environments_tests.py
# Compiled at: 2013-02-27 01:43:19
import os, shutil, tempfile, unittest
from jinja2 import TemplateSyntaxError
from webassets import Bundle
from carcade.core import get_translations
from carcade.environments import create_assets_env, create_jinja2_env

class WebassetsEnvironmentTest(unittest.TestCase):

    def setUp(self):
        self.build_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.build_dir)

    def test(self):
        bundle = Bundle('one.css', 'two.css', output='styles.css')
        assets_env = create_assets_env('./tests/fixtures/bundle', self.build_dir, {})
        bundle.build(env=assets_env)
        self.assertTrue('styles.css' in os.listdir(self.build_dir))


class Jinja2EnvironmentTest(unittest.TestCase):

    def setUp(self):
        self.build_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.build_dir)

    def test_webassets_integration(self):
        template = '{% assets "css" %}{{ ASSET_URL }}{% endassets %}'
        assets_env = create_assets_env('./tests/fixtures/bundle', self.build_dir, {'css': Bundle('one.css', 'two.css', output='styles.css')})
        jinja2_env = create_jinja2_env(assets_env=assets_env)
        result = jinja2_env.from_string(template).render()
        self.assertTrue('styles.css' in result)

    def test_translations_integration(self):
        template = '{% trans %}Hey!{% endtrans %}'
        jinja2_env = create_jinja2_env()
        result = jinja2_env.from_string(template).render()
        self.assertEqual('Hey!', result)
        translations = get_translations('tests/fixtures/ru.po')
        jinja2_env = create_jinja2_env(translations=translations)
        result = jinja2_env.from_string(template).render()
        self.assertEqual('Привет!', result)