# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/rsl/xsd/component.py
# Compiled at: 2009-01-22 17:05:45
"""
this module defines all structural elements of the xsd standard.

@todo: probably all of this classes here need some rework, to make them more
       complete to the standard.

@todo: does getsubelementnames also return attributes names? if yes, then 
       this method needs to be renamed
       
@todo: split this module into smaller pieces
"""
import logging
log = logging.getLogger('rsl.xsd')
from rsl.misc.namespace import clark, qname2clark, clark2tuple
from rsl.xsd.urtype import AnyType
from rsl.xsd.namespace import NS_XMLSCHEMA, NS_XMLSCHEMA_99

def multiplicity(occurs):
    """
    handle xsd maxOccurs/minOccurs attributes.
    """
    if occurs is None:
        return 1
    if occurs in ('unbounded', '*'):
        return -1
    return int(occurs)


class XSAnnotation(object):
    """
    implementation of <annotation> element.
    """

    def __init__(self, element):
        """
        parse child elements or ignore content for now.
        """
        self.content = None
        for child in element.getchildren():
            if child.tag in self.allowed_content:
                self.content = self.allowed_content[child.tag](child)
            elif child.tag in self.ignore_content:
                continue
            else:
                log.warn('XSAnnotation: Schemaelement ' + child.tag + ' not implemented')

        return


class XSDocumentation(object):
    """
    implementation of <documentation> element.
    """

    def __init__(self, element):
        """
        just store text.
        """
        self.text = element.text


class XSAnnotated(object):
    """
    Base class for structure types.
    Every structure type can have Annotations
    """

    def __init__(self, element, xsd):
        """
        initialise this instance and parse annotation elements.
        """
        super(XSAnnotated, self).__init__()
        self.xsd = xsd
        self.annotations = None
        self._name = None
        self.frometree(element)
        return

    def frometree(self, element):
        """
        parse annotation child elements.
        parse name attribute
        """
        if element is None:
            return
        self._name = element.get('name')
        self.findannotations(clark(NS_XMLSCHEMA, 'annotation'), element)
        self.findannotations(clark(NS_XMLSCHEMA_99, 'annotation'), element)
        return self

    def findannotations(self, tag, element):
        """
        find all elements named tag (currently only "annotation") and store
        it in the instance.
        """
        for child in element.findall(tag):
            if not self.annotations:
                self.annotations = []
            self.annotations.append(XSAnnotation(child))
            element.remove(child)


class XSSimpleType(XSAnnotated):
    """ 
    Simple types are derived by restriction, union or list.
    A simple type can't have any attributes or children.
    """

    def __init__(self, element, xsd):
        """
        parse the <simpletype> element and store all relevant information.
        """
        super(XSSimpleType, self).__init__(element, xsd)
        self.content = None
        for child in element.getchildren():
            if child.tag in self.allowed_content:
                self.content = self.allowed_content[child.tag](child, xsd)
            elif child.tag in self.ignored_content:
                continue
            else:
                log.warn('XSSimpleType : Schemaelement ' + child.tag + ' not implemented')

        return

    def getelement(self):
        """
        return xsd-element defined for this instance.
        """
        return self.content.getelement()

    def getattributes(self):
        """
        return xsd-attributes defined for this instance.
        """
        return

    def gettypename(self):
        """
        return tuple of nsurl and local name for this type.
        """
        return (
         self.xsd.targetnamespace, self._name)

    def getsubelementnames(self, visited=None):
        """
        return all possible child element names
        """
        return self.content.getsubelementnames(visited)

    def gettype(self):
        """
        return xsd-type for this type.
        """
        return self

    def encode(self, data):
        """
        serialize python data to xml-string.
        """
        return self.content.encode(data)

    def decode(self, data):
        """
        deserialize data to python data type.
        """
        return self.content.decode(data)


