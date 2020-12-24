# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/maxipago/resources/card.py
# Compiled at: 2018-07-09 07:37:35
# Size of source mod 2**32: 1115 bytes
from io import BytesIO
from maxipago.utils import etree
from maxipago.resources.base import Resource
from maxipago.exceptions import CardException

class CardAddResource(Resource):

    def process(self):
        tree = etree.parse(BytesIO(self.data))
        error_code = tree.find('errorCode').text
        if error_code != '0':
            error_message = tree.find('errorMessage').text
            raise CardException(message=error_message)
        self._meta = {'command':tree.find('command').text, 
         'time':tree.find('time').text}
        self.token = tree.find('result').find('token').text


class CardDeleteResource(Resource):

    def process(self):
        tree = etree.parse(BytesIO(self.data))
        error_code = tree.find('errorCode').text
        if error_code != '0':
            error_message = tree.find('errorMessage').text
            raise CardException(message=error_message)
        self._meta = {'command':tree.find('command').text, 
         'time':tree.find('time').text}
        self.success = True