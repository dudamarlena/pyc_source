# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/gwt/server/abstract_communication_manager.py
# Compiled at: 2013-04-04 15:36:36
"""Defines a common base class for the server-side implementations of
the communication system between the client code and the server side
components."""
import re, uuid, logging
from warnings import warn
from sys import stderr
from urlparse import urljoin
try:
    from cStringIO import StringIO as cStringIO
    from StringIO import StringIO
except ImportError as e:
    from StringIO import StringIO as cStringIO
    from StringIO import StringIO

from babel import Locale
from muntjac.util import clsname
from muntjac.terminal.gwt.server.json_paint_target import JsonPaintTarget
from muntjac.terminal.gwt.server.exceptions import UploadException
from muntjac.terminal.paintable import IPaintable, IRepaintRequestListener
from muntjac.terminal.terminal import IErrorEvent as TerminalErrorEvent
from muntjac.terminal.uri_handler import IErrorEvent as URIHandlerErrorEvent
from muntjac.ui.abstract_component import AbstractComponent
from muntjac.ui.window import Window
from muntjac.ui.component import IComponent
from muntjac.ui.abstract_field import AbstractField
from muntjac.terminal.gwt.server.streaming_events import StreamingStartEventImpl, StreamingErrorEventImpl, StreamingEndEventImpl
from muntjac.terminal.gwt.server.drag_and_drop_service import DragAndDropService
from muntjac.terminal.gwt.client.application_connection import ApplicationConnection
from muntjac.terminal.gwt.server.exceptions import NoInputStreamException, NoOutputStreamException
from muntjac.terminal.gwt.server.abstract_application_servlet import AbstractApplicationServlet, URIHandlerErrorImpl
from muntjac.terminal.gwt.server.change_variables_error_event import ChangeVariablesErrorEvent
from muntjac.terminal.gwt.server.streaming_events import StreamingProgressEventImpl
logger = logging.getLogger(__file__)

