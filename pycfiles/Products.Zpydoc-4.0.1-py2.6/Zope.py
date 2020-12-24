# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/Zpydoc/renderers/Zope.py
# Compiled at: 2011-09-28 02:31:46
"""$id$"""
import Globals, os, logging
from Products.Zpydoc.renderers.Python import Python
from Products.Zpydoc.inspectors.ZopeInfo import PackageInfo
from OFS.DTMLMethod import DTMLMethod
from Products.PageTemplates.ZopePageTemplate import ZopePageTemplate
LOG = logging.getLogger('ZpyDoc.renderers.Zope')

class Zope(Python):
    """
    Do custom processing for Zope derived objects
    """
    meta_type = 'ZopeRenderer'
    id = 'Zope'
    title = 'Customisable Zope'
    _properties = ({'id': 'show_private', 'type': 'boolean', 'mode': 'w'},)

    def __init__(self):
        self.show_private = False
        thisdir = os.path.dirname(__file__)
        self._setObject('index', ZopePageTemplate('index', open(os.path.join(thisdir, 'zpt', 'p_index.zpt')).read()))
        self._setObject('document', ZopePageTemplate('document', open(os.path.join(thisdir, 'zpt', 'z_document.zpt')).read()))
        self._setObject('standard_template.pt', ZopePageTemplate('standard_template.pt', open(os.path.join(thisdir, 'zpt', 'standard_template.zpt')).read()))
        self._setObject('stylesheet.css', DTMLMethod(open(os.path.join(thisdir, 'zpt', 'stylesheet.css')).read(), __name__='stylesheet.css'))

    def __call__(self, object, name):
        """ render page using Zope-specific info object """
        return self.document(self, self.REQUEST, PackageInfo(object, name))


Globals.InitializeClass(Zope)

def manage_addZopeRenderer(self, REQUEST=None):
    """ """
    try:
        self._setObject('Zope', Zope())
    except:
        raise

    if REQUEST:
        return self.manage_main(self, REQUEST)
    return self.Zope