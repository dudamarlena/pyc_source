# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZSI/__init__.py
# Compiled at: 2006-10-25 20:33:30
"""ZSI:  Zolera Soap Infrastructure.

Copyright 2001, Zolera Systems, Inc.  All Rights Reserved.
"""
_copyright = 'ZSI:  Zolera Soap Infrastructure.\n\nCopyright 2001, Zolera Systems, Inc.  All Rights Reserved.\nCopyright 2002-2003, Rich Salz. All Rights Reserved.\n\nPermission is hereby granted, free of charge, to any person obtaining a\ncopy of this software and associated documentation files (the "Software"),\nto deal in the Software without restriction, including without limitation\nthe rights to use, copy, modify, merge, publish, distribute, and/or\nsell copies of the Software, and to permit persons to whom the Software\nis furnished to do so, provided that the above copyright notice(s) and\nthis permission notice appear in all copies of the Software and that\nboth the above copyright notice(s) and this permission notice appear in\nsupporting documentation.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,\nEXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF\nMERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT\nOF THIRD PARTY RIGHTS. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR HOLDERS\nINCLUDED IN THIS NOTICE BE LIABLE FOR ANY CLAIM, OR ANY SPECIAL INDIRECT\nOR CONSEQUENTIAL DAMAGES, OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS\nOF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE\nOR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE\nOR PERFORMANCE OF THIS SOFTWARE.\n\nExcept as contained in this notice, the name of a copyright holder\nshall not be used in advertising or otherwise to promote the sale, use\nor other dealings in this Software without prior written authorization\nof the copyright holder.\n\n\nPortions are also:\n\nCopyright (c) 2003, The Regents of the University of California,\nthrough Lawrence Berkeley National Laboratory (subject to receipt of\nany required approvals from the U.S. Dept. of Energy). All rights\nreserved. Redistribution and use in source and binary forms, with or\nwithout modification, are permitted provided that the following\nconditions are met:\n\n(1) Redistributions of source code must retain the above copyright\nnotice, this list of conditions and the following disclaimer.\n(2) Redistributions in binary form must reproduce the above copyright\nnotice, this list of conditions and the following disclaimer in the\ndocumentation and/or other materials provided with the distribution.\n(3) Neither the name of the University of California, Lawrence Berkeley\nNational Laboratory, U.S. Dept. of Energy nor the names of its contributors\nmay be used to endorse or promote products derived from this software without\nspecific prior written permission.\n\nTHIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS\n"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED\nTO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR\nPURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS\nBE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR\nCONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE\nGOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)\nHOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT\nLIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY\nOUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF\nSUCH DAMAGE.\n\nYou are under no obligation whatsoever to provide any bug fixes,\npatches, or upgrades to the features, functionality or performance of\nthe source code ("Enhancements") to anyone; however, if you choose to\nmake your Enhancements available either publicly, or directly to\nLawrence Berkeley National Laboratory, without imposing a separate\nwritten license agreement for such Enhancements, then you hereby grant\nthe following license: a non-exclusive, royalty-free perpetual license\nto install, use, modify, prepare derivative works, incorporate into\nother computer software, distribute, and sublicense such Enhancements\nor derivative works thereof, in binary and source code form.\n\n\nFor wstools also:\n\nZope Public License (ZPL) Version 2.0\n-----------------------------------------------\n\nThis software is Copyright (c) Zope Corporation (tm) and\nContributors. All rights reserved.\n\nThis license has been certified as open source. It has also\nbeen designated as GPL compatible by the Free Software\nFoundation (FSF).\n\nRedistribution and use in source and binary forms, with or\nwithout modification, are permitted provided that the\nfollowing conditions are met:\n\n1. Redistributions in source code must retain the above\n   copyright notice, this list of conditions, and the following\n   disclaimer.\n\n2. Redistributions in binary form must reproduce the above\n   copyright notice, this list of conditions, and the following\n   disclaimer in the documentation and/or other materials\n   provided with the distribution.\n\n3. The name Zope Corporation (tm) must not be used to\n   endorse or promote products derived from this software\n   without prior written permission from Zope Corporation.\n\n4. The right to distribute this software or to use it for\n   any purpose does not give you the right to use Servicemarks\n   (sm) or Trademarks (tm) of Zope Corporation. Use of them is\n   covered in a separate agreement (see\n   http://www.zope.com/Marks).\n\n5. If any files are modified, you must cause the modified\n   files to carry prominent notices stating that you changed\n   the files and the date of any change.\n\nDisclaimer\n\n  THIS SOFTWARE IS PROVIDED BY ZOPE CORPORATION ``AS IS\'\'\n  AND ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT\n  NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY\n  AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN\n  NO EVENT SHALL ZOPE CORPORATION OR ITS CONTRIBUTORS BE\n  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,\n  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT\n  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;\n  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)\n  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN\n  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE\n  OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS\n  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH\n  DAMAGE.\n\n\nThis software consists of contributions made by Zope\nCorporation and many individuals on behalf of Zope\nCorporation.  Specific attributions are listed in the\naccompanying credits file.\n'
from xml.dom import Node as _Node
import types as _types
from ZSI.wstools.Namespaces import ZSI_SCHEMA_URI
_inttypes = [
 _types.IntType, _types.LongType]
