# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Wallpoppy/__init__.py
# Compiled at: 2018-12-24 18:50:29
# Size of source mod 2**32: 419 bytes
__license__ = 'Unlicense'
__docformat__ = 'reStructuredText'
from .bg import *

def run():
    """Run this module.

        :returns: Nothing
        :rtype: none
        .. todo::Implement this.
        """
    session_bus = pydbus.SessionBus()
    control = controlBus()
    session_bus.publish('moe.hattshire.bg', control)
    mainloop = GLib.MainLoop()
    mainloop.run()