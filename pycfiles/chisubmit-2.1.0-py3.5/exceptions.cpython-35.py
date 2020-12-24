# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/client/exceptions.py
# Compiled at: 2018-10-02 19:35:34
# Size of source mod 2**32: 4102 bytes
from __future__ import print_function
from pprint import pprint

class ChisubmitRequestException(Exception):

    def __init__(self, method, url, params, data, headers, response):
        Exception.__init__(self)
        self._ChisubmitRequestException__method = method
        self._ChisubmitRequestException__url = url
        self._ChisubmitRequestException__params = params
        self._ChisubmitRequestException__data = data
        self._ChisubmitRequestException__headers = headers
        self._ChisubmitRequestException__response = response

    @property
    def method(self):
        return self._ChisubmitRequestException__method

    @property
    def url(self):
        return self._ChisubmitRequestException__url

    @property
    def headers(self):
        return self._ChisubmitRequestException__headers

    @property
    def params(self):
        return self._ChisubmitRequestException__params

    @property
    def request_data(self):
        return self._ChisubmitRequestException__data

    @property
    def status(self):
        return self._ChisubmitRequestException__response.status_code

    @property
    def reason(self):
        return self._ChisubmitRequestException__response.reason

    @property
    def json(self):
        try:
            return self._ChisubmitRequestException__response.json()
        except ValueError:
            return {'data': self._ChisubmitRequestException__response.text}

    @property
    def response_data(self):
        return self._ChisubmitRequestException__response.text

    def __str__(self):
        return 'HTTP %i %s (%s %s)' % (self.status, self.reason, self.method, self.url)

    def print_debug_info(self):
        print('HTTP REQUEST')
        print('============')
        print('%s %s' % (self.method, self.url))
        print()
        print('Headers')
        print('-------')
        for hname, hvalue in list(self.headers.items()):
            print('%s: %s' % (hname, hvalue))

        print()
        print('Query string (GET parameters)')
        print('-----------------------------')
        if self.params is None:
            print('No querystring parameters')
        else:
            for pname, pvalue in list(self.params.items()):
                print('%s: %s' % (pname, pvalue))

        print()
        print('Request data')
        print('------------')
        if self.request_data is None:
            print('No data included in request')
        else:
            pprint(self.request_data)
        print()
        print('HTTP RESPONSE')
        print('=============')
        print('%s %s' % (self.status, self.reason))
        print()
        print('Headers')
        print('-------')
        for hname, hvalue in list(self._ChisubmitRequestException__response.headers.items()):
            print('%s: %s' % (hname, hvalue))

        print()
        print('Response body')
        print('-------------')
        try:
            response_data = self._ChisubmitRequestException__response.json()
            pprint(response_data)
        except ValueError:
            response_data = self._ChisubmitRequestException__response.text
            print(response_data)


class UnauthorizedException(ChisubmitRequestException):

    def __init__(self, *args, **kwargs):
        super(UnauthorizedException, self).__init__(*args, **kwargs)


class UnknownObjectException(ChisubmitRequestException):

    def __init__(self, *args, **kwargs):
        super(UnknownObjectException, self).__init__(*args, **kwargs)


class BadRequestException(ChisubmitRequestException):

    def __init__(self, *args, **kwargs):
        super(BadRequestException, self).__init__(*args, **kwargs)
        try:
            self.errors = self.json
            if any([not isinstance(k, (str, str)) for k in list(self.errors.keys())]):
                raise ValueError
            if any([not isinstance(v, (list, tuple)) for v in list(self.errors.values())]):
                raise ValueError
            self.valid_errors = True
        except ValueError:
            self.errors = {}
            self.valid_errors = False

    def print_errors(self):
        if self.valid_errors:
            for origin, reasons in list(self.errors.items()):
                print(origin)
                for r in reasons:
                    print(' - %s' % r)

                print()

        else:
            print('HTTP 400 response included incorrectly formatted error data:')
            print(self.response_data)