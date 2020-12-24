# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryanh/src/pynsot/tests/test_dotfile.py
# Compiled at: 2019-10-16 17:52:59
# Size of source mod 2**32: 3574 bytes
"""
Test the dotfile.
"""
from __future__ import unicode_literals
import copy, logging, os, tempfile, unittest
from pynsot import constants, dotfile
from .fixtures import DOTFILE_CONFIG_DATA
log = logging.getLogger(__name__)

class TestDotFile(unittest.TestCase):

    def setUp(self):
        """Automatically create a tempfile for each test."""
        fd, filepath = tempfile.mkstemp()
        self.filepath = filepath
        self.config_data = copy.deepcopy(DOTFILE_CONFIG_DATA)
        self.config_path = os.path.expanduser('~/.pynsotrc')
        self.backup_path = self.config_path + '.orig'
        self.backed_up = False
        if os.path.exists(self.config_path):
            log.debug('Config found, backing up...')
            os.rename(self.config_path, self.backup_path)
            self.backed_up = True

    def test_read_success(self):
        """Test that file can be read."""
        config = dotfile.Dotfile(self.filepath)
        config.write(self.config_data['auth_token'])
        config.read()

    def test_read_failure(self):
        """Test that that a missing file raises an error."""
        self.filepath = tempfile.mktemp()
        config = dotfile.Dotfile(self.filepath)
        self.assertRaises(IOError, config.read)

    def test_write(self):
        """Test that file can be written."""
        config = dotfile.Dotfile(self.filepath)
        config.write(self.config_data['auth_token'])

    def test_validate_perms_success(self):
        """Test that file permissions are ok."""
        self.filepath = tempfile.mktemp()
        config = dotfile.Dotfile(self.filepath)
        config.write({})
        config.validate_perms()

    def test_validate_fields_auth_token(self):
        """Test that auth_token fields check out."""
        config = dotfile.Dotfile(self.filepath)
        self._validate_test_fields('auth_token', config)

    def test_validate_fields_auth_header(self):
        """Test that auth_header fields check out."""
        config = dotfile.Dotfile(self.filepath)
        self._validate_test_fields('auth_header', config)

    def _validate_test_fields(self, auth_method, config):
        config_data = self.config_data[auth_method]
        for optional_field in constants.OPTIONAL_FIELDS:
            config_data.pop(optional_field, None)

        fields = sorted(config_data)
        my_config = {}
        required_fields = config.get_required_fields(auth_method)
        err = 'Missing required field: '
        for field in fields:
            with self.assertRaisesRegexp(dotfile.DotfileError, err + field):
                config.read()
                config.validate_fields(my_config, required_fields)
            my_config[field] = config_data[field]
            config.write(my_config)

    def tearDown(self):
        """Delete a tempfile if it exists. Otherwise carry on."""
        try:
            os.remove(self.filepath)
        except OSError:
            pass

        if self.backed_up:
            log.debug('Restoring original config.')
            os.rename(self.backup_path, self.config_path)