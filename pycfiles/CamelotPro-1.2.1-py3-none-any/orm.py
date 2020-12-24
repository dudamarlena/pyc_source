# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/action_steps/orm.py
# Compiled at: 2013-04-11 17:47:52
__doc__ = '\nVarious ``ActionStep`` subclasses that inform the GUI of changes\nin the model.\n\nThese action steps can be used to update the GUI before changes have been\nsaved to the database through the manual updates :\n    \n.. literalinclude:: ../../../test/test_action.py\n   :start-after: begin manual update\n   :end-before: end manual update\n       \nOr use introspection of the SQLAlchemy session to update the GUI :\n\n.. literalinclude:: ../../../test/test_action.py\n   :start-after: begin auto update\n   :end-before: end auto update\n   \n'
from camelot.admin.action.base import ActionStep
from camelot.view.remote_signals import get_signal_handler

class FlushSession(ActionStep):
    """Flushes the session and informs the GUI about the
    changes.
    
    :param session: an instance of :class:`sqlalchemy.orm.Session`
    :param update_depending_objects: set to `False` if the objects that depend
        on an object that has been modified need not to be updated in the GUI.
        This will make the flushing faster, but the GUI might become
        inconsistent.
    """

    def __init__(self, session, update_depending_objects=True):
        signal_handler = get_signal_handler()
        dirty_objects = set(session.dirty)
        for obj_to_delete in session.deleted:
            signal_handler.sendEntityDelete(self, obj_to_delete)

        for obj_to_delete in session.deleted:
            try:
                dirty_objects.remove(obj_to_delete)
            except KeyError:
                pass

        session.flush()
        for obj in dirty_objects:
            signal_handler.sendEntityUpdate(self, obj)

    def gui_run(self, gui_context):
        pass


class UpdateObject(ActionStep):
    """Inform the GUI that obj has changed.

    :param obj: the object that has changed
    """

    def __init__(self, obj):
        signal_handler = get_signal_handler()
        if obj != None:
            signal_handler.sendEntityUpdate(self, obj)
        return

    def gui_run(self, gui_context):
        pass


class DeleteObject(ActionStep):
    """Inform the GUI that obj is going to be deleted.

    :param obj: the object that is going to be deleted
    """

    def __init__(self, obj):
        signal_handler = get_signal_handler()
        if obj != None:
            signal_handler.sendEntityDelete(self, obj)
        return

    def gui_run(self, gui_context):
        pass


class CreateObject(ActionStep):
    """Inform the GUI that obj was created.

    :param obj: the object that was created
    """

    def __init__(self, obj):
        signal_handler = get_signal_handler()
        if obj != None:
            signal_handler.sendEntityCreate(self, obj)
        return

    def gui_run(self, gui_context):
        pass