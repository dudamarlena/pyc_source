# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ComunioScore/api.py
# Compiled at: 2020-05-01 18:27:16
# Size of source mod 2**32: 430 bytes
import json, logging
from flask import Response, request

class APIHandler:
    __doc__ = ' class APIHandler to link routes to specific handler function\n\n    USAGE:\n            api = APIHandler()\n\n    '

    def __init__(self):
        self.logger = logging.getLogger('ComunioScore')
        self.logger.info('Create class APIHandler')

    def index(self):
        """

        :return:
        """
        return 'hello world'