class XSRestriction(XSAnnotated):
    """
    the xsd <restriction> element.
    """

    def __init__(self, element, xsd):
        """
        parse all relevant information from the restriction element.
        """
        super(XSRestriction, self).__init__(element, xsd)
        self.base = qname2clark(element.get('base'), element.nsmap)
        self.content = None
        self.attributes = None
        for child in element.getchildren():
            if child.tag in self.allowed_content:
                self.content = self.allowed_content[child.tag](child, xsd)
            elif child.tag in self.ignored_content:
                continue
            elif child.tag in (clark(NS_XMLSCHEMA, 'attribute'),
             clark(NS_XMLSCHEMA_99, 'attribute')):
                if not self.attributes:
                    self.attributes = []
                self.attributes.append(XSAttribute(child, xsd))
            elif child.tag in (clark(NS_XMLSCHEMA, 'anyAttribute'),
             clark(NS_XMLSCHEMA_99, 'anyAttribute')):
                pass
            elif child.tag in (clark(NS_XMLSCHEMA, 'group'),
             clark(NS_XMLSCHEMA_99, 'group')):
                ref = child.get('ref')
                clarkref = qname2clark(ref, child.nsmap)
                self.content = SchemaReference(clarkref, 'group', xsd)
            else:
                log.warn('XSRestriction : Schemaelement ' + child.tag + ' not implemented')

        return

    def _getbasecontent(self):
        """
        helper method to find base type for content.
        """
        if self.content is None:
            return self.xsd.getType(self.base)
        return self.content

    def getelement(self):
        """
        return xsd-element for this type
        """
        return self._getbasecontent().getelement()

    def getattributes(self):
        """
        return defined attributes for this type.
        """
        if self.attributes is None:
            return self.xsd.getType(self.base).getattributes()
        return self.attributes

    def getsubelementnames(self, visited=None):
        """
        return all possible child element names
        """
        return self._getbasecontent().getsubelementnames(visited)

    def encode(self, data):
        """
        serialise with the help of the base type.
        """
        return self._getbasecontent().encode(data)

    def decode(self, data):
        """
        deserialise with the help of the base type.
        """
        return self._getbasecontent().decode(data)


class XSExtension(XSAnnotated):
    """
    the xsd <extension> element.
    """

    def __init__(self, element, xsd):
        """
        parse all relevant information from the restriction element.
        """
        super(XSExtension, self).__init__(element, xsd)
        self.base = qname2clark(element.get('base'), element.nsmap)
        self.extensions = None
        for child in element.getchildren():
            if child.tag in self.allowed_content:
                if not self.extensions:
                    self.extensions = []
                self.extensions.append(self.allowed_content[child.tag](child))
            elif child.tag in self.ignored_content:
                continue
            else:
                log.warn('XSExtension : Schemaelement ' + child.tag + ' not implemented')

        return

    def getelement(self):
        """
        return xsd-element for this type
        """
        return self.xsd.getType(self.base).getelement()

    def getsubelementnames(self, visited=None):
        """
        return all possible child element names
        """
        return self.xsd.getType(self.base).getsubelementnames(visited)


class XSChoice(XSAnnotated):
    """
    the xsd <choice> element.
    """

    def __init__(self, element, xsd):
        """
        parse all relevant information from the restriction element.
        """
        super(XSChoice, self).__init__(element, xsd)
        self.content = None
        for child in element.getchildren():
            if child.tag in self.allowed_content:
                if not self.content:
                    self.content = []
                self.content.append(self.allowed_content[child.tag](child, xsd))
            elif child.tag in self.ignored_content:
                continue
            else:
                log.warn('XSChoice : Schemaelement ' + child.tag + ' not implemented')

        return

    def getelement(self):
        """
        return xsd-element for all subelements
        """
        ret = []
        for ctnt in self.content:
            ret.append(ctnt.getelement())

        return ret

    def getsubelementnames(self, visited=None):
        """
        return all possible child element names
        """
        paramnames = []
        for ctnt in self.content:
            paramnames += ctnt.getsubelementnames(visited)

        return paramnames


class XSSequence(XSAnnotated):
    """
    the xsd <sequence> element.
    """

    def __init__(self, element, xsd):
        """
        parse all relevant information from the restriction element.
        """
        super(XSSequence, self).__init__(element, xsd)
        self.content = None
        for child in element.getchildren():
            if child.tag in self.allowed_content:
                if not self.content:
                    self.content = []
                self.content.append(self.allowed_content[child.tag](child, xsd))
            elif child.tag in self.ignored_content:
                continue
            else:
                log.warn('XSSequence : Schemaelement ' + child.tag + ' not implemented')

        return

    def getelement(self):
        """
        return xsd-element for all subelements
        """
        if self.content is None:
            return
        ret = []
        for ctnt in self.content:
            ret.append(ctnt.getelement())

        return ret

    def getsubelementnames(self, visited=None):
        """
        return all possible child element names
        """
        if not self.content:
            return
        paramnames = []
        for ctnt in self.content:
            paramnames += ctnt.getsubelementnames(visited)

        return paramnames


