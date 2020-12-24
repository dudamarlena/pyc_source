# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/Relations/interfaces.py
# Compiled at: 2008-09-11 19:48:09
"""Interfaces for Relations product.

See also the class diagram in "doc/relationsdia2.png".

Unless explicitely stated otherwise, source and target arguments must be of
type IBrainAggregate, which comprises all information available from catalogs
on an object.
"""
from Interface import Interface, Attribute
from Products.Archetypes.interfaces.referenceengine import IReference

class IChain(Interface):
    """A non persistent object that is passed around while processing
    reference creation and deletion. Attributes 'added' and 'deleted' are lists
    of thus far created and deleted references, respectively.

    IChain is dict-like. However, an IChain creates (ordinary) dicts where
    a normal dict would raise KeyError:
    >>> chain.keys()
    []
    >>> chain['mynamespace']
    {}
    >>> chain.keys()
    ['mynamespace']
    >>> chain['mynamespace'][123] = 456
    >>> chain['mynamespace']
    {123: 456}
    """
    __module__ = __name__
    added = Attribute('added', 'The list of reference obects added in the current process.')
    deleted = Attribute('deleted', 'The list of reference objects deleted in the current process.')


class IReferenceConnectionProcessor(Interface):
    """Manages the process of connecting and disconnecting references.

    The process is divided into three stages: implication, validation and
    finalization."""
    __module__ = __name__

    def process(context, connect=(), disconnect=()):
        """Creates and deletes references.

        ``connect`` and ``disconnect`` arguments are lists of triples
        in the form (Source UID, Target UID, Relationship) where
        Relationship is the ID of the ruleset that we intend to use.

        Elements of ``disconnect`` may also be UIDs of reference
        objects.

        If the process fails with an Exception, process rolls back the
        database to before this function was called.
        """
        pass


class IXMLImportExport(Interface):
    """ A mixin class that does the import/export of ruleset definitions."""
    __module__ = __name__

    def importXML(xmlstring):
        """Takes an XML string and stores the relation information in
        the ruleset library.  This is done recursively."""
        pass

    def exportXML():
        """Dumps the relation settings into an XML file and returns
        the XML string as result."""
        pass


class IRuleset(IXMLImportExport):
    """Ruleset is a container for implicators, validators, finalizers
    and vocabulary providers.

    It provides methods to initiate implications, do validation and
    finalization."""
    __module__ = __name__

    def getId():
        """Returns the ruleset's ID, which must be unique among rulesets."""
        pass

    def getComponents(interface):
        """Returns of my components those which implement the given
        interface."""
        pass

    def implyOnConnect(source, target, chain, metadata=None):
        """Calls the PrimaryImplicator's connect method, thereby creating
        a reference between source and target.

        Appends the newly created reference to the chain and calls each
        implicator's implyOnConnect method.

        ``metadata`` may be a dictionary with which the resulting
        Reference's __dict__ is updated."""
        pass

    def implyOnDisconnect(reference, chain):
        """Calls implyOnDisconnect() for each implicator."""
        pass

    def validateConnected(reference, chain):
        """Calls validateConnected() for each validator.

        Validator components raise exception.ValidationException if validation
        fails."""
        pass

    def validateDisconnected(reference, chain):
        """Calls validateDisconnected() for each validator.

        Validator components raise exceptions.ValidationException if validation
        fails."""
        pass

    def finalizeOnConnect(reference, chain):
        """Calls finalizeOnConnect() for each finalizer."""
        pass

    def finalizeOnDisconnect(reference, chain):
        """Calls finalizeOnDisconnect() for each finalizer."""
        pass

    def makeVocabulary(source, targets=None):
        """Calls makeVocabulary() for each vocabulary provider, forwarding
        the result of the n-th provider to the n+1-th provider, or returning
        the result if no there is no n+1-th provider.

        You may optionally provide a list of IBrainAggregates as the
        targets argument. This list is then filtered by vocabulary
        providers."""
        pass

    def listActionsFor(reference):
        """Returns a list of dictionaries according to
        IReferenceActionProvider.listActionsFor."""
        pass


class ILibrary(IXMLImportExport):
    """Holds references to Rulesets, identified by their id."""
    __module__ = __name__

    def registerRuleset(ruleset):
        """Build a reference to ruleset and make it available through
        getRuleset()."""
        pass

    def getRuleset(id):
        """Returns the ruleset with the given id or raise
        zExceptions.NotFound if no such ruleset is known."""
        pass

    def getRulesets():
        """Return the list of all registered rulesets."""
        pass

    def getFolder():
        """Convenience method that returns a suitable folder for storing
        IRulesets."""
        pass