class AbstractCommunicationManager(IPaintable, IRepaintRequestListener):
    """This is a common base class for the server-side implementations of
    the communication system between the client code (compiled with GWT
    into JavaScript) and the server side components. Its client side
    counterpart is L{ApplicationConnection}.

    A server side component sends its state to the client in a paint request
    (see L{IPaintable} and L{PaintTarget} on the server side). The
    client widget receives these paint requests as calls to
    L{muntjac.terminal.gwt.client.IPaintable.updateFromUIDL}. The
    client component communicates back to the server by sending a list of
    variable changes (see L{ApplicationConnection.updateVariable} and
    L{VariableOwner.changeVariables}).
    """
    _DASHDASH = '--'
    _GET_PARAM_REPAINT_ALL = 'repaintAll'
    _WRITE_SECURITY_TOKEN_FLAG = 'writeSecurityToken'
    _VAR_PID = 1
    _VAR_NAME = 2
    _VAR_TYPE = 3
    _VAR_VALUE = 0
    _VTYPE_PAINTABLE = 'p'
    _VTYPE_BOOLEAN = 'b'
    _VTYPE_DOUBLE = 'd'
    _VTYPE_FLOAT = 'f'
    _VTYPE_LONG = 'l'
    _VTYPE_INTEGER = 'i'
    _VTYPE_STRING = 's'
    _VTYPE_ARRAY = 'a'
    _VTYPE_STRINGARRAY = 'c'
    _VTYPE_MAP = 'm'
    _VAR_RECORD_SEPARATOR = '\x1e'
    _VAR_FIELD_SEPARATOR = '\x1f'
    VAR_BURST_SEPARATOR = '\x1d'
    VAR_ARRAYITEM_SEPARATOR = '\x1c'
    VAR_ESCAPE_CHARACTER = '\x1b'
    _MAX_BUFFER_SIZE = 65536
    _MAX_UPLOAD_BUFFER_SIZE = 4096
    _GET_PARAM_ANALYZE_LAYOUTS = 'analyzeLayouts'
    _nextUnusedWindowSuffix = 1
    _LF = '\n'
    _CRLF = '\r\n'
    _UTF8 = 'UTF8'
    _GET_PARAM_HIGHLIGHT_COMPONENT = 'highlightComponent'

    def __init__(self, application):
        self._application = application
        self._currentlyOpenWindowsInClient = dict()
        self._dirtyPaintables = list()
        self._paintableIdMap = dict()
        self._idPaintableMap = dict()
        self._idSequence = 0
        self._closingWindowName = None
        self._locales = None
        self._pendingLocalesIndex = None
        self._timeoutInterval = -1
        self._dragAndDropService = None
        self._requestThemeName = None
        self._maxInactiveInterval = None
        self.requireLocale(str(application.getLocale()))
        self._typeToKey = dict()
        self._nextTypeKey = 0
        self._highLightedPaintable = None
        return

    def getApplication(self):
        return self._application

    @classmethod
    def _readLine(cls, stream):
        return stream.readline()

    def doHandleSimpleMultipartFileUpload(self, request, response, streamVariable, variableName, owner, boundary):
        """Method used to stream content from a multipart request (either
        from servlet or portlet request) to given StreamVariable.

        @raise IOException:
        """
        inputStream = request.getInputStream()
        contentLength = request.getContentLength()
        atStart = False
        firstFileFieldFound = False
        rawfilename = 'unknown'
        rawMimeType = 'application/octet-stream'
        while not atStart:
            readLine = inputStream.readline()
            contentLength -= len(readLine) + 2
            if readLine.startswith('Content-Disposition:') and readLine.find('filename=') > 0:
                rawfilename = readLine.replace('.*filename=', '')
                parenthesis = rawfilename[:1]
                rawfilename = rawfilename[1:]
                rawfilename = rawfilename[:rawfilename.find(parenthesis)]
                firstFileFieldFound = True
            elif firstFileFieldFound and readLine == '':
                atStart = True
            elif readLine.startswith('Content-Type'):
                rawMimeType = readLine.split(': ')[1]

        contentLength -= len(boundary) + len(self._CRLF) + 2 * len(self._DASHDASH) + 2
        simpleMultiPartReader = SimpleMultiPartInputStream(inputStream, boundary, self)
        filename = self.removePath(rawfilename)
        mimeType = rawMimeType
        try:
            component = owner
            if component.isReadOnly():
                raise UploadException('Warning: file upload ignored because the component was read-only')
            forgetVariable = self.streamToReceiver(simpleMultiPartReader, streamVariable, filename, mimeType, contentLength)
            if forgetVariable:
                self.cleanStreamVariable(owner, variableName)
        except Exception as e:
            self.handleChangeVariablesError(self._application, owner, e, dict())

        self.sendUploadResponse(request, response)

    def doHandleXhrFilePost(self, request, response, streamVariable, variableName, owner, contentLength):
        """Used to stream plain file post (aka XHR2.post(File))

        @raise IOException:
        """
        filename = 'unknown'
        mimeType = filename
        stream = request.getInputStream()
        try:
            component = owner
            if component.isReadOnly():
                raise UploadException('Warning: file upload ignored because the component was read-only')
            forgetVariable = self.streamToReceiver(stream, streamVariable, filename, mimeType, contentLength)
            if forgetVariable:
                self.cleanStreamVariable(owner, variableName)
        except Exception as e:
            self.handleChangeVariablesError(self._application, owner, e, dict())

        self.sendUploadResponse(request, response)

    def streamToReceiver(self, inputStream, streamVariable, filename, typ, contentLength):
        """@return: true if the streamvariable has informed that the terminal
                    can forget this variable
        @raise UploadException:
        """
        if streamVariable is None:
            raise ValueError, 'StreamVariable for the post not found'
        out = None
        totalBytes = 0
        startedEvent = StreamingStartEventImpl(filename, typ, contentLength)
        try:
            streamVariable.streamingStarted(startedEvent)
            out = streamVariable.getOutputStream()
            listenProgress = streamVariable.listenProgress()
            if out is None:
                raise NoOutputStreamException()
            if inputStream is None:
                raise NoInputStreamException()
            bufferSize = self._MAX_UPLOAD_BUFFER_SIZE
            bytesReadToBuffer = 0
            while totalBytes < len(inputStream):
                buff = inputStream.read(bufferSize)
                bytesReadToBuffer = inputStream.pos - bytesReadToBuffer
                out.write(buff)
                totalBytes += bytesReadToBuffer
                if listenProgress:
                    progressEvent = StreamingProgressEventImpl(filename, typ, contentLength, totalBytes)
                    streamVariable.onProgress(progressEvent)
                if streamVariable.isInterrupted():
                    raise UploadInterruptedException()

            out.close()
            event = StreamingEndEventImpl(filename, typ, totalBytes)
            streamVariable.streamingFinished(event)
        except UploadInterruptedException as e:
            self.tryToCloseStream(out)
            event = StreamingErrorEventImpl(filename, typ, contentLength, totalBytes, e)
            streamVariable.streamingFailed(event)
        except Exception as e:
            self.tryToCloseStream(out)
            event = StreamingErrorEventImpl(filename, typ, contentLength, totalBytes, e)
            streamVariable.streamingFailed(event)
            raise UploadException(e)

        return startedEvent.isDisposed()

    def tryToCloseStream(self, out):
        try:
            if out is not None:
                out.close()
        except IOError:
            pass

        return

    @classmethod
    def removePath(cls, filename):
        r"""Removes any possible path information from the filename and
        returns the filename. Separators / and \ are used.
        """
        if filename is not None:
            filename = re.sub('^.*[/\\\\]', '', filename)
        return filename

    def sendUploadResponse(self, request, response):
        """@raise IOException:
        """
        response.setContentType('text/html')
        out = response.getOutputStream()
        out.write('<html><body>download handled</body></html>')
        out.flush()
        out.close()

    def doHandleUidlRequest(self, request, response, callback, window):
        """Internally process a UIDL request from the client.

        This method calls L{handleVariables} to process any changes to
        variables by the client and then repaints affected components
        using L{paintAfterVariableChanges}.

        Also, some cleanup is done when a request arrives for an application
        that has already been closed.

        The method handleUidlRequest() in subclasses should call this method.

        @param request:
        @param response:
        @param callback:
        @param window:
                   target window for the UIDL request, can be null if target
                   not found
        @raise IOException:
        @raise InvalidUIDLSecurityKeyException:
        """
        self._requestThemeName = request.getParameter('theme')
        self._maxInactiveInterval = request.getSession().getMaxInactiveInterval()
        repaintAll = request.getParameter(self._GET_PARAM_REPAINT_ALL) is not None
        out = response.getOutputStream()
        analyzeLayouts = False
        if repaintAll:
            analyzeLayouts = request.getParameter(self._GET_PARAM_ANALYZE_LAYOUTS) is not None
            param = request.getParameter(self._GET_PARAM_HIGHLIGHT_COMPONENT)
            if param != None:
                pid = request.getParameter(self._GET_PARAM_HIGHLIGHT_COMPONENT)
                highLightedPaintable = self._idPaintableMap.get(pid)
                self.highlightPaintable(highLightedPaintable)
        outWriter = out
        if self._application.isRunning():
            if window is None:
                logger.warning('Could not get window for application with request ID ' + request.getRequestID())
                return
        else:
            self.endApplication(request, response, self._application)
            return
        if not self.handleVariables(request, response, callback, self._application, window):
            ci = None
            try:
                ci = self._application.__class__.getSystemMessages()
            except Exception:
                logger.warning('getSystemMessages() failed - continuing')

            if ci is not None:
                msg = ci.getOutOfSyncMessage()
                cap = ci.getOutOfSyncCaption()
                if msg is not None or cap is not None:
                    callback.criticalNotification(request, response, cap, msg, None, ci.getOutOfSyncURL())
                    return
            repaintAll = True
        self.paintAfterVariableChanges(request, response, callback, repaintAll, outWriter, window, analyzeLayouts)
        if self._closingWindowName is not None:
            if self._closingWindowName in self._currentlyOpenWindowsInClient:
                del self._currentlyOpenWindowsInClient[self._closingWindowName]
            self._closingWindowName = None
        self._requestThemeName = None
        return

    def highlightPaintable(self, highLightedPaintable2):
        sb = StringIO()
        sb.write('*** Debug details of a component:  *** \n')
        sb.write('Type: ')
        sb.write(clsname(highLightedPaintable2))
        if isinstance(highLightedPaintable2, AbstractComponent):
            component = highLightedPaintable2
            sb.write('\nId:')
            idd = self._paintableIdMap.get(component)
            sb.write(idd if idd is not None else 'null')
            if component.getCaption() is not None:
                sb.write('\nCaption:')
                sb.write(component.getCaption())
            self.printHighlightedComponentHierarchy(sb, component)
        logger.info(sb.getvalue())
        sb.close()
        return

    def printHighlightedComponentHierarchy(self, sb, component):
        h = list()
        h.append(component)
        parent = component.getParent()
        while parent is not None:
            h.insert(0, parent)
            parent = parent.getParent()

        sb.write('\nComponent hierarchy:\n')
        application2 = component.getApplication()
        sb.write(clsname(application2))
        sb.write('.')
        sb.write(application2.__class__.__name__)
        sb.write('(')
        sb.write(application2.__class__.__name__)
        sb.write('.java')
        sb.write(':1)')
        l = 1
        for component2 in h:
            sb.write('\n')
            for _ in range(l):
                sb.write('  ')

            l += 1
            componentClass = component2.__class__
            topClass = componentClass
            sb.write(clsname(componentClass))
            sb.write('.')
            sb.write(componentClass.__name__)
            sb.write('(')
            sb.write(topClass.__name__)
            sb.write('.java:1)')

        return

    def paintAfterVariableChanges(self, request, response, callback, repaintAll, outWriter, window, analyzeLayouts):
        """@raise PaintException:
        @raise IOException:
        """
        if repaintAll:
            self.makeAllPaintablesDirty(window)
        if not self._application.isRunning():
            self.endApplication(request, response, self._application)
            return
        else:
            self.openJsonMessage(outWriter, response)
            writeSecurityTokenFlag = request.getAttribute(self._WRITE_SECURITY_TOKEN_FLAG, None)
            if writeSecurityTokenFlag is not None:
                seckey = request.getSession().getAttribute(ApplicationConnection.UIDL_SECURITY_TOKEN_ID, None)
                if seckey is None:
                    seckey = str(uuid.uuid4())
                    request.getSession().setAttribute(ApplicationConnection.UIDL_SECURITY_TOKEN_ID, seckey)
                outWriter.write('"' + ApplicationConnection.UIDL_SECURITY_TOKEN_ID + '":"')
                outWriter.write(seckey)
                outWriter.write('",')
            if window.getName() == self._closingWindowName:
                outWriter.write('"changes":[]')
            else:
                newWindow = self.doGetApplicationWindow(request, callback, self._application, window)
                if newWindow != window:
                    window = newWindow
                    repaintAll = True
                self.writeUidlResponce(callback, repaintAll, outWriter, window, analyzeLayouts)
            self.closeJsonMessage(outWriter)
            return

    def writeUidlResponce(self, callback, repaintAll, outWriter, window, analyzeLayouts):
        outWriter.write('"changes":[')
        paintables = None
        invalidComponentRelativeSizes = None
        paintTarget = JsonPaintTarget(self, outWriter, not repaintAll)
        windowCache = self._currentlyOpenWindowsInClient.get(window.getName())
        if windowCache is None:
            windowCache = OpenWindowCache()
            self._currentlyOpenWindowsInClient[window.getName()] = windowCache
        if repaintAll:
            paintables = list()
            paintables.append(window)
            self._locales = None
            self.requireLocale(self._application.getLocale())
        else:
            for p in self._paintableIdMap.keys():
                if p.getApplication() is None:
                    self.unregisterPaintable(p)
                    if self._paintableIdMap[p] in self._idPaintableMap:
                        del self._idPaintableMap[self._paintableIdMap[p]]
                    if p in self._paintableIdMap:
                        del self._paintableIdMap[p]
                    if p in self._dirtyPaintables:
                        self._dirtyPaintables.remove(p)

            paintables = self.getDirtyVisibleComponents(window)
        if paintables is not None:

            def compare(c1, c2):
                d1 = 0
                while c1.getParent() is not None:
                    d1 += 1
                    c1 = c1.getParent()

                d2 = 0
                while c2.getParent() is not None:
                    d2 += 1
                    c2 = c2.getParent()

                if d1 < d2:
                    return -1
                else:
                    if d1 > d2:
                        return 1
                    return 0

            paintables.sort(cmp=compare)
            for p in paintables:
                if isinstance(p, Window):
                    w = p
                    if w.getTerminal() is None:
                        w.setTerminal(self._application.getMainWindow().getTerminal())
                if paintTarget.needsToBePainted(p):
                    paintTarget.startTag('change')
                    paintTarget.addAttribute('format', 'uidl')
                    pid = self.getPaintableId(p)
                    paintTarget.addAttribute('pid', pid)
                    p.paint(paintTarget)
                    paintTarget.endTag('change')
                self.paintablePainted(p)
                if analyzeLayouts:
                    from muntjac.terminal.gwt.server.component_size_validator import ComponentSizeValidator
                    w = p
                    invalidComponentRelativeSizes = ComponentSizeValidator.validateComponentRelativeSizes(w.getContent(), None, None)
                    if w.getChildWindows() is not None:
                        for subWindow in w.getChildWindows():
                            invalidComponentRelativeSizes = ComponentSizeValidator.validateComponentRelativeSizes(subWindow.getContent(), invalidComponentRelativeSizes, None)

        paintTarget.close()
        outWriter.write(']')
        outWriter.write(', "meta" : {')
        metaOpen = False
        if repaintAll:
            metaOpen = True
            outWriter.write('"repaintAll":true')
            if analyzeLayouts:
                outWriter.write(', "invalidLayouts":')
                outWriter.write('[')
                if invalidComponentRelativeSizes is not None:
                    first = True
                    for invalidLayout in invalidComponentRelativeSizes:
                        if not first:
                            outWriter.write(',')
                        else:
                            first = False
                        invalidLayout.reportErrors(outWriter, self, stderr)

                outWriter.write(']')
            if self._highLightedPaintable is not None:
                outWriter.write(', "hl":"')
                idd = self._paintableIdMap.get(self._highLightedPaintable)
                outWriter.write(idd if idd is not None else 'null')
                outWriter.write('"')
                self._highLightedPaintable = None
        ci = None
        try:
            ci = self._application.getSystemMessages()
        except AttributeError as e:
            logger.warning('getSystemMessages() failed - continuing')

        if ci is not None and ci.getSessionExpiredMessage() is None and ci.getSessionExpiredCaption() is None and ci.isSessionExpiredNotificationEnabled():
            newTimeoutInterval = self.getTimeoutInterval()
            if repaintAll or self._timeoutInterval != newTimeoutInterval:
                if ci.getSessionExpiredURL() is None:
                    escapedURL = ''
                else:
                    escapedURL = ci.getSessionExpiredURL().replace('/', '\\/')
                if metaOpen:
                    outWriter.write(',')
                outWriter.write('"timedRedirect":{"interval":' + newTimeoutInterval + 15 + ',"url":"' + escapedURL + '"}')
                metaOpen = True
            self._timeoutInterval = newTimeoutInterval
        outWriter.write('}, "resources" : {')
        resourceIndex = 0
        for resource in paintTarget.getUsedResources():
            is_ = None
            try:
                is_ = callback.getThemeResourceAsStream(self.getTheme(window), resource)
            except IOError as e:
                logger.info('Failed to get theme resource stream.')

            if is_ is not None:
                outWriter.write((', ' if resourceIndex > 0 else '') + '"' + resource + '" : ')
                resourceIndex += 1
                layout = str()
                try:
                    layout = is_.read()
                except IOError as e:
                    logger.info('Resource transfer failed: ' + str(e))

                outWriter.write('"%s"' % JsonPaintTarget.escapeJSON(layout))
            else:
                logger.critical('CustomLayout not found: ' + resource)

        outWriter.write('}')
        usedPaintableTypes = paintTarget.getUsedPaintableTypes()
        typeMappingsOpen = False
        for class1 in usedPaintableTypes:
            if windowCache.cache(class1):
                if not typeMappingsOpen:
                    typeMappingsOpen = True
                    outWriter.write(', "typeMappings" : { ')
                else:
                    outWriter.write(' , ')
                canonicalName = clsname(class1)
                if canonicalName.startswith('muntjac.ui'):
                    canonicalName = 'com.vaadin.ui.' + class1.__name__
                elif canonicalName.startswith('muntjac.demo.sampler'):
                    canonicalName = 'com.vaadin.demo.sampler.' + class1.__name__
                elif hasattr(class1, 'TYPE_MAPPING'):
                    canonicalName = getattr(class1, 'TYPE_MAPPING')
                else:
                    raise ValueError('type mapping name [%s]' % canonicalName)
                outWriter.write('"')
                outWriter.write(canonicalName)
                outWriter.write('" : ')
                outWriter.write(self.getTagForType(class1))

        if typeMappingsOpen:
            outWriter.write(' }')
        self.printLocaleDeclarations(outWriter)
        if self._dragAndDropService is not None:
            self._dragAndDropService.printJSONResponse(outWriter)
        return

    def getTimeoutInterval(self):
        return self._maxInactiveInterval

    def getTheme(self, window):
        themeName = window.getTheme()
        requestThemeName = self.getRequestTheme()
        if requestThemeName is not None:
            themeName = requestThemeName
        if themeName is None:
            themeName = AbstractApplicationServlet.getDefaultTheme()
        return themeName

    def getRequestTheme(self):
        return self._requestThemeName

    def makeAllPaintablesDirty(self, window):
        for key in self._idPaintableMap.keys():
            c = self._idPaintableMap[key]
            if self.isChildOf(window, c):
                if key in self._idPaintableMap:
                    del self._idPaintableMap[key]
                if c in self._paintableIdMap:
                    del self._paintableIdMap[c]

        openWindowCache = self._currentlyOpenWindowsInClient.get(window.getName())
        if openWindowCache is not None:
            openWindowCache.clear()
        return

    def unregisterPaintable(self, p):
        """Called when communication manager stops listening for repaints
        for given component.
        """
        p.removeListener(self, IRepaintRequestListener)

    def handleVariables(self, request, response, callback, application2, window):
        """If this method returns false, something was submitted that we did
        not expect; this is probably due to the client being out-of-sync
        and sending variable changes for non-existing pids

        @return: true if successful, false if there was an inconsistency
        """
        success = True
        changes = self.getRequestPayload(request)
        if changes is not None:
            bursts = re.split(self.VAR_BURST_SEPARATOR, changes)
            if (len(bursts) > 0) & (bursts[(-1)] == ''):
                bursts = bursts[:-1]
            if application2.getProperty(AbstractApplicationServlet.SERVLET_PARAMETER_DISABLE_XSRF_PROTECTION) != 'true':
                if len(bursts) == 1 and 'init' == bursts[0]:
                    request.setAttribute(self._WRITE_SECURITY_TOKEN_FLAG, True)
                    return True
                sessId = request.getSession().getAttribute(ApplicationConnection.UIDL_SECURITY_TOKEN_ID, '')
                if sessId is None or sessId != bursts[0]:
                    msg = 'Security key mismatch'
                    raise InvalidUIDLSecurityKeyException(msg)
            for bi in range(1, len(bursts)):
                burst = bursts[bi]
                success = self.handleVariableBurst(request, application2, success, burst)
                if bi < len(bursts) - 1:
                    outWriter = cStringIO()
                    self.paintAfterVariableChanges(request, response, callback, True, outWriter, window, False)

        return success or self._closingWindowName is not None

    def handleVariableBurst(self, source, app, success, burst):
        tmp = re.split(self._VAR_RECORD_SEPARATOR, burst)
        variableRecords = [None] * len(tmp)
        for i in range(len(tmp)):
            variableRecords[i] = re.split(self._VAR_FIELD_SEPARATOR, tmp[i])

        i = 0
        while i < len(variableRecords):
            variable = variableRecords[i]
            nextVariable = None
            if i + 1 < len(variableRecords):
                nextVariable = variableRecords[(i + 1)]
            owner = self.getVariableOwner(variable[self._VAR_PID])
            if owner is not None and owner.isEnabled():
                m = dict()
                if nextVariable is not None and variable[self._VAR_PID] == nextVariable[self._VAR_PID]:
                    m[variable[self._VAR_NAME]] = self.convertVariableValue(variable[self._VAR_TYPE][0], variable[self._VAR_VALUE])
                else:
                    m[variable[self._VAR_NAME]] = self.convertVariableValue(variable[self._VAR_TYPE][0], variable[self._VAR_VALUE])
                while nextVariable is not None and variable[self._VAR_PID] == nextVariable[self._VAR_PID]:
                    i += 1
                    variable = nextVariable
                    if i + 1 < len(variableRecords):
                        nextVariable = variableRecords[(i + 1)]
                    else:
                        nextVariable = None
                    m[variable[self._VAR_NAME]] = self.convertVariableValue(variable[self._VAR_TYPE][0], variable[self._VAR_VALUE])

                try:
                    self.changeVariables(source, owner, m)
                    if isinstance(owner, Window) and owner.getParent() is None:
                        close = m.get('close')
                        if close is not None and bool(close):
                            self._closingWindowName = owner.getName()
                except Exception as e:
                    if isinstance(owner, IComponent):
                        self.handleChangeVariablesError(app, owner, e, m)
                    else:
                        raise RuntimeError(e)

            else:
                if variable[self._VAR_NAME] == 'close' and variable[self._VAR_VALUE] == 'true':
                    i += 1
                    continue
                msg = 'Warning: Ignoring variable change for '
                if owner is not None:
                    msg += 'disabled component ' + str(owner.__class__)
                    caption = owner.getCaption()
                    if caption is not None:
                        msg += ', caption=' + caption
                else:
                    msg += 'non-existent component, VAR_PID=' + variable[self._VAR_PID]
                    success = False
                logger.warning(msg)
            i += 1

        return success

    def changeVariables(self, source, owner, m):
        owner.changeVariables(source, m)

    def getVariableOwner(self, string):
        owner = self._idPaintableMap.get(string)
        if owner is None and string.startswith('DD'):
            return self.getDragAndDropService()
        else:
            return owner

    def getDragAndDropService(self):
        if self._dragAndDropService is None:
            self._dragAndDropService = DragAndDropService(self)
        return self._dragAndDropService

    def getRequestPayload(self, request):
        """Reads the request data from the Request and returns it converted
        to an UTF-8 string.

        @raise IOException:
        """
        requestLength = request.getContentLength()
        if requestLength == 0:
            return
        else:
            inputStream = request.getInputStream()
            if inputStream is not None:
                return inputStream.read()
            return
            return

    def handleChangeVariablesError(self, application, owner, e, m):
        """Handles an error (exception) that occurred when processing variable
        changes from the client or a failure of a file upload.

        For L{AbstractField} components, C{AbstractField.handleError()}
        is called. In all other cases (or if the field does not handle the
        error), L{ErrorListener.terminalError} for the application error
        handler is called.

        @param application:
        @param owner:
                   component that the error concerns
        @param e:
                   exception that occurred
        @param m:
                   map from variable names to values
        """
        handled = False
        errorEvent = ChangeVariablesErrorEvent(owner, e, m)
        if isinstance(owner, AbstractField):
            try:
                handled = owner.handleError(errorEvent)
            except Exception as handlerException:
                application.getErrorHandler().terminalError(ErrorHandlerErrorEvent(handlerException))
                handled = False

        if not handled:
            application.getErrorHandler().terminalError(errorEvent)

    def convertVariableValue(self, variableType, strValue):
        m = {self._VTYPE_ARRAY: lambda s: self.convertArray(s), 
           self._VTYPE_MAP: lambda s: self.convertMap(s), 
           self._VTYPE_STRINGARRAY: lambda s: self.convertStringArray(s), 
           self._VTYPE_STRING: lambda s: self.decodeVariableValue(s), 
           self._VTYPE_INTEGER: lambda s: int(s), 
           self._VTYPE_LONG: lambda s: long(s), 
           self._VTYPE_FLOAT: lambda s: float(s), 
           self._VTYPE_DOUBLE: lambda s: float(s), 
           self._VTYPE_BOOLEAN: lambda s: s.lower() == 'true', 
           self._VTYPE_PAINTABLE: lambda s: self._idPaintableMap.get(s)}.get(variableType)
        if m is not None:
            return m(strValue)
        else:
            return
            return

    def convertMap(self, strValue):
        parts = strValue.split(self.VAR_ARRAYITEM_SEPARATOR)
        mapp = dict()
        i = 0
        while i < len(parts):
            key = parts[i]
            if len(key) > 0:
                variabletype = key[0]
                decodedValue = self.decodeVariableValue(parts[(i + 1)])
                decodedKey = self.decodeVariableValue(key[1:])
                value = self.convertVariableValue(variabletype, decodedValue)
                mapp[decodedKey] = value
            i += 2

        return mapp

    def convertStringArray(self, strValue):
        arrayItemSeparator = self.VAR_ARRAYITEM_SEPARATOR
        splitter = re.compile('(\\' + arrayItemSeparator + '+)')
        tokens = list()
        prevToken = arrayItemSeparator
        for token in splitter.split(strValue):
            if arrayItemSeparator != token:
                tokens.append(self.decodeVariableValue(token))
            elif arrayItemSeparator == prevToken:
                tokens.append('')
            prevToken = token

        return tokens

    def convertArray(self, strValue):
        val = strValue.split(self.VAR_ARRAYITEM_SEPARATOR)
        if len(val) == 0 or len(val) == 1 and len(val[0]) == 0:
            return []
        values = [
         None] * len(val)
        for i in range(len(values)):
            string = val[i]
            variableType = string[0]
            values[i] = self.convertVariableValue(variableType, string[1:])

        return values

    def decodeVariableValue(self, encodedValue):
        """Decode encoded burst, record, field and array item separator
        characters in a variable value String received from the client.
        This protects from separator injection attacks.

        @param encodedValue: value to decode
        @return: decoded value
        """
        iterator = iter(encodedValue)
        try:
            character = iterator.next()
        except StopIteration:
            return ''

        result = StringIO()
        while True:
            try:
                if self.VAR_ESCAPE_CHARACTER == character:
                    character = iterator.next()
                    if character == chr(ord(self.VAR_ESCAPE_CHARACTER) + 48):
                        result.write(self.VAR_ESCAPE_CHARACTER)
                    elif character == chr(ord(self.VAR_BURST_SEPARATOR) + 48):
                        pass
                    elif character == chr(ord(self._VAR_RECORD_SEPARATOR) + 48):
                        pass
                    elif character == chr(ord(self._VAR_FIELD_SEPARATOR) + 48):
                        pass
                    elif character == chr(ord(self.VAR_ARRAYITEM_SEPARATOR) + 48):
                        result.write(chr(ord(character) - 48))
                    else:
                        raise ValueError('Invalid escaped character from the client - check that the widgetset and server versions match')
                else:
                    result.write(character)
                character = iterator.next()
            except StopIteration:
                break

        r = result.getvalue()
        result.close()
        return r

    def printLocaleDeclarations(self, outWriter):
        """Prints the queued (pending) locale definitions to a PrintWriter
        in a (UIDL) format that can be sent to the client and used there in
        formatting dates, times etc.
        """
        outWriter.write(', "locales":[')
        while self._pendingLocalesIndex < len(self._locales):
            l = self.generateLocale(self._locales[self._pendingLocalesIndex])
            outWriter.write('{"name":"' + str(l) + '",')
            months = l.months['format']['wide'].values()
            short_months = l.months['format']['abbreviated'].values()
            outWriter.write(('"smn":["' + short_months[0] + '","' + short_months[1] + '","' + short_months[2] + '","' + short_months[3] + '","' + short_months[4] + '","' + short_months[5] + '","' + short_months[6] + '","' + short_months[7] + '","' + short_months[8] + '","' + short_months[9] + '","' + short_months[10] + '","' + short_months[11] + '"' + '],').encode('utf-8'))
            outWriter.write(('"mn":["' + months[0] + '","' + months[1] + '","' + months[2] + '","' + months[3] + '","' + months[4] + '","' + months[5] + '","' + months[6] + '","' + months[7] + '","' + months[8] + '","' + months[9] + '","' + months[10] + '","' + months[11] + '"' + '],').encode('utf-8'))
            days = l.days['format']['wide'].values()
            short_days = l.days['format']['abbreviated'].values()
            outWriter.write(('"sdn":["' + short_days[6] + '","' + short_days[0] + '","' + short_days[1] + '","' + short_days[2] + '","' + short_days[3] + '","' + short_days[4] + '","' + short_days[5] + '"' + '],').encode('utf-8'))
            outWriter.write(('"dn":["' + days[6] + '","' + days[0] + '","' + days[1] + '","' + days[2] + '","' + days[3] + '","' + days[4] + '","' + days[5] + '"' + '],').encode('utf-8'))
            fdow = l.first_week_day
            if fdow == 0:
                fdow = 1
            else:
                fdow = 0
            outWriter.write('"fdow":' + str(fdow) + ',')
            try:
                df = l.date_formats['short'].pattern
                df += ' '
                df += l.time_formats['short'].pattern
                df = df.encode('utf-8')
            except KeyError:
                logger.warning('Unable to get default date pattern for locale ' + str(l))
                df = 'dd/MM/yy HH:mm'

            timeStart = df.find('H')
            if timeStart < 0:
                timeStart = df.find('h')
            ampm_first = df.find('a')
            if ampm_first > 0 and ampm_first < timeStart:
                timeStart = ampm_first
            timeFirst = timeStart == 0
            if timeFirst:
                dateStart = df.find(' ')
                if ampm_first > dateStart:
                    dateStart = df.find(' ', ampm_first)
                dateformat = df[dateStart + 1:]
            else:
                dateformat = df[:timeStart - 1]
            outWriter.write('"df":"' + dateformat.strip() + '",')
            timeformat = df[timeStart:len(df)]
            twelve_hour_clock = timeformat.find('a') > -1
            hour_min_delimiter = '.' if timeformat.find('.') > -1 else ':'
            outWriter.write('"thc":' + str(twelve_hour_clock).lower() + ',')
            outWriter.write('"hmd":"' + hour_min_delimiter + '"')
            if twelve_hour_clock:
                ampm = [
                 l.periods['am'].encode('utf-8'),
                 l.periods['pm'].encode('utf-8')]
                outWriter.write(',"ampm":["' + ampm[0] + '","' + ampm[1] + '"]')
            outWriter.write('}')
            if self._pendingLocalesIndex < len(self._locales) - 1:
                outWriter.write(',')
            self._pendingLocalesIndex += 1

        outWriter.write(']')

    def doGetApplicationWindow(self, request, callback, application, assumedWindow):
        window = None
        windowClientRequestedName = request.getParameter('windowName')
        if assumedWindow is not None and assumedWindow in application.getWindows():
            windowClientRequestedName = assumedWindow.getName()
        if windowClientRequestedName is not None:
            window = application.getWindow(windowClientRequestedName)
            if window is not None:
                return window
        if window is None and not request.isRunningInPortlet():
            path = callback.getRequestPathInfo(request)
            pathMayContainWindowName = path is not None and len(path) > 0 and not path == '/'
            if pathMayContainWindowName:
                uidlRequest = path.startswith('/UIDL')
                if not uidlRequest:
                    windowUrlName = None
                    if path[0] == '/':
                        path = path[1:]
                    index = path.find('/')
                    if index < 0:
                        windowUrlName = path
                        path = ''
                    else:
                        windowUrlName = path[:index]
                        path = path[index + 1:]
                    window = application.getWindow(windowUrlName)
        if window is None:
            window = application.getMainWindow()
            if window is None:
                return
        if window.getName() in self._currentlyOpenWindowsInClient:
            newWindowName = window.getName()
            while newWindowName in self._currentlyOpenWindowsInClient:
                newWindowName = window.getName() + '_' + str(self._nextUnusedWindowSuffix)
                self._nextUnusedWindowSuffix += 1

            window = application.getWindow(newWindowName)
            if window is None:
                window = application.getMainWindow()
        return window

    def endApplication(self, request, response, application):
        """Ends the Application.

        The browser is redirected to the Application logout URL set with
        L{Application.setLogoutURL}, or to the application URL if no logout
        URL is given.

        @param request:
                   the request instance.
        @param response:
                   the response to write to.
        @param application:
                   the Application to end.
        @raise IOException:
                    if the writing failed due to input/output error.
        """
        logoutUrl = application.getLogoutURL()
        if logoutUrl is None:
            logoutUrl = application.getURL()
        outWriter = response.getOutputStream()
        self.openJsonMessage(outWriter, response)
        outWriter.write('"redirect":{')
        outWriter.write('"url":"' + logoutUrl + '"}')
        self.closeJsonMessage(outWriter)
        outWriter.flush()
        return

    def closeJsonMessage(self, outWriter):
        outWriter.write('}]')

    def openJsonMessage(self, outWriter, response):
        """Writes the opening of JSON message to be sent to client.
        """
        response.setContentType('application/json; charset=UTF-8')
        outWriter.write('for(;;);[{')

    def getPaintableId(self, paintable):
        """Gets the IPaintable Id. If IPaintable has debug id set it will be
        used prefixed with "PID_S". Otherwise a sequenced ID is created.

        @param paintable:
        @return: the paintable Id.
        """
        idd = self._paintableIdMap.get(paintable)
        if idd is None:
            idd = paintable.getDebugId()
            if idd is None:
                idd = 'PID' + str(self._idSequence)
                self._idSequence += 1
            else:
                idd = 'PID_S' + idd
            old = self._idPaintableMap[idd] = paintable
            if old is not None and old != paintable and isinstance(old, IComponent):
                if old.getApplication() is not None:
                    raise ValueError('Two paintables (' + paintable.__class__.__name__ + ',' + old.__class__.__name__ + ') have been assigned the same id: ' + paintable.getDebugId())
            self._paintableIdMap[paintable] = idd
        return idd

    def hasPaintableId(self, paintable):
        return paintable in self._paintableIdMap

    def getDirtyVisibleComponents(self, w):
        """Returns dirty components which are in given window. Components
        in an invisible subtrees are omitted.

        @param w:
                   root window for which dirty components is to be fetched
        """
        resultset = list(self._dirtyPaintables)
        for p in self._dirtyPaintables:
            if isinstance(p, IComponent):
                component = p
                if component.getApplication() is None:
                    resultset.remove(p)
                    self._dirtyPaintables.remove(p)
                else:
                    componentsRoot = component.getWindow()
                    if componentsRoot is None:
                        raise ValueError('component.getWindow() returned null for a component attached to the application')
                    if componentsRoot.getParent() is not None:
                        componentsRoot = componentsRoot.getParent()
                    if componentsRoot != w:
                        resultset.remove(p)
                    elif component.getParent() is not None and not component.getParent().isVisible():
                        resultset.remove(p)

        return resultset

    def repaintRequested(self, event):
        """@see: L{IRepaintRequestListener.repaintRequested}"""
        p = event.getPaintable()
        if p not in self._dirtyPaintables:
            self._dirtyPaintables.append(p)

    def paintablePainted(self, paintable):
        """Internally mark a L{IPaintable} as painted and start
        collecting new repaint requests for it.
        """
        if paintable in self._dirtyPaintables:
            self._dirtyPaintables.remove(paintable)
        paintable.requestRepaintRequests()

    def requireLocale(self, value):
        """Queues a locale to be sent to the client (browser) for date and
        time entry etc. All locale specific information is derived from
        server-side L{Locale} instances and sent to the client when
        needed, eliminating the need to use the L{Locale} class and all
        the framework behind it on the client.
        """
        if self._locales is None:
            self._locales = list()
            l = self._application.getLocale()
            self._locales.append(str(l))
            self._pendingLocalesIndex = 0
        if str(value) not in self._locales:
            self._locales.append(str(value))
        return

    def generateLocale(self, value):
        """Constructs a L{Locale} instance to be sent to the client based on
        a short locale description string.

        @see: L{requireLocale}
        """
        temp = value.split('_')
        if len(temp) == 1:
            return Locale(temp[0], '')
        else:
            if len(temp) == 2:
                return Locale(temp[0], temp[1])
            return Locale(temp[0], temp[1])

        return value

    @classmethod
    def isChildOf(cls, parent, child):
        """Helper method to test if a component contains another.
        """
        p = child.getParent()
        while p is not None:
            if parent == p:
                return True
            p = p.getParent()

        return False

    def handleURI(self, window, request, response, callback):
        """Calls the Window URI handler for a request and returns the
        L{DownloadStream} returned by the handler.

        If the window is the main window of an application, the (deprecated)
        L{Application.handleURI} is called first
        to handle L{ApplicationResource}s, and the window handler is
        only called if it returns null.

        @param window:
                   the target window of the request
        @param request:
                   the request instance
        @param response:
                   the response to write to
        @return: DownloadStream if the request was handled and further
                    processing should be suppressed, null otherwise.
        @see: L{URIHandler}
        """
        warn('deprecated', DeprecationWarning)
        uri = callback.getRequestPathInfo(request)
        if uri is None:
            uri = ''
        else:
            while uri.startswith('/') and len(uri) > 0:
                uri = uri[1:]

            try:
                context = self._application.getURL()
                if window == self._application.getMainWindow():
                    stream = None
                    stream = self._application.handleURI(context, uri)
                    if stream is None:
                        stream = window.handleURI(context, uri)
                    return stream
                index = uri.find('/')
                if index > 0:
                    prefix = uri[:index]
                    windowContext = urljoin(context, prefix + '/')
                    if len(uri) > len(prefix) + 1:
                        windowUri = uri[len(prefix) + 1:]
                    else:
                        windowUri = ''
                    return window.handleURI(windowContext, windowUri)
                return
            except Exception as t:
                event = URIHandlerErrorImpl(self._application, t)
                self._application.getErrorHandler().terminalError(event)
                return

        return

    def getTagForType(self, class1):
        obj = self._typeToKey.get(class1)
        if obj is None:
            obj = self._nextTypeKey
            self._nextTypeKey += 1
            self._typeToKey[class1] = obj
        return str(obj)

    def getStreamVariableTargetUrl(self, owner, name, value):
        raise NotImplementedError

    def cleanStreamVariable(self, owner, name):
        raise NotImplementedError