_floattypes = [_types.FloatType]
_seqtypes = [_types.TupleType, _types.ListType]
_stringtypes = [_types.StringType, _types.UnicodeType]
_attrs = lambda E: E.attributes and E.attributes.values() or []
_children = lambda E: E.childNodes or []
_child_elements = lambda E: [ n for n in E.childNodes or [] if n.nodeType == _Node.ELEMENT_NODE
]
from ZSI.wstools.Namespaces import SOAP as _SOAP, SCHEMA as _SCHEMA, XMLNS as _XMLNS
_find_arraytype = lambda E: E.getAttributeNS(_SOAP.ENC, 'arrayType')
_find_encstyle = lambda E: E.getAttributeNS(_SOAP.ENV, 'encodingStyle')
try:
    from xml.dom import EMPTY_NAMESPACE
    _empty_nsuri_list = [
     EMPTY_NAMESPACE]
except:
    _empty_nsuri_list = [None, '']

def _find_attr(E, attr):
    for nsuri in _empty_nsuri_list:
        try:
            v = E.getAttributeNS(nsuri, attr)
            if v:
                return v
        except:
            pass

    return


def _find_attrNS(E, namespaceURI, localName):
    """namespaceURI
       localName
    """
    try:
        v = E.getAttributeNS(namespaceURI, localName)
        if v:
            return v
    except:
        pass

    return


def _find_attrNodeNS(E, namespaceURI, localName):
    """Must grab the attribute Node to distinquish between
    an unspecified attribute(None) and one set to empty string("").
       namespaceURI
       localName
    """
    attr = E.getAttributeNodeNS(namespaceURI, localName)
    if attr is None:
        return
    else:
        try:
            return attr.value
        except:
            pass

        return E.getAttributeNS(namespaceURI, localName)


_find_href = lambda E: _find_attr(E, 'href')
_find_xsi_attr = lambda E, attr: E.getAttributeNS(_SCHEMA.XSI3, attr) or E.getAttributeNS(_SCHEMA.XSI1, attr) or E.getAttributeNS(_SCHEMA.XSI2, attr)
_find_type = lambda E: _find_xsi_attr(E, 'type')
_find_xmlns_prefix = lambda E, attr: E.getAttributeNS(_XMLNS.BASE, attr)
_find_default_namespace = lambda E: E.getAttributeNS(_XMLNS.BASE, None)
_get_element_nsuri_name = lambda E: (
 E.namespaceURI, E.localName)
_is_element = lambda E: E.nodeType == _Node.ELEMENT_NODE

def _resolve_prefix(celt, prefix):
    """resolve prefix to a namespaceURI.  If None or 
    empty str, return default namespace or None.

    Parameters:
      celt -- element node
      prefix -- xmlns:prefix, or empty str or None
    """
    namespace = None
    while _is_element(celt):
        if prefix:
            namespaceURI = _find_xmlns_prefix(celt, prefix)
        else:
            namespaceURI = _find_default_namespace(celt)
        if namespaceURI:
            break
        celt = celt.parentNode

    if prefix:
        raise EvaluateException, 'cant resolve xmlns:%s' % prefix
    return namespaceURI


def _valid_encoding(elt):
    """Does this node have a valid encoding?
    """
    enc = _find_encstyle(elt)
    if not enc or enc == _SOAP.ENC:
        return 1
    for e in enc.split():
        if e.startswith(_SOAP.ENC):
            return 1

    return 0


def _backtrace(elt, dom):
    """Return a "backtrace" from the given element to the DOM root,
    in XPath syntax.
    """
    s = ''
    while elt != dom:
        name, parent = elt.nodeName, elt.parentNode
        if parent is None:
            break
        matches = [ c for c in _child_elements(parent) if c.nodeName == name
                  ]
        if len(matches) == 1:
            s = '/' + name + s
        else:
            i = matches.index(elt) + 1
            s = '/%s[%d]' % (name, i) + s
        elt = parent

    return s