class IRulesetCollection(IXMLImportExport):
    """A container for IRulesets."""
    __module__ = __name__


class IRule(IXMLImportExport):
    """Superinterface of all rules, aka components."""
    __module__ = __name__

    def getRuleset():
        """Returns the IRuleset that owns this rule."""
        pass


class IVocabularyProvider(IRule):
    """Vocabulary providers are responsible for building vocabularies,
    from which the user chooses the target object of a reference.
    
    Several vocabulary providers form a chain, so that a second
    provider can filter or add to the results of a first provider.
    """
    __module__ = __name__

    def makeVocabulary(source, targets=None):
        """Returns a list of aggregated brains.

        The targets argument may be either None or a list of IBrainAggregates.
        None is to signal that the provider must build a list of
        IBrainAggregates itself. If targets are given, the provider must filter
        them."""
        pass

    def getSearchTerms():
        """Returns a dict of search terms according to
        IZCatalog.searchResults for portal_catalog.  To signal no restrictions,
        return the empty dictionary."""
        pass


class IPrimaryImplicator(IRule):
    """The primary implicator is responsible for establishing a reference in
    the ReferenceEngine.

    See ruleset.DefaultPrimaryImplicator for an implementation."""
    __module__ = __name__

    def connect(source, target, metadata=None):
        """If a reference between source and target does not yet exist, creates
        a new reference and returns it. Returns None if a reference already
        exists.

        ``metadata`` may be a dictionary with which the resulting
        Reference's __dict__ is updated."""
        pass

    def disconnect(reference):
        """Returns None if no such reference exists. Otherwise deletes the
        reference in the db."""
        pass


class IImplicator(IRule):
    """Implicators create additional references.  For instance, a
    ruleset 'is Child Of' may imply a reference 'is Parent Of', for
    which the source and target objects are inverted."""
    __module__ = __name__

    def implyOnConnect(reference, chain):
        """Typically calls Ruleset.implyOnConnect on foreign rulesets."""
        pass

    def implyOnDisconnect(reference, chain):
        """XXX"""
        pass


class IValidator(IRule):
    """Validate references when they're created and deleted."""
    __module__ = __name__

    def validateConnected(reference, chain):
        """Raises exceptions.ValidationException if invalid.

        Note that IValidators may not expect reference to be inside of
        chain.added. validateConnected() may be called at any time for an
        existing reference."""
        pass

    def validateDisconnected(reference, chain):
        """Raises exceptions.ValidationException if invalid.

        Note that reference represents a reference that has been deleted from
        the database. Its nonexistence is to be validated.

        The reference argument is always in chain.deleted."""
        pass


class IFinalizer(IRule):
    """Finalizers define things that happen after references have been
    established and validated, or after they've been deleted and
    that's valid."""
    __module__ = __name__

    def finalizeOnConnect(reference, chain):
        """XXX"""
        pass

    def finalizeOnDisconnect(reference, chain):
        """XXX"""
        pass


class IReferenceActionProvider(IRule):
    """Provides actions for references."""
    __module__ = __name__

    def listActionsFor(reference):
        """Returns a list of dictionaries, each with the following keys:
            title: A human readable title for the action.
            url: The URL to visit to access the action.
            icon: An icon or None if unavailable.
        """
        pass


class IReferenceLayerProvider(IRule):
    """Components may signal through this interface that they want to add
    behaviour to the reference's hooks. See IReferenceLayer"""
    __module__ = __name__

    def provideReferenceLayer(reference):
        """Return an object implementing IReferenceLayer."""
        pass


class IReferenceLayer(Interface):
    """Used to add behaviour to reference class hooks.

    Note that methods are not mandatory, they are called only when they exist.
    """
    __module__ = __name__

    def addHook(reference):
        """XXX"""
        pass

    def delHook(reference):
        """XXX"""
        pass

    def beforeTargetDeleteInformSource(reference):
        """XXX"""
        pass

    def beforeSourceDeleteInformTarget(reference):
        """XXX"""
        pass


class IBrainAggregate(Interface):
    """Resembles a ZCatalog brain in usage, i.e. all metadata is available
    through attributes and the real object itself can be retrieved through
    getObject()."""
    __module__ = __name__

    def getObject():
        """Return the actual object that this aggregate holds the metadata
        for."""
        pass


class IReferenceWithBrains(IReference):
    """Minimal extension to IReference with two convenience methods added."""
    __module__ = __name__

    def getSourceBrain():
        """Returns an IBrainAggregate, which comprises all catalog metadata
        available for source object."""
        pass

    def getTargetBrain():
        """Returns an IBrainAggregate, which comprises all catalog metadata
        available for target object."""
        pass