# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jess/.local/conda/lib/python3.6/site-packages/earthchem/validation.py
# Compiled at: 2018-06-02 08:11:53
# Size of source mod 2**32: 5391 bytes
""" file:   validation.py
    author: Jess Robertson, CSIRO Minerals
    date:   May 2018

    description: Handles validation against EarthChem's API schema
"""
from lxml import etree, objectify
from lxml.etree import XMLSyntaxError
import requests, os, pkg_resources
SOAP_SCHEMA_URL = 'http://ecp.iedadata.org/soap_search_schema.xsd'
SOAP_SCHEMA = pkg_resources.resource_filename('earthchem.resources', 'soap_search_schema.xsd')
TYPE_MAPPING = {'{http://www.w3.org/2001/XMLSchema}complexType':'complex', 
 '{http://www.w3.org/2001/XMLSchema}simpleType':'simple', 
 '{http://www.w3.org/2001/XMLSchema}string':'string', 
 'xs:string':'string'}
_NS = {'xs': 'http://www.w3.org/2001/XMLSchema'}

def get_type(elem):
    """ Get the data type for an XML element
    """
    attrtype = elem.get('type')
    if attrtype is not None:
        return TYPE_MAPPING[attrtype]
    else:
        for child in elem.getchildren():
            try:
                return TYPE_MAPPING[child.tag]
            except KeyError:
                continue

        return TYPE_MAPPING['xs:string']


VALIDATOR_MAPPING = {}

def complex_validator(elem):
    """ Construct a validator for an xs:complexType
    """
    attributes = elem.xpath('./xs:complexType/xs:attribute', namespaces=_NS)
    validators = {attr.get('name'):VALIDATOR_MAPPING[get_type(attr)](attr) for attr in attributes}
    name = elem.get('name')

    def _validator(obj):
        if type(obj) != dict:
            raise ValueError('I expected a dict for parameter {} - got a {} instead ({})'.format(name, type(obj), obj))
        for key, value in obj.items():
            try:
                vd = validators[key]
            except KeyError:
                raise KeyError('Unknown key {} - valid values are {}'.format(key, list(validators.keys())))

        return True

    return _validator


def simple_validator(elem):
    """ Construct a validator for an xs:simpleType - these are normally values
        with particular restrictions
    """
    name = elem.get('name')

    def _validator(obj):
        if type(obj) != dict:
            raise ValueError('I expected a str for parameter {} - got a {} instead ({})'.format(name, type(obj), obj))
        return True

    return _validator


def string_validator(elem):
    """ String validator for objects - validates any string it's passed
    """
    name = elem.get('name')

    def _validator(obj):
        if type(obj) != str:
            raise ValueError('I expected a string for parameter {} - got a {} instead ({})'.format(name, type(obj), obj))
        return True

    return _validator


VALIDATOR_MAPPING = {'string':string_validator, 
 'complex':complex_validator, 
 'simple':simple_validator}

class ElementValidator(dict):
    __doc__ = ' Class to generate a query validator for each \n        part of the query\n        \n        This generates fairly kludgy validators against \n        the SOAP search schema which will let us check that\n        a query is well-formed.\n        \n        Parameters:\n            name - the name of the query element.\n                Should be the same as in the XML soap\n                search schema.\n    '

    def __init__(self, name):
        self.name = name.lower()
        self.xmlname = name
        self._tree = None
        query = "//xs:element[@name='{}']".format(self.xmlname)
        self.root = self.xpath(query)[0]
        self.dtype = get_type(self.root)
        self._validator = VALIDATOR_MAPPING[self.dtype](self.root)

    @property
    def tree(self):
        """Return the XML tree for the SOAP schema"""
        if self._tree is not None:
            return self._tree
        else:
            with open(SOAP_SCHEMA, 'r') as (src):
                self._tree = etree.parse(src)
            return self._tree

    def xpath(self, query):
        """Run an xpath query against our schema"""
        return self.tree.xpath(query, namespaces=_NS)

    def validate(self, obj):
        """ Validate a python object against the schema

            Parameters:
                obj - the object to validate 
        """
        return self._validator(obj)