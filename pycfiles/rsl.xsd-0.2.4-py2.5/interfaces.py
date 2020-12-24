# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/rsl/xsd/interfaces.py
# Compiled at: 2009-01-12 07:29:42
from zope.interface import Interface

class IXMLSerializer(Interface):
    """
    defines the method signature to serialize python data types to xml 
    according to xsd definition.
    """

    def serialize(data, typename, schema, root):
        """
        data ... data structure to turn into xml
        typename ... the schema name to start with
        schema ... an ISchema which knows about all types
        root ... the root element to add the serialized data
        
        returns the newly create element.
        """
        pass


class IXMLDeserializer(Interface):
    """
    defines the method signature to serialize xml to python data structures
    with the help of schema definitions.
    """

    def deserialize(datatree, typename, schema):
        """
        datatree ... some data structure which can be deserialized according to typename
        typename ... the schema name to start with
        schema ... an ISchema which knows all types
        
        returns a data structure representing the parse xml
        """
        pass