class IRequest(object):
    """Generic interface of a (HTTP or Portlet) request to the application.

    This is a wrapper interface that allows
    L{AbstractCommunicationManager} to use a unified API.

    @author: peholmst
    """

    def getSession(self):
        """Gets a L{Session} wrapper implementation representing the
        session for which this request was sent.

        Multiple Muntjac applications can be associated with a single session.

        @return: Session
        """
        raise NotImplementedError

    def isRunningInPortlet(self):
        """Are the applications in this session running in a portlet or
        directly as servlets.

        @return: true if in a portlet
        """
        raise NotImplementedError

    def getParameter(self, name):
        """Get the named HTTP or portlet request parameter.
        """
        raise NotImplementedError

    def getContentLength(self):
        """Returns the length of the request content that can be read from the
        input stream returned by L{getInputStream}.

        @return: content length in bytes
        """
        raise NotImplementedError

    def getInputStream(self):
        """Returns an input stream from which the request content can be read.
        The request content length can be obtained with
        L{getContentLength} without reading the full stream contents.

        @raise IOException:
        """
        raise NotImplementedError

    def getRequestID(self):
        """Returns the request identifier that identifies the target Muntjac
        window for the request.

        @return: String identifier for the request target window
        """
        raise NotImplementedError

    def getAttribute(self, name):
        raise NotImplementedError

    def setAttribute(self, name, value):
        raise NotImplementedError

    def getWrappedRequest(self):
        """Gets the underlying request object. The request is typically either
        a L{ServletRequest} or a L{PortletRequest}.

        @return: wrapped request object
        """
        raise NotImplementedError


