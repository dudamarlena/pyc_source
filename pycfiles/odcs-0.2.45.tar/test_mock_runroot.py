# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/tests/test_mock_runroot.py
# Compiled at: 2019-05-07 00:57:40
import unittest
from mock import patch, mock_open
from odcs.server.mock_runroot import mock_runroot_init, raise_if_runroot_key_invalid, mock_runroot_run, mock_runroot_install
from .utils import AnyStringWith

class TestMockRunroot(unittest.TestCase):

    def setUp(self):
        super(TestMockRunroot, self).setUp()

    def tearDown(self):
        super(TestMockRunroot, self).tearDown()

    @patch('odcs.server.mock_runroot.create_koji_session')
    @patch('odcs.server.mock_runroot.execute_mock')
    @patch('odcs.server.mock_runroot.print', create=True)
    def test_mock_runroot_init(self, fake_print, execute_mock, create_koji_session):
        koji_session = create_koji_session.return_value
        koji_session.getRepo.return_value = {'id': 1}
        m = mock_open()
        with patch('odcs.server.mock_runroot.open', m, create=True):
            mock_runroot_init('f30-build')
        fake_print.assert_called_once()
        m.return_value.write.assert_called_once_with(AnyStringWith('f30-build'))
        execute_mock.assert_called_once_with(AnyStringWith('-'), ['--init'])

    def test_raise_if_runroot_key_invalid(self):
        with self.assertRaises(ValueError):
            raise_if_runroot_key_invalid('../../test')
        with self.assertRaises(ValueError):
            raise_if_runroot_key_invalid('/tmp')
        with self.assertRaises(ValueError):
            raise_if_runroot_key_invalid('x.cfg')
        raise_if_runroot_key_invalid('1-2-3-4-a-s-d-f')

    @patch('odcs.server.mock_runroot.execute_mock')
    @patch('odcs.server.mock_runroot.execute_cmd')
    def test_mock_runroot_run(self, execute_cmd, execute_mock):
        mock_runroot_run('foo-bar', ['df', '-h'])
        execute_mock.assert_called_once_with('foo-bar', [
         '--old-chroot', '--chroot', '--', '/bin/sh', '-c', '{ df -h; }'], False)
        execute_cmd.assert_any_call([
         'mount', '-o', 'bind', AnyStringWith('test_composes'), AnyStringWith('test_composes')])
        execute_cmd.assert_any_call(['umount', '-l', AnyStringWith('test_composes')])

    @patch('odcs.server.mock_runroot.execute_mock')
    def test_mock_runroot_install(self, execute_mock):
        mock_runroot_install('foo-bar', ['lorax', 'dracut'])
        execute_mock.assert_called_once_with('foo-bar', ['--install', 'lorax', 'dracut'])