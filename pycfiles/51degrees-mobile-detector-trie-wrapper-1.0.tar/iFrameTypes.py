# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\ThirdParty\Xvif\iFrameTypes.py
# Compiled at: 2005-09-19 16:44:10
import xml.dom, rng

def transform(self, node):
    if node.nodeType == xml.dom.Node.TEXT_NODE:
        (library, type) = self.apply.split('#')
        rng._Callback.set_datatypeLibrary(self, None, library)
        module = __import__(rng.RngParser.typeLibraries[self.library])
        cl = module.__dict__[(type + 'Type')]
        try:
            value = cl(node.nodeValue)
        except ValueError:
            return None
        else:
            return node.ownerDocument.createTextNode(value.__str__())
    else:
        return None
    return


def validate(self, node):
    res = self.transform(node)
    if res == None:
        return None
    else:
        return node
    return