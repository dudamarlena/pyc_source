# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/suds/soaparray.py
# Compiled at: 2014-02-26 03:37:27
"""
The I{soaparray} module provides XSD extensions for handling
soap (section 5) encoded arrays.
"""
from suds.xsd.sxbasic import Factory as SXFactory
from suds.xsd.sxbasic import Attribute as SXAttribute

class Attribute(SXAttribute):
    """
    Represents an XSD <attribute/> that handles special
    attributes that are extensions for WSDLs.
    @ivar aty: Array type information.
    @type aty: The value of wsdl:arrayType.
    """

    def __init__(self, schema, root, aty):
        """
        @param aty: Array type information.
        @type aty: The value of wsdl:arrayType.
        """
        SXAttribute.__init__(self, schema, root)
        if aty.endswith('[]'):
            self.aty = aty[:-2]
        else:
            self.aty = aty

    def autoqualified(self):
        aqs = SXAttribute.autoqualified(self)
        aqs.append('aty')
        return aqs

    def description(self):
        d = SXAttribute.description(self)
        d = d + ('aty', )
        return d


def __fn(x, y):
    ns = (None, 'http://schemas.xmlsoap.org/wsdl/')
    aty = y.get('arrayType', ns=ns)
    if aty is None:
        return SXAttribute(x, y)
    else:
        return Attribute(x, y, aty)
        return


SXFactory.maptag('attribute', __fn)