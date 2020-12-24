# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/cabig/cacore/ws/axis.py
# Compiled at: 2010-06-24 14:29:31
import sys
from ZSI import ParsedSoap
from xml.dom import minidom
debug = False
ns = 'http://webservice.system.nci.nih.gov'
nsa = 'ws'

class AxisReader:
    """ A drop-in replacement SOAP reader for ZSI which deals with some Axis 
        idiosyncrasies (meaning bugs!).
        
        Besides the XML mangling done here on the SOAP responses, the WSDL also 
        had to be modified in the following ways:
        
        1) Change extension base of HashMap to "anyType"
        2) Change namespace on all wsdl:output bodies to match the wsdl:input.
        3) Add namespace ws = http://webservice.system.nci.nih.gov
        4) Change namespace of schema containing ArrayOf_xsd_anyType to ws
        5) Change all instances of impl:ArrayOf_xsd_anyType to ws:ArrayOf_xsd_anyType
    """

    def fromString(self, input):
        dom = minidom.parseString(input, None)
        env = dom.childNodes[0]
        body = env.childNodes[0]
        if body.childNodes[0].nodeName == 'soapenv:Fault':
            return dom
        else:
            response = body.childNodes[0]
            result = response.childNodes[0]
            if not result.childNodes:
                return dom
            if result.childNodes[0].nodeType == result.TEXT_NODE:
                return dom
            a = dom.createAttributeNS('http://www.w3.org/2000/xmlns/', 'xmlns:' + nsa)
            a.value = ns
            env.setAttributeNodeNS(a)
            if result.childNodes[0].nodeName != result.nodeName:
                result.namespaceURI = None
                fix_member_types(result, dom)
                return dom
            fix_array(result, dom)
            if debug:
                print dom.toprettyxml()
            return dom

    def __call__(self, args):
        """ If this happens, we will need to implement whatever method is 
            needed. Until then... 
        """
        from exceptions import NotImplementedError
        raise NotImplementedError


def fix_array(node, dom):
    """ Fix bug in Axis which causes item nodes to be incorrectly named
        with the parent node name.
    """
    for item in node.childNodes:
        if item.nodeType == item.ELEMENT_NODE:
            dom.renameNode(item, None, 'item')
            item.localName = 'item'
            fix_member_types(item, dom)

    return


def fix_member_types(item, dom):
    """ For associations, replace soapenc:Array with generated List type
    """
    for member in item.childNodes:
        if not member:
            continue
        if member.childNodes and member.childNodes[0].localName == member.localName:
            fix_array(member, dom)
        if member.attributes:
            attr = member.attributes['xsi:type']
            if attr.value == 'soapenc:Array':
                attr.value = nsa + ':ArrayOf_xsd_anyType'


class ZSIDebugStreamReader:

    def write(self, c):
        if not c[0] == '<':
            return
        else:
            dom = minidom.parseString(c, None)
            xml = dom.toprettyxml()
            sys.stderr.write(xml.encode('UTF-8'))
            return


def parse(self, elt, ps):
    self.checkname(elt, ps)
    if self.nilled(elt, ps):
        return None
    else:
        elt = self.SimpleHREF(elt, ps, 'boolean')
        if not elt:
            return None
        v = self.simple_value(elt, ps).lower()
        return self.text_to_data(v, elt, ps)


from ZSI.TC import Boolean
Boolean.parse = parse