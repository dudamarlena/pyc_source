# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/syp/test_syp.py
# Compiled at: 2017-01-22 12:02:12
import os
from unittest import TestCase
from unittest import main
import pytest, syp
packages = [
 'one', 'two']

def test_nominal(monkeypatch):

    def truthy(*args, **kwargs):
        return True

    def nofile(*args, **kwargs):
        return False

    def check_file_and_get_package_list_mock(afile, **kwargs):
        return packages

    monkeypatch.setattr(syp, 'check_file_and_get_package_list', check_file_and_get_package_list_mock)
    monkeypatch.setattr(syp, 'check_conf_dir', truthy)
    monkeypatch.setattr(os.path, 'isfile', nofile)
    monkeypatch.setattr(syp, 'write_packages', truthy)
    with pytest.raises(SystemExit):
        ret = syp.main(['another-package'])
        assert ret == 0


class TestUtils(TestCase):

    def setUp(self):
        pass

    def test_lines_filter_comments(self):
        lines = [
         '# comment', 'package']
        ret = syp.filter_packages(lines)
        self.assertEqual(ret, ['package'])
        lines = [
         'package # comment inline']
        self.assertEqual(['package'], syp.filter_packages(lines))

    def test_get_diff(self):
        cached = [
         'rst']
        conf = []
        self.assertEqual(([], ['rst']), syp.get_diff(cached, conf))
        conf = [
         'rst', 'foo']
        cached = ['foo']
        self.assertEqual((['rst'], []), syp.get_diff(cached, conf))

    def test_shell_cmd(self):
        syp.REQUIREMENTS_FILES = {'apt': {'file': 'apt.txt', 
                   'pacman': 'apt-get', 
                   'install': 'install -y --force-yes', 
                   'uninstall': 'remove'}}
        items = syp.REQUIREMENTS_FILES.items()
        self.assertEqual('sudo apt-get install -y --force-yes', syp.get_shell_cmd(items[0]))


if __name__ == '__main__':
    main()