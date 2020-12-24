# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/CliSimple.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 1670 bytes
from .__version__ import __version__
from sys import exit
import bitwarden_simple_cli.Bitwarden as Bitwarden
import bitwarden_simple_cli.exceptions.ManagedException as ManagedException
from uuid import UUID

def is_uuid(uuid_string, version=4):
    try:
        uid = UUID(uuid_string, version=version)
        return uid.hex == uuid_string.replace('-', '')
    except ValueError:
        return False


class CliSimple:
    action: str
    field: str
    script_name: str
    uuid: str

    def __init__(self, script_name, action='version', field='password', uuid=None):
        self.field = field
        self.uuid = uuid
        if uuid is None:
            if is_uuid(self.field):
                self.field = 'password'
                self.uuid = field
        self.action = action
        self.script_name = script_name

    def run(self):
        if self.action == 'get':
            if self.uuid is None:
                print('Error: UUID is required to get secret')
                print(self.usage())
                exit(1)
            return self.get(self.uuid, self.field)
        if self.action == 'list':
            return self.list()
        return self.version()

    @staticmethod
    def usage(action='get'):
        if action == 'get':
            print('Usage: get UUID [field]')

    @staticmethod
    def get(uuid, field):
        try:
            app = Bitwarden()
            return app.get(uuid, field)
        except ManagedException as e:
            try:
                exit(e.args[0])
            finally:
                e = None
                del e

    @staticmethod
    def list():
        app = Bitwarden()
        return app.list()

    @staticmethod
    def version():
        print('Version: ' + __version__)