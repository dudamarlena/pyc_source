# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/droopescan/dscan/common/testutils.py
# Compiled at: 2019-06-14 01:34:00
# Size of source mod 2**32: 1223 bytes
from inspect import getmembers, isfunction, ismethod
from lxml import etree
import dscan, inspect

def decallmethods(decorator, prefix='test_'):
    """
    Decorates all methods in class which begin with prefix test_ to prevent
    accidental external HTTP requests.
    """

    def dectheclass(cls):
        for name, m in getmembers(cls, predicate=lambda x: isfunction(x) or ismethod(x)):
            if name.startswith(prefix):
                setattr(cls, name, decorator(m))

        return cls

    return dectheclass


def _validate(xmlparser, xmlfilename):
    """
    Raises an exception if the XML file doesn't validate.
    """
    with open(xmlfilename, 'r') as (f):
        etree.fromstring(f.read(), xmlparser)


def xml_validate(xml_file, xsd_file):
    with open(xsd_file, 'r') as (f):
        schema_root = etree.XML(f.read())
    schema = etree.XMLSchema(schema_root)
    xmlparser = etree.XMLParser(schema=schema)
    return _validate(xmlparser, xml_file)


class MockBuffer:
    string = ''

    def write(self, data):
        self.string += data

    def flush(self):
        pass

    def __repr__(self):
        return self.string

    def get(self):
        return self.string