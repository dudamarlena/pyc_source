# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tau/selectorstrings/zcml_directives.py
# Compiled at: 2010-12-21 05:25:17
"""Implement of two directives; a simple one and complex top/sub directive pair.

   ZCML directives can be divided into two kinds; simple and complex.  A
   simple directive is a standalone XML tag.  A complex directive acts as a
   container of other ZCML directives, giving them context and allowing for
   the factoring out of redundant XML tags.

   A simple directive has a handler implemented as a simple function, which is
   called in the XML-tag closure phase.

   A complex directive has a handler that is a class instantiated at XML-tag
   open with the XML tag attributes, and the instance called at XML tag
   closure.

   In this module we'll implement one of each.

   For the simple directive::

      <selectorstring
          cluster="sitedocs"
          label="Public Materials"
          value="/usr/share/public"
          />

   For the complex directive::

      <selectorcluster name="sitedocs">
          <selectorstring label="Public Materials", value="/usr/share/public" />
          <selectorstring label="For-Pay Materials", value="/home/jeff/works" />
          <selectorstring label="Family Photos", value="/home/jeff/photos" />
      </selectorcluster>

   And then you reference the declared strings as a Zope vocabulary named with
   the cluster name using a Choice-type of schema dropdown widget::

      from zope.schema import Choice
      class ILibrary(Interface):
          sitedocs = Choice(title=u"Path to Site Documents",
                            vocabulary="sitedocs")
"""
from zope.interface import implements, alsoProvides
from zope.component import queryUtility, provideUtility
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory
from .interfaces import ISelectorStringDirective, ISelectorClusterDirective, IClusterOfSelectors
import logging
log = logging.getLogger('tau.selectorstrings')

def selectorstring_SimpleDirectiveHandler(_context, cluster, value, label=None):
    """Handler of a simple ZCML directive.

       NOTE: A handler does NOT execute an action immediately but instead
       registers an action to occur at the end of the configuration process.
       This is because the system should go through all of the configuration
       first, detecting potential conflicts and implementing possible
       overrides.  Only after the configuration is fully determined are the
       registered actions performed.

       Takes as arguments any attributes of the simple directive, after they
       have been automatically validated by Zope against the directive's schema.
    """

    def deferred__append_selector(_context, clustername, value, label):
        """The actual handling that is performed at the -END- of configuration.

           Append each selectorstring, as it is parsed from a ZCML file, onto
           a 'cluster' object of which there is one for each clustername ever
           seen.  The 'cluster' object is created the first time we ever see a
           particular clustername used.

           The 'cluster' object represents a Zope vocabulary of a dropdown
           list with each string being a pick value on that dropdown.
        """
        cluster = queryUtility(IClusterOfSelectors, name=clustername)
        if cluster is None:
            log.info('No such cluster as %r, creating one' % clustername)
            cluster = ClusterOfSelectors(clustername)
            provideUtility(cluster, provides=IClusterOfSelectors, name=clustername)

            def SelectorFactory(context):
                cluster = queryUtility(IClusterOfSelectors, name=clustername)
                return cluster

            alsoProvides(SelectorFactory, IVocabularyFactory)
            provideUtility(SelectorFactory, provides=IVocabularyFactory, name=clustername)
        cluster.register(value, label)
        return

    _context.action(discriminator=(
     'selectorstring', cluster, value, label), callable=deferred__append_selector, args=(
     _context, cluster, value, label))


class selectorcluster_ComplexDirectiveHandler(object):
    """Handler for a complex ZCML directive, including any subdirectives.

       NOTE: A handler does NOT execute an action immediately but instead
       registers an action to occur at the end of the configuration process.
       This is because the system should go through all of the configuration
       first, detecting potential conflicts and implementing possible
       overrides.  Only after the configuration is fully determined are the
       registered actions performed.

       Subdirectives (i.e. nested ones) are handled as methods on this class,
       where the name of the method *MUST* match the name of the subdirective.
    """

    def __init__(self, _context, name):
        """Handle of a complex directive.

           Takes as arguments any attributes of the complex (outer) directive,
           after they have been automatically validated by Zope against the
           directive's schema.
        """
        self.__context = _context
        self.name = name
        _context.action(discriminator=(
         'selectorcluster', name), callable=self.deferred__instantiate_cluster, args=(
         _context, name))

    def deferred__instantiate_cluster(self, _context, name):
        """The actual handling that is performed at the -END- of configuration.

           Create one 'cluster' object for each unique clustername seen as
           they are parsed from a ZCML file.
        """
        self.cluster = queryUtility(IClusterOfSelectors, name=name)
        if self.cluster is None:
            log.info('No such cluster as %r, creating one' % name)
            self.cluster = ClusterOfSelectors(name)
            provideUtility(self.cluster, provides=IClusterOfSelectors, name=name)

            def SelectorFactory(context):
                cluster = queryUtility(IClusterOfSelectors, name=name)
                return cluster

            alsoProvides(SelectorFactory, IVocabularyFactory)
            provideUtility(SelectorFactory, provides=IVocabularyFactory, name=name)
        return

    def selectorstring(self, _context, value, label=None):
        """Handler for the 'selectorstring' subdirective.

           Handlers for subdirectives also must AVOID executing an action
           immediately but instead register an action to occur at the end of
           the configuration process.
        """
        _context.action(discriminator=(
         'selectorstring', self.name, value, label), callable=self.deferred__append_selector, args=(
         _context, value, label))

    def deferred__append_selector(self, _context, value, label):
        """The actual handling that is performed at the -END- of configuration.

           Append each selectorstring, as it is parsed from a ZCML file, onto
           a 'cluster' object of which there is one for each clustername ever
           seen.

           The 'cluster' object represents a Zope vocabulary of a dropdown
           list with each string being a pick value on that dropdown.
        """
        self.cluster.register(value, label)

    def __call__(self):
        """Called when the complex directive is *** empty ***.

           Use of this method is optional and we don't need it as we don't do
           anything special if our complex directive has no subdirectives
           within it.
        """
        return ()


class SelectorTerm(SimpleTerm):
    """One term or pick choice for our vocabulary of selectorstrings.

       Subclassed only to provide a meaningful repr() string to make debugging
       easier.
    """

    def __repr__(self):
        return '%s(token=%r, value=%r, title=%r)' % (
         self.__class__.__name__, self.token, self.value, self.title)


class ClusterOfSelectors(SimpleVocabulary):
    """A iterable container of selector strings ***for a particular cluster***.
    """
    implements(IClusterOfSelectors)

    def __init__(self, clustername):
        SimpleVocabulary.__init__(self, [])
        self.clustername = clustername

    def __repr__(self):
        return '%s(%r, id=%r)' % (
         self.__class__.__name__, self.clustername, id(self))

    @classmethod
    def createTerm(cls, *args):
        return SelectorTerm(*args)

    def register(self, value, label=None):
        """Append a selectorstring to the cluster, along with a label.

           A label is what is shown to the human, the value is what is used
           internally.
        """
        title = value if label is None else label
        token = str(value)
        term = self.createTerm(value, token, title)
        self._terms.append(term)
        self.by_value[term.value] = term
        self.by_token[term.token] = term
        if len(self.by_value) != len(self.by_token) != len(self._terms):
            raise ValueError('Adding selector (value=%r, label=%r) resulted in a duplicate entry.' % (
             value, label))
        return