# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/medialog/boardfile/__init__.py
# Compiled at: 2011-10-07 04:21:09
"""Main product initializer
"""
from zope.i18nmessageid import MessageFactory
from medialog.boardfile import config
from Products.Archetypes import atapi
from Products.CMFCore import utils
from Products.CMFCore.permissions import setDefaultRoles
boardfileMessageFactory = MessageFactory('medialog.boardfile')

def initialize(context):
    """Initializer called when used as a Zope 2 product.

    This is referenced from configure.zcml. Regstrations as a "Zope 2 product"
    is necessary for GenericSetup profiles to work, for example.

    Here, we call the Archetypes machinery to register our content types
    with Zope and the CMF.
    """
    content_types, constructors, ftis = atapi.process_types(atapi.listTypes(config.PROJECTNAME), config.PROJECTNAME)
    for atype, constructor in zip(content_types, constructors):
        utils.ContentInit('%s: %s' % (config.PROJECTNAME, atype.portal_type), content_types=(
         atype,), permission=config.ADD_PERMISSIONS[atype.portal_type], extra_constructors=(
         constructor,)).initialize(context)