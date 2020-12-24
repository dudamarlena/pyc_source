# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/gui/action/impl/action.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Feb 27, 2012\n\n@package: gui action\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Mihai Balaceanu\n\nAction Manager Implementation\n'
from ally.container.ioc import injected
from ally.container.support import setup
from ally.support.api.util_service import copy
from gui.action.api.action import IActionManagerService, Action
import re

@injected
@setup(IActionManagerService, name='actionManager')
class ActionManagerService(IActionManagerService):
    """
    @see: IActionManagerService
    """

    def __init__(self):
        """  """
        self._actions = {}

    def add(self, action):
        """
        @see: IActionManagerService.add
        """
        assert isinstance(action, Action), 'Invalid action %s' % action
        self._actions[action.Path] = action
        return action.Path

    def getAll(self, path, origPath=None):
        """
        @see: IActionManagerService.getAll
        """
        actions = self._actions.values()
        if path:
            if re.match('".+"', path):
                actions = [action for action in actions if action.Path == path.strip('"')]
            else:
                if path.find('*') != -1:
                    p = '^' + re.sub('\\\\\\*', '(\\d|\\w|-|_)+', re.escape(path)) + '$'
                    actions = [action for action in actions if re.match(p, action.Path)]
                else:
                    actions = [action for action in actions if action.Path.startswith(path.rstrip('.'))]
        return processChildCount(actions)


def processChildCount(actions):
    """
    Process the child count for the provided actions list.
    """
    actions = sorted(actions, key=lambda action: action.Path)
    for k, action in enumerate(actions):
        actionWithCount = Action()
        copy(action, actionWithCount, exclude=('ChildrenCount', ))
        childCount, path = 0, action.Path + '.'
        for i in range(k + 1, len(actions)):
            if actions[i].Path.startswith(path):
                childCount += 1
            else:
                break

        actionWithCount.ChildrenCount = childCount
        yield actionWithCount