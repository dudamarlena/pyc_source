# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ekca_service/settings.py
# Compiled at: 2020-03-08 11:02:40
# Size of source mod 2**32: 2218 bytes
"""
Default settings for ekca_service
"""
import logging, os
from .srv import app
LOG_CONFIG = os.path.join(app.instance_path, 'ekca-stderr-logging.conf')
LOG_NAME = 'ekca_service'
MAX_CONTENT_LENGTH = 500
VALID_USERNAME_REGEX = '^[a-z0-9_-]+$'
SSH_CA_PASSPHRASE = ''
SSH_CA_DIR = '/var/lib/ekca-ssh-ca'
SSH_KEYGEN_CMD = '/usr/bin/ssh-keygen'
SSH_CERT_VALIDITY = '+1h'
SSH_GENCA_ARGS = [
 '-t', 'rsa',
 '-b', '4096',
 '-N', SSH_CA_PASSPHRASE,
 '-q']
SSH_PASSPHRASE_LENGTH = 40
SSH_PASSPHRASE_ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
SSH_CERT_PERMISSIONS = [
 'pty']
SSH_FROMIP_METHOD = ''
OTP_CHECK_MOD = None
VALID_OTP_REGEX = '^[0-9]+$'
PASSWORD_CHECK_MOD = None