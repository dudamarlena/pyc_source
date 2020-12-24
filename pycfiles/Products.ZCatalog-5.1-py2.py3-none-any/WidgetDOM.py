# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.freebsd-7.1-PRERELEASE-i386/egg/Products/XMLWidgets/WidgetDOM.py
# Compiled at: 2008-08-28 08:23:26
__doc__ = '\nXMLWidgets support for DOM classes.\n'
import Globals, Acquisition
from Products.ParsedXML import DOMProxy, DOM, ExtraDOM
from Products.ParsedXML.ManageableDOM import DOMTraversable
import xml.dom
from Products.ParsedXML.NodePath import registry

class WidgetAttribute(Acquisition.Implicit):
    __module__ = __name__

    def __getitem__(self, name):
        """
        """
        node = self.aq_parent
        return getattr(self.service_editor.getWidget(node), name)


def getWidgetWrappedNode(node):
    """Get a node for the widget wrapped with the WidgetDOM wrappers.
    """
    if node is None:
        return
    wrapper_type = WRAPPER_TYPES[node._get_nodeType()]
    parent = node.getPersistentDoc() or node
    return wrapper_type(node._node, node._persistentDoc).__of__(parent)


class WidgetWrapper:
    """
    Mixin class to go alongside WidgetNode classes.
    """
    __module__ = __name__
    __allow_access_to_unprotected_subobjects__ = 1

    def wrapNamedNodeMap(self, obj):
        if obj is None:
            return
        parent = self.getPersistentDoc() or self
        wrapped = WidgetNamedNodeMap(obj, self._persistentDoc).__of__(parent)
        return wrapped

    def wrapNodeList(self, obj):
        parent = self.getPersistentDoc() or self
        wrapped = WidgetNodeList(obj, self._persistentDoc).__of__(parent)
        return wrapped

    def wrapDOMObj(self, node):
        """Return the appropriate class wrapped around the node."""
        if node is None:
            return
        wrapper_type = WRAPPER_TYPES[node._get_nodeType()]
        parent = self.getPersistentDoc() or self
        wrapped = wrapper_type(node, self._persistentDoc).__of__(parent)
        return wrapped

    def getWidgetRegistryName(self):
        session = self.REQUEST.SESSION
        node = self
        while getattr(node.aq_base, 'meta_type', None) != 'Parsed XML':
            node = node.aq_parent

        document_url = node.absolute_url()
        document = node
        if session.has_key('xmlwidgets_node_event_handler'):
            xmlwidgets_node_event_handler = session['xmlwidgets_node_event_handler']
        else:
            xmlwidgets_node_event_handler = {}
        nodepath_wr_names = xmlwidgets_node_event_handler.get(document_url, None)
        if nodepath_wr_names:
            node = self
            while node is not None:
                path = registry.create_path(node.ownerDocument, node, 'widget')
                name = nodepath_wr_names.get(path, None)
                if name:
                    return name
                node = node.parentNode

        if not session.has_key('xmlwidgets_event_handler'):
            session['xmlwidgets_event_handler'] = {}
        result = session['xmlwidgets_event_handler'].get(document_url, 'service_document_editor')
        return result

    def getWidgetRegistryNode(self):
        session = self.REQUEST.SESSION
        node = self
        while getattr(node.aq_base, 'meta_type', None) != 'Parsed XML':
            node = node.aq_parent

        document_url = node.absolute_url()
        if session.has_key('xmlwidgets_node_event_handler'):
            xmlwidgets_node_event_handler = session['xmlwidgets_node_event_handler']
        else:
            xmlwidgets_node_event_handler = {}
        nodepath_wr_names = xmlwidgets_node_event_handler.get(document_url, None)
        if nodepath_wr_names:
            node = self
            while node is not None:
                path = registry.create_path(node.ownerDocument, node, 'widget')
                name = nodepath_wr_names.get(path, None)
                if name:
                    return node
                node = node.parentNode

        return document.documentElement

    edit = WidgetAttribute()


class WidgetTraversable(DOMTraversable):
    """Traversing the widget way.
    """
    __module__ = __name__


_WIDGET_DOM_FEATURES = (
 ('org.zope.dom.persistence', None), ('org.zope.dom.persistence', ''), ('org.zope.dom.persistence', '1.0'), ('org.zope.dom.acquisition', None), ('org.zope.dom.acquisition', ''), ('org.zope.dom.acquisition', '1.0'))
_WIDGET_DOM_NON_FEATURES = (
 ('load', None), ('load', ''), ('load', '3.0'))

class WidgetDOMImplementation(DOMProxy.DOMImplementationProxy):
    """A proxy of a DOMImplementation node that defines createDocument
    to return a WidgetDocument.
    """
    __module__ = __name__

    def hasFeature(self, feature, version):
        feature = string.lower(feature)
        if (feature, version) in _WIDGET_DOM_FEATURES:
            return 1
        if (
         feature, version) in _WIDGET_DOM_NON_FEATURES:
            return 0
        return DOMProxy.DOMImplementationProxy.hasFeature(self, feature, version)

    def createDocumentType(self, qualifiedName, publicId, systemId):
        DOMDocumentType = self._createDOMDocumentType(qualifiedName, publicId, systemId)
        return WidgetDocumentType(DOMDocumentType)

    def createDocument(self, namespaceURI, qualifiedName, docType=None):
        if docType is not None:
            if docType.ownerDocument is not None:
                raise xml.dom.WrongDocumentErr
            mdocType = docType.getDOMObj()
        else:
            mdocType = None
        DOMDocument = self._createDOMDocument(namespaceURI, qualifiedName, mdocType)
        return WidgetDocument(DOMDocument)


