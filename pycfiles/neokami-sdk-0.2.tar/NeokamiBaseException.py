# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: neokami/src/Neokami/Exceptions/NeokamiBaseException.py
# Compiled at: 2015-04-29 13:37:13
""" Copyright 2015 Neokami GmbH. """

class NeokamiBaseException(Exception):
    response = None

    def __init__(self, response, code=0):
        """
                Initialize the exception with information from the response and the status code
                :param dict response:
                :param int code:
                :return object Exception:
                """
        self.response = response
        message = 'Malformed server response, please try again later.'
        if isinstance(response, dict):
            errors = response['errors']
            message = ''
            for errorTuple in errors:
                message += errorTuple['message']

        super(NeokamiBaseException, self).__init__(message, code)

    def isMalformed(self):
        """
                Check whether or not is a valid response
                :return bool:
                """
        return not self.response

    def getError(self):
        """
                Get errors from the response
                :return dict :
                """
        if not self.isMalformed():
            return self.response['errors']

    def getWarnings(self):
        if not self.isMalformed():
            return self.response['warnings']