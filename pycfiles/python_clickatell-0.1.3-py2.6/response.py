# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/clickatell/response.py
# Compiled at: 2010-05-25 14:30:08
import re

class Response(object):
    key_value_pattern = re.compile('([a-zA-Z]+)\\: ([a-zA-Z0-9]+)')

    def __init__(self, data=''):
        self.data = data
        self.process(self.data)

    def parse_parts(self, data):
        """
        Parses incoming data like:
        
            312312312312 To: 27123456789
        
        To:
        
            '312312312312', {'To':'27123456789'}
        
        """
        collection = {}
        while 1:
            match = self.key_value_pattern.search(data)
            if match is None:
                break
            (key, value) = match.group(1, 2)
            collection[key] = value
            data = data.replace(match.group(0), '')

        return (
         data.strip(), collection)

    def process(self, data):
        """
        Override this method if you're expecting data in a different format.
        """
        (self.value, self.extra) = self.parse_parts(data)

    def __repr__(self):
        return '%s: %s' % (self.__class__.__name__, self.data)


class OKResponse(Response):
    pass


class ERRResponse(Response):

    def process(self, string):
        parts = string.split(', ', 1)
        code = parts[0]
        reason = ('').join(parts[1:]).strip()
        if code.isdigit():
            self.code = int(code)
            self.reason = reason
        else:
            self.code = 0
            self.value = code


class IDResponse(Response):
    pass


class CreditResponse(Response):
    kind = 'Credit'

    def process(self, string):
        self.value = float(string)


class ApiMsgIdResponse(Response):
    pass