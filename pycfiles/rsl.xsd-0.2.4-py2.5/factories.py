# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/rsl/xsd/factories.py
# Compiled at: 2009-08-27 18:51:21
from lxml import etree
from pkg_resources import resource_stream
from zope.interface import directlyProvides
from rsl.globalregistry import registerimpl
from rsl.interfaces import ISchemaFactory, ISchema
from rsl.xsd.namespace import NS_XMLSCHEMA, NS_XMLSCHEMA_99, NS_XML
from rsl.xsd.urtype import AnyType, AnySimpleType
from rsl.xsd.simpletype import FloatType, BooleanType, Base64Type, DateType
from rsl.xsd.simpletype import HexBinaryType, DateTimeType, IntegerType
from rsl.xsd.schema import XMLSchema
from rsl.xsd.interfaces import IXMLSerializer, IXMLDeserializer
from rsl.xsd.serializer import XMLElementSerializer, XMLTypeSerializer

def createXSD01Schema(schemaparent):
    xsd = XMLSchema(schemaparent)
    xsd.elementformdefault = 'qualified'
    xsd.targetnamespace = NS_XMLSCHEMA
    xsd.types['anyType'] = AnyType('anyType', xsd)
    xsd.types['anySimpleType'] = AnySimpleType('anySimpleType', xsd)
    xsd.types['string'] = AnySimpleType('string', xsd)
    xsd.types['decimal'] = FloatType('decimal', xsd)
    xsd.types['float'] = FloatType('float', xsd)
    xsd.types['double'] = FloatType('double', xsd)
    xsd.types['boolean'] = BooleanType('boolean', xsd)
    xsd.types['base64Binary'] = Base64Type('base64Binary', xsd)
    xsd.types['hexBinary'] = HexBinaryType('hexBinary', xsd)
    xsd.types['dateTime'] = DateTimeType('dateTime', xsd)
    xsd.types['date'] = DateType('date', xsd)
    xsd.types['timeInstant'] = xsd.types['dateTime']
    xsd.types['time'] = AnySimpleType('time', xsd)
    xsd.types['duration'] = AnySimpleType('duration', xsd)
    xsd.types['gYearMonth'] = AnySimpleType('gYearMonth', xsd)
    xsd.types['gYear'] = AnySimpleType('gYear', xsd)
    xsd.types['gMonthDay'] = AnySimpleType('gMonthDay', xsd)
    xsd.types['gDay'] = AnySimpleType('gDay', xsd)
    xsd.types['gMonth'] = AnySimpleType('gMonth', xsd)
    xsd.types['anyURI'] = AnySimpleType('anyURI', xsd)
    xsd.types['QName'] = AnySimpleType('QName', xsd)
    xsd.types['NOTATION'] = AnySimpleType('NOTATION', xsd)
    xsd.types['short'] = IntegerType('short', xsd)
    xsd.types['int'] = IntegerType('int', xsd)
    xsd.types['integer'] = IntegerType('integer', xsd)
    xsd.types['long'] = IntegerType('long', xsd)
    xsd.types['unsignedLong'] = IntegerType('unsignedLong', xsd)
    xsd.types['NMTOKEN'] = AnySimpleType('NMTOKEN', xsd)
    xsd.types['normalizedString'] = AnySimpleType('normalizedString', xsd)
    xsd.types['token'] = AnySimpleType('token', xsd)
    xsd.types['language'] = AnySimpleType('language', xsd)
    xsd.types['NMTOKENS'] = AnySimpleType('NMTOKENS', xsd)
    xsd.types['Name'] = AnySimpleType('Name', xsd)
    xsd.types['NCName'] = AnySimpleType('NCName', xsd)
    xsd.types['ID'] = AnySimpleType('ID', xsd)
    xsd.types['IDREF'] = AnySimpleType('IDREF', xsd)
    xsd.types['IDREFS'] = AnySimpleType('IDREFS', xsd)
    xsd.types['ENTITY'] = AnySimpleType('ENTITY', xsd)
    xsd.types['ENTITIES'] = AnySimpleType('ENTITIES', xsd)
    xsd.types['nonPositiveInteger'] = IntegerType('nonPositiveInteger', xsd)
    xsd.types['negativeInteger'] = IntegerType('negativeInteger', xsd)
    xsd.types['byte'] = IntegerType('byte', xsd)
    xsd.types['nonNegativeInteger'] = IntegerType('nonNegativeInteger', xsd)
    xsd.types['unsignedInt'] = IntegerType('unsignedInt', xsd)
    xsd.types['unsignedShort'] = IntegerType('unsignedShort', xsd)
    xsd.types['unsignedByte'] = IntegerType('unsignedByte', xsd)
    xsd.types['positiveInteger'] = IntegerType('positiveInteger', xsd)
    return xsd


directlyProvides(createXSD01Schema, ISchemaFactory)

