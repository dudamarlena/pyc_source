# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/infrae/plone/relations/schema/interfaces.py
# Compiled at: 2008-06-11 04:04:51
__author__ = 'sylvain@infrae.com'
__format__ = 'plaintext'
__version__ = '$Id: interfaces.py 29100 2008-06-11 08:04:50Z sylvain $'
from zope.interface import Interface
from zope.schema.interfaces import IField, IMinMaxLen
from zope.schema import TextLine, Bool, InterfaceField
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('plone')

class IPloneRelation(IField, IMinMaxLen):
    """Used to administrate a plone.app.relation
       on an object.
    """
    __module__ = __name__
    relation = TextLine(title=_('Relation name'), description=_('The relation name used.'), required=True)
    reverse = Bool(title=_('Direction of relation'), description=_('If true, the relation is a source one, otherwiser a target'), required=True)
    context_schema = InterfaceField(title=_('Interface that should implement the context object'), required=False)
    relation_schema = InterfaceField(title=_('Relation items must implements this interface'), required=False)
    unique = Bool(title=_('Relation items have to be alone in a relation'), required=False)


class IPloneRelationContextFactory(Interface):
    """Factory used to create a new context object.
    """
    __module__ = __name__

    def __call__(src, tgt, data):
        """
           - src: source of the relation,
           - tgt: target of the relation,
           - data: dictionnary with the parameters of the context.
        """
        pass


class IPloneRelationContext(Interface):
    """Base content type for plone relation context object.
    """
    __module__ = __name__
    meta_type = TextLine(title=_('Zope2 meta type.'))

    def __init__(id):
        """Constructor, using id as object id.
        """
        pass


class IManyToManyRelationship(Interface):
    """An complex relation manager. You can administrate many to many
       relation, in the both direction.
    """
    __module__ = __name__

    def createRelationship(targets, sources, interfaces, default_deletion):
        """Create relation.
        """
        pass

    def deleteRelationship(target, source, relation, state, context, rel_filter, multiple, remove_all_target, ignore_missing, remove_all_sources):
        """Delete relation.
        """
        pass

    def getRelationships(target, source, relation, state, context, rel_filter):
        """Return a list of relations.
        """
        pass

    def getRelationshipChains(target, source, relation, state, context, rel_filter, maxDepth, minDepth, transitivity):
        """Return all the relation link.
        """
        pass

    def getSources(relation, state, context, maxDepth, minDepth, transivity):
        """Return the sources of the relation.
        """
        pass

    def getTargets(relation, state, context, maxDepth, minDepth, transitivity):
        """Return the targets of relation.
        """
        pass

    def setDirection(direction):
        """Set the direction of the relation. True for normal use,
           False for reverse.
        """
        pass