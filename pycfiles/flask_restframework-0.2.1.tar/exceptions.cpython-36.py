# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/logviewer/flask_validator/exceptions.py
# Compiled at: 2017-01-12 12:04:40
# Size of source mod 2**32: 209 bytes
__author__ = 'stas'

class ValidationError(Exception):

    def __init__(self, data):
        """
        :param data: Can be string or dict in format {field: "Message"}
        """
        self.data = data