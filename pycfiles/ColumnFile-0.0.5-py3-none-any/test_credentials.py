# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/tests/test_credentials.py
# Compiled at: 2017-08-21 17:07:37
import json
from mock import patch
import testtools
from columnclient import client
from columnclient import credentials
from tests import utils
DECRYPTED = 'secret'
ENCRYPTED = '$ANSIBLE_VAULT;1.1;AES256326134383462373862303630623564633433383134663034646630383964626333613363383033303336613235633364653763323033623661633566666563630a373830636233393835373361653935333461333537366464626639393934303438343038323734663636646362616437383663383166396334393233393663620a3966653835306537386538653362366239353636386162343537343935653630'

class TestCredentialsManager(testtools.TestCase):

    def setUp(self):
        super(TestCredentialsManager, self).setUp()

    def tearDown(self):
        super(TestCredentialsManager, self).tearDown()

    @patch('requests.session')
    def test_init(self, mock_session):
        base_url = 'http://127.0.0.1:48620'
        cred_manager = credentials.CredentialsManager(mock_session, base_url)
        self.assertEqual(mock_session, cred_manager.session)
        self.assertEqual(base_url + '/credentials', cred_manager.base_url)

    @patch('requests.session')
    def test_vault_decrypt(self, mock_session):
        instance = mock_session.return_value
        instance.get.return_value = utils.MockResponse(text='{"value": "' + DECRYPTED + '"}')
        col_client = client.Client()
        col_client.credentials.vault_decrypt(ENCRYPTED)
        url = 'http://127.0.0.1:48620/credentials?value=' + ENCRYPTED
        instance.get.assert_called_once_with(url)

    @patch('requests.session')
    def test_vault_encrypt(self, mock_session):
        instance = mock_session.return_value
        instance.put.return_value = utils.MockResponse(text='{"value": "' + ENCRYPTED + '"}')
        col_client = client.Client()
        col_client.credentials.vault_encrypt(DECRYPTED)
        url = 'http://127.0.0.1:48620/credentials'
        data = {'value': DECRYPTED}
        headers = {'content-type': 'application/json'}
        instance.put.assert_called_once_with(url, data=json.dumps(data), headers=headers)