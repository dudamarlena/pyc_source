# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/wavescli/__main__.py
# Compiled at: 2020-04-24 10:21:35
# Size of source mod 2**32: 785 bytes
import click
from .cli import main
from .apiclient import ApiClient

class CliObject(dict):
    __doc__ = 'Classe auxiliar criada para fazer lazy-initialization do\n    client da API sem mudar muito a estrutura do CLI'

    def __init__(self):
        self._client = None
        super(CliObject, self).__init__()

    @property
    def client(self):
        if self._client is None:
            cfg = self['config']
            url = cfg['WAVES_URL']
            key = cfg['API_KEY']
            self._client = ApiClient(url, key)
        return self._client


def run():
    default_context = CliObject()
    try:
        return main(obj=default_context)
    except Exception as exc:
        try:
            click.secho((str(exc)), fg='red')
        finally:
            exc = None
            del exc


if __name__ == '__main__':
    run()