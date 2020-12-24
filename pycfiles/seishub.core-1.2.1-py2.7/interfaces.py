# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\xmldb\interfaces.py
# Compiled at: 2010-12-23 17:42:44
from seishub.core.core import Interface, Attribute

class IResource(Interface):
    """
    Marker interface for the xmldb resources.
    """
    id = Attribute('Id of resource (Integer)')
    revision = Attribute('Revision of that resource')
    resource_id = Attribute('Unique id of related XML resource')
    package_id = Attribute('Package id, that resource belongs to')
    resourcetype_id = Attribute('Resourcetype id, that resource is type of')
    version_control = Attribute('Boolean, specifies if version control is' + 'enabled or disabled for related resource')


class IDocumentMeta(Interface):
    """
    Marker interface for xmldb document-specific metadata objects.
    """
    pass


class IXmlDocument(Interface):
    """
    Marker interface for xmldb XML documents.
    """

    def getXml_doc():
        """@return: xml document object"""
        pass

    def setXml_doc(xml_doc):
        """@param xml_doc: xml document object as provided by a xml parser,
        must implement seishub.util.xml.IXmlDoc"""
        pass

    def getResourceType(self):
        """the resource type is determined by the root node of the underlying 
        xml document
        @return: resource type (string)"""
        pass

    def setData(xml_data):
        """@param xml_data: raw xml data
        @type xml_data: string"""
        pass

    def getData(self):
        """@return: xml data (string)"""
        pass


class IIndexBase(Interface):
    """
    Base class for index interfaces
    """

    def init(value_path=None, key_path=None, type='text'):
        pass

    def getKey_path():
        """@return: key path"""
        pass

    def getValue_path():
        """@return: value path"""
        pass

    def getType():
        """@return: data type of the index key"""
        pass

    def getValues():
        """@return: values of this index"""
        pass


class IXmlIndex(IIndexBase):
    """
    Marker interface for xmldb xml indexes.
    
    An XmlIndex is used in order to index data stored inside a XmlResource's
    XML structure
    """

    def eval(xml_resource):
        """Evaluate this index on a given XmlResource
        @param xml_resource: xmldb.xmlresource.XmlResource object
        @return: list with key, value pairs on success, None else"""
        pass


class IXPathQuery(Interface):
    """
    Marker interface for xmldb xpath query objects.
    """

    def init(query, order_by=None, limit=None):
        """@param param: XPath query
        @type query: string
        @param order_by: list of order by clauses of the form: 
        [["/somenode/someelement/@someattribute" (, "ASC"|"DESC")], 
        ...]
        @type order_by: python list
        @param limit: maximum number of results
        @type limit: int"""
        pass

    def getPredicates():
        """Get parsed predicates
        @return: parsed predicate expression
        @rtype: L{seishub.xmldb.xpath.PredicateExpression}"""
        pass

    def getValue_path():
        """Get value path
        @return: value path this query corresponds to
        @rtype: string"""
        pass

    def has_predicates():
        """@return: True if query has predicates
        @rtype: True | False"""
        pass

    def getOrder_by():
        """@return: List of parsed order by clauses
        @rtype: python list"""
        pass

    def getLimit():
        """@return: Result set limit (maximum number of results)
        @rtype: integer"""
        pass