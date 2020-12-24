# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ice/control/controls/tree/xmlnice.py
# Compiled at: 2010-08-27 06:32:04
from zope.component import adapts, queryMultiAdapter
from zope.container.interfaces import IReadContainer
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.security.interfaces import Unauthorized
from zope.component.interfaces import ISite
from interfaces import IXML, XMLDOC
from xmlbase import XMLBase

class XMLReadContainer(XMLBase):
    adapts(IReadContainer, IBrowserRequest)

    def is_container(self):
        return True

    def size(self):
        return len(self.context)

    def length(self):
        return len(self.context)


class XMLSite(XMLReadContainer):
    adapts(ISite, IBrowserRequest)

    def size(self):
        return len(self.context) + 1

    def length(self):
        return len(self.context) + 1

    def children_xmldoc(self):
        try:
            rc = IReadContainer(self.context)
        except TypeError:
            return XMLDOC % ''
        except Unauthorized:
            return XMLDOC % ''

        specs = [ queryMultiAdapter((value, self.request), IXML) for value in rc.values()
                ]
        specs = filter(lambda x: x, specs)
        specs.sort(key=lambda x: x.sort_key())
        nodes = [ x.to_xml() for x in specs ]
        sm = self.context.getSiteManager()
        sm_spec = queryMultiAdapter((sm, self.request), IXML)
        nodes.append(sm_spec.to_xml())
        return XMLDOC % ('\n').join(nodes)