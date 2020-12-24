# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/crito/Work/docar/tests/document_tests.py
# Compiled at: 2012-09-26 08:45:40
from nose.tools import eq_, ok_, assert_raises
from nose.exc import SkipTest
from mock import Mock, patch
from .factory import article_factory, editor_factory
from .factory import Article, Editor, Kiosk, Entrepeneur, Newspaper
from docar import fields, Document
from docar.documents import Options
from docar.backends import DummyBackend
from docar.exceptions import ValidationError, BackendDoesNotExist
import unittest

class when_a_system_interacts_with_a_document(unittest.TestCase):
    """Test the API of the document."""

    def it_access_properties_as_members_of_the_python_object(self):
        article = article_factory()
        eq_(5, len(article._meta.local_fields))
        eq_(True, hasattr(article, 'id'))
        eq_(True, hasattr(article, 'title'))
        eq_(True, hasattr(article, 'slug'))
        eq_(True, hasattr(article, 'editor'))
        eq_(True, hasattr(article, 'category'))

    def it_sets_foreign_documents_and_collections_as_manager(self):
        kiosk = Kiosk()
        eq_(True, isinstance(kiosk.owner, Entrepeneur))
        eq_(True, isinstance(kiosk.newspaper, Newspaper))

    def it_can_create_itself_from_a_dict(self):
        """Populate a document by supplying a nested dictionary."""
        editor = Editor()
        editor_data = {'id': 23, 
           'name': 'Jules Vernes'}
        editor.from_dict(editor_data)
        eq_(23, editor.id)
        eq_('Jules Vernes', editor.name)
        article = Article()
        article_data = {'id': 42, 
           'slug': 'article-slug', 
           'title': 'article-title', 
           'editor': editor_data}
        article.from_dict(article_data)
        eq_(42, article.id)
        eq_(23, article.editor.id)
        eq_('Jules Vernes', article.editor.name)
        kiosk = Kiosk()
        kiosk.from_dict({'newspaper': [
                       {'name': 'article 1', 
                          'slug': 'article-slug', 
                          'editor': {'name': 'Jules Vernes'}, 
                          'id': 45},
                       {'name': 'article 2', 
                          'slug': 'article2-slug'}], 
           'owner': {'name': 'Johnny Cash', 
                     'cash': 50, 
                     'subscriptions': [
                                     {'newspaper': [
                                                    {'title': 'Title A', 
                                                       'slug': 'title-a', 
                                                       'editor': {'name': 'Fidel Castro'}},
                                                    {'title': 'Title A', 
                                                       'slug': 'title-a', 
                                                       'editor': {'name': 'Fidel Castro'}}]},
                                     {'newspaper': [
                                                    {'title': 'Title A', 
                                                       'slug': 'title-a', 
                                                       'editor': {'name': 'Fidel Castro'}},
                                                    {'title': 'Title B', 
                                                       'slug': 'title-b', 
                                                       'editor': {'name': 'Luiz Castro'}}]}]}})
        eq_(2, len(kiosk.newspaper.collection_set))
        eq_('Jules Vernes', kiosk.newspaper.collection_set[0].editor.name)
        eq_('Luiz Castro', kiosk.owner.subscriptions.collection_set[1].newspaper.collection_set[1].editor.name)
        eq_('Johnny Cash', kiosk.owner.name)

    def it_can_turn_the_document_into_a_dict(self):
        """Generate a dict from a document."""
        article = article_factory()
        expected = {'id': 1, 
           'slug': 'article-slug', 
           'title': 'article title', 
           'editor': {'id': 1, 
                      'name': 'Jules Vernes'}}
        eq_(expected, article.to_dict())

    def it_fetches_itself_from_a_backend(self):
        """Retrieve from the backend the document as a dict and configure."""
        data = {'id': 1, 
           'slug': 'article-slug', 
           'title': 'article title', 
           'editor': {'id': 1, 
                      'name': 'Jules Vernes'}}
        article = Article({'id': 1})
        article.fetch_title_field = Mock()
        article.fetch_title_field.return_value = 'article post fetch'
        article._meta.backend = Mock()
        article._meta.backend.fetch.return_value = data
        article.fetch(arg='some variable')
        eq_(1, article.editor.id)
        eq_('article post fetch', article.title)
        eq_('article-slug', article.slug)
        article._meta.backend.fetch.assert_called_once_with(article, arg='some variable')
        article.fetch_title_field.assert_called_once_with('article title')

    def it_can_save_the_document_to_a_backend(self):
        """Save the document to a backend."""
        data = {'id': 1, 
           'slug': 'article-slug', 
           'title': 'article post save', 
           'editor': {'id': 1, 
                      'name': 'Jules Vernes'}}
        article = article_factory()
        article.editor.security_number = 'bogus'
        article.save_title_field = Mock()
        article.save_title_field.return_value = 'article post save'
        article.validate = Mock()
        article.validate.return_value = True
        article._meta.backend = Mock()
        article.save(arg='some variable')
        article.validate.assert_called_once()
        article._meta.backend.save.assert_called_once_with(article, data, arg='some variable')
        article.save_title_field.assert_called_once_with()

    def it_can_delete_data_the_document_represents_from_a_backend(self):
        """Delete the documents real data from the backend."""
        article = article_factory()
        article._meta.backend = Mock()
        article.delete(arg='some variable')
        article._meta.backend.delete.assert_called_once_with(article, arg='some variable')

    def it_can_render_the_document_into_a_dict(self):
        """Rendering outputs a dict, that is cleaned from attributes with
        rendering off or attributes that are mapped by a render field."""
        data = {'slug': 'article-slug', 
           'title': 'article post render', 
           'editor': {'name': 'Jules Vernes'}}
        article = article_factory()
        article.render_title_field = Mock()
        article.render_title_field.return_value = 'article post render'
        out = article.render()
        eq_(data, out)
        article.render_title_field.assert_called_once_with('article title')


