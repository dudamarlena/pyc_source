# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/dnaStreaming/test/test_config.py
# Compiled at: 2020-05-12 03:20:35
# Size of source mod 2**32: 5601 bytes
from __future__ import absolute_import, division
import os, unittest
from unittest import TestCase
from unittest.mock import patch
from dnaStreaming.config import Config

class TestConfig(TestCase):

    def tearDown(self):
        self.ensure_remove_environment_variable(Config.ENV_VAR_USER_KEY)
        self.ensure_remove_environment_variable(Config.ENV_VAR_SUBSCRIPTION_ID)
        self.ensure_remove_environment_variable(Config.ENV_VAR_EXTRACTION_API_HOST)
        self.ensure_remove_environment_variable(Config.ENV_VAR_USER_ID)
        self.ensure_remove_environment_variable(Config.ENV_VAR_CLIENT_ID)
        self.ensure_remove_environment_variable(Config.ENV_VAR_PASSWORD)

    def ensure_remove_environment_variable(self, key):
        if key in os.environ:
            os.environ.pop(key)

    def test_customer_config_not_found_success(self):
        config = Config()
        path_bogus = '\\does\\not\\exist'
        config.customer_config_path = path_bogus
        error_message_expected = 'No such file or directory'
        was_exception_thrown = False
        error_message_actual = None
        try:
            config._validate()
        except FileNotFoundError as ex:
            try:
                error_message_actual = ex.strerror
                error_message_filename = ex.filename
                was_exception_thrown = True
            finally:
                ex = None
                del ex

        assert was_exception_thrown
        assert error_message_expected == error_message_actual
        assert path_bogus == error_message_filename

    def test_get_vals_from_file_success(self):
        config = Config()
        fileFolder = os.path.dirname(os.path.realpath(__file__))
        config._set_customer_config_path(os.path.join(fileFolder, 'test_customer_config.json'))
        user_key = config.get_user_key()
        subscription = config.subscription()
        oauth2_credentials = config.oauth2_credentials()
        assert user_key
        assert subscription == 'bar'
        assert oauth2_credentials.get('user_id')
        assert oauth2_credentials.get('password')
        assert oauth2_credentials.get('client_id')

    def test_environment_variables_success(self):
        os.environ[Config.ENV_VAR_USER_KEY] = '123'
        os.environ[Config.ENV_VAR_SUBSCRIPTION_ID] = 'ABC'
        os.environ[Config.ENV_VAR_USER_ID] = 'user'
        os.environ[Config.ENV_VAR_CLIENT_ID] = 'client'
        os.environ[Config.ENV_VAR_PASSWORD] = 'password'
        config = Config()
        fileFolder = os.path.dirname(os.path.realpath(__file__))
        config._set_customer_config_path(os.path.join(fileFolder, 'test_customer_config.json'))
        config._initialize()
        assert os.environ[Config.ENV_VAR_USER_KEY] == config.get_user_key()
        subscription_id = config.subscription()
        assert subscription_id == 'ABC'
        assert os.environ[Config.ENV_VAR_USER_ID] == config.oauth2_credentials().get('user_id')
        assert os.environ[Config.ENV_VAR_CLIENT_ID] == config.oauth2_credentials().get('client_id')
        assert os.environ[Config.ENV_VAR_PASSWORD] == config.oauth2_credentials().get('password')

    def test_environment_variable_service_account_id_success(self):
        os.environ[Config.ENV_VAR_SERVICE_ACCOUNT_ID] = 'lemme_in'
        os.environ[Config.ENV_VAR_SUBSCRIPTION_ID] = 'ABC'
        config = Config()
        fileFolder = os.path.dirname(os.path.realpath(__file__))
        config._set_customer_config_path(os.path.join(fileFolder, 'test_customer_config.json'))
        config._initialize()
        assert os.environ[Config.ENV_VAR_SERVICE_ACCOUNT_ID] == config.get_user_key()
        subscription_id = config.subscription()
        assert subscription_id == 'ABC'

    def test_oauth2_creds_not_provided(self):
        config = Config()
        creds = config.oauth2_credentials()
        assert creds is None

    def test_user_key_passed_success(self):
        config = Config(user_key='123')
        assert config.get_user_key() == '123'

    def test_service_account_id_passed_success(self):
        config = Config(service_account_id='123')
        assert config.get_user_key() == '123'

    @patch.object(Config, '_fetch_jwt', return_value='test_jwt_value')
    def test_get_headers_jwt(self, fetch_jwt_mock):
        config = Config()
        fileFolder = os.path.dirname(os.path.realpath(__file__))
        config._set_customer_config_path(os.path.join(fileFolder, 'test_customer_config.json'))
        headers_expected = {'Authorization': 'test_jwt_value'}
        headers_actual = config.get_authentication_headers()
        assert headers_actual == headers_expected
        fetch_jwt_mock.assert_called_once()

    @patch.object(Config, '_fetch_jwt', return_value='test_jwt_value')
    def test_get_headers_user_key(self, fetch_jwt_mock):
        user_key = 'just some user key'
        config = Config(user_key)
        headers_expected = {'user-key': user_key}
        headers_actual = config.get_authentication_headers()
        assert headers_actual == headers_expected
        fetch_jwt_mock.assert_not_called()


if __name__ == '__main__':
    if __package__ is None:
        unittest.main()