class XSAll(XSAnnotated):
    """
    the xsd <all> element.
    """

    def __init__(self, element, xsd):
        """
        parse all relevant information from the restriction element.
        """
        super(XSAll, self).__init__(element, xsd)
        self.content = None
        for child in element.getchildren():
            (childns, childname) = clark2tuple(child.tag)
            if childns in (NS_XMLSCHEMA, NS_XMLSCHEMA_99):
                if childname == 'element':
                    if not self.content:
                        self.content = []
                    self.content.append(XSElement(child, xsd))
                else:
                    log.warn('XSAll : Schemaelement ' + child.tag + ' not implemented')
            else:
                log.warn('XSAll : Schema namespace  ' + childns + ' not supported')

        return

    def getelement(self):
        """
        return xsd-element for all subelements
        """
        ret = []
        for ctnt in self.content:
            ret.append(ctnt.getelement())

        return ret

    def getsubelementnames(self, visited=None):
        """
        return all possible child element names
        """
        paramnames = []
        for ctnt in self.content:
            paramnames += ctnt.getsubelementnames(visited)

        return paramnames


class XSAny(XSAnnotated):
    """
    the xsd <any> element.
    """

    def __init__(self, element, xsd):
        """
        parse all relevant information from the restriction element.
        """
        super(XSAny, self).__init__(element, xsd)
        self.minoccurs = multiplicity(element.get('minOccurs'))
        self.maxoccurs = multiplicity(element.get('maxOccurs'))
        self.namespace = element.get('namespace')
        self.processcontents = element.get('processCotnents')
        self.xstype = AnyType('any', xsd)
        self._name = 'any'

    def getelement(self):
        """
        return xsd-element for this element
        """
        return self

    def getsubelementnames(self, visited=None):
        """
        return all possible child element names
        """
        return {'any': None}

    def gettype(self):
        """
        return xsd-type for this type.
        """
        return self.xstype

    def getlocalname(self):
        """
        return always the unqalified element name.
        """
        return self._name

    def getname(self):
        """
        return un/qualified element name according to element form. 
        """
        return self._name


class XSGroup(XSAnnotated):
    """
    the xsd <group> element.
    """

    def __init__(self, element, xsd):
        """
        parse all relevant information from the restriction element.
        """
        super(XSGroup, self).__init__(element, xsd)
        self.name = element.get('name')
        for child in element.getchildren():
            (childns, childname) = clark2tuple(child.tag)
            if childns in (NS_XMLSCHEMA, NS_XMLSCHEMA_99):
                if childname == 'choice':
                    self.content = XSChoice(child, xsd)
                elif childname == 'sequence':
                    self.content = XSSequence(child, xsd)
                elif childname == 'all':
                    self.content = XSAll(child, xsd)
                else:
                    log.warn('XSGroup : Schemaelement ' + child.tag + ' not implemented')
            else:
                log.warn('XSGroup : Schema namespace ' + childns + ' not supported')

    def getelement(self):
        """
        return xsd-element for this element
        """
        return self.content.getelement()

    def getattributes(self):
        """
        return defined attributes for this type.
        """
        if self.content is not None:
            if hasattr(self.content, 'getattributes'):
                return self.content.getattributes()
        return

    def getsubelementnames(self, visited=None):
        """
        return all possible child element names
        """
        return self.content.getsubelementnames(visited)


