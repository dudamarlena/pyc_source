# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/starwater/blowdrycss_venv/lib/python3.6/site-packages/blowdrycss/unit_tests/test_write_blowdrycss_settings_dot_py.py
# Compiled at: 2018-03-07 18:42:13
# Size of source mod 2**32: 6006 bytes
from __future__ import absolute_import
from unittest import TestCase, main
from os import getcwd, path, remove, chdir
from logging import DEBUG
from blowdrycss.settingsbuilder import write_blowdrycss_settings_dot_py

class TestWriteBlowdrycssSettingsDotPy(TestCase):

    def test_write_blowdrycss_settings_dot_py(self):
        settings_file = 'blowdrycss_settings.py'
        cwd = getcwd()
        if cwd.endswith('unit_tests'):
            if path.isfile(settings_file):
                remove(settings_file)
            write_blowdrycss_settings_dot_py()
            self.assertTrue(path.isfile('blowdrycss_settings.py'))
        else:
            chdir(path.join('blowdrycss', 'unit_tests'))
            if path.isfile(settings_file):
                remove(settings_file)
            write_blowdrycss_settings_dot_py()
            self.assertTrue(path.isfile('blowdrycss_settings.py'))
            chdir(cwd)
        import blowdrycss.unit_tests.blowdrycss_settings as test_settings
        cwd = getcwd()
        self.assertEqual((test_settings.markdown_directory),
          (path.join(cwd, 'docs', 'markdown')), msg=(test_settings.markdown_directory + '\t' + path.join(cwd, 'docs', 'markdown')))
        self.assertEqual(test_settings.project_directory, path.join(cwd, 'examplesite'))
        self.assertEqual(test_settings.css_directory, path.join(cwd, 'examplesite', 'css'))
        self.assertEqual(test_settings.docs_directory, path.join(cwd, 'docs'))
        self.assertEqual(test_settings.logging_enabled, False)
        self.assertEqual(test_settings.logging_level, DEBUG)
        self.assertEqual(test_settings.log_to_console, False)
        self.assertEqual(test_settings.log_to_file, False)
        self.assertEqual(test_settings.log_directory, path.join(cwd, 'log'))
        self.assertEqual(test_settings.log_file_name, 'blowdrycss.log')
        one_mega_byte = 1048576
        self.assertEqual(test_settings.log_file_size, 4 * one_mega_byte)
        self.assertEqual(test_settings.log_backup_count, 1)
        self.assertTrue(test_settings.file_types == ('*.html', ))
        true_settings = [
         test_settings.html_docs, test_settings.timing_enabled, test_settings.human_readable,
         test_settings.minify, test_settings.media_queries_enabled, test_settings.use_em,
         test_settings.hide_css_errors]
        for true_setting in true_settings:
            self.assertTrue(true_setting)

        false_settings = [
         test_settings.markdown_docs, test_settings.rst_docs]
        for false_setting in false_settings:
            self.assertFalse(false_setting)

        self.assertTrue(test_settings.base == 16)
        self.assertTrue(test_settings.xxsmall == (test_settings.px_to_em(0), test_settings.px_to_em(120)))
        self.assertTrue(test_settings.xsmall == (test_settings.px_to_em(121), test_settings.px_to_em(240)))
        self.assertTrue(test_settings.small == (test_settings.px_to_em(241), test_settings.px_to_em(480)))
        self.assertTrue(test_settings.medium == (test_settings.px_to_em(481), test_settings.px_to_em(720)))
        self.assertTrue(test_settings.large == (test_settings.px_to_em(721), test_settings.px_to_em(1024)))
        self.assertTrue(test_settings.xlarge == (test_settings.px_to_em(1025), test_settings.px_to_em(1366)))
        self.assertTrue(test_settings.xxlarge == (test_settings.px_to_em(1367), test_settings.px_to_em(1920)))
        self.assertTrue(test_settings.giant == (test_settings.px_to_em(1921), test_settings.px_to_em(2560)))
        self.assertTrue(test_settings.xgiant == (test_settings.px_to_em(2561), test_settings.px_to_em(2800)))
        self.assertTrue(test_settings.xxgiant == (test_settings.px_to_em(2801), test_settings.px_to_em(1000000)))
        self.assertEqual(test_settings.custom_property_alias_dict, {'background':{
          'bg-'}, 
         'background-color':{
          'bgc-', 'bg-c-', 'bg-color-'}, 
         'color':{
          'c-'}, 
         'font-size':{
          'fsize-', 'f-size-'}, 
         'font-weight':{
          'fweight-', 'f-weight-'}, 
         'height':{
          'h-'}, 
         'margin':{
          'm-'}, 
         'margin-top':{
          'm-top-'}, 
         'margin-bottom':{
          'm-bot-'}, 
         'padding':{
          'p-', 'pad-'}, 
         'padding-top':{
          'p-top-'}, 
         'position':{
          'pos-'}, 
         'text-align':{
          'talign-', 't-align-'}, 
         'vertical-align':{
          'valign-', 'v-align-'}, 
         'width':{
          'w-'}})
        if path.isfile(settings_file):
            remove(settings_file)
        if not cwd.endswith('unit_tests'):
            chdir(path.join('blowdrycss', 'unit_tests'))
            if path.isfile(settings_file):
                remove(settings_file)
            chdir(cwd)


if __name__ == '__main__':
    main()