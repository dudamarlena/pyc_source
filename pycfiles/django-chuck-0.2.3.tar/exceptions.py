# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/django-chuck/django_chuck/exceptions.py
# Compiled at: 2012-06-01 04:12:37


class TemplateError(Exception):
    """
    General template error
    """
    __msg = ''

    def __init__(self, what):
        super(TemplateError, self).__init__()
        self.__msg = what

    def __str__(self):
        return str(self.__msg)