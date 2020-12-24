# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/starwater/blowdrycss_venv/lib/python3.6/site-packages/blowdrycss/unit_tests/test_blowdry.py
# Compiled at: 2018-03-07 18:42:13
# Size of source mod 2**32: 8896 bytes
from __future__ import absolute_import, unicode_literals
from builtins import bytes
from unittest import TestCase, main
import sys
from io import StringIO
import os
from blowdrycss.utilities import unittest_file_path, delete_file_paths
import blowdrycss.blowdry as blowdry, blowdrycss_settings as settings
__author__ = 'chad nelson'
__project__ = 'blowdrycss'

class TestMain(TestCase):

    def test_boilerplate_markdown_docs(self):
        project_directory = settings.project_directory
        markdown_directory = settings.markdown_directory
        markdown_docs = settings.markdown_docs
        settings.project_directory = unittest_file_path(folder='test_examplesite')
        settings.markdown_directory = unittest_file_path(folder='test_markdown')
        settings.markdown_docs = True
        expected_files = (
         os.path.join(settings.markdown_directory, 'clashing_aliases.md'),
         os.path.join(settings.markdown_directory, 'property_aliases.md'))
        for expected_file in expected_files:
            if os.path.isfile(expected_file):
                os.remove(expected_file)

        blowdry.boilerplate()
        for expected_file in expected_files:
            self.assertTrue((os.path.isfile(expected_file)), msg=expected_file)
            os.remove(expected_file)

        settings.project_directory = project_directory
        settings.markdown_directory = markdown_directory
        settings.markdown_docs = markdown_docs

    def test_boilerplate_rst_docs(self):
        project_directory = settings.project_directory
        docs_directory = settings.docs_directory
        rst_docs = settings.rst_docs
        settings.project_directory = unittest_file_path(folder='test_examplesite')
        settings.docs_directory = unittest_file_path(folder='test_docs')
        settings.rst_docs = True
        expected_files = (
         os.path.join(settings.docs_directory, 'clashing_aliases.rst'),
         os.path.join(settings.docs_directory, 'property_aliases.rst'))
        for expected_file in expected_files:
            if os.path.isfile(expected_file):
                os.remove(expected_file)

        blowdry.boilerplate()
        for expected_file in expected_files:
            self.assertTrue((os.path.isfile(expected_file)), msg=expected_file)
            os.remove(expected_file)

        settings.project_directory = project_directory
        settings.docs_directory = docs_directory
        settings.rst_docs = rst_docs

    def test_parse(self):
        expected_class_set = {
         'medium-up', 'border-1px-solid-gray', 'padding-5', 'margin-top-10', 'display-none',
         'width-50', 'height-150px', 'color-hfff', 'font-size-25-s', 't-align-center',
         'display-inline', 'margin-top-50px', 'talign-center', 'width-150',
         'display-960-up-i', 'font-size-48', 'bold', 'margin-20', 'bgc-h000', 'c-red-i-hover',
         'hfff-hover-i', 'padding-10', 'bgc-hf8f8f8', 'text-align-center',
         'c-blue', 'height-200',
         'padding-10-s', 'height-50px', 'padding-top-10'}
        substrings = [
         '~~~ blowdrycss started ~~~',
         'CSSBuilder Running...',
         '.css']
        project_directory = settings.project_directory
        settings.project_directory = unittest_file_path()
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            class_set, css_text = blowdry.parse(recent=False, class_set=(set()), css_text=b'')
            self.assertTrue((expected_class_set == class_set), msg=class_set)
            output = out.getvalue()
            for substring in substrings:
                self.assertTrue((substring in output), msg=(output + '\tsubstring: ' + substring))

        finally:
            sys.stdout = saved_stdout
            settings.project_directory = project_directory

    def test_parse_on_modify_class_set(self):
        expected_class_set = {
         'green', 'purple-medium-up', 'bgc-h454545',
         'pink-hover'}
        substrings = [
         '~~~ blowdrycss started ~~~',
         'CSSBuilder Running...',
         '.css']
        project_directory = settings.project_directory
        css_directory = settings.css_directory
        settings.project_directory = unittest_file_path()
        settings.css_directory = unittest_file_path()
        current_set = {
         'green', 'purple-medium-up', 'bgc-h454545'}
        css_file = unittest_file_path(filename='blowdry.css')
        css_min_file = unittest_file_path(filename='blowdry.min.css')
        with open(css_file, 'w') as (generic_file):
            generic_file.write('test test test')
        modify_file = unittest_file_path(filename='modify.html')
        with open(modify_file, 'w') as (generic_file):
            generic_file.write('<html><div class="pink-hover not-valid">Modified</div></html>')
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            class_set, css_text = blowdry.parse(recent=True, class_set=current_set)
            self.assertTrue((expected_class_set == class_set), msg=class_set)
            output = out.getvalue()
            for substring in substrings:
                self.assertTrue((substring in output), msg=(output + '\tsubstring: ' + substring))

        finally:
            sys.stdout = saved_stdout
            settings.project_directory = project_directory
            settings.css_directory = css_directory
            delete_file_paths((css_file, css_min_file, modify_file))

    def test_parse_on_modify_css_text_PREXISTING(self):
        expected_css_text = b'.green {\n            color: green\n            }\n        .pink-hover:hover {\n    color: pink\n    }'
        substrings = [
         '~~~ blowdrycss started ~~~',
         'CSSBuilder Running...',
         settings.output_file_name,
         settings.output_extension]
        project_directory = settings.project_directory
        css_directory = settings.css_directory
        settings.project_directory = unittest_file_path()
        settings.css_directory = unittest_file_path()
        current_set = {
         'green'}
        current_css_text = b'.green {\n            color: green\n            }\n        '
        css_file = unittest_file_path(filename='blowdry.css')
        css_min_file = unittest_file_path(filename='blowdry.min.css')
        with open(css_file, 'w') as (generic_file):
            generic_file.write('test test test')
        modify_file = unittest_file_path(filename='modify.html')
        with open(modify_file, 'w') as (generic_file):
            generic_file.write('<html><div class="pink-hover not-valid">Modified</div></html>')
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            class_set, css_text = blowdry.parse(recent=True, class_set=current_set, css_text=current_css_text)
            self.assertTrue((expected_css_text == css_text), msg=css_text)
            output = out.getvalue()
            for substring in substrings:
                self.assertTrue((substring in output), msg=(output + '\tsubstring: ' + substring))

        finally:
            sys.stdout = saved_stdout
            settings.project_directory = project_directory
            settings.css_directory = css_directory
            delete_file_paths((css_file, css_min_file, modify_file))


if __name__ == '__main__':
    main()