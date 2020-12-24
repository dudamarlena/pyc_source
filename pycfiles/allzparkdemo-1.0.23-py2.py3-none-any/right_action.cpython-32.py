# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/acl/right_action.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jan 20, 2013\n\n@package: GUI security\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the ACL GUI right.\n'
from .right_sevice import RightService
from gui.action.api.action import Action

class RightAction(RightService):
    """
    The model that describes a right that is binded with actions.
    @see: RightService
    """

    def __init__(self, name, description):
        """
        @see: RightService.__init__
        """
        super().__init__(name, description)
        self._actions = []

    def actions(self):
        """
        Provides an iterator over the actions of the right.
        """
        return iter(self._actions)

    def addActions(self, *actions):
        """
        Add a new action to the right action.
        
        @param action: Action
            The action to be added.
        @return: self
            The self object for chaining purposes.
        """
        for action in actions:
            assert isinstance(action, Action), 'Invalid action %s' % action
            self._actions.append(action)

        return self