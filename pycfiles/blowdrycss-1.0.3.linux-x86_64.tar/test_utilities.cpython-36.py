# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/starwater/blowdrycss_venv/lib/python3.6/site-packages/blowdrycss/unit_tests/test_utilities.py
# Compiled at: 2018-03-07 18:42:13
# Size of source mod 2**32: 19936 bytes
from __future__ import absolute_import, division
from builtins import round
from unittest import TestCase, main
from os import getcwd, path, removedirs, chdir
import sys
from io import StringIO, open
import blowdrycss.unit_tests.unittest_settings as unittest_settings
from blowdrycss.utilities import contains_a_digit, deny_empty_or_whitespace, get_file_path, unittest_file_path, change_settings_for_testing, print_minification_stats, print_blow_dryer, make_directory, delete_file_paths, validate_output_file_name_setting, validate_output_extension_setting
import blowdrycss_settings as settings
change_settings_for_testing()

class TestUtilities(TestCase):

    def test_contains_a_digit_true(self):
        digits = [
         'n12px', '1p 7p 1p 7p', '-1_25em', '-1.35%', 'rgba 255 0 0 0.5', 'h0ff48f']
        for value in digits:
            self.assertTrue(contains_a_digit(string=value), msg=value)

    def test_contains_a_digit_false(self):
        no_digits = ['bold', 'none', 'left']
        for value in no_digits:
            self.assertFalse(contains_a_digit(string=value), msg=value)

    def test_deny_empty_or_whitespace_valid(self):
        self.assertEqual(deny_empty_or_whitespace(string='valid_string', variable_name='valid_variable'), None)

    def test_deny_empty_or_whitespace_invalid_string(self):
        invalid = [
         '', None, '          ']
        for string in invalid:
            self.assertRaises(ValueError, deny_empty_or_whitespace, string, 'valid_variable')

    def test_deny_empty_or_whitespace_invalid_variable_name(self):
        invalid = ['', None, '          ']
        for variable_name in invalid:
            self.assertRaises(ValueError, deny_empty_or_whitespace, 'valid_string', variable_name)

    def test_get_file_path(self):
        file_directory = getcwd()
        file_name = 'blowdry'
        extensions = ['.css', '.min.css', '.txt', '.mp3', '.anything', '.md', '.html', '.rst']
        for extension in extensions:
            expected_file_path = path.join(getcwd(), file_name + extension)
            file_path = get_file_path(file_directory=file_directory, file_name=file_name, extension=extension)
            self.assertEqual(file_path, expected_file_path)

    def test_get_file_path_empty_input_valueerrror(self):
        file_directory = getcwd()
        file_name = 'blowdry'
        extension = '.css'
        self.assertRaises(ValueError, get_file_path, '', file_name, extension)
        self.assertRaises(ValueError, get_file_path, file_directory, '', extension)
        self.assertRaises(ValueError, get_file_path, file_directory, file_name, '')

    def test_get_file_path_invalid_extension(self):
        file_directory = getcwd()
        file_name = 'blowdry'
        extensions = ['.c$@$0f00ss', '.min.!@#css', '.tx^*()&)/\t', '.a@\nything', 'txt', 'md.', '.min.']
        for extension in extensions:
            self.assertRaises(ValueError, get_file_path, file_directory, file_name, extension)

    def test_px_to_em_typecast_string_input(self):
        base = 16
        for pixels in range(-1000, 1001):
            expected = round(pixels / base, 4)
            expected = str(expected) + 'em'
            actual = unittest_settings.px_to_em(pixels=(str(pixels)))
            self.assertEqual(actual, (str(expected)), msg=pixels)

    def test_px_to_em_int_input(self):
        base = 16
        for pixels in range(-1000, 1001):
            expected = round(pixels / base, 4)
            expected = str(expected) + 'em'
            actual = unittest_settings.px_to_em(pixels=pixels)
            self.assertEqual(actual, (str(expected)), msg=pixels)

    def test_px_to_em_float_input(self):
        base = 16
        for pixels in range(-11, 11, 1):
            pixels /= 10.0
            expected = round(float(pixels) / float(base), 4)
            expected = str(expected) + 'em'
            actual = unittest_settings.px_to_em(pixels=pixels)
            self.assertEqual(actual, (str(expected)), msg=(str(pixels) + ': ' + str(actual) + ' vs ' + str(expected)))

    def test_px_to_em_invalid_input(self):
        invalid_inputs = [
         '1 2', '5 6 5 6', 'cat', '11px', ' 234.8', 'n2_4p', '25deg', '16kHz']
        for invalid in invalid_inputs:
            expected = invalid
            actual = unittest_settings.px_to_em(pixels=invalid)
            self.assertEqual(actual, expected, msg=invalid)

    def test_px_to_em_change_base(self):
        base = 16
        for pixels in range(-1000, 1001):
            expected = round(pixels / base, 4)
            expected = str(expected) + 'em'
            actual = unittest_settings.px_to_em(pixels=pixels)
            self.assertEqual(actual, expected, msg=(str(actual) + ' vs ' + str(expected)))

    def test_px_to_em_string_base(self):
        base = 16
        for pixels in range(-1000, 1001):
            expected = round(pixels / base, 4)
            expected = str(expected) + 'em'
            actual = unittest_settings.px_to_em(pixels=pixels)
            self.assertEqual(actual, (str(expected)), msg=pixels)

    def test_px_to_em_Wrong_base(self):
        unittest_settings.base = 'aoenth'
        self.assertRaises(ValueError, (unittest_settings.px_to_em), pixels='32')
        unittest_settings.base = 16

    def test_unittest_file_path(self):
        folders = [
         'test_aspx', 'test_jinja']
        filenames = ['test.aspx', 'test.jinja2']
        for i, folder in enumerate(folders):
            the_path = unittest_file_path(folder, filenames[i])
            self.assertTrue(path.isfile(the_path))

    def test_unittest_file_path_exact_path(self):
        folder = 'test_html'
        filename = 'index.html'
        cwd = getcwd()
        expected_if_path = path.join(cwd, folder, filename)
        expecetd_else_path = path.join(cwd, 'blowdrycss', 'unit_tests', folder, filename)
        test_path = unittest_file_path(folder=folder, filename=filename)
        if cwd.endswith('unit_tests'):
            self.assertTrue(test_path, expected_if_path)
            chdir('../..')
            test_path = unittest_file_path(folder=folder, filename=filename)
            cwd_else = getcwd()
            expecetd_else_path = path.join(cwd_else, 'blowdrycss', 'unit_tests', folder, filename)
            self.assertTrue(test_path, expecetd_else_path)
        else:
            self.assertTrue(test_path, expecetd_else_path)
            chdir(path.join(cwd, 'blowdrycss', 'unit_tests'))
            test_path = unittest_file_path(folder=folder, filename=filename)
            cwd_if = getcwd()
            expected_if_path = path.join(cwd_if, folder, filename)
            self.assertTrue(test_path, expected_if_path)
        chdir(cwd)

    def test_change_settings_for_testing(self):
        cwd = getcwd()
        if_cases = (
         settings.markdown_directory == path.join(cwd, 'test_markdown'),
         settings.project_directory == path.join(cwd, 'test_examplesite'),
         settings.css_directory == path.join(settings.project_directory, 'test_css'),
         settings.docs_directory == path.join(cwd, 'test_docs'))
        else_cases = (
         settings.markdown_directory == path.join(cwd, 'blowdrycss', 'unit_tests', 'test_markdown'),
         settings.project_directory == path.join(cwd, 'blowdrycss', 'unit_tests', 'test_examplesite'),
         settings.css_directory == path.join(settings.project_directory, 'test_css'),
         settings.docs_directory == path.join(cwd, 'blowdrycss', 'unit_tests', 'test_docs'))
        change_settings_for_testing()
        if cwd.endswith('unit_tests'):
            for i, if_case in enumerate(if_cases):
                self.assertTrue(if_case, msg=('index %s\n%s\n%s' % (i, settings.project_directory, path.join(cwd, 'test_examplesite'))))

            chdir('../..')
            cwd_else = getcwd()
            change_settings_for_testing()
            else_cases = (
             settings.markdown_directory == path.join(cwd_else, 'blowdrycss', 'unit_tests', 'test_markdown'),
             settings.project_directory == path.join(cwd_else, 'blowdrycss', 'unit_tests', 'test_examplesite'),
             settings.css_directory == path.join(settings.project_directory, 'test_css'),
             settings.docs_directory == path.join(cwd_else, 'blowdrycss', 'unit_tests', 'test_docs'))
            for else_case in else_cases:
                self.assertTrue(else_case)

        else:
            for else_case in else_cases:
                self.assertTrue(else_case)

            chdir(path.join(cwd, 'blowdrycss', 'unit_tests'))
            cwd_if = getcwd()
            change_settings_for_testing()
            if_cases = (
             settings.markdown_directory == path.join(cwd_if, 'test_markdown'),
             settings.project_directory == path.join(cwd_if, 'test_examplesite'),
             settings.css_directory == path.join(settings.project_directory, 'test_css'),
             settings.docs_directory == path.join(cwd_if, 'test_docs'))
            for if_case in if_cases:
                self.assertTrue(if_case)

        chdir(cwd)

    def test_print_minification_stats(self):
        blowdry_css = unittest_file_path('test_examplesite/test_css', 'blowdry.css')
        blowdry_min_css = unittest_file_path('test_examplesite/test_css', 'blowdry.min.css')
        substrings = [
         'blowdry.css:\t 0.3kB',
         'blowdry.min.css: 0.2kB',
         'File size reduced by 28.4%.']
        blowdry_css_text = '.bgc-hf8f8f8 {\n    background-color: #f8f8f8\n    }\n.border-1px-solid-gray {\n    border: 1px solid gray\n    }\n.padding-5 {\n    padding: 0.3125em\n    }\n.bold {\n    font-weight: bold\n    }\n.talign-center {\n    text-align: center\n    }\n.display-inline {\n    display: inline\n    }'
        blowdry_min_css_text = '.bgc-hf8f8f8{background-color:#f8f8f8}.border-1px-solid-gray{border:1px solid gray}.padding-5{padding:.3125em}.bold{font-weight:bold}.talign-center{text-align:center}.display-inline{display:inline}'
        make_directory(unittest_file_path('test_examplesite', ''))
        make_directory(unittest_file_path('test_examplesite/test_css', ''))
        with open(blowdry_css, 'wb') as (generic_file):
            generic_file.write(bytearray(blowdry_css_text, 'utf-8'))
        with open(blowdry_min_css, 'wb') as (generic_file):
            generic_file.write(bytearray(blowdry_min_css_text, 'utf-8'))
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            print_minification_stats(file_name='blowdry', extension='.css')
            output = out.getvalue()
            for substring in substrings:
                self.assertTrue((substring in output), msg=(substring + '\noutput:\n' + output))

        finally:
            sys.stdout = saved_stdout

    def test_print_minification_stats_SCSS(self):
        _folder = 'test_examplesite/test_css'
        blowdry_scss = unittest_file_path(_folder, '_blowdry.scss')
        blowdry_min_scss = unittest_file_path(_folder, '_blowdry.min.scss')
        substrings = [
         '_blowdry.scss:\t 0.3kB',
         '_blowdry.min.scss: 0.2kB',
         'File size reduced by 28.4%.']
        blowdry_scss_text = '.bgc-hf8f8f8 {\n    background-color: #f8f8f8\n    }\n.border-1px-solid-gray {\n    border: 1px solid gray\n    }\n.padding-5 {\n    padding: 0.3125em\n    }\n.bold {\n    font-weight: bold\n    }\n.talign-center {\n    text-align: center\n    }\n.display-inline {\n    display: inline\n    }'
        blowdry_min_scss_text = '.bgc-hf8f8f8{background-color:#f8f8f8}.border-1px-solid-gray{border:1px solid gray}.padding-5{padding:.3125em}.bold{font-weight:bold}.talign-center{text-align:center}.display-inline{display:inline}'
        make_directory(unittest_file_path('test_examplesite', ''))
        make_directory(unittest_file_path(_folder, ''))
        with open(blowdry_scss, 'wb') as (generic_file):
            generic_file.write(bytearray(blowdry_scss_text, 'utf-8'))
        with open(blowdry_min_scss, 'wb') as (generic_file):
            generic_file.write(bytearray(blowdry_min_scss_text, 'utf-8'))
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            print_minification_stats(file_name='_blowdry', extension='.scss')
            output = out.getvalue()
            for substring in substrings:
                self.assertTrue((substring in output), msg=(substring + '\noutput:\n' + output))

        finally:
            sys.stdout = saved_stdout

    def test_print_minification_stats_ZeroDivisionError(self):
        empty_css = unittest_file_path('test_examplesite/test_css', 'empty.css')
        empty_min_css = unittest_file_path('test_examplesite/test_css', 'empty.min.css')
        substrings = [
         'empty.css:\t 0.0kB',
         'empty.min.css: 0.0kB',
         'File size reduced by 0.0%.']
        make_directory(unittest_file_path('test_examplesite', ''))
        make_directory(unittest_file_path('test_examplesite/test_css', ''))
        with open(empty_css, 'w') as (generic_file):
            generic_file.write('')
        with open(empty_min_css, 'w') as (generic_file):
            generic_file.write('')
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            print_minification_stats(file_name='empty', extension='.css')
            output = out.getvalue()
            for substring in substrings:
                self.assertTrue((substring in output), msg=(substring + '\noutput:\n' + output))

        finally:
            sys.stdout = saved_stdout
            delete_file_paths((empty_css, empty_min_css))

    def test_print_blow_dryer(self):
        expected_ascii = "\n                     .-'-.\n                  ;@@@@@@@@@'\n    ~~~~ ;@@@@@@@@@@@@@@@@@@@+`\n    ~~~~ ;@@@@@@@@@@@@@``@@@@@@\n                +@@@@@`  `@@@@@'\n                   @@@@``@@@@@\n                     .-@@@@@@@+\n                          @@@@@\n                           .@@@.\n                            `@@@.\n    "
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            print_blow_dryer()
            output = out.getvalue()
            self.assertTrue((expected_ascii in output), msg=(expected_ascii + '\noutput:\n' + output))
        finally:
            sys.stdout = saved_stdout

    def test_make_directory_non_existing(self):
        directory_name = 'test_make_directory'
        directory = unittest_file_path(folder=directory_name)
        if path.isdir(directory):
            removedirs(directory)
        self.assertFalse(path.isdir(directory))
        make_directory(directory=directory)
        self.assertTrue(path.isdir(directory))
        if path.isdir(directory):
            removedirs(directory)

    def test_make_directory_pre_existing(self):
        directory_name = 'test_html'
        directory = unittest_file_path(folder=directory_name)
        self.assertTrue(path.isdir(directory))
        make_directory(directory=directory)
        self.assertTrue(path.isdir(directory))

    def test_delete_file_paths(self):
        file_paths = (
         unittest_file_path('test_examplesite', 'file1.html'),
         unittest_file_path('test_examplesite', 'file2.html'),
         unittest_file_path('test_examplesite', 'file3.html'))
        text = 'test123'
        make_directory(unittest_file_path('test_examplesite', ''))
        for file_path in file_paths:
            with open(file_path, 'wb') as (generic_file):
                generic_file.write(bytearray(text, 'utf-8'))

        for file_path in file_paths:
            self.assertTrue(path.isfile(file_path))

        delete_file_paths(file_paths=file_paths)
        for file_path in file_paths:
            self.assertFalse(path.isfile(file_path))

    def test_validate_output_file_name_setting_valid_input(self):
        validate_output_file_name_setting()

    def test_validate_output_file_name_setting_invalid_inputs(self):
        output_file_name = settings.output_file_name
        invalid_file_names = [
         ' custom', '/co/a', 'a\\cat', 'custom.']
        for invalid_file_name in invalid_file_names:
            settings.output_file_name = invalid_file_name
            self.assertRaises(SyntaxError, validate_output_file_name_setting)

        settings.output_file_name = output_file_name

    def test_validate_output_extension_setting_valid_input(self):
        validate_output_extension_setting()

    def test_validate_output_extension_setting_invalid_inputs(self):
        output_extension = settings.output_extension
        invalid_extensions = [
         'custom', '. custom', './co/a', '.a\\cat', '.custom.']
        for invalid_extension in invalid_extensions:
            settings.output_extension = invalid_extension
            self.assertRaises(SyntaxError, validate_output_extension_setting)

        settings.output_extension = output_extension


if __name__ == '__main__':
    main()