class IResponse(object):
    """Generic interface of a (HTTP or Portlet) response from the application.

    This is a wrapper interface that allows L{AbstractCommunicationManager} to
    use a unified API.

    @author: peholmst
    """

    def getOutputStream(self):
        """Gets the output stream to which the response can be written.

        @raise IOException:
        """
        raise NotImplementedError

    def setContentType(self, typ):
        """Sets the MIME content type for the response to be communicated
        to the browser.
        """
        raise NotImplementedError

    def getWrappedResponse(self):
        """Gets the wrapped response object, usually a class implementing
        either L{ServletResponse}.

        @return: wrapped request object
        """
        raise NotImplementedError


class ISession(object):
    """Generic wrapper interface for a (HTTP or Portlet) session.

    Several applications can be associated with a single session.

    @author: peholmst
    """

    def isNew(self):
        raise NotImplementedError

    def getAttribute(self, name):
        raise NotImplementedError

    def setAttribute(self, name, o):
        raise NotImplementedError

    def getMaxInactiveInterval(self):
        raise NotImplementedError

    def getWrappedSession(self):
        raise NotImplementedError


class ICallback(object):
    """@author: peholmst
    """

    def criticalNotification(self, request, response, cap, msg, details, outOfSyncURL):
        raise NotImplementedError

    def getRequestPathInfo(self, request):
        raise NotImplementedError

    def getThemeResourceAsStream(self, themeName, resource):
        raise NotImplementedError