class XSComplexContent(XSAnnotated):
    """
    the xsd <complexcontent> element.
    """

    def __init__(self, element, xsd):
        """
        parse all relevant information from the restriction element.
        """
        super(XSComplexContent, self).__init__(element, xsd)
        self.content = None
        for child in element.getchildren():
            (childns, childname) = clark2tuple(child.tag)
            if childns in (NS_XMLSCHEMA, NS_XMLSCHEMA_99):
                if childname == 'restriction':
                    self.content = XSRestriction(child, xsd)
                elif childname == 'extension':
                    self.content = XSExtension(child, xsd)
                elif childname == 'all':
                    self.content = XSAll(child, xsd)
                else:
                    log.warn('XSComplexContent : Schemaelement ' + child.tag + ' not implemented')
            else:
                log.warn('XSComplexContent : Schema namespace ' + childns + ' not supported')

        return

    def getelement(self):
        """
        return xsd-element for this element
        """
        return self.content.getelement()

    def getattributes(self):
        """
        return defined attributes for this type.
        """
        if self.content is not None:
            if hasattr(self.content, 'getattributes'):
                return self.content.getattributes()
        return

    def getsubelementnames(self, visited=None):
        """
        return all possible child element names
        """
        return self.content.getsubelementnames(visited)


class XSComplexType(XSAnnotated):
    """ 
    A complex content type allows attributes and child elements.
    If it containts simplecontent then no child elements are allowd.
    The default for complex content is to derive from anyType and contain complexcontent.
    So if the child element of complexType is not simpleContent or complexContent it
    defaults to complexContent with base="anyType".
    A content element which does not allow any content, must be a complexcontent with no
    structure defined. (simplecontent allows data content)
    
    @todo: maybe interpret XSComplexType always as XSComplexContent
    """

    def __init__(self, element, xsd):
        """
        parse all relevant information from the restriction element.
        """
        super(XSComplexType, self).__init__(element, xsd)
        self.content = None
        self.attributes = None
        self.base = qname2clark(element.get('base'), element.nsmap)
        for child in element.getchildren():
            if child.tag in self.allowed_content:
                self.content = self.allowed_content[child.tag](child, xsd)
            elif child.tag in self.ignored_content:
                continue
            elif child.tag in (clark(NS_XMLSCHEMA, 'attribute'),
             clark(NS_XMLSCHEMA_99, 'attribute')):
                if not self.attributes:
                    self.attributes = []
                self.attributes.append(XSAttribute(child, xsd))
            elif child.tag in (clark(NS_XMLSCHEMA, 'anyAttribute'),
             clark(NS_XMLSCHEMA_99, 'anyAttribute')):
                pass
            elif child.tag in (clark(NS_XMLSCHEMA, 'group'),
             clark(NS_XMLSCHEMA_99, 'group')):
                ref = child.get('ref')
                clarkref = qname2clark(ref, child.nsmap)
                self.content = SchemaReference(clarkref, 'group', xsd)
            else:
                log.warn('XSComplexType : Schemaelement ' + child.tag + ' not implemented')

        return

    def getelement(self):
        """
        return xsd-element for this element
        """
        if self.content is None:
            return
        return self.content.getelement()

    def getattributes(self):
        """
        return defined attributes for this type.
        """
        if self.attributes is None:
            if hasattr(self.content, 'getattributes'):
                return self.content.getattributes()
        return self.attributes

    def gettypename(self):
        """
        return tuple of nsurl and local name for this type.
        """
        return (
         self.xsd.targetnamespace, self._name)

    def getsubelementnames(self, visited=None):
        """
        return all possible child element names
        """
        if self.content is None:
            return
        return self.content.getsubelementnames(visited)

    def gettype(self):
        """
        return xsd-type for this type.
        """
        return self


class XSSimpleContent(XSAnnotated):
    """
    the xsd <simplecontent> element.
    """

    def __init__(self, element, xsd):
        """
        parse all relevant information from the restriction element.
        """
        super(XSSimpleContent, self).__init__(element, xsd)
        self.content = None
        for child in element.getchildren():
            (childns, childname) = clark2tuple(child.tag)
            if childns in (NS_XMLSCHEMA, NS_XMLSCHEMA_99):
                if childname == 'restriction':
                    self.content = XSRestriction(child, xsd)
                elif childname == 'extension':
                    self.content = XSExtension(child, xsd)
                else:
                    log.warn('XSSimpleContent : Schemaelement ' + child.tag + ' not implemented')
            else:
                log.warn('XSSimpleContent : Schema namespace ' + childns + ' not supported')

        return

    def getelement(self):
        """
        return xsd-element for this element
        """
        return self.content.getelement()

    def getsubelementnames(self, visited=None):
        """
        return all possible child element names
        """
        return self.content.getsubelementnames(visited)


