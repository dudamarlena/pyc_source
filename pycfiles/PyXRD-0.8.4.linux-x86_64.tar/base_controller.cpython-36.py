# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/generic/controllers/base_controller.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 434 bytes
from mvc.controller import Controller
from .status_bar_mixin import StatusBarMixin

class BaseController(StatusBarMixin, Controller):
    file_filters = ('All Files', '*.*')
    widget_handlers = {}