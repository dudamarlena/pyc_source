# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/starwater/blowdrycss_venv/lib/python3.6/site-packages/blowdrycss/unit_tests/test_watchdog_fileEditEventHandler.py
# Compiled at: 2018-03-07 18:42:13
# Size of source mod 2**32: 8223 bytes
from __future__ import absolute_import, print_function, with_statement, unicode_literals
from builtins import str
from unittest import TestCase, main
from os import path, SEEK_END, remove
import logging, sys
from io import StringIO, open
from time import sleep
from watchdog.observers import Observer
from blowdrycss.utilities import change_settings_for_testing, unittest_file_path, make_directory
from blowdrycss.watchdogwrapper import FileEditEventHandler
import blowdrycss_settings as settings
change_settings_for_testing()

class TestFileEditEventHandler(TestCase):

    def test_print_status(self):
        file_types = '(' + ', '.join(settings.file_types) + ')'
        substrings = [
         '-' * 96,
         'The blowdrycss watchdog is watching all ' + str(file_types) + ' files',
         '\nin the project directory: ' + settings.project_directory,
         'Pressing Ctrl + C stops the process.']
        event_handler = FileEditEventHandler(patterns=(list(file_types)),
          ignore_patterns=[],
          ignore_directories=True)
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            event_handler.print_status()
            output = out.getvalue()
            for substring in substrings:
                self.assertTrue((substring in output), msg=(substring + '\noutput:\n' + output))

        finally:
            sys.stdout = saved_stdout

    def test_excluded_True(self):
        excluded_true = [
         unittest_file_path(folder=(str('test_examplesite')), filename=(str('clashing_aliases.html'))),
         unittest_file_path(folder=(str('test_examplesite')), filename=(str('property_aliases.html')))]
        file_types = '(' + ', '.join(settings.file_types) + ')'
        event_handler = FileEditEventHandler(patterns=(list(file_types)),
          ignore_patterns=[],
          ignore_directories=True)
        for excluded in excluded_true:
            self.assertTrue(event_handler.excluded(src_path=excluded))

    def test_excluded_False(self):
        excluded_false = [
         unittest_file_path(folder='test_examplesite', filename='index.html'),
         unittest_file_path(folder='test_examplesite', filename='test.html')]
        file_types = '(' + ', '.join(settings.file_types) + ')'
        event_handler = FileEditEventHandler(patterns=(list(file_types)),
          ignore_patterns=[],
          ignore_directories=True)
        for excluded in excluded_false:
            self.assertFalse(event_handler.excluded(src_path=excluded))

    def test_on_modified(self):
        logging.basicConfig(level=(logging.DEBUG))
        substrings = [
         '~~~ blowdrycss started ~~~',
         'Auto-Generated CSS',
         'Completed',
         'blowdry.css',
         'blowdry.min.css',
         'The blowdrycss watchdog is watching all (*.html) files',
         '-' * 96]
        html_text = '<html></html> '
        test_examplesite = unittest_file_path(folder='test_examplesite')
        modify_dot_html = unittest_file_path(folder='test_examplesite', filename='modify.html')
        file_types = '(' + ', '.join(settings.file_types) + ')'
        make_directory(test_examplesite)
        self.assertTrue(path.isdir(test_examplesite))
        with open(modify_dot_html, 'w', encoding='utf-8') as (_file):
            _file.write(html_text)
        event_handler = FileEditEventHandler(patterns=(list(file_types)),
          ignore_patterns=[],
          ignore_directories=True)
        observer = Observer()
        observer.schedule(event_handler, unittest_file_path(folder='test_examplesite'), recursive=True)
        observer.start()
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            with open(modify_dot_html, 'rb+') as (_file):
                _file.seek(-1, SEEK_END)
                _file.truncate()
            count = 0
            while substrings[(-1)] not in out.getvalue():
                if count > 100:
                    break
                else:
                    sleep(0.05)
                    count += 1

            output = out.getvalue()
            for substring in substrings:
                self.assertTrue((substring in output), msg=(substring + '\noutput:\n' + output))

        finally:
            sys.stdout = saved_stdout

        remove(modify_dot_html)
        observer.stop()
        observer.join()

    def test_on_modified_verify_do_double_runs(self):
        logging.basicConfig(level=(logging.DEBUG))
        once = [
         '~~~ blowdrycss started ~~~',
         'Auto-Generated CSS',
         'Completed',
         'The blowdrycss watchdog is watching all (*.html) files']
        twice = [
         'blowdry.css',
         'blowdry.min.css',
         '-' * 96]
        html_text = '<html class="bold"></html>  '
        test_examplesite = unittest_file_path(folder='test_examplesite')
        modify_dot_html = unittest_file_path(folder='test_examplesite', filename='modify.html')
        file_types = '(' + ', '.join(settings.file_types) + ')'
        make_directory(test_examplesite)
        self.assertTrue(path.isdir(test_examplesite))
        with open(modify_dot_html, 'w', encoding='utf-8') as (_file):
            _file.write(html_text)
        event_handler = FileEditEventHandler(patterns=(list(file_types)),
          ignore_patterns=[],
          ignore_directories=True)
        observer = Observer()
        observer.schedule(event_handler, unittest_file_path(folder='test_examplesite'), recursive=True)
        observer.start()
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            with open(modify_dot_html, 'rb+') as (_file):
                _file.seek(-1, SEEK_END)
                _file.truncate()
            count = 0
            while once[(-1)] not in out.getvalue():
                if count > 100:
                    break
                else:
                    sleep(0.02)
                    count += 1

            with open(modify_dot_html, 'rb+') as (_file):
                _file.seek(-1, SEEK_END)
                _file.truncate()
            count = 0
            while once[(-1)] not in out.getvalue():
                if count > 100:
                    break
                else:
                    sleep(0.02)
                    count += 1

            output = out.getvalue()
            for substring in once:
                self.assertTrue((output.count(substring) == 1), msg=(substring + ' only allowed once.\noutput:\n' + output))

            for substring in twice:
                self.assertTrue((output.count(substring) == 2), msg=(substring + ' only allowed twice\noutput:\n' + output))

        finally:
            sys.stdout = saved_stdout

        remove(modify_dot_html)
        observer.stop()
        observer.join()


if __name__ == '__main__':
    main()