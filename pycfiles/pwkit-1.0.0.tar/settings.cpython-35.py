# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pwkeeper/settings.py
# Compiled at: 2016-05-22 12:07:37
# Size of source mod 2**32: 471 bytes
import os
KEY_LENGTH = 256
BLOCK_LENGTH = 16
DEFAULT_PASSWORD_LENGTH = 25
PASSWORD_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
DATA_DIR = os.path.join(os.path.expanduser('~'), '.pwkeeper')
KEY_FILE = os.path.join(DATA_DIR, 'key')
PASSWORD_FILE = os.path.join(DATA_DIR, 'data')
PASSWORD_FILE_BACKUP = os.path.join(DATA_DIR, 'data-last')
PASSWORD_FILE_PLAINTEXT = os.path.join(DATA_DIR, 'tmp')
PAD_BYTE = '\x00'
CLIPBOARD_COMMAND = 'xsel'