def createXSD99Schema(schemaparent):
    xsd = XMLSchema(schemaparent)
    xsd.elementformdefault = 'qualified'
    xsd.targetnamespace = NS_XMLSCHEMA_99
    xsd.types['anyType'] = AnyType('anyType', xsd)
    xsd.types['anySimpleType'] = AnySimpleType('anySimpleType', xsd)
    xsd.types['string'] = AnySimpleType('string', xsd)
    xsd.types['decimal'] = FloatType('decimal', xsd)
    xsd.types['float'] = FloatType('float', xsd)
    xsd.types['double'] = FloatType('double', xsd)
    xsd.types['boolean'] = BooleanType('boolean', xsd)
    xsd.types['base64Binary'] = Base64Type('base64Binary', xsd)
    xsd.types['hexBinary'] = HexBinaryType('hexBinary', xsd)
    xsd.types['dateTime'] = DateTimeType('dateTime', xsd)
    xsd.types['date'] = DateType('date', xsd)
    xsd.types['timeInstant'] = xsd.types['dateTime']
    xsd.types['time'] = AnySimpleType('time', xsd)
    xsd.types['duration'] = AnySimpleType('duration', xsd)
    xsd.types['gYearMonth'] = AnySimpleType('gYearMonth', xsd)
    xsd.types['gYear'] = AnySimpleType('gYear', xsd)
    xsd.types['gMonthDay'] = AnySimpleType('gMonthDay', xsd)
    xsd.types['gDay'] = AnySimpleType('gDay', xsd)
    xsd.types['gMonth'] = AnySimpleType('gMonth', xsd)
    xsd.types['anyURI'] = AnySimpleType('anyURI', xsd)
    xsd.types['QName'] = AnySimpleType('QName', xsd)
    xsd.types['NOTATION'] = AnySimpleType('NOTATION', xsd)
    xsd.types['short'] = IntegerType('short', xsd)
    xsd.types['int'] = IntegerType('int', xsd)
    xsd.types['integer'] = IntegerType('integer', xsd)
    xsd.types['long'] = IntegerType('long', xsd)
    xsd.types['unsignedLong'] = IntegerType('unsignedLong', xsd)
    xsd.types['NMTOKEN'] = AnySimpleType('NMTOKEN', xsd)
    xsd.types['normalizedString'] = AnySimpleType('normalizedString', xsd)
    xsd.types['token'] = AnySimpleType('token', xsd)
    xsd.types['language'] = AnySimpleType('language', xsd)
    xsd.types['NMTOKENS'] = AnySimpleType('NMTOKENS', xsd)
    xsd.types['Name'] = AnySimpleType('Name', xsd)
    xsd.types['NCName'] = AnySimpleType('NCName', xsd)
    xsd.types['ID'] = AnySimpleType('ID', xsd)
    xsd.types['IDREF'] = AnySimpleType('IDREF', xsd)
    xsd.types['IDREFS'] = AnySimpleType('IDREFS', xsd)
    xsd.types['ENTITY'] = AnySimpleType('ENTITY', xsd)
    xsd.types['ENTITIES'] = AnySimpleType('ENTITIES', xsd)
    xsd.types['nonPositiveInteger'] = IntegerType('nonPositiveInteger', xsd)
    xsd.types['negativeInteger'] = IntegerType('negativeInteger', xsd)
    xsd.types['byte'] = IntegerType('byte', xsd)
    xsd.types['nonNegativeInteger'] = IntegerType('nonNegativeInteger', xsd)
    xsd.types['unsignedInt'] = IntegerType('unsignedInt', xsd)
    xsd.types['unsignedShort'] = IntegerType('unsignedShort', xsd)
    xsd.types['unsignedByte'] = IntegerType('unsignedByte', xsd)
    xsd.types['positiveInteger'] = IntegerType('positiveInteger', xsd)
    return xsd


directlyProvides(createXSD99Schema, ISchemaFactory)

def loadXMLSchema(schemaparent):
    xmlschema = resource_stream(__name__, 'xsds/xml.xsd')
    schema = XMLSchema(schemaparent)
    tree = etree.parse(xmlschema)
    schema.frometree(tree.getroot())
    return schema


directlyProvides(loadXMLSchema, ISchemaFactory)

def register():
    registerimpl(ISchema, NS_XMLSCHEMA, XMLSchema)
    registerimpl(ISchemaFactory, NS_XMLSCHEMA, createXSD01Schema)
    registerimpl(ISchemaFactory, NS_XMLSCHEMA_99, createXSD99Schema)
    registerimpl(ISchemaFactory, NS_XML, loadXMLSchema)
    registerimpl(IXMLSerializer, 'xml:type', XMLTypeSerializer)
    registerimpl(IXMLDeserializer, 'xml:type', XMLTypeSerializer)
    registerimpl(IXMLSerializer, 'xml:element', XMLElementSerializer)
    registerimpl(IXMLDeserializer, 'xml:element', XMLElementSerializer)