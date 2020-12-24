# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/whistle/event.py
# Compiled at: 2018-03-18 07:17:27
# Size of source mod 2**32: 627 bytes


class Event(object):
    __doc__ = "\n    Base class to represent whistle's events. You can subclass this if you want to embed special data and associated\n    logic with your events, or just let the event dispatcher create instances for you\n\n    The event handlers will have :class:`Event` instances passed, so you can bundle any data required by your handlers\n    there.\n\n    "
    propagation_stopped = False

    def stop_propagation(self):
        """Stop event propagation, meaning that the remaining handlers won't be called after this one."""
        self.propagation_stopped = True