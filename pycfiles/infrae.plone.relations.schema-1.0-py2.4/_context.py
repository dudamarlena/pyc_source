# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/infrae/plone/relations/schema/_context.py
# Compiled at: 2008-06-11 03:54:55
__author__ = 'sylvain@infrae.com'
__format__ = 'plaintext'
__version__ = '$Id: _context.py 29099 2008-06-11 07:54:54Z sylvain $'
from zope.interface import implements
from interfaces import IPloneRelationContextFactory, IPloneRelationContext
from OFS.SimpleItem import SimpleItem
from zExceptions import BadRequest
from Products.Archetypes.Referenceable import Referenceable

class BasePloneRelationContext(Referenceable, SimpleItem):
    """Sample context object, stored as a SimpleItem. Referenceable
    from archetype is used by widget."""
    __module__ = __name__
    implements(IPloneRelationContext)
    meta_type = ''

    def __init__(self, id):
        super(BasePloneRelationContext, self).__init__()
        self.id = id


class BasePloneRelationContextFactory(object):
    """Sample factory, storing the context object in the src object,
    which have to be folderish."""
    __module__ = __name__
    implements(IPloneRelationContextFactory)

    def __init__(self, klass, schema):
        self.klass = klass
        self.schema = schema

    def __call__(self, src, tgt, data):
        name = tgt.UID()
        context = self.klass(name)
        try:
            src._setObject(name, context)
        except BadRequest:
            context = getattr(src, name)

        for (key, value) in data.iteritems():
            field = self.schema.get(key)
            field.validate(value)
            field.set(context, value)

        return getattr(src, name)