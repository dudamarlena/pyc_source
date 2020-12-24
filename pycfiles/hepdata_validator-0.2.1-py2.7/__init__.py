# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hepdata_validator/__init__.py
# Compiled at: 2020-02-28 12:45:28
import abc, os
from .version import __version__
__all__ = ('__version__', )
VALID_SCHEMA_VERSIONS = [
 '1.0.0', '0.1.0']
LATEST_SCHEMA_VERSION = VALID_SCHEMA_VERSIONS[0]
RAW_SCHEMAS_URL = 'https://raw.githubusercontent.com/HEPData/hepdata-validator/' + __version__ + '/hepdata_validator/schemas'

class Validator(object):
    """
    Provides a general 'interface' for Validator in HEPdata
    which validates schema files created with the
    JSONschema syntax http://json-schema.org/
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        self.messages = {}
        self.default_schema_file = ''
        self.schemas = kwargs.get('schemas', {})
        self.schema_version = kwargs.get('schema_version', LATEST_SCHEMA_VERSION)
        if self.schema_version not in VALID_SCHEMA_VERSIONS:
            raise ValueError('Invalid schema version ' + self.schema_version)

    def _get_schema_filepath(self, schema_filename):
        full_filepath = os.path.join(self.base_path, 'schemas', self.schema_version, schema_filename)
        if not os.path.isfile(full_filepath):
            raise ValueError('Invalid schema file ' + full_filepath)
        return full_filepath

    @abc.abstractmethod
    def validate(self, **kwargs):
        """
        Validates a file.
        :param file_path: path to file to be loaded.
        :param data: pre loaded YAML object (optional).
        :return: true if valid, false otherwise
        """
        pass

    def has_errors(self, file_name):
        """
        Returns true if the provided file name has error messages
        associated with it, false otherwise.
        :param file_name:
        :return: boolean
        """
        return file_name in self.messages

    def get_messages(self, file_name=None):
        """
        Return messages for a file (if file_name provided).
        If file_name is none, returns all messages as a dict.
        :param file_name:
        :return: array if file_name is provided, dict otherwise.
        """
        if file_name is None:
            return self.messages
        else:
            if file_name in self.messages:
                return self.messages[file_name]
            else:
                return []

            return

    def clear_messages(self):
        """
        Removes all error messages
        :return:
        """
        self.messages = {}

    def add_validation_message(self, message):
        """
        Adds a message to the messages dict
        :param message:
        """
        if message.file not in self.messages:
            self.messages[message.file] = []
        self.messages[message.file].append(message)

    def print_errors(self, file_name):
        """
        Prints the errors observed for a file
        """
        for error in self.get_messages(file_name):
            print (
             '\t', error.__unicode__())


class ValidationMessage(object):
    """
    An object to encapsulate information about an error including
    the file the error originated in, the error level, and the
    message itself.
    """
    file = ''
    level = ''
    message = ''

    def __init__(self, file='', level='error', message=''):
        self.file = file
        self.level = level
        self.message = message

    def __unicode__(self):
        return self.level + ' - ' + self.message