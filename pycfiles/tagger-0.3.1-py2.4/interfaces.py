# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-fat/egg/tagger/interfaces.py
# Compiled at: 2006-11-03 15:10:45
from utils import Interface, Attribute

class AnnotationNotFoundError(Exception):
    """Requested annotation not found in store"""
    __module__ = __name__


class ITaggable(Interface):
    """
    entity that can be tagged
    """
    __module__ = __name__
    identifier = Attribute('a unique identifier in operative tagging scenario.May be the tag itself')


class ITag(ITaggable):
    """
    entity that represents a tag
    """
    __module__ = __name__


class IUser(ITaggable):
    """
    entity that can tag
    """
    __module__ = __name__


class IItem(ITaggable):
    """
    entity that can be tagged
    """
    __module__ = __name__


class ITagger(Interface):
    """
    Utility class for adding, removing, and updating tags as
    annotations to a graph.

    A tag is an annotation represented by a string literal
    """
    __module__ = __name__
    ns = Attribute('collection of namespaces used by tagger')
    annotates = Attribute('URI for annotation relationship')
    authoredby = Attribute('URI for author relationship')
    identifies = Attribute('URI for canonical identification')
    isannotation = Attribute('URI for annotation type')
    isbody = Attribute('URI for annotea:body type')
    isperson = Attribute('URI for person type')
    istag = Attribute('URI for tag type')
    tags = Attribute('URI for tagging relationship')

    def __init__(graph):
        """ @param graph: rdflib graph for tagging """
        pass

    def _annotate(item, author, body, context, related=None):
        """
        adds a annotation to the graph

        basic interface for annotation using Annotea Namespace

        @param item: item annotated
        @param author: person doing the annotating
        @param body: annotation itself
        @type body: resource
        @param context: context that annotation is active in
        @type related: tuple of type and resource for
                       subclass of annotea:related
        @param related: generic pointer to other resources
        """
        pass

    def getById(identifier, type_=None, context=None, create=True):
        """
        Retrieves a node from a graph, creating one if needs

        @param identifier: unique identifier
        @param type_: optional type for node creation
        @return uri for node for identifier
        """
        pass

    def _addTag(tag):
        """adds new tag to graph"""
        pass

    def _reap(tag):
        """ remove tag from graph if it is orphaned """
        pass

    def tagItem(item, tags, user, context, related=None):
        """
        retrieves or creates tags and applies it for all appropriate
        contexts
        """
        pass

    def delete_tag(item, user, tag, context=None):
        """ remove a tag from an item """
        pass

    def delete(obj, context=None):
        """
        removes all annotations for a tag, item or user
        
        @param obj: user, item, or tag
        @type obj: str identifier
        """
        pass

    def count(tag=None, user=None, item=None, context=None):
        """
        returns count for intersection
        """
        pass

    def getItemsFor(subject, context):
        """
        @rtype: list
        @return: tag uris
        """
        pass

    def getTagsFor(subject, context):
        """
        @rtype: list
        @return: tag uris
        """
        pass

    def getUsersFor(subject, context):
        """
        returns a list of user uris
        """
        pass

    def annotations(tag=None, user=None, item=None, context=None):
        """ annotations by intersection """
        pass

    def annotations_by(self, pred, subject, spec=None):
        """
        simple scope query to return all nodes represent annotations
        for a particular 'subject' of relation 'pred'

        @param subject: node id for item of interest
        
        @param pred:    predicate defining relationship of subject to an
                        annotation.

        @return         list of node ids for annotations
        """
        pass

    def intersect(s1, s2, context=None):
        """
        generic 2 dimension intersection (in IUT order)::
        
        item, user >> all tags for user & item
        user, tag >> all items for user & tag
        item, tag >> all users for item & tag

        nonimplemented permutations::

        tag, tag  >> all users and items shared by both tags
        item, item >> all tags and users shared by both items
        user, user >> all tags and items shared by both users

        tag, RDF.type >> all ids for all type tagged with tag

        what the s1 and s2 represent in the graph and/or context
        determines typing. further permutations could occur by
        dispatch upon type of s1 and s2 for objects provided
        dispatched function converted objects to identifiers readable
        by self.getById
        """
        pass

    def getById(identifier, spec=None, context=None, create=False):
        """
        get a node by it's identifier

        *method is ruledispatch extensible*
        
        @param create: flag for autocreation of resource if resource
        not found
        @param create: boolean
        
        @param spec: rdf predicate and object for new node created
        @type spec: tuple
        """
        pass

    def items_for_tag(self, subject, spec=None):
        """ returns id for items tags by string:subject """
        pass

    def items_for_user(self, subject, spec=None):
        """ for item for user id """
        pass

    def users_for_tag(self, subject, spec=None):
        """ for item for user id """
        pass

    def users_for_item(self, subject, spec=None):
        """ for item for user id """
        pass

    def tags_for_item(self, subject, spec=None):
        """ for item for user id """
        pass

    def tags_for_user(self, subject, spec=None):
        """ for item for user id """
        pass