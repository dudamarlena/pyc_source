# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/rdf/store.py
# Compiled at: 2008-03-20 22:31:44
"""
This module defines the store plugin interface.

The module is useful for those wanting to write a store plugin for
rdf. Otherwise see the rdf.graph documentation on how to specify
which store your graph is to use.

"""
from rdf.term import RDF
from rdf import exceptions
VALID_STORE = 1
CORRUPTED_STORE = 0
NO_STORE = -1
UNKNOWN = None

class Event(object):
    """
    An event is a container for attributes.  The source of an event
    creates this object, or a subclass, gives it any kind of data that
    the events handlers need to handle the event, and then calls
    notify(event).

    The target of an event registers a function to handle the event it
    is interested with subscribe().  When a sources calls
    notify(event), each subscriber to that even will be called i no
    particular order.
    """

    def __init__(self, **kw):
        self.__dict__.update(kw)

    def __repr__(self):
        attrs = self.__dict__.keys()
        attrs.sort()
        return '<rdf.events.Event %s>' % ([ a for a in attrs ],)


class Dispatcher(object):
    """
    An object that can dispatch events to a privately managed group of
    subscribers.
    """
    _dispatch_map = None

    def set_map(self, amap):
        self._dispatch_map = amap

    def get_map(self):
        return self._dispatch_map

    def subscribe(self, event_type, handler):
        """ Subscribe the given handler to an event_type.  Handlers
        are called in the order they are subscribed.
        """
        if self._dispatch_map is None:
            self.set_map({})
        lst = self._dispatch_map.get(event_type, None)
        if lst is None:
            lst = [
             handler]
        else:
            lst.append(handler)
        self._dispatch_map[event_type] = lst
        return

    def dispatch(self, event):
        """ Dispatch the given event to the subscribed handlers for
        the event's type"""
        if self._dispatch_map is not None:
            lst = self._dispatch_map.get(type(event), None)
            if lst is None:
                raise ValueError('unknown event type: %s' % type(event))
            for l in lst:
                l(event)

        return


class StoreCreatedEvent(Event):
    """
    This event is fired when the Store is created, it has the folloing attribute:
    
      - 'configuration' string that is used to create the store

    """
    pass


class TripleAddedEvent(Event):
    """
    This event is fired when a triple is added, it has the following attributes:

      - 'triple' added to the graph
      - 'context' of the triple if any
      - 'graph' that the triple was added to
    """
    pass


class TripleRemovedEvent(Event):
    """
    This event is fired when a triple is removed, it has the following attributes:

      - 'triple' removed from the graph
      - 'context' of the triple if any
      - 'graph' that the triple was removed from
    """
    pass


