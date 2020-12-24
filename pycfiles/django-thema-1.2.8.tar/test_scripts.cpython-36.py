# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/syre/work/django-thema/thema/tests/test_scripts.py
# Compiled at: 2018-03-07 08:25:48
# Size of source mod 2**32: 13832 bytes
import subprocess, polib, sys
from os import path
from os.path import join
from shutil import copyfile
from mock import patch
from xlrd import XLRDError
from django.test import TestCase
from thema.scripts.excel_to_json import main as main_excel_to_json, ThemaFileParser, ExcelThemaFileParser, CODE_COLNAME, HEADING_COLNAME_BY_LANGUAGE, CODE_NEW_COLNAME, PARENT_COLNAME, PARENT_NEW_COLNAME, NOTES_NEW_COLNAME, NOTES_COLNAME_BY_LANGUAGE, RELATED_NEW_COLNAME, RELATED_COLNAME
from thema.scripts import json_to_language_file
from thema.scripts.json_to_language_file import main as main_json_to_language
from thema.tests.utils import ThemaTemporaryFilesMixin
TEMPORARY_TEST_DATA_DIR = join(path.dirname(path.realpath(__file__)), 'test_data')
MOCK_LOCALE_BASE_DIR = join(TEMPORARY_TEST_DATA_DIR, 'locale')
_IS_PYTHON2 = sys.version_info[0] == 2

def mock_parse_exception(obj, filter_by, clean_headers_language):
    """Mock to simulate a parsing error."""
    raise XLRDError


class TestExcelToJSON(ThemaTemporaryFilesMixin, TestCase):
    __doc__ = 'Test case to check the script excel_to_json.py works as expected.'
    LANGUAGES_TO_TEST = ['en', 'da', 'es']

    def setUp(self):
        super(TestExcelToJSON, self).setUp()
        self.base_dir = path.dirname(path.realpath(__file__))
        self.excel_en = join(TEMPORARY_TEST_DATA_DIR, 'Thema_v1.2.8_en.xlsx')
        self.excel_da = join(TEMPORARY_TEST_DATA_DIR, 'Thema_v1.2.8_da.xlsx')
        self.excel_es = join(TEMPORARY_TEST_DATA_DIR, 'Thema_v1.2.8_es.xlsx')
        original_data_dir = join(self.base_dir, '../data/')
        copyfile(join(original_data_dir, 'Thema_v1.2.8_en.xlsx'), self.excel_en)
        copyfile(join(original_data_dir, 'Thema_v1.2.8_da.xlsx'), self.excel_da)
        copyfile(join(original_data_dir, 'Thema_v1.2.8_es.xlsx'), self.excel_es)
        self.excel = {'en':self.excel_en, 
         'da':self.excel_da, 
         'es':self.excel_es}
        self.excel_to_json_path = join(self.base_dir, '../scripts/excel_to_json.py')

    def _are_all_random_codes_included(self, target, language, clean_headers):
        """Utility to verify some random codes are present in the target list.

        :param target: list of sheet-as-dicts with dirty/clean codes
        :param language: language to verify
        :param clean_headers: whether the headings are clean or not
        :return: True or False
        """
        heading_col_name = 'heading' if clean_headers else HEADING_COLNAME_BY_LANGUAGE[language]
        code_col_name = CODE_NEW_COLNAME if clean_headers else CODE_COLNAME
        parent_col_name = PARENT_NEW_COLNAME if clean_headers else PARENT_COLNAME
        notes_col_name = NOTES_NEW_COLNAME if clean_headers else NOTES_COLNAME_BY_LANGUAGE[language]
        related_col_name = RELATED_NEW_COLNAME if clean_headers else RELATED_COLNAME
        for code, heading_parent in self.random_codes.items():
            for item in target['categories']:
                if item[code_col_name] == code:
                    if item[heading_col_name] == heading_parent[language][0]:
                        if item[parent_col_name] == heading_parent['parent']:
                            if item[related_col_name] == heading_parent['related_categories']:
                                if item[notes_col_name] == heading_parent[language][1]:
                                    return True

        return False

    def test_output_no_args(self):
        """Check the script returns Exit 1 when we don't pass args."""
        self.assertRaises(subprocess.CalledProcessError, subprocess.check_output, [
         self.excel_to_json_path])

    def test_output_missing_arg_file(self):
        """Check the script returns Exit 1 when input file is missing."""
        for lang in self.LANGUAGES_TO_TEST:
            self.assertRaises(subprocess.CalledProcessError, subprocess.check_output, [
             self.excel_to_json_path, '-l', lang])

    def test_output_missing_arg_language(self):
        """Check the script returns Exit 1 when language is missing."""
        self.assertRaises(subprocess.CalledProcessError, subprocess.check_output, [
         self.excel_to_json_path, '-i', '/dummy'])

    def test_regular_case(self):
        """Verify the regular case work as it should.

        For now, it just checks a json file is created.

        Note: The content of the JSON file is checked in another test.
        """
        for lang in self.LANGUAGES_TO_TEST:
            main_excel_to_json(lang, self.excel[lang])
            self.assertTrue(path.exists(join(TEMPORARY_TEST_DATA_DIR, 'thema_{}.json'.format(lang))))

    def test_themafileparser_baseclass(self):
        """Check NotImplementedError is raised on the base class."""
        self.assertRaises(NotImplementedError, ThemaFileParser('/').parse)

    @patch('thema.scripts.excel_to_json.ExcelThemaFileParser.parse', mock_parse_exception)
    def test_parse_error_da(self):
        """ Check the script returns Exit 1 due to a parse error."""
        for lang in self.LANGUAGES_TO_TEST:
            self.assertRaises(SystemExit, main_excel_to_json, lang, self.excel[lang])

    def test_parse_verify_keys_dirty_heading(self):
        """Verify the content of the result.

        This test cover the case of dirty headings: original
        column names e.g. `New Language Heading`
        """
        for lang in self.LANGUAGES_TO_TEST:
            parser = ExcelThemaFileParser(self.excel[lang])
            self.assertTrue(self._are_all_random_codes_included(parser.parse([
             CODE_COLNAME,
             HEADING_COLNAME_BY_LANGUAGE[lang],
             PARENT_COLNAME,
             NOTES_COLNAME_BY_LANGUAGE[lang],
             RELATED_COLNAME]), lang, False))

    def test_parse_verify_keys_clean_heading(self):
        """Verify the content of the result.

        This test cover the case of clean headings: `heading` as key
        """
        for lang in self.LANGUAGES_TO_TEST:
            parser = ExcelThemaFileParser(self.excel[lang])
            self.assertTrue(self._are_all_random_codes_included(parser.parse([
             CODE_COLNAME,
             HEADING_COLNAME_BY_LANGUAGE[lang],
             PARENT_COLNAME,
             NOTES_COLNAME_BY_LANGUAGE[lang],
             RELATED_COLNAME], lang), lang, True))

    def test_parse_language_info_included(self):
        for lang in self.LANGUAGES_TO_TEST:
            parser = ExcelThemaFileParser(self.excel[lang])
            data = parser.parse([
             CODE_COLNAME,
             HEADING_COLNAME_BY_LANGUAGE[lang],
             PARENT_COLNAME,
             NOTES_COLNAME_BY_LANGUAGE[lang],
             RELATED_COLNAME], lang)
            self.assertIn('language_info', data)
            self.assertIn('see_also_translation', data['language_info'])
            self.assertIn('and_subcategories_translation', data['language_info'])


