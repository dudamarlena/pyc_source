# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/gwt/server/drag_and_drop_service.py
# Compiled at: 2013-04-04 15:36:36
import logging
from muntjac.event.dd.target_details_impl import TargetDetailsImpl
from muntjac.terminal.variable_owner import IVariableOwner
from muntjac.terminal.gwt.server.json_paint_target import JsonPaintTarget
from muntjac.event.dd.drag_and_drop_event import DragAndDropEvent
from muntjac.event.transferable_impl import TransferableImpl
from muntjac.event.dd.drop_target import IDropTarget
from muntjac.event.dd.drag_source import IDragSource
from muntjac.terminal.gwt.client.ui.dd.v_drag_and_drop_manager import DragEventType
logger = logging.getLogger(__name__)

class DragAndDropService(IVariableOwner):

    def __init__(self, manager):
        self._manager = manager
        self._lastVisitId = None
        self._lastVisitAccepted = False
        self._dragEvent = None
        self._acceptCriterion = None
        return

    def changeVariables(self, source, variables):
        owner = variables.get('dhowner')
        if not isinstance(owner, IDropTarget):
            logger.critical('DropHandler owner ' + owner + ' must implement IDropTarget')
            return
        dropTarget = owner
        self._lastVisitId = variables.get('visitId')
        dropRequest = self.isDropRequest(variables)
        if dropRequest:
            self.handleDropRequest(dropTarget, variables)
        else:
            self.handleDragRequest(dropTarget, variables)

    def handleDropRequest(self, dropTarget, variables):
        """Handles a drop request from the VDragAndDropManager.
        """
        dropHandler = dropTarget.getDropHandler()
        if dropHandler is None:
            logger.info('IDropTarget.getDropHandler() returned null for owner: ' + dropTarget)
            return
        else:
            transferable = self.constructTransferable(dropTarget, variables)
            dropData = self.constructDragDropDetails(dropTarget, variables)
            dropEvent = DragAndDropEvent(transferable, dropData)
            if dropHandler.getAcceptCriterion().accept(dropEvent):
                dropHandler.drop(dropEvent)
            return

    def handleDragRequest(self, dropTarget, variables):
        """Handles a drag/move request from the VDragAndDropManager.
        """
        self._lastVisitId = variables.get('visitId')
        self._acceptCriterion = dropTarget.getDropHandler().getAcceptCriterion()
        transferable = self.constructTransferable(dropTarget, variables)
        dragDropDetails = self.constructDragDropDetails(dropTarget, variables)
        self._dragEvent = DragAndDropEvent(transferable, dragDropDetails)
        self._lastVisitAccepted = self._acceptCriterion.accept(self._dragEvent)

    def constructDragDropDetails(self, dropTarget, variables):
        """Construct DragDropDetails based on variables from client drop
        target. Uses DragDropDetailsTranslator if available, otherwise a
        default DragDropDetails implementation is used.
        """
        rawDragDropDetails = variables.get('evt')
        dropData = dropTarget.translateDropTargetDetails(rawDragDropDetails)
        if dropData is None:
            dropData = TargetDetailsImpl(rawDragDropDetails, dropTarget)
        return dropData

    def isDropRequest(self, variables):
        return self.getRequestType(variables) == DragEventType.DROP

    def getRequestType(self, variables):
        typ = int(variables.get('type'))
        return DragEventType.values()[typ]

    def constructTransferable(self, dropHandlerOwner, variables):
        sourceComponent = variables.get('component')
        variables = variables.get('tra')
        transferable = None
        if sourceComponent is not None and isinstance(sourceComponent, IDragSource):
            transferable = sourceComponent.getTransferable(variables)
        if transferable is None:
            transferable = TransferableImpl(sourceComponent, variables)
        return transferable

    def isEnabled(self):
        return True

    def isImmediate(self):
        return True

    def printJSONResponse(self, outWriter):
        if self._isDirty():
            outWriter.write(', "dd":')
            jsonPaintTarget = JsonPaintTarget(self._manager, outWriter, False)
            jsonPaintTarget.startTag('dd')
            jsonPaintTarget.addAttribute('visitId', self._lastVisitId)
            if self._acceptCriterion is not None:
                jsonPaintTarget.addAttribute('accepted', self._lastVisitAccepted)
                self._acceptCriterion.paintResponse(jsonPaintTarget)
            jsonPaintTarget.endTag('dd')
            jsonPaintTarget.close()
            self._lastVisitId = -1
            self._lastVisitAccepted = False
            self._acceptCriterion = None
            self._dragEvent = None
        return

    def _isDirty(self):
        if self._lastVisitId > 0:
            return True
        return False