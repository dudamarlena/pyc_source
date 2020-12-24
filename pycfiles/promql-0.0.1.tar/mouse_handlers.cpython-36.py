# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/layout/mouse_handlers.py
# Compiled at: 2019-08-15 23:31:02
# Size of source mod 2**32: 780 bytes
from __future__ import unicode_literals
from itertools import product
from collections import defaultdict
__all__ = ('MouseHandlers', )

class MouseHandlers(object):
    """MouseHandlers"""

    def __init__(self):

        def dummy_callback(cli, mouse_event):
            """
            :param mouse_event: `MouseEvent` instance.
            """
            pass

        self.mouse_handlers = defaultdict(lambda : dummy_callback)

    def set_mouse_handler_for_range(self, x_min, x_max, y_min, y_max, handler=None):
        """
        Set mouse handler for a region.
        """
        for x, y in product(range(x_min, x_max), range(y_min, y_max)):
            self.mouse_handlers[(x, y)] = handler