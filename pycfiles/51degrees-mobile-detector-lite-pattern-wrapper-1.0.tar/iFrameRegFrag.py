# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\ThirdParty\Xvif\iFrameRegFrag.py
# Compiled at: 2005-09-19 16:44:10
from xml.dom import XMLNS_NAMESPACE
from Ft.Xml.Domlette import implementation

def transform(self, node):
    import FragmentFilter
    from Ft.Xml.Sax import CreateParser, DomBuilder
    rules = FragmentFilter.RulesLoader()
    parser = CreateParser()
    parser.setContentHandler(rules)
    parser.setFeature(xml.sax.handler.property_dom_node, self.applyElt.dom)
    parser.parse(None)
    fragFilter = FragmentFilter.FragmentFilter(rules)
    parser.setContentHandler(fragFilter)
    parser.setFeature(xml.sax.handler.property_dom_node, node)
    parser.setContentHandler(fragFilter)
    builder = DomBuilder()
    fragFilter.setContentHandler(builder)
    try:
        parser.parse(None)
    except:
        return None

    return builder.getDocument().documentElement
    return