class Store(object):
    context_aware = False
    formula_aware = False
    transaction_aware = False
    batch_unification = False

    def __init__(self, configuration=None, identifier=None):
        """
        identifier: URIRef of the Store. Defaults to CWD
        configuration: string containing infomation open can use to
        connect to datastore.
        """
        self.__node_pickler = None
        self.dispatcher = Dispatcher()
        if configuration:
            self.open(configuration)
        return

    def __get_node_pickler(self):
        if self.__node_pickler is None:
            from rdf.term import URIRef
            from rdf.term import BNode
            from rdf.term import Literal
            from rdf.graph import Graph, QuotedGraph, GraphValue
            from rdf.term import Variable
            from rdf.term import Statement
            self.__node_pickler = np = NodePickler()
            np.register(self, 'S')
            np.register(URIRef, 'U')
            np.register(BNode, 'B')
            np.register(Literal, 'L')
            np.register(Graph, 'G')
            np.register(QuotedGraph, 'Q')
            np.register(Variable, 'V')
            np.register(Statement, 's')
            np.register(GraphValue, 'v')
        return self.__node_pickler

    node_pickler = property(__get_node_pickler)

    def create(self, configuration):
        self.dispatcher.dispatch(StoreCreatedEvent(configuration=configuration))

    def open(self, configuration, create=False):
        """
        Opens the store specified by the configuration string. If
        create is True a store will be created if it does not already
        exist. If create is False and a store does not already exist
        an exception is raised. An exception is also raised if a store
        exists, but there is insufficient permissions to open the
        store.  This should return one of VALID_STORE,CORRUPTED_STORE,or NO_STORE
        """
        return UNKNOWN

    def close(self, commit_pending_transaction=False):
        """
        This closes the database connection. The commit_pending_transaction parameter specifies whether to
        commit all pending transactions before closing (if the store is transactional).
        """
        pass

    def destroy(self, configuration):
        """
        This destroys the instance of the store identified by the configuration string.
        """
        pass

    def gc(self):
        """
        Allows the store to perform any needed garbage collection
        """
        pass

    def add(self, triple, context, quoted=False):
        """
        Adds the given statement to a specific context or to the
        model. The quoted argument is interpreted by formula-aware
        stores to indicate this statement is quoted/hypothetical It
        should be an error to not specify a context and have the
        quoted argument be True.  It should also be an error for the
        quoted argument to be True when the store is not
        formula-aware.
        """
        self.dispatcher.dispatch(TripleAddedEvent(triple=triple, context=context))

    def addN(self, quads):
        """
        Adds each item in the list of statements to a specific
        context. The quoted argument is interpreted by formula-aware
        stores to indicate this statement is quoted/hypothetical.
        Note that the default implementation is a redirect to adda
        """
        for (s, p, o, c) in quads:
            assert c is not None, 'Context associated with %s %s %s is None!' % (s, p, o)
            self.add((s, p, o), c)

        return

    def remove(self, triple, context=None):
        """ Remove the set of triples matching the pattern from the store """
        self.dispatcher.dispatch(TripleRemovedEvent(triple=triple, context=context))

    def triples_choices(self, triple, context=None):
        """
        A variant of triples that can take a list of terms instead of a single
        term in any slot.  Stores can implement this to optimize the response time
        from the default 'fallback' implementation, which will iterate
        over each term in the list and dispatch to tripless
        """
        (subject, predicate, object_) = triple
        if isinstance(object_, list):
            assert not isinstance(subject, list), 'object_ / subject are both lists'
            assert not isinstance(predicate, list), 'object_ / predicate are both lists'
            if object_:
                for obj in object_:
                    for ((s1, p1, o1), cg) in self.triples((subject, predicate, obj), context):
                        yield (
                         (
                          s1, p1, o1), cg)

            else:
                for ((s1, p1, o1), cg) in self.triples((subject, predicate, None), context):
                    yield (
                     (
                      s1, p1, o1), cg)

        elif isinstance(subject, list):
            assert not isinstance(predicate, list), 'subject / predicate are both lists'
            if subject:
                for subj in subject:
                    for ((s1, p1, o1), cg) in self.triples((subj, predicate, object_), context):
                        yield (
                         (
                          s1, p1, o1), cg)

            else:
                for ((s1, p1, o1), cg) in self.triples((None, predicate, object_), context):
                    yield (
                     (
                      s1, p1, o1), cg)

        elif isinstance(predicate, list):
            assert not isinstance(subject, list), 'predicate / subject are both lists'
            if predicate:
                for pred in predicate:
                    for ((s1, p1, o1), cg) in self.triples((subject, pred, object_), context):
                        yield (
                         (
                          s1, p1, o1), cg)

            else:
                for ((s1, p1, o1), cg) in self.triples((subject, None, object_), context):
                    yield (
                     (
                      s1, p1, o1), cg)

        return

    def triples(self, triple, context=None):
        """
        A generator over all the triples matching the pattern. Pattern can
        include any objects for used for comparing against nodes in the store, for
        example, REGEXTerm, URIRef, Literal, BNode, Variable, Graph, QuotedGraph, Date? DateRange?

        A conjunctive query can be indicated by either providing a value of None
        for the context or the identifier associated with the Conjunctive Graph (if it's context aware).
        """
        (subject, predicate, object) = triple

    def __len__(self, context=None):
        """
        Number of statements in the store. This should only account for non-quoted (asserted) statements
        if the context is not specified, otherwise it should return the number of statements in the formula or context given.
        """
        pass

    def contexts(self, triple=None):
        """
        Generator over all contexts in the graph. If triple is specified, a generator over all
        contexts the triple is in.
        """
        pass

    def bind(self, prefix, namespace):
        """ """
        pass

    def prefix(self, namespace):
        """ """
        pass

    def namespace(self, prefix):
        """ """
        pass

    def namespaces(self):
        """ """
        pass

    def commit(self):
        """ """
        pass

    def rollback(self):
        """ """
        pass


from cPickle import Pickler, Unpickler, UnpicklingError
from cStringIO import StringIO

class NodePickler(object):
    r"""

    >>> from rdf.store import NodePickler
    >>> from rdf.term import Literal
    >>> np = NodePickler()
    >>> a = Literal(u'''A test with a \n (backslash n), "\u00a9" , and newline
    ... and a second line.''')
    >>> b = np.loads(np.dumps(a))
    >>> a==b
    True

    """

    def __init__(self):
        self._objects = {}
        self._ids = {}
        self._get_object = self._objects.__getitem__

    def _get_ids(self, key):
        try:
            return self._ids.get(key)
        except TypeError, e:
            return

        return

    def register(self, object, id):
        self._objects[id] = object
        self._ids[object] = id

    def loads(self, s):
        up = Unpickler(StringIO(s))
        up.persistent_load = self._get_object
        try:
            return up.load()
        except KeyError, e:
            raise UnpicklingError, 'Could not find Node class for %s' % e

    def dumps(self, obj, protocol=None, bin=None):
        src = StringIO()
        p = Pickler(src)
        p.persistent_id = self._get_ids
        p.dump(obj)
        return src.getvalue()