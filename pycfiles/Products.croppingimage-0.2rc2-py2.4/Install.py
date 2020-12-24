# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/croppingimage/Extensions/Install.py
# Compiled at: 2008-07-23 09:49:01
from Products.CMFCore.utils import getToolByName
from cStringIO import StringIO
from Products.Archetypes.public import listTypes, process_types
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.croppingimage.config import PROJECTNAME, GLOBALS

def install(self, reinstall=False):
    out = StringIO()
    the_types = listTypes(PROJECTNAME)
    installTypes(self, out, the_types, PROJECTNAME)
    types_as_str = (', ').join([ each['portal_type'] for each in the_types ])
    out.write('Installed the portal_types: %s\n' % types_as_str)
    install_subskin(self, out, GLOBALS)
    print >> out, 'Successfully installed %s.\n' % PROJECTNAME
    return out.getvalue()