class SchemaReference(object):
    """
    this is not a real structural element of XML Schema, but it helps me here
    to late bind schema references.
    """

    def __init__(self, nameref, what, xsd):
        """
        @param what: what to reference? a "type", "element" or "group"
        @type what: C{string}
        
        @param xsd: the XMLSchema where this instance is contained in
        @type xsd: L{XMLSchema}
        """
        self.nameref = nameref
        self.what = what
        self.xsd = xsd

    def resolve(self):
        """
        reslve the actual xsd-isntance referred to by this instance.
        """
        if self.what == 'type':
            ref = self.xsd.getType(self.nameref)
        elif self.what == 'element':
            ref = self.xsd.getElement(self.nameref)
        elif self.what == 'group':
            ref = self.xsd.getGroup(self.nameref)
        elif self.what == 'attribute':
            ref = self.xsd.getAttribute(self.nameref)
        else:
            raise Exception('unknown reference type:' + self.what)
        return ref

    def getelement(self):
        """
        return xsd-element for this element
        """
        return self.resolve().getelement()

    def getattributes(self):
        """
        return defined attributes for this type.
        """
        return self.resolve().getattributes()

    def gettype(self):
        """
        return xsd-type for this type.
        """
        return self.resolve().gettype()

    def gettypename(self):
        """
        return tuple of nsurl and local name for this type.
        """
        return self.resolve().gettypename()

    def tostring(self, data):
        """
        return string representation of this instance/reference.
        """
        return self.resolve().tostring(data)

    def getsubelementnames(self, visited=None):
        """
        return all possible child element names
        """
        return self.resolve().getsubelementnames(visited)


class XSAttribute(XSAnnotated):
    """
    the xsd <attribute> element.
    """

    def __init__(self, element, xsd):
        """
        parse all relevant information from the restriction element.
        """
        super(XSAttribute, self).__init__(element, xsd)
        elemattrib = element.attrib
        self._xstype = elemattrib.pop('type', None)
        if self._xstype:
            self._xstype = SchemaReference(qname2clark(self._xstype, element.nsmap), 'type', xsd)
        self.default = elemattrib.pop('default', None)
        self.fixed = elemattrib.pop('fixed', None)
        self._tns = xsd.targetnamespace
        self._form = elemattrib.pop('form', None)
        if not self._form:
            if element.getparent().tag in (clark(NS_XMLSCHEMA, 'schema'),
             clark(NS_XMLSCHEMA_99, 'schema')):
                self._form = 'qualified'
            else:
                self._form = xsd.attributeformdefault or 'unqualified'
        self._ref = elemattrib.pop('ref', None)
        if self._ref:
            self._ref = SchemaReference(qname2clark(self._ref, element.nsmap), 'attribute', xsd)
        self.use = elemattrib.pop('use', None)
        for child in element.getchildren():
            (childns, childname) = clark2tuple(child.tag)
            if childns in (NS_XMLSCHEMA, NS_XMLSCHEMA_99):
                if childname == 'simpleType':
                    self.xstype = XSSimpleType(child, xsd)
                else:
                    log.warn('XSAttribute : Schemaelement ' + child.tag + ' not implemented')
            else:
                log.warn('XSAttribute : Schema namespace ' + childns + ' not supported')

        return

    def getname(self):
        """
        return un/qualified name depending on attribute from.
        """
        if self._ref:
            return self._ref.resolve().getname()
        if self._form == 'qualified':
            return clark(self._tns, self._name)
        elif self._form == 'unqualified':
            return self._name
        else:
            raise Exception('attribute from must be qualified or unqualified                              (%s)' % self._form)

    def getlocalname(self):
        """
        return alwaus unqualified name.
        """
        if self._ref:
            return self._ref.resolve().getlocalname()
        return self._name

    def encode(self, data):
        """
        data should be a dictionary possibly containing a value for this 
        attribute return value or None
        
        @todo: change this method to accept value in data instead of dict
        """
        if self._ref:
            return self._ref.resolve().encode(data)
        if self.use == 'prohibited':
            return (None, None)
        attrvalue = None
        if self.fixed:
            attrvalue = self.fixed
        elif self._name in data:
            attrvalue = self._xstype.resolve().encode(data[self._name])
        elif self.default:
            attrvalue = self.default
        elif self.use == 'required':
            log.warn('XSAttribute : required attribute ' + self._name + ' not serialized')
            attrvalue = ''
        return attrvalue

    def decode(self, data):
        """
        deserialize data to python data type.
        """
        if self._ref:
            return self._ref.resolve().decode(data)
        return self._xstype.resolve().decode(data)


