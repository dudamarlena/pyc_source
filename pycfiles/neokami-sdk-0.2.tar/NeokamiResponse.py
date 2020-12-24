# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: neokami/src/Neokami/NeokamiResponse.py
# Compiled at: 2015-04-30 12:24:14
""" Copyright 2015 Neokami GmbH. """
from .Base import Base as BaseNeokami
import json
from .Exceptions.NeokamiSDKException import NeokamiSDKException
from .Exceptions.NeokamiAuthorizationException import NeokamiAuthorizationException
from .Exceptions.NeokamiBlockedException import NeokamiBlockedException
from .Exceptions.NeokamiServerException import NeokamiServerException

class NeokamiResponse(BaseNeokami):

    def __init__(self, rawResponse, outputFormat='array', silentFails=False):
        """
                Initialize the response object
                :param object rawResponse:
                :param string outputFormat:
                :param bool silentFails:
                :return bool:
                """
        self.rawResponse = rawResponse
        self.responseObj = rawResponse.json()
        self.outputFormat = outputFormat
        self.silentFails = silentFails
        if not self.responseObj:
            raise NeokamiServerException(None, 503)
        self.validateResponse()
        return

    def validateResponse(self):
        """
                Check the response's status code and raise exception in case of a client or server error
                :return bool True:
                """
        if self.silentFails == True:
            return True
        status = self.status()
        for case in switch(status):
            if case(426):
                raise NeokamiSDKException(self.responseObj, 426)
            if case(401):
                raise NeokamiAuthorizationException(self.responseObj, 401)
            if case(500):
                raise NeokamiServerException(self.responseObj, 500)
            if case(400):
                raise NeokamiSDKException(self.responseObj, 400)
            if case(402):
                raise NeokamiBlockedException(self.responseObj, 402)
            if case(403):
                raise NeokamiBlockedException(self.responseObj, 403)
            if case():
                return True

    def format(self, data):
        """
                Return data in the specified format
                :param dict data:
                :return file_format data:
                """
        outputFormat = self.outputFormat
        for case in switch(outputFormat):
            if case('xml'):
                return self.toXML(data)
            if case('json'):
                return json.dumps(data)
            if case():
                return data

    def hasError(self):
        """
                Check whether or not the response has errors
                :return bool:
                """
        return self.responseObj['errors'] != None

    def retries(self):
        """
                Get the number of retries made during the request
                :return int:
                """
        if self.warnings()['retries']:
            return self.warnings()['retries']
        return 0

    def warnings(self):
        """
                Get warnings from the response
                :return dict:
                """
        return self.format(self.responseObj['warnings'])

    def result(self):
        """
                Get result from the response
                :return dict:
                """
        return self.format(self.responseObj['result'])

    def status(self):
        """
                Get status code from the response
                :return int:
                """
        return self.responseObj['status_code']

    def errors(self):
        """
                Get errors from the response
                :return dict:
                """
        if self.hasError():
            return self.responseObj['errors']

    def rawResponse(self):
        """
                Returns the json structure of the response
                :return:
                """
        return self.responseObj


class switch(object):

    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        if self.value in args:
            self.fall = True
            return True
        else:
            return False