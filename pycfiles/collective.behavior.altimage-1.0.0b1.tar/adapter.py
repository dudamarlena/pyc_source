# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/beancounter/adapter.py
# Compiled at: 2007-11-14 13:15:30
__author__ = 'Stefan Eletzhofer <stefan.eletzhofer@inquant.de>'
__docformat__ = 'plaintext'
__revision__ = '$Revision: 53835 $'
__version__ = '$Revision: 53835 $'[11:-2]
from zope import interface
from collective.beancounter.interfaces import IBeanCounter, IBeanCounterFieldFilter

def null_filter(dummy):
    return True


def countable_fields(content):
    schema = content.Schema()
    field_filter = IBeanCounterFieldFilter(content, null_filter)
    return filter(field_filter, schema.fields())


def count_schema_fields(content):
    schema = content.Schema()
    return len(countable_fields(schema))


def filled_fields(content):
    l = countable_fields(content)
    return [ f.getName() for f in l if f.get(content) ]


def empty_fields(content):
    l = countable_fields(content)
    return [ f.getName() for f in l if not f.get(content) ]


class ATBeanCounter(object):
    __module__ = __name__
    interface.implements(IBeanCounter)

    def __init__(self, context):
        self.context = context

    @property
    def percentage(self):
        nr = len(countable_fields(self.context))
        filled = len(filled_fields(self.context))
        return filled * 1.0 / (nr * 1.0) * 100.0


class ATFieldFilter(object):
    """
    Filter out fields which:
      - are not user settable
      - are not in the "default" schemata
      - are not in the special plone field blacklist
      - are not boolean fields (these are true or false, i.e. always "filled")
    """
    __module__ = __name__
    interface.implements(IBeanCounterFieldFilter)
    PLONE_FIELDS = ('constrainTypesMode locallyAllowedTypes immediatelyAddableTypes').split()
    FIELD_BLACKLIST = 'BooleanField'

    def __init__(self, context):
        self.context = context

    def __call__(self, f):
        return f.schemata == 'default' and f.mode == 'rw' and f.getName() not in self.PLONE_FIELDS and f.__class__.__name__ not in self.FIELD_BLACKLIST