theDOMImplementation = WidgetDOMImplementation()

class WidgetNode(WidgetWrapper, DOMProxy.NodeProxy, WidgetTraversable, Acquisition.Implicit):
    """A wrapper around a DOM Node."""
    __module__ = __name__


class WidgetNodeList(WidgetWrapper, DOMProxy.NodeListProxy, Acquisition.Implicit):
    """A wrapper around a DOM NodeList."""
    __module__ = __name__
    meta_type = 'Widget NodeList'

    def __getslice__(self, i, j):
        return self.wrapNodeList(self._node.__getslice__(i, j))

    def __getitem__(self, i):
        return self.wrapDOMObj(self._node.__getitem__(i))


class WidgetNamedNodeMap(WidgetWrapper, DOMProxy.NamedNodeMapProxy, Acquisition.Implicit):
    """A wrapper around a DOM NamedNodeMap."""
    __module__ = __name__
    meta_type = 'Widget NamedNodeMap'

    def __getitem__(self, i):
        return self.wrapDOMObj(self._node.__getitem__(i))


class WidgetDocumentFragment(WidgetWrapper, DOMProxy.DocumentFragmentProxy, WidgetNode):
    """A wrapper around a DOM DocumentFragment."""
    __module__ = __name__
    meta_type = 'Widget Document Fragment'


class WidgetElement(WidgetWrapper, DOMProxy.ElementProxy, WidgetNode):
    """A wrapper around a DOM Element."""
    __module__ = __name__
    meta_type = 'Widget Element'


class WidgetCharacterData(WidgetWrapper, DOMProxy.CharacterDataProxy, WidgetNode):
    """A wrapper around a DOM CharacterData."""
    __module__ = __name__
    meta_type = 'Widget Character Data'


class WidgetCDATASection(WidgetWrapper, DOMProxy.CDATASectionProxy, WidgetNode):
    """A wrapper around a DOM CDATASection."""
    __module__ = __name__
    meta_type = 'Widget CDATASection'


class WidgetText(WidgetWrapper, DOMProxy.TextProxy, WidgetCharacterData):
    """A wrapper around a DOM Text."""
    __module__ = __name__
    meta_type = 'Widget Text'


class WidgetComment(WidgetWrapper, DOMProxy.CommentProxy, WidgetCharacterData):
    """A wrapper around a DOM Comment."""
    __module__ = __name__
    meta_type = 'Widget Comment'


class WidgetProcessingInstruction(WidgetWrapper, DOMProxy.ProcessingInstructionProxy, WidgetNode):
    """A wrapper around a DOM ProcessingInstruction."""
    __module__ = __name__
    meta_type = 'Widget Processing Instruction'


class WidgetAttr(WidgetWrapper, DOMProxy.AttrProxy, WidgetNode):
    """A wrapper around a DOM Attr."""
    __module__ = __name__
    meta_type = 'Widget Attr'


class WidgetDocument(WidgetWrapper, DOMProxy.DocumentProxy, WidgetNode):
    """A wrapper around a DOM Document."""
    __module__ = __name__
    meta_type = 'Widget Document'
    implementation = theDOMImplementation

    def __init__(self, node, persistentDocument=None):
        WidgetNode.__init__(self, node, persistentDocument)

    def _get_implementation(self):
        return self.implementation

    def __setattr__(self, name, value):
        if name == 'implementation':
            raise xml.dom.NoModificationAllowedErr()
        WidgetDocument.inheritedAttribute('__setattr__')(self, name, value)


class WidgetEntityReference(WidgetWrapper, DOMProxy.EntityReferenceProxy, WidgetNode):
    """A wrapper around a DOM EntityReference."""
    __module__ = __name__
    meta_type = 'Widget Entity Reference'


class WidgetEntity(WidgetWrapper, DOMProxy.EntityProxy, WidgetNode):
    """A wrapper around a DOM Entity."""
    __module__ = __name__
    meta_type = 'Widget Entity'


class WidgetNotation(WidgetWrapper, DOMProxy.NotationProxy, WidgetNode):
    """A wrapper around a DOM Notation."""
    __module__ = __name__
    meta_type = 'Widget Notation'


class WidgetDocumentType(WidgetWrapper, DOMProxy.DocumentTypeProxy, WidgetNode):
    """A wrapper around a DOM DocumentType."""
    __module__ = __name__
    meta_type = 'Widget Document Type'


Node = xml.dom.Node
WRAPPER_TYPES = {Node.ELEMENT_NODE: WidgetElement, Node.ATTRIBUTE_NODE: WidgetAttr, Node.TEXT_NODE: WidgetText, Node.CDATA_SECTION_NODE: WidgetCDATASection, Node.ENTITY_REFERENCE_NODE: WidgetEntityReference, Node.ENTITY_NODE: WidgetEntity, Node.PROCESSING_INSTRUCTION_NODE: WidgetProcessingInstruction, Node.COMMENT_NODE: WidgetComment, Node.DOCUMENT_NODE: WidgetDocument, Node.DOCUMENT_TYPE_NODE: WidgetDocumentType, Node.DOCUMENT_FRAGMENT_NODE: WidgetDocumentFragment, Node.NOTATION_NODE: WidgetNotation}
del Node