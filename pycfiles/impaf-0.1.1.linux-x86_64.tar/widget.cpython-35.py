# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/socek/projects/impaf/core/build/lib/impaf/widget.py
# Compiled at: 2015-11-11 15:52:19
# Size of source mod 2**32: 415 bytes
from .requestable import Requestable

class Widget(Requestable):

    def feed_request(self, request):
        super().feed_request(request)
        self._create_context()

    def _create_context(self):
        self.context = {'request': self.request, 
         'widget': self}

    def add_widget(self, name, obj):
        obj.feed_request(self.request)
        self.context[name] = obj