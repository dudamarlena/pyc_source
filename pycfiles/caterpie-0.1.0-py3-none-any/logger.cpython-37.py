# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/catenae/logger.py
# Compiled at: 2019-08-07 08:55:15
# Size of source mod 2**32: 451 bytes
import logging

class Logger:

    def __init__(self, instance, level='info'):
        self.instance = instance
        logging.getLogger().setLevel(getattr(logging, level, logging.INFO))

    def log(self, message='', level='info'):
        if message:
            message = f"{self.instance.__class__.__name__}/{self.instance.uid} → {message}"
        getattr(logging, level.lower(), 'INFO')(message)