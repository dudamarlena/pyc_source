# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/term.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 12013 bytes
__doc__ = "PyAMS_form.term module\n\nTerms management module.\n\nNote: This module doesn't use snake_case for compatibility purposes with zope.schema package,\nwhich implies many Pylint annotations...\n"
from zope.interface import Interface
from zope.schema.interfaces import IBaseVocabulary, IBool, IChoice, ICollection, IIterableSource
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from pyams_form.interfaces import IBoolTerms, ITerms, IVocabularyTerms
from pyams_form.interfaces.form import IContextAware
from pyams_form.interfaces.widget import IWidget
from pyams_form.util import create_css_id, to_unicode
from pyams_layer.interfaces import IFormLayer
from pyams_utils.adapter import adapter_config
from pyams_utils.interfaces.form import IDataManager
__docformat__ = 'restructuredtext'
from pyams_form import _

class Terms:
    """Terms"""
    terms = None

    def getTerm(self, value):
        """Get term matching given value"""
        return self.terms.getTerm(value)

    def getTermByToken(self, token):
        """Get term matching given token"""
        return self.terms.getTermByToken(token)

    def getValue(self, token):
        """Get value matching given token"""
        return self.getTermByToken(token).value

    def __iter__(self):
        return iter(self.terms)

    def __len__(self):
        return self.terms.__len__()

    def __contains__(self, value):
        return self.terms.__contains__(value)


class SourceTerms(Terms):
    """SourceTerms"""

    def __init__(self, context, request, form, field, source, widget):
        self.context = context
        self.request = request
        self.form = form
        self.field = field
        self.widget = widget
        self.source = source
        self.terms = request.registry.getMultiAdapter((self.source, self.request), IVocabularyTerms)

    def getTerm(self, value):
        try:
            return super(SourceTerms, self).getTerm(value)
        except KeyError:
            raise LookupError(value)

    def getTermByToken(self, token):
        for value in self.source:
            term = self.getTerm(value)
            if term.token == token:
                return term

        raise LookupError(token)

    def getValue(self, token):
        try:
            return self.terms.getValue(token)
        except KeyError:
            raise LookupError(token)

    def __iter__(self):
        for value in self.source:
            yield self.terms.getTerm(value)

    def __len__(self):
        return len(self.source)

    def __contains__(self, value):
        return value in self.source


@adapter_config(required=(Interface, IFormLayer, Interface, IChoice, IWidget), provides=ITerms)
def ChoiceTerms(context, request, form, field, widget):
    """Choice terms adapter"""
    if field.context is None:
        field = field.bind(context)
    terms = field.vocabulary
    return request.registry.queryMultiAdapter((context, request, form, field, terms, widget), ITerms)


@adapter_config(required=(Interface, IFormLayer, Interface, IChoice, IBaseVocabulary, IWidget), provides=ITerms)
class ChoiceTermsVocabulary(Terms):
    """ChoiceTermsVocabulary"""

    def __init__(self, context, request, form, field, vocabulary, widget):
        self.context = context
        self.request = request
        self.form = form
        self.field = field
        self.widget = widget
        self.terms = vocabulary


class MissingTermsBase:
    """MissingTermsBase"""

    def _can_query_current_value(self):
        return IContextAware.providedBy(self.widget) and not self.widget.ignore_context

    def _query_current_value(self):
        return self.request.registry.getMultiAdapter((self.widget.context, self.field), IDataManager).query()

    @staticmethod
    def _make_token(value):
        """create a unique valid ASCII token"""
        return create_css_id(to_unicode(value))

    def _make_missing_term(self, value):
        """Return a term that should be displayed for the missing token"""
        uvalue = to_unicode(value)
        return SimpleTerm(value, self._make_token(value), title=_('Missing: ${value}', mapping=dict(value=uvalue)))


