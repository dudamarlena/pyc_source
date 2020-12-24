# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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