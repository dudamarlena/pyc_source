# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/gwt/server/json_paint_target.py
# Compiled at: 2013-04-04 15:36:36
"""UIDL target"""
import logging
from warnings import warn
from collections import deque
from muntjac.util import getSuperClass
from muntjac.util import clsname
try:
    from cStringIO import StringIO
except ImportError as e:
    from StringIO import StringIO

from muntjac.ui.custom_layout import CustomLayout
from muntjac.terminal.resource import IResource
from muntjac.terminal.external_resource import ExternalResource
from muntjac.terminal.application_resource import IApplicationResource
from muntjac.terminal.theme_resource import ThemeResource
from muntjac.ui.alignment import Alignment
from muntjac.terminal.stream_variable import IStreamVariable
from muntjac.terminal.paintable import IPaintable, IRepaintRequestListener
from muntjac.terminal.paint_target import IPaintTarget
from muntjac.terminal.paint_exception import PaintException
logger = logging.getLogger(__name__)

class JsonPaintTarget(IPaintTarget):
    """User Interface Description Language Target.

    TODO: document better: role of this class, UIDL format,
    attributes, variables, etc.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """
    _UIDL_ARG_NAME = 'name'

    def __init__(self, manager, outWriter, cachingRequired):
        """Creates a new XMLPrintWriter, without automatic line flushing.

        @param manager:
        @param outWriter:
                   A character-output stream.
        @param cachingRequired:
                   True if this is not a full repaint, i.e. caches are to
                   be used.
        @raise PaintException:
                   if the paint operation failed.
        """
        self._manager = manager
        self._uidlBuffer = outWriter
        self._mOpenTags = deque()
        self._openJsonTags = deque()
        self._cacheEnabled = cachingRequired
        self._closed = False
        self._changes = 0
        self._usedResources = set()
        self._customLayoutArgumentsOpen = False
        self._tag = None
        self._errorsOpen = 0
        self._paintedComponents = set()
        self._identifiersCreatedDueRefPaint = None
        self._usedPaintableTypes = list()
        return

    def startTag(self, arg, arg2=False):
        """Prints the element start tag.

        @param arg:
                   paintable or the name of the start tag
        @param arg2:
                   the name of the start tag for the given paintable
        @raise PaintException:
                    if the paint operation failed.
        """
        if isinstance(arg, IPaintable):
            paintable, tagName = arg, arg2
            self.startTag(tagName, True)
            isPreviouslyPainted = self._manager.hasPaintableId(paintable) and (self._identifiersCreatedDueRefPaint is None or paintable not in self._identifiersCreatedDueRefPaint)
            idd = self._manager.getPaintableId(paintable)
            paintable.addListener(self._manager, IRepaintRequestListener)
            self.addAttribute('id', idd)
            self._paintedComponents.add(paintable)
            if isinstance(paintable, CustomLayout):
                self._customLayoutArgumentsOpen = True
            return self._cacheEnabled and isPreviouslyPainted
        else:
            tagName, _ = arg, arg2
            if tagName is None:
                raise ValueError
            if self._closed:
                raise PaintException, 'Attempted to write to a closed IPaintTarget.'
            if self._tag is not None:
                self._openJsonTags.append(self._tag)
            self._mOpenTags.append(tagName)
            self._tag = JsonTag(tagName, self)
            if 'error' == tagName:
                self._errorsOpen += 1
            self._customLayoutArgumentsOpen = False
            return

    def endTag(self, tagName):
        """Prints the element end tag.

        If the parent tag is closed before every child tag is closed an
        PaintException is raised.

        @param tagName:
                   the name of the end tag.
        @raise Paintexception:
                    if the paint operation failed.
        """
        if tagName is None:
            raise ValueError
        if self._closed:
            raise PaintException, 'Attempted to write to a closed IPaintTarget.'
        if len(self._openJsonTags) > 0:
            parent = self._openJsonTags.pop()
            lastTag = ''
            lastTag = self._mOpenTags.pop()
            if tagName.lower() != lastTag.lower():
                raise PaintException, "Invalid UIDL: wrong ending tag: '" + tagName + "' expected: '" + lastTag + "'."
            if 'error' == lastTag:
                if self._errorsOpen == 1:
                    parent.addAttribute('"error":["error",{}' + self._tag.getData() + ']')
                else:
                    parent.addData(self._tag.getJSON())
                self._errorsOpen -= 1
            else:
                parent.addData(self._tag.getJSON())
            self._tag = parent
        else:
            self._changes += 1
            self._uidlBuffer.write((',' if self._changes > 1 else '') + self._tag.getJSON())
            self._tag = None
        return

    @classmethod
    def escapeXML(cls, xml):
        """Substitutes the XML sensitive characters with predefined XML
        entities.

        @param xml:
                the string to be substituted.
        @return: A new string instance where all occurrences of XML
                sensitive characters are substituted with entities.
        """
        if xml is None or len(xml) <= 0:
            return ''
        return cls._escapeXML(xml)

    @classmethod
    def _escapeXML(cls, xml):
        """Substitutes the XML sensitive characters with predefined XML
        entities.

        @param xml:
                the string to be substituted.
        @return: A new StringBuilder instance where all occurrences of XML
                sensitive characters are substituted with entities.
        """
        if xml is None or len(xml) <= 0:
            return ''
        buff = StringIO()
        for c in xml:
            s = cls.toXmlChar(c)
            if s is not None:
                buff.write(s)
            else:
                buff.write(c)

        result = buff.getvalue()
        buff.close()
        return result

    @staticmethod
    def _default(ch, sb):
        if ch >= '\\u0000' and ch <= '\\u001F':
            ss = hex(int(ch))
            sb.write('\\u')
            for _ in range(4 - len(ss)):
                sb.write('0')

            sb.write(ss.upper())
        else:
            sb.write(ch)

    _json_map = {'"': lambda ch, sb: sb.write('\\"'), 
       '\\': lambda ch, sb: sb.write('\\\\'), 
       '\x08': lambda ch, sb: sb.write('\\b'), 
       '\x0c': lambda ch, sb: sb.write('\\f'), 
       '\n': lambda ch, sb: sb.write('\\n'), 
       '\r': lambda ch, sb: sb.write('\\r'), 
       '\t': lambda ch, sb: sb.write('\\t'), 
       '/': lambda ch, sb: sb.write('\\/')}

    @classmethod
    def escapeJSON(cls, s):
        """Escapes the given string so it can safely be used as a JSON string.

        @param s: The string to escape
        @return: Escaped version of the string
        """
        if s is None:
            return ''
        else:
            sb = StringIO()
            for c in s:
                cls._json_map.get(c, cls._default)(c, sb)

            result = sb.getvalue()
            sb.close()
            return result

    @classmethod
    def toXmlChar(cls, c):
        """Substitutes a XML sensitive character with predefined XML entity.

        @param c:
                the character to be replaced with an entity.
        @return: String of the entity or null if character is not to be
                replaced with an entity.
        """
        return {'&': '&amp;', 
           '>': '&gt;', 
           '<': '&lt;', 
           '"': '&quot;', 
           "'": '&apos;'}.get(c)

    def addText(self, s):
        """Prints XML-escaped text.

        @raise PaintException:
                    if the paint operation failed.
        """
        self._tag.addData('"' + self.escapeJSON(s) + '"')

    def addAttribute(self, name, value):
        if isinstance(value, list):
            values = value
            if values is None or name is None:
                raise ValueError, 'Parameters must be non-null strings'
            buf = StringIO()
            buf.write('"' + name + '":[')
            for i in range(len(values)):
                if i > 0:
                    buf.write(',')
                buf.write('"')
                buf.write(self.escapeJSON(str(values[i])))
                buf.write('"')

            buf.write(']')
            self._tag.addAttribute(buf.getvalue())
            buf.close()
        elif isinstance(value, IPaintable):
            idd = self.getPaintIdentifier(value)
            self.addAttribute(name, idd)
        elif isinstance(value, IResource):
            if isinstance(value, ExternalResource):
                self.addAttribute(name, value.getURL())
            elif isinstance(value, IApplicationResource):
                r = value
                a = r.getApplication()
                if a is None:
                    raise PaintException, 'Application not specified for resource ' + value.__class__.__name__
                uri = a.getRelativeLocation(r)
                self.addAttribute(name, uri)
            elif isinstance(value, ThemeResource):
                uri = 'theme://' + value.getResourceId()
                self.addAttribute(name, uri)
            else:
                raise PaintException, 'Ajax adapter does not support resources of type: ' + value.__class__.__name__
        elif isinstance(value, bool):
            self._tag.addAttribute('"' + name + '":' + ('true' if value else 'false'))
        elif isinstance(value, dict):
            sb = StringIO()
            sb.write('"')
            sb.write(name)
            sb.write('": ')
            sb.write('{')
            i = 0
            for key, mapValue in value.iteritems():
                sb.write('"')
                if isinstance(key, IPaintable):
                    paintable = key
                    sb.write(self.getPaintIdentifier(paintable))
                else:
                    sb.write(self.escapeJSON(str(key)))
                sb.write('":')
                if isinstance(mapValue, (float, int, float, bool, Alignment)):
                    sb.write(str(mapValue))
                else:
                    sb.write('"')
                    sb.write(self.escapeJSON(str(mapValue)))
                    sb.write('"')
                if i < len(value) - 1:
                    sb.write(',')
                i += 1

            sb.write('}')
            self._tag.addAttribute(sb.getvalue())
            sb.close()
        elif isinstance(value, str):
            if value is None or name is None:
                raise ValueError, 'Parameters must be non-null strings'
            self._tag.addAttribute('"' + name + '": "' + self.escapeJSON(value) + '"')
            if self._customLayoutArgumentsOpen and 'template' == name:
                self.getUsedResources().add('layouts/' + value + '.html')
            if name == 'locale':
                self._manager.requireLocale(value)
        else:
            self._tag.addAttribute('"' + name + '":' + str(value))
        return

    def addVariable(self, owner, name, value):
        if value is None:
            value = ''
        if isinstance(value, IPaintable):
            var = StringVariable(owner, name, self.getPaintIdentifier(value))
            self._tag.addVariable(var)
        elif isinstance(value, IStreamVariable):
            url = self._manager.getStreamVariableTargetUrl(owner, name, value)
            if url is not None:
                self.addVariable(owner, name, url)
        elif isinstance(value, bool):
            self._tag.addVariable(BooleanVariable(owner, name, value))
        elif isinstance(value, float):
            self._tag.addVariable(DoubleVariable(owner, name, value))
        elif isinstance(value, int):
            self._tag.addVariable(IntVariable(owner, name, value))
        elif isinstance(value, long):
            self._tag.addVariable(LongVariable(owner, name, value))
        elif isinstance(value, basestring):
            var = StringVariable(owner, name, self.escapeJSON(value))
            self._tag.addVariable(var)
        elif isinstance(value, list):
            self._tag.addVariable(ArrayVariable(owner, name, value))
        else:
            raise ValueError, '%s %s %s' % (str(owner), name, value)
        return

    def addUploadStreamVariable(self, owner, name):
        """Adds a upload stream type variable.

        @param owner:
                   the Listener for variable changes.
        @param name:
                   the Variable name.
        @raise PaintException:
                    if the paint operation failed.
        """
        self.startTag('uploadstream')
        self.addAttribute(self._UIDL_ARG_NAME, name)
        self.endTag('uploadstream')

    def addSection(self, sectionTagName, sectionData):
        """Prints the single text section.

        Prints full text section. The section data is escaped

        @param sectionTagName:
                   the name of the tag.
        @param sectionData:
                   the section data to be printed.
        @raise PaintException:
                    if the paint operation failed.
        """
        self._tag.addData('{"' + sectionTagName + '":"' + self.escapeJSON(sectionData) + '"}')

    def addUIDL(self, xml):
        """Adds XML directly to UIDL.

        @param xml:
                   the Xml to be added.
        @raise PaintException:
                    if the paint operation failed.
        """
        if self._closed:
            raise PaintException, 'Attempted to write to a closed IPaintTarget.'
        if xml is not None:
            self._tag.addData('"' + self.escapeJSON(xml) + '"')
        return

    def addXMLSection(self, sectionTagName, sectionData, namespace):
        """Adds XML section with namespace.

        @param sectionTagName:
                   the name of the tag.
        @param sectionData:
                   the section data.
        @param namespace:
                   the namespace to be added.
        @raise PaintException:
                    if the paint operation failed.
        @see: L{IPaintTarget.addXMLSection}
        """
        if self._closed:
            raise PaintException, 'Attempted to write to a closed IPaintTarget.'
        self.startTag(sectionTagName)
        if namespace is not None:
            self.addAttribute('xmlns', namespace)
        if sectionData is not None:
            self._tag.addData('"' + self.escapeJSON(sectionData) + '"')
        self.endTag(sectionTagName)
        return

    def getUIDL(self):
        """Gets the UIDL already printed to stream. Paint target must be
        closed before the C{getUIDL} can be called.

        @return: the UIDL.
        """
        if self._closed:
            return self._uidlBuffer.getvalue()
        raise ValueError, 'Tried to read UIDL from open IPaintTarget'

    def close(self):
        """Closes the paint target. Paint target must be closed before the
        C{getUIDL} can be called. Subsequent attempts to write to paint
        target. If the target was already closed, call to this function
        is ignored. will generate an exception.

        @raise PaintException:
                    if the paint operation failed.
        """
        if self._tag is not None:
            self._uidlBuffer.write(self._tag.getJSON())
        self.flush()
        self._closed = True
        return

    def flush(self):
        """Method flush."""
        pass

    def paintReference(self, paintable, referenceName):
        warn('deprecated', DeprecationWarning)
        self.addAttribute(referenceName, paintable)

    def getPaintIdentifier(self, paintable):
        if not self._manager.hasPaintableId(paintable):
            if self._identifiersCreatedDueRefPaint is None:
                self._identifiersCreatedDueRefPaint = set()
            self._identifiersCreatedDueRefPaint.add(paintable)
        return self._manager.getPaintableId(paintable)

    def addCharacterData(self, text):
        if text is not None:
            self._tag.addData(text)
        return

    def getUsedResources(self):
        return self._usedResources

    def needsToBePainted(self, p):
        """Method to check if paintable is already painted into this target.

        @return: true if is not yet painted into this target and is connected
                to app
        """
        if p in self._paintedComponents:
            return False
        else:
            if p.getApplication() is None:
                return False
            else:
                return True

            return

    _widgetMappingCache = dict()

    def getTag(self, paintable):
        class1 = self._widgetMappingCache.get(paintable.__class__)
        if class1 is None:
            class1 = paintable.__class__
            while not self.hasClientWidgetMapping(class1):
                superclass = getSuperClass(class1)
                if superclass is not None and issubclass(class1, IPaintable):
                    class1 = superclass
                else:
                    logger.warning('No superclass of ' + clsname(paintable.__class__) + ' has a @ClientWidget annotation. Component will not be mapped correctly on client side.')
                    break

            self._widgetMappingCache[paintable.__class__] = class1
        self._usedPaintableTypes.append(class1)
        return self._manager.getTagForType(class1)

    def hasClientWidgetMapping(self, class1):
        return 'CLIENT_WIDGET' in class1.__dict__

    def getUsedPaintableTypes(self):
        return self._usedPaintableTypes

    def isFullRepaint(self):
        """@see L{PaintTarget.isFullRepaint}"""
        return not self._cacheEnabled


