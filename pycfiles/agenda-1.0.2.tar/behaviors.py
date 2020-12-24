# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ageliaco/tracker/behavior/behaviors.py
# Compiled at: 2011-07-15 05:56:27
__doc__ = 'Behaviours to assign contributors.\n\nIncludes a form field and a behaviour adapter that stores the data in the\nstandard Subject field.\n'
from rwproperty import getproperty, setproperty
from zope.interface import implements, alsoProvides
from zope.component import adapts
from plone.directives import form
from zope import schema
from Products.CMFCore.interfaces import IDublinCore
from ageliaco.tracker import _
from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget

class IContributors(form.Schema):
    """Add contributors to content
    """
    form.widget(contributor=AutocompleteMultiFieldWidget)
    contributor = schema.List(title=_('Contributeurs'), default=[], value_type=schema.Choice(vocabulary='plone.principalsource.Users'), required=False)


alsoProvides(IContributors, form.IFormFieldProvider)

class Contributors(object):
    """Store contributors in the Dublin Core metadata contributors field. This makes
    contributors easy to search for.
    """
    implements(IContributors)
    adapts(IDublinCore)

    def __init__(self, context):
        self.context = context

    @getproperty
    def contributors(self):
        return set(self.context.contributors())

    @setproperty
    def contributors(self, value):
        if value is None:
            value = ()
        self.context.setContributors(tuple(value))
        return