# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/mrlpy/mevent.py
# Compiled at: 2017-08-14 10:53:07


class MEvent(object):
    """
    Event object to use with MEventDispatch.
    """

    def __init__(self, event_type):
        """
        The constructor accepts an event type as string
        """
        self._type = event_type

    @property
    def type(self):
        """
        Returns the event type
        """
        return self._type

    @property
    def data(self):
        """
        Returns the data associated to the event
        """
        return self._data