class JsonTag(object):
    """This is basically a container for UI components variables, that
    will be added at the end of JSON object.

    @author: mattitahvonen
    """

    def __init__(self, tagName, target):
        self._firstField = False
        self._variables = list()
        self._children = list()
        self._attr = list()
        self._data = StringIO()
        self.childrenArrayOpen = False
        self._childNode = False
        self._tagClosed = False
        self._data.write('["' + tagName + '"')
        self._target = target

    def _closeTag(self):
        if not self._tagClosed:
            self._data.write(self._attributesAsJsonObject())
            self._data.write(self.getData())
            self._data.write(']')
            self._tagClosed = True

    def getJSON(self):
        if not self._tagClosed:
            self._closeTag()
        return self._data.getvalue()

    def openChildrenArray(self):
        if not self.childrenArrayOpen:
            self.childrenArrayOpen = True

    def closeChildrenArray(self):
        pass

    def setChildNode(self, b):
        self._childNode = b

    def isChildNode(self):
        return self._childNode

    def startField(self):
        if self._firstField:
            self._firstField = False
            return ''
        else:
            return ','

    def addData(self, s):
        """@param s: json string, object or array"""
        self._children.append(s)

    def getData(self):
        buf = StringIO()
        for c in self._children:
            buf.write(self.startField())
            buf.write(c)

        result = buf.getvalue()
        buf.close()
        return result

    def addAttribute(self, jsonNode):
        self._attr.append(jsonNode)

    def _attributesAsJsonObject(self):
        buf = StringIO()
        buf.write(self.startField())
        buf.write('{')
        for i, element in enumerate(self._attr):
            buf.write(element)
            if i != len(self._attr) - 1:
                buf.write(',')

        buf.write(self._target._tag._variablesAsJsonObject())
        buf.write('}')
        result = buf.getvalue()
        buf.close()
        return result

    def addVariable(self, v):
        self._variables.append(v)

    def _variablesAsJsonObject(self):
        if len(self._variables) == 0:
            return ''
        buf = StringIO()
        buf.write(self.startField())
        buf.write('"v":{')
        for i, element in enumerate(self._variables):
            buf.write(element.getJsonPresentation())
            if i != len(self._variables) - 1:
                buf.write(',')

        buf.write('}')
        result = buf.getvalue()
        buf.close()
        return result


