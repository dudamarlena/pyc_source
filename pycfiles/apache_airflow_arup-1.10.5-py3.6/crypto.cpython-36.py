# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/models/crypto.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3042 bytes
from builtins import ImportError as BuiltinImportError
from airflow import configuration
from airflow.exceptions import AirflowException
from airflow.utils.log.logging_mixin import LoggingMixin

class InvalidFernetToken(Exception):
    pass


class NullFernet(object):
    __doc__ = '\n    A "Null" encryptor class that doesn\'t encrypt or decrypt but that presents\n    a similar interface to Fernet.\n\n    The purpose of this is to make the rest of the code not have to know the\n    difference, and to only display the message once, not 20 times when\n    `airflow initdb` is ran.\n    '
    is_encrypted = False

    def decrypt(self, b):
        return b

    def encrypt(self, b):
        return b


_fernet = None

def get_fernet():
    """
    Deferred load of Fernet key.

    This function could fail either because Cryptography is not installed
    or because the Fernet key is invalid.

    :return: Fernet object
    :raises: airflow.exceptions.AirflowException if there's a problem trying to load Fernet
    """
    global InvalidFernetToken
    global _fernet
    log = LoggingMixin().log
    if _fernet:
        return _fernet
    try:
        from cryptography.fernet import Fernet, MultiFernet, InvalidToken
        InvalidFernetToken = InvalidToken
    except BuiltinImportError:
        log.warning('cryptography not found - values will not be stored encrypted.')
        _fernet = NullFernet()
        return _fernet
    else:
        try:
            fernet_key = configuration.conf.get('core', 'FERNET_KEY')
            if not fernet_key:
                log.warning('empty cryptography key - values will not be stored encrypted.')
                _fernet = NullFernet()
            else:
                _fernet = MultiFernet([Fernet(fernet_part.encode('utf-8')) for fernet_part in fernet_key.split(',')])
                _fernet.is_encrypted = True
        except (ValueError, TypeError) as ve:
            raise AirflowException('Could not create Fernet object: {}'.format(ve))

        return _fernet