class when_a_document_gets_configured(unittest.TestCase):

    def it_stores_meta_configuration_in_a_object_attribute(self):
        """All options are stored in the _meta attribute."""
        article = article_factory()
        eq_(True, hasattr(article, '_meta'))
        eq_(True, isinstance(article._meta, Options))

    def it_sets_the_backend_manager_on_the_met_attribute(self):
        """The correct backend is stored as a property of _meta."""
        editor = editor_factory()
        eq_(True, hasattr(editor._meta, 'backend'))
        eq_(editor._meta.backend, editor._backend_manager)

    def it_has_a_list_of_fields_in_meta(self):
        """The document keeps a list of its properties."""
        article = article_factory()
        eq_(True, isinstance(article._meta.local_fields, list))
        for field in article._meta.local_fields:
            eq_(True, isinstance(field, fields.Field))

    def it_initializes_with_many_default_values(self):
        """Check on the default values. Changing here an assertion to fix a
        broken test, means also updating the documentation!!!"""
        article = Article()
        eq_(True, not article._meta.model)
        eq_('dummy', article._meta.backend_type)
        eq_(['id'], article._meta.identifier)
        eq_([], article._meta.excludes)
        eq_([], article._meta.context)

    def it_gets_bound_when_created_from_the_a_dict(self):
        """A instantiated document is not bound. creating the document from
        a dict, binds it."""
        data = {'id': 1, 
           'slug': 'article-slug', 
           'title': 'article title', 
           'editor': {'id': 1, 
                      'name': 'Jules Vernes'}}
        article = Article()
        eq_(False, article._bound)
        article.from_dict(data)
        eq_(True, article._bound)

    def it_converts_string_identifiers_to_a_list_of_identifiers(self):
        """Providing only a string for the identifier list, makes the string a
        list with one item."""

        class Doc(Document):
            name = fields.StringField()

            class Meta:
                identifier = 'name'

        d = Doc()
        eq_(['name'], d._meta.identifier)

    def it_stores_the_declared_fields_in_the_right_order(self):
        """Fields are stored in the order they are declared."""
        article = Article()
        eq_('id', article._meta.local_fields[0].name)
        eq_('slug', article._meta.local_fields[1].name)
        eq_('title', article._meta.local_fields[2].name)
        eq_('editor', article._meta.local_fields[3].name)


