# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/unimr/red5/protectedvod/setuphandlers.py
# Compiled at: 2009-08-19 12:31:49
"""
    Run after Generic XML setup.
    
    Add new Kupu styles - can't use kupu.xml, because it is not additive,
    but replaces all styles & resource types once.
    
    Thanks to Twinapex Research <research@twinapex.com>
              http://www.twinapex.com

    cf. plone's plonelibrarytool.py
        kupu's  librarytool.py

"""
import string
from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
paragraph_styles = [
 'Red5 Stream|div|red5-stream']
table_classnames = []
resource_types = {'linkable': ('Red5Stream', )}

def importFinalSteps(context):
    """
    The last bit of code that runs as part of this setup profil
    """
    site = context.getSite()
    out = StringIO()
    print >> out, 'Installing additional Kupu styles'
    kupu = site.kupu_library_tool
    for s in paragraph_styles:
        s = s.strip()
        if s not in kupu.paragraph_styles:
            kupu.paragraph_styles.append(s)
            print >> out, 'Installed style:' + s

    for s in table_classnames:
        s = s.strip()
        if s not in kupu.table_classnames:
            kupu.table_classnames.append(s)
            print >> out, 'Installed table class:' + s

    resource_type = 'linkable'
    old_types = kupu.getPortalTypesForResourceType(resource_type)
    new_types = []
    for t in resource_types[resource_type]:
        if t not in old_types:
            new_types.append(t)

    if new_types:
        kupu.addResourceType(resource_type, list(old_types) + new_types)
        print >> out, 'Installed %s resource type(s) %s' % (resource_type, new_types)
    return out.getvalue()