class UploadInterruptedException(Exception):

    def __init__(self):
        msg = 'Upload interrupted by other thread'
        super(UploadInterruptedException, self).__init__(msg)


class ErrorHandlerErrorEvent(TerminalErrorEvent):

    def __init__(self, throwable):
        self._throwable = throwable

    def getThrowable(self):
        return self._throwable


class URIHandlerErrorImpl(URIHandlerErrorEvent):
    """Implementation of L{IErrorEvent} interface."""

    def __init__(self, owner, throwable):
        self._owner = owner
        self._throwable = throwable

    def getThrowable(self):
        """@see: L{IErrorEvent.getThrowable}"""
        return self._throwable

    def getURIHandler(self):
        """@see: L{IErrorEvent.getURIHandler}"""
        return self._owner


class InvalidUIDLSecurityKeyException(Exception):

    def __init__(self, message):
        super(InvalidUIDLSecurityKeyException, self).__init__(message)


class OpenWindowCache(object):
    """Helper class for terminal to keep track of data that client is
    expected to know.

    TODO: make customlayout templates (from theme) to be cached here.
    """

    def __init__(self):
        self._res = set()

    def cache(self, obj):
        """@return: true if the given class was added to cache
        """
        if obj in self._res:
            return False
        else:
            self._res.add(obj)
            return True

    def clear(self):
        self._res.clear()