def _get_idstr(pyobj):
    """Python 2.3.x generates a FutureWarning for negative IDs, so
    we use a different prefix character to ensure uniqueness, and
    call abs() to avoid the warning."""
    x = id(pyobj)
    if x < 0:
        return 'x%x' % abs(x)
    return 'o%x' % x


def _get_postvalue_from_absoluteURI(url):
    """Bug [ 1513000 ] POST Request-URI not limited to "abs_path"
    Request-URI = "*" | absoluteURI | abs_path | authority
    
    Not a complete solution, but it seems to work with all known
    implementations.  ValueError thrown if bad uri.
    """
    cache = _get_postvalue_from_absoluteURI.cache
    path = cache.get(url, '')
    if not path:
        scheme, authpath = url.split('://')
        s = authpath.split('/', 1)
        if len(s) == 2:
            path = '/%s' % s[1]
        if len(cache) > _get_postvalue_from_absoluteURI.MAXLEN:
            cache.clear()
        cache[url] = path
    return path


_get_postvalue_from_absoluteURI.cache = {}
_get_postvalue_from_absoluteURI.MAXLEN = 20

class ZSIException(Exception):
    """Base class for all ZSI exceptions.
    """
    pass


class ParseException(ZSIException):
    """Exception raised during parsing.
    """

    def __init__(self, str, inheader, elt=None, dom=None):
        Exception.__init__(self)
        self.str, self.inheader, self.trace = str, inheader, None
        if elt and dom:
            self.trace = _backtrace(elt, dom)
        return

    def __str__(self):
        if self.trace:
            return self.str + '\n[Element trace: ' + self.trace + ']'
        return self.str

    def __repr__(self):
        return '<%s.ParseException %s>' % (__name__, _get_idstr(self))


class EvaluateException(ZSIException):
    """Exception raised during data evaluation (serialization).
    """

    def __init__(self, str, trace=None):
        Exception.__init__(self)
        self.str, self.trace = str, trace

    def __str__(self):
        if self.trace:
            return self.str + '\n[Element trace: ' + self.trace + ']'
        return self.str

    def __repr__(self):
        return '<%s.EvaluateException %s>' % (__name__, _get_idstr(self))


class FaultException(ZSIException):
    """Exception raised when a fault is received.
    """

    def __init__(self, fault):
        self.fault = fault

    def __str__(self):
        return str(self.fault)

    def __repr__(self):
        return '<%s.FaultException %s>' % (__name__, _get_idstr(self))


class WSActionException(ZSIException):
    """Exception raised when WS-Address Action Header is incorrectly
    specified when received by client or server.
    """
    pass


import version

def Version():
    return version.Version


from writer import SoapWriter
from parse import ParsedSoap
from fault import Fault, FaultFromActor, FaultFromException, FaultFromFaultMessage, FaultFromNotUnderstood, FaultFromZSIException
import TC
TC.RegisterType(TC.String, minOccurs=0, nillable=False)
TC.RegisterType(TC.URI, minOccurs=0, nillable=False)
TC.RegisterType(TC.Base64String, minOccurs=0, nillable=False)
TC.RegisterType(TC.HexBinaryString, minOccurs=0, nillable=False)
for pyclass in (TC.IunsignedByte, TC.IunsignedShort, TC.IunsignedInt, TC.IunsignedLong,
 TC.Ibyte, TC.Ishort, TC.Iint, TC.Ilong, TC.InegativeInteger,
 TC.InonPositiveInteger, TC.InonNegativeInteger, TC.IpositiveInteger,
 TC.Iinteger, TC.FPfloat, TC.FPdouble):
    TC.RegisterType(pyclass, minOccurs=0, nillable=False)

TC.RegisterType(TC.Boolean, minOccurs=0, nillable=False)
TC.RegisterType(TC.Duration, minOccurs=0, nillable=False)
TC.RegisterType(TC.gDateTime, minOccurs=0, nillable=False)
TC.RegisterType(TC.gDate, minOccurs=0, nillable=False)
TC.RegisterType(TC.gYearMonth, minOccurs=0, nillable=False)
TC.RegisterType(TC.gYear, minOccurs=0, nillable=False)
TC.RegisterType(TC.gMonthDay, minOccurs=0, nillable=False)
TC.RegisterType(TC.gDay, minOccurs=0, nillable=False)
TC.RegisterType(TC.gTime, minOccurs=0, nillable=False)
TC.RegisterType(TC.Apache.Map, minOccurs=0, nillable=False)
import schema
for i in [int, float, str, tuple, list, unicode]:
    schema._GetPyobjWrapper.RegisterBuiltin(i)

schema.RegisterAnyElement()
if __name__ == '__main__':
    print _copyright