class XSElement(XSAnnotated):
    """ 
    An element is a bit special. It can be an element referece, or just 
    reference a type defnition, or it can have its own complexType included.
    """

    def __init__(self, element, xsd):
        """
        parse all relevant information from the restriction element.
        """
        super(XSElement, self).__init__(element, xsd)
        self.keys = []
        self.minoccurs = multiplicity(element.get('minOccurs'))
        self.maxoccurs = multiplicity(element.get('maxOccurs'))
        self._tns = xsd.targetnamespace
        self._form = element.get('form')
        if not self._form:
            if element.getparent().tag in (clark(NS_XMLSCHEMA, 'schema'),
             clark(NS_XMLSCHEMA_99, 'schema')):
                self._form = 'qualified'
            else:
                self._form = xsd.elementformdefault
        self._xstype = element.get('type')
        if self._xstype:
            self._xstype = SchemaReference(qname2clark(self._xstype, element.nsmap), 'type', xsd)
        self.ref = element.get('ref')
        if self.ref:
            self.ref = SchemaReference(qname2clark(self.ref, element.nsmap), 'element', xsd)
        self.content = None
        for child in element.getchildren():
            (childns, childname) = clark2tuple(child.tag)
            if childns in (NS_XMLSCHEMA, NS_XMLSCHEMA_99):
                if childname == 'complexType':
                    self.content = XSComplexType(child, xsd)
                elif childname == 'simpleType':
                    self.content = XSSimpleType(child, xsd)
                elif childname in ('key', 'unique'):
                    pass
                else:
                    log.warn('XSElement : Schemaelement ' + child.tag + ' not implemented ')
            else:
                log.warn('XSElement : Schema namespace ' + childns + ' not supported')

        return

    def getname(self):
        """
        return un/qualified element name according to element form. 
        """
        if self.ref:
            return self.ref.resolve().getname()
        if self._form == 'qualified':
            return clark(self._tns, self._name)
        elif self._form == 'unqualified':
            return self._name
        else:
            raise Exception('element form has to be qualified or unqualified                              (%s)' % self._form)

    def getlocalname(self):
        """
        return unqualified name of this attribute.
        """
        if self.ref:
            return self.ref.resolve().getlocalname()
        return self._name

    def getsubelementnames(self, visited=None):
        """
        all elements represent paramnames....
        """
        if self.ref:
            return self.ref.getsubelementnames(visited)
        if visited is None:
            visited = set()
        if self in visited:
            return self._name
        visited.add(self)
        paramnames = None
        if self._xstype:
            paramnames = self._xstype.getsubelementnames(visited)
        if self.content:
            paramnames = self.content.getsubelementnames(visited)
        if self._name:
            visited.remove(self)
            return {self._name: paramnames}
        raise Exception('Should never reach here....')
        return

    def getelement(self):
        """
        return xsd-element for this element
        """
        return self

    def gettype(self):
        """
        return xsd-type for this type.
        """
        if self.ref:
            return self.ref.gettype()
        if self._xstype:
            return self._xstype.gettype()
        return self.content

    def getattributes(self):
        """
        return defined attributes for this type.
        """
        if self.ref:
            return self.ref.getattributes()
        if self._xstype:
            return self._xstype.getattributes()
        return self.content.getattributes()


XSAnnotation.allowed_content = {clark(NS_XMLSCHEMA, 'documentation'): XSDocumentation, clark(NS_XMLSCHEMA_99, 'documentation'): XSDocumentation}
XSAnnotation.ignore_content = [clark(NS_XMLSCHEMA, 'appinfo'),
 clark(NS_XMLSCHEMA_99, 'appinfo')]
