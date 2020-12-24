# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/clickatell/client.py
# Compiled at: 2010-05-25 10:01:47
import logging
from clickatell.http import HttpClient
from clickatell import response
from clickatell.errors import ClickatellError
from clickatell.utils import Dispatcher

class ResponseDispatcher(Dispatcher):

    def do_ok(self, *args, **kwargs):
        return response.OKResponse(*args)

    def do_err(self, *args, **kwargs):
        return response.ERRResponse(*args)

    def do_id(self, *args, **kwargs):
        return response.IDResponse(*args)

    def do_credit(self, *args, **kwargs):
        return response.CreditResponse(*args)

    def do_apimsgid(self, *args, **kwargs):
        return response.ApiMsgIdResponse(*args)


class Client(HttpClient):
    base_url = 'https://api.clickatell.com'
    http_url = '%s/http' % base_url
    http_batch_url = '%s/http_batch' % base_url
    utils_url = '%s/utils' % base_url

    def __init__(self):
        self.dispatcher = ResponseDispatcher()

    def process_response(self, data):
        return [ self.dispatcher.dispatch(*response) for response in data ]

    def call(self, url, kwargs={}):
        response = self.get(url, kwargs)
        logging.debug('Got response: %s' % response)
        return self.process_response(response)

    def http(self, command, kwargs={}):
        return self.call('%s/%s' % (self.http_url, command), kwargs)

    def batch(self, command, kwargs={}):
        return self.call('%s/%s' % (self.http_batch_url, command), kwargs)

    def utils(self, command, kwargs={}):
        return self.call('%s/%s' % (self.utils_url, command), kwargs)