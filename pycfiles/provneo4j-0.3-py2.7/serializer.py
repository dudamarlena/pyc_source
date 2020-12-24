# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/provneo4j/connectors/serializer.py
# Compiled at: 2016-10-26 07:49:18
from prov.constants import *
from prov.model import QualifiedName, Identifier, Literal
from datetime import datetime
LITERAL_XSDTYPE_MAP = {float: 'xsd:double', 
   int: 'xsd:int'}
if six.integer_types[(-1)] not in LITERAL_XSDTYPE_MAP:
    LITERAL_XSDTYPE_MAP[six.integer_types[(-1)]] = 'xsd:long'

class Serializer:

    @staticmethod
    def encode_string_value(value):
        if type(value) is unicode:
            return value.encode('utf8')
        if isinstance(value, Literal):
            return value.value
        if type(value) is bool:
            return value
        return str(value)

    @staticmethod
    def valid_qualified_name(bundle, value):
        if value is None:
            return
        else:
            qualified_name = bundle.valid_qualified_name(value)
            return qualified_name

    @staticmethod
    def literal_json_representation(literal):
        value, datatype, langtag = literal.value, literal.datatype, literal.langtag
        if langtag:
            return {'lang': langtag}
        else:
            return {'type': six.text_type(datatype)}

    @staticmethod
    def encode_json_representation(value):
        if isinstance(value, Literal):
            return Serializer.literal_json_representation(value)
        else:
            if isinstance(value, datetime):
                return {'type': 'xsd:dateTime'}
            else:
                if isinstance(value, QualifiedName):
                    return {'type': PROV_QUALIFIEDNAME._str}
                if isinstance(value, Identifier):
                    return {'type': 'xsd:anyURI'}
                if type(value) in LITERAL_XSDTYPE_MAP:
                    return {'type': LITERAL_XSDTYPE_MAP[type(value)]}
                return

            return

    def __init__(self):
        pass