class when_a_document_wires_data_it_uses_a_backend_manager(unittest.TestCase):
    """All data can be synced with a backend, using so called backend
    managers."""

    def it_per_default_sets_the_dummy_backend_manager(self):
        """If no backend configuration is provided, the document uses the dummy
        backend manager."""
        article = article_factory()
        eq_(False, bool(article._meta.backend))
        eq_(True, isinstance(article._meta.backend, DummyBackend))

    def it_calls_the_backends_save_method_on_save(self):
        """Saving a document calls the backends save method."""
        article = article_factory()
        article._meta.backend.save = Mock()
        article._meta.backend.save.return_value = {}
        article.save(arg='value')
        article._meta.backend.save.assert_called_once_with(article, {'id': 1, 
           'slug': 'article-slug', 'title': 'article title', 'editor': {'id': 1, 'name': 'Jules Vernes'}}, arg='value')

    def it_calls_the_backends_fetch_method_on_save(self):
        """Fetching a document calls the backend fetch method."""
        article = article_factory()
        article._meta.backend.fetch = Mock()
        article._meta.backend.fetch.return_value = {}
        article.fetch(arg='value')
        article._meta.backend.fetch.assert_called_once(article, arg='value')


class when_checking_on_the_input_of_a_document(unittest.TestCase):
    """A document has possibilities for validation."""

    def it_can_use_the_documents_validator(self):
        article = article_factory()
        eq_(True, article.validate())
        article.id = ''
        assert_raises(ValidationError, article.validate)

    def it_fails_validation_if_a_referenced_foreign_document_is_required_and_does_not_exist(self):
        """The validator checks if a foreign document really exists."""
        raise SkipTest
        article = article_factory()
        article.editor._meta.backend.fetch = Mock()
        article.editor._meta.backend.fetch.side_effect = BackendDoesNotExist
        article.editor._bound = False
        assert_raises(ValidationError, article.validate)
        article.editor._meta.backend.fetch.assert_called()
        article.editor._meta.backend.fetch.reset_mock()
        article.editor._meta.backend.fetch.side_effect = None
        article.editor._bound = True
        ok_(article.validate())
        return

    def it_validates_optional_fields_that_are_not_set(self):
        """If a field is optional and not set validation still succeeds."""
        editor = editor_factory()
        article = article_factory()
        eq_(None, editor.security_number)
        ok_(editor.validate())
        eq_(True, not article.category._bound)
        ok_(article.validate())
        return


class when_documents_inherit(unittest.TestCase):
    """Documents can inherit from each other."""

    def it_can_inherit_documents_and_not_options(self):
        """Fields are inherited, options not."""

        class DocBase(Document):
            id = fields.NumberField()
            name = fields.StringField()

            class Meta:
                identifier = [
                 'name']

        class DocChild(DocBase):
            another = fields.StringField()

        base_doc = DocBase()
        child_doc = DocChild()
        eq_(['name'], base_doc._meta.identifier)
        eq_(['id'], child_doc._meta.identifier)
        eq_(2, len(base_doc._meta.local_fields))
        eq_(3, len(child_doc._meta.local_fields))


class describe_the_documents_mechanics(unittest.TestCase):
    """Test document specific quirks and internal workings."""

    def it_calls_from_dict_when_instantiated_with_data(self):
        """Providing initial data to a document, uses from_dict to parse the
        input."""
        with patch.object(Article, 'from_dict') as (mock_from):
            Article()
            Article({'id': 23})
            mock_from.assert_called_once_with({'id': 23})

    def it_can_extract_the_identifier_state_from_itself(self):
        article = article_factory()
        expected = {'id': 1}
        eq_(expected, article._identifier_state())

    def it_can_lookup_a_field_when_provided_with_a_name(self):
        """Lookup a field when given a name."""
        article = article_factory()
        field = article._field('title')
        eq_(True, isinstance(field, fields.Field))

    def it_can_set_context_to_its_referenced_documents(self):
        """When supplying context, it is also supplied to its related
        documents."""
        context = {'context': 'hello'}
        article = Article()
        eq_({}, article._context)
        eq_({}, article.editor._context)
        article._set_context(context)
        eq_(context, article._context)
        eq_(context, article.editor._context)
        with patch.object(Article, '_set_context') as (mock_setter):
            Article(context=context)
            mock_setter.assert_called_once_with(context)

    def it_can_retrieve_context_values_as_configured_in_the_meta_attribute(self):
        """Documents can retrieve their context options depending on the
        configuration in meta."""
        context = {'context': 'hello', 'context1': 'world'}
        article = Article(context=context)
        eq_(context, article._get_context())
        eq_({'context1': 'world'}, article.editor._get_context())