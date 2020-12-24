# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/event/dd/drop_target.py
# Compiled at: 2013-04-04 15:36:37
"""An interface for components supporting drop operations."""
from muntjac.ui.component import IComponent

class IDropTarget(IComponent):
    """IDropTarget is an interface for components supporting drop operations. A
    component that wants to receive drop events should implement this interface
    and provide a L{DropHandler} which will handle the actual drop event.
    """

    def getDropHandler(self):
        """@return: the drop handler that will receive the dragged data or null
                if drops are not currently accepted
        """
        raise NotImplementedError

    def translateDropTargetDetails(self, clientVariables):
        """Called before the L{DragAndDropEvent} is passed to
        L{DropHandler}. Implementation may for example translate the drop
        target details provided by the client side (drop target) to meaningful
        server side values. If null is returned the terminal implementation
        will automatically create a L{TargetDetails} with raw client side data.

        @see: DragSource#getTransferable(Map)

        @param clientVariables:
                   data passed from the DropTargets client side counterpart.
        @return: A DropTargetDetails object with the translated data or null to
                use a default implementation.
        """
        raise NotImplementedError