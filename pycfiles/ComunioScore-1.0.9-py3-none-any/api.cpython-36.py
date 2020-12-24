# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ComunioScore/api.py
# Compiled at: 2020-05-01 18:27:16
# Size of source mod 2**32: 430 bytes
import json, logging
from flask import Response, request

class APIHandler:
    """APIHandler"""

    def __init__(self):
        self.logger = logging.getLogger('ComunioScore')
        self.logger.info('Create class APIHandler')

    def index(self):
        """

        :return:
        """
        return 'hello world'