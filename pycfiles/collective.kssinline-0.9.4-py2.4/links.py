# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/kssinline/examples/utilities/links.py
# Compiled at: 2008-10-08 12:38:32
from zope.interface import implements
from collective.kssinline.browser.interfaces import ILinkableItem

class CollectivePortletExplore(object):
    """
    A link utility which handles nodes that are provided 
    by collective.portlet.explore

    Experimental! collective.portlet.portlet needs a small 
    patch to recurse.pt for this to take effect.

    I still have to discuss with the developers.

    Basically, put the following next to the link anchor in
    recurse.pt:

    <tal:def define="dummy python:request.set('item', node)">
      <div tal:replace="structure provider:content.links" />
    </tal:def>
    """
    __module__ = __name__
    implements(ILinkableItem)

    def obj(self, item):
        return item['item'].getObject()

    def uid(self, item):
        return item['item'].UID

    def url(self, item):
        return item['item'].getURL()