class SimpleMultiPartInputStream(StringIO):
    """Stream that extracts content from another stream until the boundary
    string is encountered.

    Public only for unit tests, should be considered private for all other
    purposes.
    """

    def __init__(self, realInputStream, boundaryString, manager):
        super(SimpleMultiPartInputStream, self).__init__()
        self._matchedCount = -1
        self._curBoundaryIndex = 0
        self._bufferedByte = -1
        self._atTheEnd = False
        self._boundary = manager.CRLF + manager.DASHDASH + boundaryString
        self._realInputStream = realInputStream

    def getvalue(self):
        if self._atTheEnd:
            return -1
        else:
            if self._bufferedByte >= 0:
                return self.getBuffered()
            if self._matchedCount != -1:
                return self.matchForBoundary()
            fromActualStream = self._realInputStream.read()
            if fromActualStream == -1:
                raise IOError('The multipart stream ended unexpectedly')
            if self._boundary[0] == fromActualStream:
                return self.matchForBoundary()
            return fromActualStream

    def matchForBoundary(self):
        """Reads the input to expect a boundary string. Expects that the first
        character has already been matched.

        @return: -1 if the boundary was matched, else returns the first byte
                from boundary
        @raise IOException:
        """
        self._matchedCount = 0
        while True:
            self._matchedCount += 1
            if self._matchedCount == len(self._boundary):
                self._atTheEnd = True
                return -1
            fromActualStream = self._realInputStream.read()
            if fromActualStream != self._boundary[self._matchedCount]:
                self._bufferedByte = fromActualStream
                return self.getBuffered()

    def getBuffered(self):
        """Returns the partly matched boundary string and the byte following
        that.

        @raise IOException:
        """
        if self._matchedCount == 0:
            b = self._bufferedByte
            self._bufferedByte = -1
            self._matchedCount = -1
        else:
            b = self._boundary[self._curBoundaryIndex]
            self._curBoundaryIndex += 1
            if self._curBoundaryIndex == self._matchedCount:
                self._curBoundaryIndex = 0
                if self._bufferedByte != self._boundary[0]:
                    self._matchedCount = 0
                else:
                    self._matchedCount = 0
                    self._bufferedByte = -1
        if b == -1:
            raise IOError('The multipart stream ended unexpectedly')
        return b