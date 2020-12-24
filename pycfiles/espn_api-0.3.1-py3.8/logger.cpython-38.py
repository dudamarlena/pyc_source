# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/espn_api/utils/logger.py
# Compiled at: 2020-04-25 13:44:14
# Size of source mod 2**32: 1361 bytes
import logging, sys

class Logger(object):

    def __init__(self, name: str, debug=False):
        level = logging.DEBUG if debug else logging.INFO
        self.logging = logging.getLogger(name)
        if len(self.logging.handlers):
            self.logging.handlers[0].setLevel(level)
            return None
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        handler.setLevel(level)
        self.logging.addHandler(handler)
        self.logging.setLevel(level)

    def log_request(self, endpoint: str, response: dict, params: dict=None, headers: dict=None):
        log = f"ESPN API Request: url: {endpoint} params: {params} headers: {headers} \nESPN API Response: {response}"
        self.logging.debug(log)