class TestJSONToLanguage(ThemaTemporaryFilesMixin, TestCase):
    __doc__ = 'Test case to check the json_to_language_file.py works as expected.'
    LANGUAGES_TO_TEST = [
     'da', 'es']

    def setUp(self):
        super(TestJSONToLanguage, self).setUp()
        self.base_dir = path.dirname(path.realpath(__file__))
        self.json_en = join(TEMPORARY_TEST_DATA_DIR, 'thema_en.json')
        self.json_da = join(TEMPORARY_TEST_DATA_DIR, 'thema_da.json')
        self.json_es = join(TEMPORARY_TEST_DATA_DIR, 'thema_es.json')
        original_data_dir = join(self.base_dir, '../data/')
        copyfile(join(original_data_dir, 'thema_en.json'), self.json_en)
        copyfile(join(original_data_dir, 'thema_da.json'), self.json_da)
        copyfile(join(original_data_dir, 'thema_es.json'), self.json_es)
        self.json_files = {'en':self.json_en, 
         'da':self.json_da, 
         'es':self.json_es}
        self.json_to_language_path = join(self.base_dir, '../scripts/json_to_language_file.py')
        for lang in self.LANGUAGES_TO_TEST:
            setattr(self, 'po_{}_path'.format(lang), join(TEMPORARY_TEST_DATA_DIR, 'locale/{}/LC_MESSAGES/django.po'.format(lang)))
            setattr(self, 'mo_{}_path'.format(lang), join(TEMPORARY_TEST_DATA_DIR, 'locale/{}/LC_MESSAGES/django.mo'.format(lang)))

    def test_output_no_args(self):
        """Check the script returns Exit 1 when we don't pass args."""
        self.assertRaises(subprocess.CalledProcessError, subprocess.check_output, [
         self.json_to_language_path])

    @patch.object(json_to_language_file, 'DATA_DIR', '/whatever1.2')
    def test_json_file_missing_language_file(self):
        """Check Exit 1 is raised when the input language file are missing."""
        for lang in self.LANGUAGES_TO_TEST:
            self.assertRaises(SystemExit, main_json_to_language, lang)

    @patch.object(json_to_language_file, 'THEMA_JSON_EN', '/whatever1.2')
    def test_json_file_missing_en_file(self):
        """Check Exit 1 is raised when the input EN json file are missing."""
        for lang in self.LANGUAGES_TO_TEST:
            self.assertRaises(SystemExit, main_json_to_language, lang)

    @patch.object(json_to_language_file, 'DATA_DIR', TEMPORARY_TEST_DATA_DIR)
    @patch.object(json_to_language_file, 'LOCALE_BASE_DIR', MOCK_LOCALE_BASE_DIR)
    def test_regular_case(self):
        """Verify the regular case works as it should.

        For now, it just checks the language files are created.

        Note: The content of the generated .po file is checked in another test.
        """
        for lang in self.LANGUAGES_TO_TEST:
            main_json_to_language(lang)
            self.assertTrue(path.exists(getattr(self, 'po_{}_path'.format(lang))))
            self.assertTrue(path.exists(getattr(self, 'mo_{}_path'.format(lang))))

    @patch.object(json_to_language_file, 'DATA_DIR', TEMPORARY_TEST_DATA_DIR)
    @patch.object(json_to_language_file, 'LOCALE_BASE_DIR', MOCK_LOCALE_BASE_DIR)
    def test_po_content(self):
        """Verify the content of the .po generated files."""
        for lang in self.LANGUAGES_TO_TEST:
            main_json_to_language(lang)
            file = getattr(self, 'po_{}_path'.format(lang))
            po = polib.pofile(file)
            all_translations_in_po = [(entry.msgid, entry.msgstr) for entry in po]
            for code, value in self.random_codes.items():
                po_translation = next((item for item in all_translations_in_po if item[0] == value['en'][0]), None)
                self.assertEqual(po_translation[1].encode('utf-8') if _IS_PYTHON2 else str(po_translation[1]), value[lang][0])