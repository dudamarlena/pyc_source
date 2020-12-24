# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyops\py_request.py
# Compiled at: 2020-04-17 11:56:32
# Size of source mod 2**32: 543 bytes


class PyRequest:

    def __init__(self, req):
        self.req = req
        self.env_config = req.config.ah_class_config

    def get_global(self, key):
        return self.env_config.get(key)

    def set_global(self, key, value):
        self.env_config[key] = value

    def del_global(self, key):
        if key in self.env_config:
            del self.env_config[key]

    def clear_global(self):
        self.env_config = {}