# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/loup/Workspace/Projects/personal/palmer/palmer/request.py
# Compiled at: 2016-11-16 03:38:58
# Size of source mod 2**32: 786 bytes
from __future__ import unicode_literals
import datetime
from flask import Request
from palmer.config import default_config

class APIRequest(Request):
    renderer_class = default_config.RENDERER_CLASS

    def __init__(self, *args, **kwargs):
        self.request_at = datetime.datetime.utcnow()
        super(APIRequest, self).__init__(*args, **kwargs)

    @property
    def form_data(self):
        data = self.form.copy()
        if self.files:
            data.update(self.files)
        return data

    @property
    def renderer(self):
        if not hasattr(self, '_renderer'):
            self._renderer = self.renderer_class()
        return self._renderer

    @renderer.setter
    def renderer(self, renderer):
        self._renderer = renderer