# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/zeg/tests/test_config.py
# Compiled at: 2018-05-22 09:29:16
# Size of source mod 2**32: 11891 bytes
"""Config tests."""
import unittest
from unittest.mock import patch, mock_open
from jsonschema import exceptions
from .. import config

class TestValidateConfig(unittest.TestCase):

    def _get_configuration(self, data):
        with patch('builtins.open', mock_open(read_data=data)):
            return config.load_config('foo')

    def test_file_upload_path(self):
        config_data = '\n            dataset_type: file\n            file_config:\n                path: test\n        '
        configuration = self._get_configuration(config_data)
        try:
            config.validate_config(configuration)
        except exceptions.ValidationError:
            self.fail('Failed validation')

    def test_file_upload_directory(self):
        config_data = '\n            dataset_type: file\n            file_config:\n                directory: test\n        '
        configuration = self._get_configuration(config_data)
        try:
            config.validate_config(configuration)
        except exceptions.ValidationError:
            self.fail('Failed validation')

    def test_unknown_configuration(self):
        config_data = '\n            foo: bar\n        '
        configuration = self._get_configuration(config_data)
        with self.assertRaises(exceptions.ValidationError):
            config.validate_config(configuration)

    def test_unknown_dataset_type(self):
        config_data = '\n            dataset_type: foo\n            file_config:\n                path: test\n        '
        configuration = self._get_configuration(config_data)
        with self.assertRaises(exceptions.ValidationError):
            config.validate_config(configuration)

    def test_file_dataset_multiple_valid(self):
        config_data = '\n            dataset_type: foo\n            file_config:\n                path: test\n                directory: test\n        '
        configuration = self._get_configuration(config_data)
        with self.assertRaises(exceptions.ValidationError):
            config.validate_config(configuration)

    def test_file_dataset_multiple_invalid(self):
        config_data = '\n            dataset_type: foo\n            file_config:\n                path: test\n                foo: test\n        '
        configuration = self._get_configuration(config_data)
        with self.assertRaises(exceptions.ValidationError):
            config.validate_config(configuration)

    def test_file_unknown_config(self):
        config_data = '\n            dataset_type: file\n            foo_config:\n                path: test\n        '
        configuration = self._get_configuration(config_data)
        with self.assertRaises(exceptions.ValidationError):
            config.validate_config(configuration)

    def test_file_config_missing(self):
        config_data = '\n            dataset_type: file\n        '
        configuration = self._get_configuration(config_data)
        with self.assertRaises(exceptions.ValidationError):
            config.validate_config(configuration)

    def test_file_config_missing_value(self):
        config_data = '\n            dataset_type: file\n            file_config:\n        '
        configuration = self._get_configuration(config_data)
        with self.assertRaises(exceptions.ValidationError):
            config.validate_config(configuration)

    def test_file_config_unknown(self):
        config_data = '\n            dataset_type: file\n            file_config:\n                foo: test\n        '
        configuration = self._get_configuration(config_data)
        with self.assertRaises(exceptions.ValidationError):
            config.validate_config(configuration)

    def test_sql_config(self):
        config_data = '\n            dataset_type: sql\n            sql_config:\n                connection: test\n                query: test\n        '
        configuration = self._get_configuration(config_data)
        try:
            config.validate_config(configuration)
        except exceptions.ValidationError:
            self.fail('Failed validation')

    def test_sql_missing_config(self):
        config_data = '\n            dataset_type: sql\n        '
        configuration = self._get_configuration(config_data)
        with self.assertRaises(exceptions.ValidationError):
            config.validate_config(configuration)

    def test_sql_unknown_config(self):
        config_data = '\n            dataset_type: sql\n            foo_config:\n                connection: test\n                query: test\n        '
        configuration = self._get_configuration(config_data)
        with self.assertRaises(exceptions.ValidationError):
            config.validate_config(configuration)

    def test_sql_config_missing_connection(self):
        config_data = '\n            dataset_type: sql\n            sql_config:\n                query: test\n        '
        configuration = self._get_configuration(config_data)
        with self.assertRaises(exceptions.ValidationError):
            config.validate_config(configuration)

    def test_sql_config_missing_query(self):
        config_data = '\n            dataset_type: sql\n            sql_config:\n                connection: test\n        '
        configuration = self._get_configuration(config_data)
        with self.assertRaises(exceptions.ValidationError):
            config.validate_config(configuration)

    def test_image_config(self):
        config_data = '\n            imageset_type: file\n            file_config:\n                paths:\n                    - image.jpg\n                    - a/directory/path\n            collection_id: 5ad3a99b75f3b30001732f36\n            dataset_id: 5ad3a99b75f3b30001732f36\n            dataset_column: foo\n        '
        configuration = self._get_configuration(config_data)
        try:
            config.validate_config(configuration)
        except exceptions.ValidationError:
            self.fail('Failed validation')

    def test_image_config_file_config_missing(self):
        config_data = '\n            imageset_type: file\n        '
        configuration = self._get_configuration(config_data)
        with self.assertRaises(exceptions.ValidationError):
            config.validate_config(configuration)

    def test_image_config_invalid_type(self):
        config_data = '\n            imageset_type: foo\n            file_config:\n                paths:\n                    - image.jpg\n            collection_id: 5ad3a99b75f3b30001732f36\n            dataset_id: 5ad3a99b75f3b30001732f36\n            dataset_column: foo\n        '
        configuration = self._get_configuration(config_data)
        with self.assertRaises(exceptions.ValidationError):
            config.validate_config(configuration)

    def test_image_config_invalid_paths(self):
        config_data = '\n            imageset_type: file\n            file_config:\n                paths:\n                    - 123\n            collection_id: 5ad3a99b75f3b30001732f36\n            dataset_id: 5ad3a99b75f3b30001732f36\n            dataset_column: foo\n        '
        configuration = self._get_configuration(config_data)
        with self.assertRaises(exceptions.ValidationError):
            config.validate_config(configuration)

    def test_image_config_missing_config(self):
        config_data = '\n            imageset_type: file\n            collection_id: 5ad3a99b75f3b30001732f36\n            dataset_id: 5ad3a99b75f3b30001732f36\n            dataset_column: foo\n        '
        configuration = self._get_configuration(config_data)
        with self.assertRaises(exceptions.ValidationError):
            config.validate_config(configuration)

    def test_image_config_missing_collection(self):
        config_data = '\n            imageset_type: file\n            file_config:\n                paths:\n                    - image.jpg\n            dataset_id: 5ad3a99b75f3b30001732f36\n            dataset_column: foo\n        '
        configuration = self._get_configuration(config_data)
        with self.assertRaises(exceptions.ValidationError):
            config.validate_config(configuration)

    def test_image_config_missing_dataset(self):
        config_data = '\n            imageset_type: file\n            file_config:\n                paths:\n                    - image.jpg\n                    - a/directory/path\n            collection_id: 5ad3a99b75f3b30001732f36\n            dataset_column: foo\n        '
        configuration = self._get_configuration(config_data)
        with self.assertRaises(exceptions.ValidationError):
            config.validate_config(configuration)

    def test_image_config_missing_dataset_column(self):
        config_data = '\n            imageset_type: file\n            file_config:\n                paths:\n                    - image.jpg\n                    - a/directory/path\n            collection_id: 5ad3a99b75f3b30001732f36\n            dataset_id: 5ad3a99b75f3b30001732f36\n        '
        configuration = self._get_configuration(config_data)
        with self.assertRaises(exceptions.ValidationError):
            config.validate_config(configuration)

    def test_collection_publish(self):
        config_data = '\n            update_type: publish\n            publish_config:\n                publish: true\n                destination_project: foo\n        '
        configuration = self._get_configuration(config_data)
        try:
            config.validate_config(configuration)
        except exceptions.ValidationError:
            self.fail('Failed validation')

    def test_collection_update_unknown(self):
        config_data = '\n            update_type: foo\n            publish_config:\n                publish: true\n                destination_project: foo\n        '
        configuration = self._get_configuration(config_data)
        with self.assertRaises(exceptions.ValidationError):
            config.validate_config(configuration)

    def test_collection_publish_config_missing(self):
        config_data = '\n            update_type: publish\n        '
        configuration = self._get_configuration(config_data)
        with self.assertRaises(exceptions.ValidationError):
            config.validate_config(configuration)

    def test_collection_publish_publish_missing(self):
        config_data = '\n            update_type: publish\n            publish_config:\n                destination_project: foo\n        '
        configuration = self._get_configuration(config_data)
        with self.assertRaises(exceptions.ValidationError):
            config.validate_config(configuration)

    def test_collection_publish_destination_missing(self):
        config_data = '\n            update_type: publish\n            publish_config:\n                publish: true\n        '
        configuration = self._get_configuration(config_data)
        with self.assertRaises(exceptions.ValidationError):
            config.validate_config(configuration)

    def test_collection_publish_incorrect_publish_type(self):
        config_data = '\n            update_type: publish\n            publish_config:\n                publish: foo\n                destination_project: foo\n        '
        configuration = self._get_configuration(config_data)
        with self.assertRaises(exceptions.ValidationError):
            config.validate_config(configuration)

    def test_collection_publish_incorrect_destination_type(self):
        config_data = '\n            update_type: publish\n            publish_config:\n                publish: true\n                destination_project: 123\n        '
        configuration = self._get_configuration(config_data)
        with self.assertRaises(exceptions.ValidationError):
            config.validate_config(configuration)