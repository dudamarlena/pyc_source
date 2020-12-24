# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/drag_and_drop_wrapper.py
# Compiled at: 2013-04-04 15:36:35
from muntjac.event.transferable_impl import TransferableImpl
from muntjac.event.dd.drag_source import IDragSource
from muntjac.event.dd.drop_target import IDropTarget
from muntjac.event.dd.target_details_impl import TargetDetailsImpl
from muntjac.ui.html5_file import Html5File
from muntjac.ui.custom_component import CustomComponent
from muntjac.terminal.gwt.client.mouse_event_details import MouseEventDetails
from muntjac.terminal.stream_variable import IStreamVariable, IStreamingEndEvent, IStreamingErrorEvent, IStreamingProgressEvent, IStreamingStartEvent
from muntjac.terminal.gwt.client.ui.dd.horizontal_drop_location import HorizontalDropLocation
from muntjac.terminal.gwt.client.ui.dd.vertical_drop_location import VerticalDropLocation

class DragAndDropWrapper(CustomComponent, IDropTarget, IDragSource):
    CLIENT_WIDGET = None

    def __init__(self, root):
        """Wraps given component in a L{DragAndDropWrapper}.

        @param root: the component to be wrapped
        """
        super(DragAndDropWrapper, self).__init__(root)
        self._receivers = dict()
        self._dragStartMode = DragStartMode.NONE
        self._dropHandler = None
        return

    def paintContent(self, target):
        super(DragAndDropWrapper, self).paintContent(target)
        target.addAttribute('dragStartMode', DragStartMode.ordinal(self._dragStartMode))
        if self.getDropHandler() is not None:
            self.getDropHandler().getAcceptCriterion().paint(target)
        if self._receivers is not None and len(self._receivers) > 0:
            for idd, html5File in self._receivers.iteritems():
                if html5File.getStreamVariable() is not None:
                    target.addVariable(self, 'rec-' + idd, ProxyReceiver(html5File))
                else:
                    target.addVariable(self, 'rec-' + idd, None)
                    del self._receivers[idd]

        return

    def getDropHandler(self):
        return self._dropHandler

    def setDropHandler(self, dropHandler):
        self._dropHandler = dropHandler
        self.requestRepaint()

    def translateDropTargetDetails(self, clientVariables):
        return WrapperTargetDetails(clientVariables, self)

    def getTransferable(self, rawVariables):
        return WrapperTransferable(self, rawVariables)

    def setDragStartMode(self, dragStartMode):
        self._dragStartMode = dragStartMode
        self.requestRepaint()

    def getDragStartMode(self):
        return self._dragStartMode


class WrapperTransferable(TransferableImpl):

    def __init__(self, sourceComponent, rawVariables):
        super(WrapperTransferable, self).__init__(sourceComponent, rawVariables)
        self._files = None
        fc = rawVariables.get('filecount')
        if fc is not None:
            self._files = [
             None] * fc
            for i in range(fc):
                fd = Html5File(rawVariables.get('fn%d' % i), rawVariables.get('fs%d' % i), rawVariables.get('ft%d' % i))
                idd = rawVariables.get('fi%d' % i)
                self._files[i] = fd
                self._sourceComponent._receivers[idd] = fd
                self._sourceComponent.requestRepaint()

        return

    def getDraggedComponent(self):
        """The component in wrapper that is being dragged or null if the
        transferrable is not a component (most likely an html5 drag).
        """
        return self.getData('component')

    def getMouseDownEvent(self):
        """@return: the mouse down event that started the drag and drop
        operation
        """
        return MouseEventDetails.deSerialize(self.getData('mouseDown'))

    def getFiles(self):
        return self._files

    def getText(self):
        data = self.getData('Text')
        if data is None:
            data = self.getData('text/plain')
        return data

    def getHtml(self):
        data = self.getData('Html')
        if data is None:
            data = self.getData('text/html')
        return data


