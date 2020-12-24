# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/rsl/xsd/urtype.py
# Compiled at: 2009-01-12 07:29:42
"""
This module provides an implementation of XSD-urtypes.
"""
from rsl.xsd.deserialtypes import Unicode

class AnyType(object):
    """
    This is the base type for all schema types.
    """

    def __init__(self, name, xsd):
        """
        init type. needs local name and xsd where it is defined in.
        """
        self.name = name
        self.xsd = xsd

    def getsubelementnames(self, visited=None):
        """
        return the names of subelements if any.
        
        visited is used to handle recursive structures.
        """
        return []

    def gettypename(self):
        """
        return type name tuple (nsurl, name)
        """
        return (
         self.xsd.targetnamespace, self.name)


class AnySimpleType(AnyType):
    """
    This is the base type for all simple types.
    """

    def getelement(self):
        """
        return xsd-element instance.
        
        TODO: should be none here shouldn't it?
        """
        return self

    def encode(self, data):
        """
        it is used to convert the given data to a string
        """
        return unicode(data)

    def decode(self, data):
        """
        it is used to convert the given data to a string
        """
        return Unicode(data)

    def getsubelementnames(self, visited=None):
        """
        return names of subelements.
        a simple type can not have sub elements.
        
        visited is used to handle recursive structures.
        """
        return []

    def gettype(self):
        """
        return the xsd type instance.
        """
        return self

    def getattributes(self):
        """
        return defined xsd attribute instances.
        a simple type can not have attributes.
        """
        return