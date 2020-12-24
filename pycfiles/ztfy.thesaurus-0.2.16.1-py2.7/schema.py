# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/thesaurus/schema.py
# Compiled at: 2012-12-05 09:13:07
from zope.schema.interfaces import IObject, IList, SchemaNotProvided
from zope.interface import implements, Interface
from zope.schema import Object, List, Set, Choice, TextLine
from ztfy.thesaurus import _

class IThesaurusTermField(IObject):
    """Marker interface to define a thesaurus term field"""
    thesaurus_name = TextLine(title=_('Thesaurus name'), required=False)
    extract_name = TextLine(title=_('Extract name'), required=False)


class IThesaurusTermsListField(IList):
    """Marker interface to define a list of thesaurus terms"""
    thesaurus_name = TextLine(title=_('Thesaurus name'), required=False)
    extract_name = TextLine(title=_('Extract name'), required=False)


class ThesaurusTermField(Object):
    """Thesaurus term schema field"""
    implements(IThesaurusTermField)

    def __init__(self, schema=None, thesaurus_name='', extract_name='', **kw):
        super(ThesaurusTermField, self).__init__(schema=Interface, **kw)
        self.thesaurus_name = thesaurus_name
        self.extract_name = extract_name

    def _validate(self, value):
        super(Object, self)._validate(value)
        if not self.schema.providedBy(value):
            raise SchemaNotProvided


class ThesaurusTermsListField(List):
    """Thesaurus terms list schema field"""
    implements(IThesaurusTermsListField)

    def __init__(self, value_type=None, unique=False, thesaurus_name='', extract_name='', **kw):
        super(ThesaurusTermsListField, self).__init__(value_type=Object(schema=Interface), unique=False, **kw)
        self.thesaurus_name = thesaurus_name
        self.extract_name = extract_name


class ValidatedSet(Set):
    """A set field validated when not bound to a context"""

    def _validate(self, value):
        if self.context is None:
            return
        else:
            super(ValidatedSet, self)._validate(value)
            return


class ValidatedChoice(Choice):
    """An always validated choice field"""

    def _validate(self, value):
        pass