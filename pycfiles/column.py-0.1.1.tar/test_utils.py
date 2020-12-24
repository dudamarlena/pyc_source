# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/tests/test_utils.py
# Compiled at: 2017-08-02 01:06:09
from mock import patch
from testtools import TestCase
from column import utils

class TestUtils(TestCase):

    def setUp(self):
        super(TestUtils, self).setUp()
        self.vault_password = 'h2RV4pEX2M2TXvLxYhuy'

    @patch('__builtin__.reload')
    @patch('ansible.cli.CLI.read_vault_password_file')
    def test_vault_decrypt(self, mock_read_vault_password, mock_reload):
        encrypted_value = '$ANSIBLE_VAULT;1.1;AES256\n31396632336565373837376136333436383139343033363766663532326434386435376639316434\n3930306333303835316564373530656365376561356466330a383238373762656238336432373261\n62303063306463323939323165363232353235613038386232636331363931373538626461396364\n6338336334343366650a353631653166616662363637636234666230333764323361643866643863\n3933\n'
        mock_read_vault_password.return_value = self.vault_password
        self.assertEqual('vmware', utils.vault_decrypt(encrypted_value))
        self.assertTrue(mock_read_vault_password.called)

    @patch('__builtin__.reload')
    @patch('ansible.cli.CLI.read_vault_password_file')
    def test_vault_encrypt(self, mock_read_vault_password, mock_reload):
        mock_read_vault_password.return_value = self.vault_password
        encrypted = utils.vault_encrypt('vmware')
        self.assertTrue(encrypted.startswith('$ANSIBLE_VAULT;1.1;AES256'))
        self.assertTrue(mock_read_vault_password.called)