XSSimpleType.allowed_content = {clark(NS_XMLSCHEMA, 'restriction'): XSRestriction, clark(NS_XMLSCHEMA_99, 'restriction'): XSRestriction}
XSSimpleType.ignored_content = [
 clark(NS_XMLSCHEMA, 'union'),
 clark(NS_XMLSCHEMA, 'list'),
 clark(NS_XMLSCHEMA_99, 'union'),
 clark(NS_XMLSCHEMA_99, 'list')]
XSRestriction.allowed_content = {clark(NS_XMLSCHEMA, 'sequence'): XSSequence, clark(NS_XMLSCHEMA_99, 'sequence'): XSSequence, 
   clark(NS_XMLSCHEMA, 'all'): XSAll, 
   clark(NS_XMLSCHEMA_99, 'all'): XSAll, 
   clark(NS_XMLSCHEMA, 'choice'): XSChoice, 
   clark(NS_XMLSCHEMA_99, 'choice'): XSChoice}
XSRestriction.ignored_content = [ clark(NS_XMLSCHEMA, x) for x in [
 'enumeration', 'pattern',
 'whiteSpace', 'minLength', 'simpleType',
 'fractionDigits', 'maxInclusive',
 'minInclusive']
                                ] + [ clark(NS_XMLSCHEMA_99, x) for x in [
 'enumeration', 'pattern',
 'whiteSpace', 'minLength', 'simpleType',
 'fractionDigits', 'maxInclusive', 'minInclusive']
                                    ]
XSExtension.allowed_content = []
XSExtension.ignored_content = [ clark(NS_XMLSCHEMA, x) for x in [
 'sequence', 'attribute', 'attributeGroup', 'group',
 'choice', 'anyAttribute']
                              ] + [ clark(NS_XMLSCHEMA_99, x) for x in [
 'sequence', 'attribute', 'attributeGroup', 'group',
 'choice', 'anyAttribute']
                                  ]
XSChoice.allowed_content = {clark(NS_XMLSCHEMA, 'element'): XSElement, clark(NS_XMLSCHEMA, 'choice'): XSChoice, 
   clark(NS_XMLSCHEMA, 'sequence'): XSSequence, 
   clark(NS_XMLSCHEMA_99, 'element'): XSElement, 
   clark(NS_XMLSCHEMA_99, 'choice'): XSChoice, 
   clark(NS_XMLSCHEMA_99, 'sequence'): XSSequence}
XSChoice.ignored_content = [clark(NS_XMLSCHEMA, 'group'),
 clark(NS_XMLSCHEMA_99, 'group')]
XSSequence.allowed_content = {clark(NS_XMLSCHEMA, 'element'): XSElement, clark(NS_XMLSCHEMA_99, 'element'): XSElement, 
   clark(NS_XMLSCHEMA, 'choice'): XSChoice, 
   clark(NS_XMLSCHEMA_99, 'choice'): XSChoice, 
   clark(NS_XMLSCHEMA, 'sequence'): XSSequence, 
   clark(NS_XMLSCHEMA_99, 'sequence'): XSSequence, 
   clark(NS_XMLSCHEMA, 'any'): XSAny, 
   clark(NS_XMLSCHEMA_99, 'any'): XSAny}
XSSequence.ignored_content = [clark(NS_XMLSCHEMA, 'group'),
 clark(NS_XMLSCHEMA_99, 'group')]
XSComplexType.allowed_content = {clark(NS_XMLSCHEMA, 'sequence'): XSSequence, clark(NS_XMLSCHEMA_99, 'sequence'): XSSequence, 
   clark(NS_XMLSCHEMA, 'all'): XSAll, 
   clark(NS_XMLSCHEMA_99, 'all'): XSAll, 
   clark(NS_XMLSCHEMA, 'choice'): XSChoice, 
   clark(NS_XMLSCHEMA_99, 'choice'): XSChoice, 
   clark(NS_XMLSCHEMA, 'simpleContent'): XSSimpleContent, 
   clark(NS_XMLSCHEMA_99, 'simpleContent'): XSSimpleContent, 
   clark(NS_XMLSCHEMA, 'complexContent'): XSComplexContent, 
   clark(NS_XMLSCHEMA_99, 'complexContent'): XSComplexContent}
XSComplexType.ignored_content = [
 clark(NS_XMLSCHEMA, 'attributeGroup'),
 clark(NS_XMLSCHEMA_99, 'attributeGroup')]