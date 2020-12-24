# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/omer/DjangoProjects/basitapi/basitapi/exception.py
# Compiled at: 2012-11-04 09:37:42


class ApiException(Exception):
    """
    Beklenilen hatalar için kullanılır. Kullanıcıların düzgün bir şekilde bilgilendirilmesini sağlar.
    """

    def __init__(self, message='', status=400, application_code=None):
        self.message = message
        self.status = status
        self.application_code = application_code