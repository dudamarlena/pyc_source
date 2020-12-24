# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/services/StorageService.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 2027 bytes
from os import environ, path as os_path
from platform import system
from json import load as json_load
import bitwarden_simple_cli.models.domain.CipherString as CipherString

class StorageService:
    app_path: str
    database_path: str
    database_filename = 'data.json'
    database_filename: str

    def __init__(self, database_path=None):
        self.database_path = self.set_database_path(database_path)
        self.database = self._read_datase_file()

    def get(self, key):
        return self.database.get(key)

    @staticmethod
    def guess_database_dir():
        if environ.get('BITWARDENCLI_APPDATA_DIR'):
            path = environ.get('BITWARDENCLI_APPDATA_DIR')
        else:
            if system() == 'Linux':
                path = environ.get('XDG_CONFIG_HOME')
            else:
                if system() == 'Darwin':
                    path = os_path.join(environ.get('HOME'), 'Library/Application Support/Bitwarden CLI')
                else:
                    if system() == 'Windows':
                        path = os_path.join(environ.get('APPDATA'), 'Bitwarden CLI')
                    else:
                        path = None
        if path is not None:
            if path != '':
                return path
        return os_path.join(environ.get('HOME'), '.config/Bitwarden CLI')

    def list_ciphers(self, user_id):
        ciphers = self.database.get('ciphers_' + user_id)
        list = []
        for k, cipher in ciphers.items():
            list.append(dict(id=(cipher['id']), name=(CipherString(cipher['name'])), org_id=(cipher.get('organizationId'))))

        return list

    def _read_datase_file(self):
        with open(self.database_path, 'r') as (fp):
            try:
                database = json_load(fp)
                return database
            except ValueError:
                print('error loading JSON')

    def set_database_path(self, path):
        if path is None:
            return self.set_database_path(os_path.join(self.guess_database_dir(), self.database_filename))
        if os_path.isfile(path):
            return path
        raise Exception('Database file not found at ' + path)