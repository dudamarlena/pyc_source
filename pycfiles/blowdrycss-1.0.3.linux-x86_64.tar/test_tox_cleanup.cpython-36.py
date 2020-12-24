# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/starwater/blowdrycss_venv/lib/python3.6/site-packages/blowdrycss/unit_tests/test_tox_cleanup.py
# Compiled at: 2018-03-07 18:42:13
# Size of source mod 2**32: 2302 bytes
from __future__ import absolute_import, unicode_literals, with_statement
from io import open
from unittest import TestCase, main
from os import path, getcwd, chdir, remove
import tox_cleanup
__author__ = 'chad nelson'
__project__ = 'blowdrycss'

def create_file(file_path=''):
    """ Build create a file at the defined file_path, and write the word 'test' inside it.

    :type file_path: str
    :param file_path: Path to the file to be created.

    """
    with open(file_path, 'w', encoding='utf-8') as (_file):
        _file.write('test')


class TestToxCleanup(TestCase):

    def test_tox_cleanup_file_exists(self):
        original_dir = getcwd()
        print('The tox_cleanup started in', original_dir)
        cwd = original_dir
        module_path = path.join(cwd, 'blowdrycss')
        if cwd.endswith('unit_tests'):
            if not path.isdir(module_path):
                up2 = path.join('..', '..')
                chdir(up2)
                cwd = getcwd()
        settings_path = path.join(cwd, 'blowdrycss_settings.py')
        if not path.isfile(settings_path):
            create_file(file_path=settings_path)
        self.assertTrue((path.isfile(settings_path)), msg=settings_path)
        tox_cleanup.main()
        self.assertFalse((path.isfile(settings_path)), msg=settings_path)
        chdir(original_dir)

    def test_tox_cleanup_file_does_not_exist(self):
        original_dir = getcwd()
        print('The tox_cleanup started in', original_dir)
        cwd = original_dir
        if cwd.endswith('unit_tests'):
            up2 = path.join('..', '..')
            chdir(up2)
            cwd = getcwd()
        settings_path = path.join(cwd, 'blowdrycss_settings.py')
        if path.isfile(settings_path):
            remove(settings_path)
        self.assertFalse((path.isfile(settings_path)), msg=settings_path)
        tox_cleanup.main()
        self.assertFalse((path.isfile(settings_path)), msg=settings_path)
        chdir(original_dir)


if __name__ == '__main__':
    main()