class Variable(object):

    def getJsonPresentation(self):
        pass


class BooleanVariable(Variable):

    def __init__(self, owner, name, v):
        self._value = v
        self.name = name

    def getJsonPresentation(self):
        return '"' + self.name + '":' + ('true' if self._value == True else 'false')


class StringVariable(Variable):

    def __init__(self, owner, name, v):
        self._value = v
        self.name = name

    def getJsonPresentation(self):
        return '"' + self.name + '":"' + self._value + '"'


class IntVariable(Variable):

    def __init__(self, owner, name, v):
        self._value = v
        self.name = name

    def getJsonPresentation(self):
        return '"' + self.name + '":' + str(self._value)


class LongVariable(Variable):

    def __init__(self, owner, name, v):
        self._value = v
        self.name = name

    def getJsonPresentation(self):
        return '"' + self.name + '":' + str(self._value)


class FloatVariable(Variable):

    def __init__(self, owner, name, v):
        self._value = v
        self.name = name

    def getJsonPresentation(self):
        return '"' + self.name + '":' + str(self._value)


class DoubleVariable(Variable):

    def __init__(self, owner, name, v):
        self._value = v
        self.name = name

    def getJsonPresentation(self):
        return '"' + self.name + '":' + str(self._value)


class ArrayVariable(Variable):

    def __init__(self, owner, name, v):
        self._value = v
        self.name = name

    def getJsonPresentation(self):
        sb = StringIO()
        sb.write('"')
        sb.write(self.name)
        sb.write('":[')
        for i in range(len(self._value)):
            sb.write('"')
            sb.write(JsonPaintTarget.escapeJSON(str(self._value[i])))
            sb.write('"')
            if i < len(self._value) - 1:
                sb.write(',')

        sb.write(']')
        result = sb.getvalue()
        sb.close()
        return result