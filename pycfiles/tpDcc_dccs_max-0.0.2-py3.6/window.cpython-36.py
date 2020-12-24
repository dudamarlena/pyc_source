# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/dccs/max/ui/window.py
# Compiled at: 2020-04-11 22:25:56
# Size of source mod 2**32: 548 bytes
"""
Module that contains functionality for Maya windows
"""
from __future__ import print_function, division, absolute_import
from tpDcc import register
from tpDcc.libs.qt.core import window as core_window

class MaxWindow(core_window.MainWindow, object):

    def __init__(self, *args, **kwargs):
        (super(MaxWindow, self).__init__)(*args, **kwargs)


register.register_class('Window', MaxWindow)
register.register_class('DockWindow', MaxWindow)
register.register_class('SubWindow', MaxWindow)