class WrapperTargetDetails(TargetDetailsImpl):

    def __init__(self, rawDropData, wrapper):
        super(WrapperTargetDetails, self).__init__(rawDropData, wrapper)

    def getAbsoluteLeft(self):
        """@return: the absolute position of wrapper on the page"""
        return self.getData('absoluteLeft')

    def getAbsoluteTop(self):
        """@return: the absolute position of wrapper on the page"""
        return self.getData('absoluteTop')

    def getMouseEvent(self):
        """@return: details about the actual event that caused the event
                    details. Practically mouse move or mouse up.
        """
        return MouseEventDetails.deSerialize(self.getData('mouseEvent'))

    def getVerticalDropLocation(self):
        """@return: a detail about the drags vertical position over the
                    wrapper.
        """
        data = self.getData('verticalLocation')
        return VerticalDropLocation.valueOf[data]

    def getHorizontalDropLocation(self):
        """@return: a detail about the drags horizontal position over the
                    wrapper.
        """
        data = self.getData('horizontalLocation')
        return HorizontalDropLocation.valueOf[data]

    def verticalDropLocation(self):
        """@deprecated: use L{getVerticalDropLocation} instead"""
        return self.getVerticalDropLocation()

    def horizontalDropLocation(self):
        """@deprecated: use L{getHorizontalDropLocation} instead"""
        return self.getHorizontalDropLocation()


class DragStartMode(object):
    NONE = 'NONE'
    COMPONENT = 'COMPONENT'
    WRAPPER = 'WRAPPER'
    _values = [
     NONE, COMPONENT, WRAPPER]

    @classmethod
    def values(cls):
        return cls._values[:]

    @classmethod
    def ordinal(cls, val):
        return cls._values.index(val)


class ProxyReceiver(IStreamVariable):

    def __init__(self, fd):
        self._file = fd
        self._listenProgressOfUploadedFile = None
        return

    def getOutputStream(self):
        if self._file.getStreamVariable() is None:
            return
        else:
            return self._file.getStreamVariable().getOutputStream()

    def listenProgress(self):
        return self._file.getStreamVariable().listenProgress()

    def onProgress(self, event):
        wrapper = ReceivingEventWrapper(event, self._file, self)
        self._file.getStreamVariable().onProgress(wrapper)

    def streamingStarted(self, event):
        self._listenProgressOfUploadedFile = self._file.getStreamVariable() is not None
        if self._listenProgressOfUploadedFile:
            wrapper = ReceivingEventWrapper(event, self._file, self)
            self._file.getStreamVariable().streamingStarted(wrapper)
        self.receivers.remove(self._file)
        event.disposeStreamVariable()
        return

    def streamingFinished(self, event):
        if self._listenProgressOfUploadedFile:
            wrapper = ReceivingEventWrapper(event, self._file, self)
            self._file.getStreamVariable().streamingFinished(wrapper)

    def streamingFailed(self, event):
        if self._listenProgressOfUploadedFile:
            wrapper = ReceivingEventWrapper(event, self._file, self)
            self._file.getStreamVariable().streamingFailed(wrapper)

    def isInterrupted(self):
        return self._file.getStreamVariable().isInterrupted()


class ReceivingEventWrapper(IStreamingErrorEvent, IStreamingEndEvent, IStreamingStartEvent, IStreamingProgressEvent):

    def __init__(self, e, fd, receiver):
        self._wrappedEvent = e
        self._file = fd
        self._receiver = receiver

    def getMimeType(self):
        return self._file.getType()

    def getFileName(self):
        return self._file.getFileName()

    def getContentLength(self):
        return self._file.getFileSize()

    def getReceiver(self):
        return self._receiver

    def getException(self):
        if isinstance(self._wrappedEvent, IStreamingErrorEvent):
            return self._wrappedEvent.getException()
        else:
            return

    def getBytesReceived(self):
        return self._wrappedEvent.getBytesReceived()

    def disposeStreamVariable(self):
        """Calling this method has no effect. DD files are receive only
        once anyway.
        """
        pass