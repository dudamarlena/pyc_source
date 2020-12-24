# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/action.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 3650 bytes
__doc__ = 'PyAMS_form.action module\n\nThis module defines all actions.\n'
from zope.interface import implementer, implementer_only
from pyams_form.interfaces.button import ActionExecutionError, IAction, IActionErrorEvent, IActionEvent, IActionHandler, IActions
from pyams_form.util import Manager, create_id
__docformat__ = 'restructuredtext'

@implementer(IActionEvent)
class ActionEvent:
    """ActionEvent"""

    def __init__(self, action):
        self.action = action

    def __repr__(self):
        return '<%s for %r>' % (self.__class__.__name__, self.action)


@implementer(IActionErrorEvent)
class ActionErrorOccurred(ActionEvent):
    """ActionErrorOccurred"""

    def __init__(self, action, error):
        super(ActionErrorOccurred, self).__init__(action)
        self.error = error


class ActionSuccessful(ActionEvent):
    """ActionSuccessful"""
    pass


@implementer(IAction)
class Action:
    """Action"""
    __name__ = __parent__ = None

    def __init__(self, request, title, name=None):
        self.request = request
        self.title = title
        if name is None:
            name = create_id(title)
        self.name = name

    def is_executed(self):
        """Check if action was executed by looking for action name into request params"""
        return self.name in self.request.params

    def __repr__(self):
        return '<%s %r %r>' % (self.__class__.__name__, self.name, self.title)


@implementer_only(IActions)
class Actions(Manager):
    """Actions"""
    __name__ = __parent__ = None

    def __init__(self, form, request, content):
        super(Actions, self).__init__()
        self.form = form
        self.request = request
        self.content = content

    @property
    def executed_actions(self):
        """Get list of executed actions"""
        return [action for action in self.values() if action.is_executed()]

    def update(self):
        """See pyams_form.interfaces.button.IActions."""
        pass

    def execute(self):
        """See pyams_form.interfaces.button.IActions."""
        registry = self.request.registry
        for action in self.executed_actions:
            handler = registry.queryMultiAdapter((self.form, self.request, self.content, action), IActionHandler)
            if handler is not None:
                try:
                    result = handler()
                except ActionExecutionError as error:
                    registry.notify(ActionErrorOccurred(action, error))
                else:
                    registry.notify(ActionSuccessful(action))
                    return result

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.__name__)


@implementer(IActionHandler)
class ActionHandlerBase:
    """ActionHandlerBase"""

    def __init__(self, form, request, content, action):
        self.form = form
        self.request = request
        self.content = content
        self.action = action