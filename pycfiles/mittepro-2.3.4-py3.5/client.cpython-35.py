# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mittepro/client.py
# Compiled at: 2020-01-28 09:11:47
# Size of source mod 2**32: 1838 bytes
import json
from api import endpoint, Api
from models import SearchMailArgs
from mitte_exceptions import ImproperlyConfigured

class MittePro(Api):

    def __init__(self, key=None, secret=None, fail_silently=False, server_uri=None, timeout_read=15):
        super(MittePro, self).__init__(fail_silently, timeout_read)
        if server_uri:
            self.server_uri = server_uri
        else:
            self.server_uri = 'https://www.mitte.pro'
        if not key:
            raise ImproperlyConfigured('A chave pública da API tem que ser passada no construtor')
        if not secret:
            raise ImproperlyConfigured('A chave privada da API tem que ser passada no construtor')
        self._api_key = key
        self._api_secret = secret

    @endpoint(Api.POST, '/api/send_mail/')
    def send(self, mail):
        response = self.request(payload=mail.get_payload())
        return response

    @endpoint(Api.POST, '/api/send_mail/template/')
    def send_template(self, mail):
        response = self.request(payload=mail.get_payload(endpoint='template'))
        return response

    @endpoint(Api.GET, '/api/mail/search/')
    def mail_search(self, search_args):
        if not isinstance(search_args, SearchMailArgs):
            AssertionError("Deve ser fornecido uma instancia do 'SearchMailArgs'.")
        response = self.request(payload=search_args.get_payload())
        return response

    @endpoint(Api.GET, '/api/mail/search/specifics/')
    def mail_search_by_ids(self, uuids):
        if not uuids:
            AssertionError('Uma lista de uuids tem que ser fornecida.')
        specifics = uuids
        if not isinstance(specifics, list):
            specifics = [
             specifics]
        response = self.request(payload={'uuids': json.dumps(specifics)})
        return response