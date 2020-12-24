# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/inqbus/ocf/generic/handlers.py
# Compiled at: 2011-11-29 11:34:50
from container import Container
ACTION_START = 'start'
ACTION_STOP = 'stop'
ACTION_MONITOR = 'monitor'
ACTION_METADATA = 'meta-data'
ACTION_VALIDATE_ALL = 'validate-all'

class Handler(object):
    """Represents a handler for an action"""

    def __init__(self, handler, timeout):
        self.action = ''
        self.handler = handler
        self.timeout = timeout


class Handlers(Container):
    """Hold the handlers of a agent instance"""

    def __init__(self, *arg, **kw):
        super(Handlers, self).__init__(*arg, **kw)
        self.VALID_ACTIONS = [ACTION_START, ACTION_STOP, ACTION_MONITOR,
         ACTION_METADATA, ACTION_VALIDATE_ALL]

    def __setitem__(self, action, handler):
        """
        >>> a = Handlers()
        >>> a[ACTION_START] = Handler(Agent.meta_data, 10)
        
        >>> a['hello'] = Handler(Agent.meta_data, 10)
        Traceback (most recent call last):
            ...
        NotImplementedError: wrong OCF action name: hello

        >>> a[ACTION_START] = 3 
        Traceback (most recent call last):
            ...
        AttributeError: 'int' object has no attribute 'action'
        """
        self.__check_valid_action(action)
        dict.__setitem__(self, action, handler)
        handler.action = action

    def __getitem__(self, action):
        """
        >>> a = Handlers()
        
        >>> a['hello']
        Traceback (most recent call last):
            ...
        NotImplementedError: wrong OCF action name: hello
        """
        self.__check_valid_action(action)
        return dict.__getitem__(self, action)

    def __check_valid_action(self, action):
        """
        Check if the desired action is in the list of valid actions

        >>> a = Handlers()
        
        >>> a['hello']
        Traceback (most recent call last):
            ...
        NotImplementedError: wrong OCF action name: hello
        """
        if action not in self.VALID_ACTIONS:
            raise NotImplementedError('wrong OCF action name: %s' % action)