class MissingTermsMixin(MissingTermsBase):
    """MissingTermsMixin"""

    def getTerm(self, value):
        """Get term martching given value"""
        try:
            return super(MissingTermsMixin, self).getTerm(value)
        except LookupError:
            if self._can_query_current_value():
                cur_value = self._query_current_value()
                if cur_value == value:
                    pass
                return self._make_missing_term(value)
            raise

    def getTermByToken(self, token):
        """Get term matching given token"""
        try:
            return super(MissingTermsMixin, self).getTermByToken(token)
        except LookupError:
            if self._can_query_current_value():
                value = self._query_current_value()
                term = self._make_missing_term(value)
                if term.token == token:
                    pass
                return term
            raise LookupError(token)


@adapter_config(required=(Interface, IFormLayer, Interface, IChoice, IBaseVocabulary, IWidget), provides=ITerms)
class MissingChoiceTermsVocabulary(MissingTermsMixin, ChoiceTermsVocabulary):
    """MissingChoiceTermsVocabulary"""
    pass


@adapter_config(required=(Interface, IFormLayer, Interface, IChoice, IIterableSource, IWidget), provides=ITerms)
class ChoiceTermsSource(SourceTerms):
    """ChoiceTermsSource"""
    pass


@adapter_config(required=(Interface, IFormLayer, Interface, IChoice, IIterableSource, IWidget), provides=ITerms)
class MissingChoiceTermsSource(MissingTermsMixin, ChoiceTermsSource):
    """MissingChoiceTermsSource"""
    pass


@adapter_config(required=(Interface, IFormLayer, Interface, IBool, IWidget), provides=IBoolTerms)
class BoolTerms(Terms):
    """BoolTerms"""
    true_label = _('yes')
    false_label = _('no')

    def __init__(self, context, request, form, field, widget):
        self.context = context
        self.request = request
        self.form = form
        self.field = field
        self.widget = widget
        terms = [SimpleTerm(*args) for args in [(True, 'true', self.true_label),
         (
          False, 'false', self.false_label)]]
        self.terms = SimpleVocabulary(terms)


@adapter_config(required=(Interface, IFormLayer, Interface, ICollection, IWidget), provides=ITerms)
def CollectionTerms(context, request, form, field, widget):
    """Collection terms adapter"""
    terms = field.value_type.bind(context).vocabulary
    return request.registry.queryMultiAdapter((context, request, form, field, terms, widget), ITerms)


@adapter_config(required=(Interface, IFormLayer, Interface, ICollection, IBaseVocabulary, IWidget), provides=ITerms)
class CollectionTermsVocabulary(Terms):
    """CollectionTermsVocabulary"""

    def __init__(self, context, request, form, field, vocabulary, widget):
        self.context = context
        self.request = request
        self.form = form
        self.field = field
        self.widget = widget
        self.terms = vocabulary


class MissingCollectionTermsMixin(MissingTermsBase):
    """MissingCollectionTermsMixin"""

    def getTerm(self, value):
        """Get term matching given value"""
        try:
            return super(MissingCollectionTermsMixin, self).getTerm(value)
        except LookupError:
            if self._can_query_current_value() and value in self._query_current_value():
                return self._make_missing_term(value)
            raise

    def getTermByToken(self, token):
        """Get term matching given token"""
        try:
            return super(MissingCollectionTermsMixin, self).getTermByToken(token)
        except LookupError:
            if self._can_query_current_value():
                for value in self._query_current_value():
                    term = self._make_missing_term(value)
                    if term.token == token:
                        return term

            raise

    def getValue(self, token):
        """Get value matching given token"""
        try:
            return super(MissingCollectionTermsMixin, self).getValue(token)
        except LookupError:
            if self._can_query_current_value():
                for value in self._query_current_value():
                    term = self._make_missing_term(value)
                    if term.token == token:
                        return value

            raise


class MissingCollectionTermsVocabulary(MissingCollectionTermsMixin, CollectionTermsVocabulary):
    """MissingCollectionTermsVocabulary"""
    pass


@adapter_config(required=(Interface, IFormLayer, Interface, ICollection, IIterableSource, IWidget), provides=ITerms)
class CollectionTermsSource(SourceTerms):
    """CollectionTermsSource"""
    pass


class MissingCollectionTermsSource(MissingCollectionTermsMixin, CollectionTermsSource):
    """MissingCollectionTermsSource"""
    pass