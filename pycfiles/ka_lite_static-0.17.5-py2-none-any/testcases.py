# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/test/testcases.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import unicode_literals
import difflib, json, os, re, socket, sys
from copy import copy
from functools import wraps
try:
    from urllib.parse import urlsplit, urlunsplit
except ImportError:
    from urlparse import urlsplit, urlunsplit

import select, socket, threading, errno
from django.conf import settings
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core import mail
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.core.handlers.wsgi import WSGIHandler
from django.core.management import call_command
from django.core.management.color import no_style
from django.core.signals import request_started
from django.core.servers.basehttp import WSGIRequestHandler, WSGIServer
from django.core.urlresolvers import clear_url_caches
from django.core.validators import EMPTY_VALUES
from django.db import transaction, connection, connections, DEFAULT_DB_ALIAS, reset_queries
from django.forms.fields import CharField
from django.http import QueryDict
from django.test import _doctest as doctest
from django.test.client import Client
from django.test.html import HTMLParseError, parse_html
from django.test.signals import template_rendered
from django.test.utils import get_warnings_state, restore_warnings_state, override_settings, compare_xml, strip_quotes
from django.test.utils import ContextList
from django.utils import unittest as ut2
from django.utils.encoding import force_text
from django.utils import six
from django.utils.unittest.util import safe_repr
from django.utils.unittest import skipIf
from django.views.static import serve
__all__ = (
 b'DocTestRunner', b'OutputChecker', b'TestCase', b'TransactionTestCase',
 b'SimpleTestCase', b'skipIfDBFeature', b'skipUnlessDBFeature')
normalize_long_ints = lambda s: re.sub(b'(?<![\\w])(\\d+)L(?![\\w])', b'\\1', s)
normalize_decimals = lambda s: re.sub(b"Decimal\\('(\\d+(\\.\\d*)?)'\\)", lambda m: b'Decimal("%s")' % m.groups()[0], s)

def to_list(value):
    """
    Puts value into a list if it's not already one.
    Returns an empty list if value is None.
    """
    if value is None:
        value = []
    elif not isinstance(value, list):
        value = [
         value]
    return value


real_commit = transaction.commit
real_rollback = transaction.rollback
real_enter_transaction_management = transaction.enter_transaction_management
real_leave_transaction_management = transaction.leave_transaction_management
real_managed = transaction.managed
real_abort = transaction.abort

def nop(*args, **kwargs):
    pass


def disable_transaction_methods():
    transaction.commit = nop
    transaction.rollback = nop
    transaction.enter_transaction_management = nop
    transaction.leave_transaction_management = nop
    transaction.managed = nop
    transaction.abort = nop


def restore_transaction_methods():
    transaction.commit = real_commit
    transaction.rollback = real_rollback
    transaction.enter_transaction_management = real_enter_transaction_management
    transaction.leave_transaction_management = real_leave_transaction_management
    transaction.managed = real_managed
    transaction.abort = real_abort


def assert_and_parse_html(self, html, user_msg, msg):
    try:
        dom = parse_html(html)
    except HTMLParseError as e:
        standardMsg = b'%s\n%s' % (msg, e.msg)
        self.fail(self._formatMessage(user_msg, standardMsg))

    return dom


class OutputChecker(doctest.OutputChecker):

    def check_output(self, want, got, optionflags):
        """
        The entry method for doctest output checking. Defers to a sequence of
        child checkers
        """
        checks = (
         self.check_output_default,
         self.check_output_numeric,
         self.check_output_xml,
         self.check_output_json)
        for check in checks:
            if check(want, got, optionflags):
                return True

        return False

    def check_output_default(self, want, got, optionflags):
        """
        The default comparator provided by doctest - not perfect, but good for
        most purposes
        """
        return doctest.OutputChecker.check_output(self, want, got, optionflags)

    def check_output_numeric(self, want, got, optionflags):
        """Doctest does an exact string comparison of output, which means that
        some numerically equivalent values aren't equal. This check normalizes
         * long integers (22L) so that they equal normal integers. (22)
         * Decimals so that they are comparable, regardless of the change
           made to __repr__ in Python 2.6.
        """
        return doctest.OutputChecker.check_output(self, normalize_decimals(normalize_long_ints(want)), normalize_decimals(normalize_long_ints(got)), optionflags)

    def check_output_xml(self, want, got, optionsflags):
        try:
            return compare_xml(want, got)
        except Exception:
            return False

    def check_output_json(self, want, got, optionsflags):
        """
        Tries to compare want and got as if they were JSON-encoded data
        """
        want, got = strip_quotes(want, got)
        try:
            want_json = json.loads(want)
            got_json = json.loads(got)
        except Exception:
            return False

        return want_json == got_json


class DocTestRunner(doctest.DocTestRunner):

    def __init__(self, *args, **kwargs):
        doctest.DocTestRunner.__init__(self, *args, **kwargs)
        self.optionflags = doctest.ELLIPSIS

    def report_unexpected_exception(self, out, test, example, exc_info):
        doctest.DocTestRunner.report_unexpected_exception(self, out, test, example, exc_info)
        for conn in connections:
            transaction.rollback_unless_managed(using=conn)


class _AssertNumQueriesContext(object):

    def __init__(self, test_case, num, connection):
        self.test_case = test_case
        self.num = num
        self.connection = connection

    def __enter__(self):
        self.old_debug_cursor = self.connection.use_debug_cursor
        self.connection.use_debug_cursor = True
        self.starting_queries = len(self.connection.queries)
        request_started.disconnect(reset_queries)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.use_debug_cursor = self.old_debug_cursor
        request_started.connect(reset_queries)
        if exc_type is not None:
            return
        else:
            final_queries = len(self.connection.queries)
            executed = final_queries - self.starting_queries
            self.test_case.assertEqual(executed, self.num, b'%d queries executed, %d expected' % (
             executed, self.num))
            return


class _AssertTemplateUsedContext(object):

    def __init__(self, test_case, template_name):
        self.test_case = test_case
        self.template_name = template_name
        self.rendered_templates = []
        self.rendered_template_names = []
        self.context = ContextList()

    def on_template_render(self, sender, signal, template, context, **kwargs):
        self.rendered_templates.append(template)
        self.rendered_template_names.append(template.name)
        self.context.append(copy(context))

    def test(self):
        return self.template_name in self.rendered_template_names

    def message(self):
        return b'%s was not rendered.' % self.template_name

    def __enter__(self):
        template_rendered.connect(self.on_template_render)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        template_rendered.disconnect(self.on_template_render)
        if exc_type is not None:
            return
        else:
            if not self.test():
                message = self.message()
                if len(self.rendered_templates) == 0:
                    message += b' No template was rendered.'
                else:
                    message += b' Following templates were rendered: %s' % (b', ').join(self.rendered_template_names)
                self.test_case.fail(message)
            return


class _AssertTemplateNotUsedContext(_AssertTemplateUsedContext):

    def test(self):
        return self.template_name not in self.rendered_template_names

    def message(self):
        return b'%s was rendered.' % self.template_name


class SimpleTestCase(ut2.TestCase):

    def __call__(self, result=None):
        """
        Wrapper around default __call__ method to perform common Django test
        set up. This means that user-defined Test Cases aren't required to
        include a call to super().setUp().
        """
        testMethod = getattr(self, self._testMethodName)
        skipped = getattr(self.__class__, b'__unittest_skip__', False) or getattr(testMethod, b'__unittest_skip__', False)
        if not skipped:
            try:
                self._pre_setup()
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception:
                result.addError(self, sys.exc_info())
                return

        super(SimpleTestCase, self).__call__(result)
        if not skipped:
            try:
                self._post_teardown()
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception:
                result.addError(self, sys.exc_info())
                return

    def _pre_setup(self):
        pass

    def _post_teardown(self):
        pass

    def save_warnings_state(self):
        """
        Saves the state of the warnings module
        """
        self._warnings_state = get_warnings_state()

    def restore_warnings_state(self):
        """
        Restores the state of the warnings module to the state
        saved by save_warnings_state()
        """
        restore_warnings_state(self._warnings_state)

    def settings(self, **kwargs):
        """
        A context manager that temporarily sets a setting and reverts
        back to the original value when exiting the context.
        """
        return override_settings(**kwargs)

    def assertRaisesMessage(self, expected_exception, expected_message, callable_obj=None, *args, **kwargs):
        """
        Asserts that the message in a raised exception matches the passed
        value.

        Args:
            expected_exception: Exception class expected to be raised.
            expected_message: expected error message string value.
            callable_obj: Function to be called.
            args: Extra args.
            kwargs: Extra kwargs.
        """
        return six.assertRaisesRegex(self, expected_exception, re.escape(expected_message), callable_obj, *args, **kwargs)

    def assertFieldOutput(self, fieldclass, valid, invalid, field_args=None, field_kwargs=None, empty_value=b''):
        """
        Asserts that a form field behaves correctly with various inputs.

        Args:
            fieldclass: the class of the field to be tested.
            valid: a dictionary mapping valid inputs to their expected
                    cleaned values.
            invalid: a dictionary mapping invalid inputs to one or more
                    raised error messages.
            field_args: the args passed to instantiate the field
            field_kwargs: the kwargs passed to instantiate the field
            empty_value: the expected clean output for inputs in EMPTY_VALUES

        """
        if field_args is None:
            field_args = []
        if field_kwargs is None:
            field_kwargs = {}
        required = fieldclass(*field_args, **field_kwargs)
        optional = fieldclass(*field_args, **dict(field_kwargs, required=False))
        for input, output in valid.items():
            self.assertEqual(required.clean(input), output)
            self.assertEqual(optional.clean(input), output)

        for input, errors in invalid.items():
            with self.assertRaises(ValidationError) as (context_manager):
                required.clean(input)
            self.assertEqual(context_manager.exception.messages, errors)
            with self.assertRaises(ValidationError) as (context_manager):
                optional.clean(input)
            self.assertEqual(context_manager.exception.messages, errors)

        error_required = [force_text(required.error_messages[b'required'])]
        for e in EMPTY_VALUES:
            with self.assertRaises(ValidationError) as (context_manager):
                required.clean(e)
            self.assertEqual(context_manager.exception.messages, error_required)
            self.assertEqual(optional.clean(e), empty_value)

        if issubclass(fieldclass, CharField):
            field_kwargs.update({b'min_length': 2, b'max_length': 20})
            self.assertTrue(isinstance(fieldclass(*field_args, **field_kwargs), fieldclass))
        return

    def assertHTMLEqual(self, html1, html2, msg=None):
        """
        Asserts that two HTML snippets are semantically the same.
        Whitespace in most cases is ignored, and attribute ordering is not
        significant. The passed-in arguments must be valid HTML.
        """
        dom1 = assert_and_parse_html(self, html1, msg, b'First argument is not valid HTML:')
        dom2 = assert_and_parse_html(self, html2, msg, b'Second argument is not valid HTML:')
        if dom1 != dom2:
            standardMsg = b'%s != %s' % (
             safe_repr(dom1, True), safe_repr(dom2, True))
            diff = b'\n' + (b'\n').join(difflib.ndiff(six.text_type(dom1).splitlines(), six.text_type(dom2).splitlines()))
            standardMsg = self._truncateMessage(standardMsg, diff)
            self.fail(self._formatMessage(msg, standardMsg))

    def assertHTMLNotEqual(self, html1, html2, msg=None):
        """Asserts that two HTML snippets are not semantically equivalent."""
        dom1 = assert_and_parse_html(self, html1, msg, b'First argument is not valid HTML:')
        dom2 = assert_and_parse_html(self, html2, msg, b'Second argument is not valid HTML:')
        if dom1 == dom2:
            standardMsg = b'%s == %s' % (
             safe_repr(dom1, True), safe_repr(dom2, True))
            self.fail(self._formatMessage(msg, standardMsg))

    def assertInHTML(self, needle, haystack, count=None, msg_prefix=b''):
        needle = assert_and_parse_html(self, needle, None, b'First argument is not valid HTML:')
        haystack = assert_and_parse_html(self, haystack, None, b'Second argument is not valid HTML:')
        real_count = haystack.count(needle)
        if count is not None:
            self.assertEqual(real_count, count, msg_prefix + b"Found %d instances of '%s' in response (expected %d)" % (
             real_count, needle, count))
        else:
            self.assertTrue(real_count != 0, msg_prefix + b"Couldn't find '%s' in response" % needle)
        return

    def assertJSONEqual(self, raw, expected_data, msg=None):
        try:
            data = json.loads(raw)
        except ValueError:
            self.fail(b'First argument is not valid JSON: %r' % raw)

        if isinstance(expected_data, six.string_types):
            try:
                expected_data = json.loads(expected_data)
            except ValueError:
                self.fail(b'Second argument is not valid JSON: %r' % expected_data)

        self.assertEqual(data, expected_data, msg=msg)

    def assertXMLEqual(self, xml1, xml2, msg=None):
        """
        Asserts that two XML snippets are semantically the same.
        Whitespace in most cases is ignored, and attribute ordering is not
        significant. The passed-in arguments must be valid XML.
        """
        try:
            result = compare_xml(xml1, xml2)
        except Exception as e:
            standardMsg = b'First or second argument is not valid XML\n%s' % e
            self.fail(self._formatMessage(msg, standardMsg))

        if not result:
            standardMsg = b'%s != %s' % (safe_repr(xml1, True), safe_repr(xml2, True))
            self.fail(self._formatMessage(msg, standardMsg))

    def assertXMLNotEqual(self, xml1, xml2, msg=None):
        """
        Asserts that two XML snippets are not semantically equivalent.
        Whitespace in most cases is ignored, and attribute ordering is not
        significant. The passed-in arguments must be valid XML.
        """
        try:
            result = compare_xml(xml1, xml2)
        except Exception as e:
            standardMsg = b'First or second argument is not valid XML\n%s' % e
            self.fail(self._formatMessage(msg, standardMsg))

        if result:
            standardMsg = b'%s == %s' % (safe_repr(xml1, True), safe_repr(xml2, True))
            self.fail(self._formatMessage(msg, standardMsg))


class TransactionTestCase(SimpleTestCase):
    client_class = Client
    reset_sequences = False

    def _pre_setup(self):
        """Performs any pre-test setup. This includes:

            * Flushing the database.
            * If the Test Case class has a 'fixtures' member, installing the
              named fixtures.
            * If the Test Case class has a 'urls' member, replace the
              ROOT_URLCONF with it.
            * Clearing the mail test outbox.
        """
        self.client = self.client_class()
        self._fixture_setup()
        self._urlconf_setup()
        mail.outbox = []

    def _databases_names(self, include_mirrors=True):
        if getattr(self, b'multi_db', False):
            return [ alias for alias in connections if include_mirrors or not connections[alias].settings_dict[b'TEST_MIRROR']
                   ]
        else:
            return [
             DEFAULT_DB_ALIAS]

    def _reset_sequences(self, db_name):
        conn = connections[db_name]
        if conn.features.supports_sequence_reset:
            sql_list = conn.ops.sequence_reset_by_name_sql(no_style(), conn.introspection.sequence_list())
            if sql_list:
                try:
                    cursor = conn.cursor()
                    for sql in sql_list:
                        cursor.execute(sql)

                except Exception:
                    transaction.rollback_unless_managed(using=db_name)
                    raise

                transaction.commit_unless_managed(using=db_name)

    def _fixture_setup(self):
        for db_name in self._databases_names(include_mirrors=False):
            if self.reset_sequences:
                self._reset_sequences(db_name)
            if hasattr(self, b'fixtures'):
                call_command(b'loaddata', *self.fixtures, **{b'verbosity': 0, b'database': db_name, b'skip_validation': True})

    def _urlconf_setup(self):
        if hasattr(self, b'urls'):
            self._old_root_urlconf = settings.ROOT_URLCONF
            settings.ROOT_URLCONF = self.urls
            clear_url_caches()

    def _post_teardown(self):
        """ Performs any post-test things. This includes:

            * Putting back the original ROOT_URLCONF if it was changed.
            * Force closing the connection, so that the next test gets
              a clean cursor.
        """
        self._fixture_teardown()
        self._urlconf_teardown()
        for conn in connections.all():
            conn.close()

    def _fixture_teardown(self):
        for conn in connections.all():
            conn.rollback_unless_managed()

        for db in self._databases_names(include_mirrors=False):
            call_command(b'flush', verbosity=0, interactive=False, database=db, skip_validation=True, reset_sequences=False)

    def _urlconf_teardown(self):
        if hasattr(self, b'_old_root_urlconf'):
            settings.ROOT_URLCONF = self._old_root_urlconf
            clear_url_caches()

    def assertRedirects(self, response, expected_url, status_code=302, target_status_code=200, host=None, msg_prefix=b''):
        """Asserts that a response redirected to a specific URL, and that the
        redirect URL can be loaded.

        Note that assertRedirects won't work for external links since it uses
        TestClient to do a request.
        """
        if msg_prefix:
            msg_prefix += b': '
        if hasattr(response, b'redirect_chain'):
            self.assertTrue(len(response.redirect_chain) > 0, msg_prefix + b"Response didn't redirect as expected: Response code was %d (expected %d)" % (
             response.status_code, status_code))
            self.assertEqual(response.redirect_chain[0][1], status_code, msg_prefix + b"Initial response didn't redirect as expected: Response code was %d (expected %d)" % (
             response.redirect_chain[0][1], status_code))
            url, status_code = response.redirect_chain[(-1)]
            self.assertEqual(response.status_code, target_status_code, msg_prefix + b"Response didn't redirect as expected: Final Response code was %d (expected %d)" % (
             response.status_code, target_status_code))
        else:
            self.assertEqual(response.status_code, status_code, msg_prefix + b"Response didn't redirect as expected: Response code was %d (expected %d)" % (
             response.status_code, status_code))
            url = response[b'Location']
            scheme, netloc, path, query, fragment = urlsplit(url)
            redirect_response = response.client.get(path, QueryDict(query))
            self.assertEqual(redirect_response.status_code, target_status_code, msg_prefix + b"Couldn't retrieve redirection page '%s': response code was %d (expected %d)" % (
             path, redirect_response.status_code, target_status_code))
        e_scheme, e_netloc, e_path, e_query, e_fragment = urlsplit(expected_url)
        if not (e_scheme or e_netloc):
            expected_url = urlunsplit((b'http', host or b'testserver', e_path,
             e_query, e_fragment))
        self.assertEqual(url, expected_url, msg_prefix + b"Response redirected to '%s', expected '%s'" % (
         url, expected_url))

    def assertContains(self, response, text, count=None, status_code=200, msg_prefix=b'', html=False):
        """
        Asserts that a response indicates that some content was retrieved
        successfully, (i.e., the HTTP status code was as expected), and that
        ``text`` occurs ``count`` times in the content of the response.
        If ``count`` is None, the count doesn't matter - the assertion is true
        if the text occurs at least once in the response.
        """
        if hasattr(response, b'render') and callable(response.render) and not response.is_rendered:
            response.render()
        if msg_prefix:
            msg_prefix += b': '
        self.assertEqual(response.status_code, status_code, msg_prefix + b"Couldn't retrieve content: Response code was %d (expected %d)" % (
         response.status_code, status_code))
        if response.streaming:
            content = (b'').join(response.streaming_content)
        else:
            content = response.content
        if not isinstance(text, bytes) or html:
            text = force_text(text, encoding=response._charset)
            content = content.decode(response._charset)
            text_repr = b"'%s'" % text
        else:
            text_repr = repr(text)
        if html:
            content = assert_and_parse_html(self, content, None, b"Response's content is not valid HTML:")
            text = assert_and_parse_html(self, text, None, b'Second argument is not valid HTML:')
        real_count = content.count(text)
        if count is not None:
            self.assertEqual(real_count, count, msg_prefix + b'Found %d instances of %s in response (expected %d)' % (
             real_count, text_repr, count))
        else:
            self.assertTrue(real_count != 0, msg_prefix + b"Couldn't find %s in response" % text_repr)
        return

    def assertNotContains(self, response, text, status_code=200, msg_prefix=b'', html=False):
        """
        Asserts that a response indicates that some content was retrieved
        successfully, (i.e., the HTTP status code was as expected), and that
        ``text`` doesn't occurs in the content of the response.
        """
        if hasattr(response, b'render') and callable(response.render) and not response.is_rendered:
            response.render()
        if msg_prefix:
            msg_prefix += b': '
        self.assertEqual(response.status_code, status_code, msg_prefix + b"Couldn't retrieve content: Response code was %d (expected %d)" % (
         response.status_code, status_code))
        content = response.content
        if not isinstance(text, bytes) or html:
            text = force_text(text, encoding=response._charset)
            content = content.decode(response._charset)
            text_repr = b"'%s'" % text
        else:
            text_repr = repr(text)
        if html:
            content = assert_and_parse_html(self, content, None, b"Response's content is not valid HTML:")
            text = assert_and_parse_html(self, text, None, b'Second argument is not valid HTML:')
        self.assertEqual(content.count(text), 0, msg_prefix + b'Response should not contain %s' % text_repr)
        return

    def assertFormError(self, response, form, field, errors, msg_prefix=b''):
        """
        Asserts that a form used to render the response has a specific field
        error.
        """
        if msg_prefix:
            msg_prefix += b': '
        contexts = to_list(response.context)
        if not contexts:
            self.fail(msg_prefix + b'Response did not use any contexts to render the response')
        errors = to_list(errors)
        found_form = False
        for i, context in enumerate(contexts):
            if form not in context:
                continue
            found_form = True
            for err in errors:
                if field:
                    if field in context[form].errors:
                        field_errors = context[form].errors[field]
                        self.assertTrue(err in field_errors, msg_prefix + b"The field '%s' on form '%s' in context %d does not contain the error '%s' (actual errors: %s)" % (
                         field, form, i, err, repr(field_errors)))
                    elif field in context[form].fields:
                        self.fail(msg_prefix + b"The field '%s' on form '%s' in context %d contains no errors" % (
                         field, form, i))
                    else:
                        self.fail(msg_prefix + b"The form '%s' in context %d does not contain the field '%s'" % (
                         form, i, field))
                else:
                    non_field_errors = context[form].non_field_errors()
                    self.assertTrue(err in non_field_errors, msg_prefix + b"The form '%s' in context %d does not contain the non-field error '%s' (actual errors: %s)" % (
                     form, i, err, non_field_errors))

        if not found_form:
            self.fail(msg_prefix + b"The form '%s' was not used to render the response" % form)

    def assertTemplateUsed(self, response=None, template_name=None, msg_prefix=b''):
        """
        Asserts that the template with the provided name was used in rendering
        the response. Also usable as context manager.
        """
        if response is None and template_name is None:
            raise TypeError(b'response and/or template_name argument must be provided')
        if msg_prefix:
            msg_prefix += b': '
        if not hasattr(response, b'templates') or response is None and template_name:
            if response:
                template_name = response
                response = None
            context = _AssertTemplateUsedContext(self, template_name)
            return context
        else:
            template_names = [ t.name for t in response.templates ]
            if not template_names:
                self.fail(msg_prefix + b'No templates used to render the response')
            self.assertTrue(template_name in template_names, msg_prefix + b"Template '%s' was not a template used to render the response. Actual template(s) used: %s" % (
             template_name, (b', ').join(template_names)))
            return

    def assertTemplateNotUsed(self, response=None, template_name=None, msg_prefix=b''):
        """
        Asserts that the template with the provided name was NOT used in
        rendering the response. Also usable as context manager.
        """
        if response is None and template_name is None:
            raise TypeError(b'response and/or template_name argument must be provided')
        if msg_prefix:
            msg_prefix += b': '
        if not hasattr(response, b'templates') or response is None and template_name:
            if response:
                template_name = response
                response = None
            context = _AssertTemplateNotUsedContext(self, template_name)
            return context
        else:
            template_names = [ t.name for t in response.templates ]
            self.assertFalse(template_name in template_names, msg_prefix + b"Template '%s' was used unexpectedly in rendering the response" % template_name)
            return

    def assertQuerysetEqual(self, qs, values, transform=repr, ordered=True):
        items = six.moves.map(transform, qs)
        if not ordered:
            return self.assertEqual(set(items), set(values))
        return self.assertEqual(list(items), values)

    def assertNumQueries(self, num, func=None, *args, **kwargs):
        using = kwargs.pop(b'using', DEFAULT_DB_ALIAS)
        conn = connections[using]
        context = _AssertNumQueriesContext(self, num, conn)
        if func is None:
            return context
        else:
            with context:
                func(*args, **kwargs)
            return


def connections_support_transactions():
    """
    Returns True if all connections support transactions.
    """
    return all(conn.features.supports_transactions for conn in connections.all())


class TestCase(TransactionTestCase):
    """
    Does basically the same as TransactionTestCase, but surrounds every test
    with a transaction, monkey-patches the real transaction management routines
    to do nothing, and rollsback the test transaction at the end of the test.
    You have to use TransactionTestCase, if you need transaction management
    inside a test.
    """

    def _fixture_setup(self):
        if not connections_support_transactions():
            return super(TestCase, self)._fixture_setup()
        assert not self.reset_sequences, b'reset_sequences cannot be used on TestCase instances'
        for db_name in self._databases_names():
            transaction.enter_transaction_management(using=db_name)
            transaction.managed(True, using=db_name)

        disable_transaction_methods()
        from django.contrib.sites.models import Site
        Site.objects.clear_cache()
        for db in self._databases_names(include_mirrors=False):
            if hasattr(self, b'fixtures'):
                call_command(b'loaddata', *self.fixtures, **{b'verbosity': 0, 
                   b'commit': False, 
                   b'database': db, 
                   b'skip_validation': True})

    def _fixture_teardown(self):
        if not connections_support_transactions():
            return super(TestCase, self)._fixture_teardown()
        restore_transaction_methods()
        for db in self._databases_names():
            transaction.rollback(using=db)
            transaction.leave_transaction_management(using=db)


def _deferredSkip(condition, reason):

    def decorator(test_func):
        if not (isinstance(test_func, type) and issubclass(test_func, TestCase)):

            @wraps(test_func)
            def skip_wrapper(*args, **kwargs):
                if condition():
                    raise ut2.SkipTest(reason)
                return test_func(*args, **kwargs)

            test_item = skip_wrapper
        else:
            test_item = test_func
        test_item.__unittest_skip_why__ = reason
        return test_item

    return decorator


def skipIfDBFeature(feature):
    """
    Skip a test if a database has the named feature
    """
    return _deferredSkip(lambda : getattr(connection.features, feature), b'Database has feature %s' % feature)


def skipUnlessDBFeature(feature):
    """
    Skip a test unless a database has the named feature
    """
    return _deferredSkip(lambda : not getattr(connection.features, feature), b"Database doesn't support feature %s" % feature)


class QuietWSGIRequestHandler(WSGIRequestHandler):
    """
    Just a regular WSGIRequestHandler except it doesn't log to the standard
    output any of the requests received, so as to not clutter the output for
    the tests' results.
    """

    def log_message(*args):
        pass


if sys.version_info >= (3, 3, 0):
    _ImprovedEvent = threading.Event
elif sys.version_info >= (2, 7, 0):
    _ImprovedEvent = threading._Event
else:

    class _ImprovedEvent(threading._Event):
        """
        Does the same as `threading.Event` except it overrides the wait() method
        with some code borrowed from Python 2.7 to return the set state of the
        event (see: http://hg.python.org/cpython/rev/b5aa8aa78c0f/). This allows
        to know whether the wait() method exited normally or because of the
        timeout. This class can be removed when Django supports only Python >= 2.7.
        """

        def wait(self, timeout=None):
            self._Event__cond.acquire()
            try:
                if not self._Event__flag:
                    self._Event__cond.wait(timeout)
                return self._Event__flag
            finally:
                self._Event__cond.release()


class StoppableWSGIServer(WSGIServer):
    """
    The code in this class is borrowed from the `SocketServer.BaseServer` class
    in Python 2.6. The important functionality here is that the server is non-
    blocking and that it can be shut down at any moment. This is made possible
    by the server regularly polling the socket and checking if it has been
    asked to stop.
    Note for the future: Once Django stops supporting Python 2.6, this class
    can be removed as `WSGIServer` will have this ability to shutdown on
    demand and will not require the use of the _ImprovedEvent class whose code
    is borrowed from Python 2.7.
    """

    def __init__(self, *args, **kwargs):
        super(StoppableWSGIServer, self).__init__(*args, **kwargs)
        self.__is_shut_down = _ImprovedEvent()
        self.__serving = False

    def serve_forever(self, poll_interval=0.5):
        """
        Handle one request at a time until shutdown.

        Polls for shutdown every poll_interval seconds.
        """
        self.__serving = True
        self.__is_shut_down.clear()
        while self.__serving:
            r, w, e = select.select([self], [], [], poll_interval)
            if r:
                self._handle_request_noblock()

        self.__is_shut_down.set()

    def shutdown(self):
        """
        Stops the serve_forever loop.

        Blocks until the loop has finished. This must be called while
        serve_forever() is running in another thread, or it will
        deadlock.
        """
        self.__serving = False
        if not self.__is_shut_down.wait(2):
            raise RuntimeError(b'Failed to shutdown the live test server in 2 seconds. The server might be stuck or generating a slow response.')

    def handle_request(self):
        """Handle one request, possibly blocking.
        """
        fd_sets = select.select([self], [], [], None)
        if not fd_sets[0]:
            return
        else:
            self._handle_request_noblock()
            return

    def _handle_request_noblock(self):
        """
        Handle one request, without blocking.

        I assume that select.select has returned that the socket is
        readable before this function was called, so there should be
        no risk of blocking in get_request().
        """
        try:
            request, client_address = self.get_request()
        except socket.error:
            return

        if self.verify_request(request, client_address):
            try:
                self.process_request(request, client_address)
            except Exception:
                self.handle_error(request, client_address)
                self.close_request(request)


class _MediaFilesHandler(StaticFilesHandler):
    """
    Handler for serving the media files. This is a private class that is
    meant to be used solely as a convenience by LiveServerThread.
    """

    def get_base_dir(self):
        return settings.MEDIA_ROOT

    def get_base_url(self):
        return settings.MEDIA_URL

    def serve(self, request):
        relative_url = request.path[len(self.base_url[2]):]
        return serve(request, relative_url, document_root=self.get_base_dir())


class LiveServerThread(threading.Thread):
    """
    Thread for running a live http server while the tests are running.
    """

    def __init__(self, host, possible_ports, connections_override=None):
        self.host = host
        self.port = None
        self.possible_ports = possible_ports
        self.is_ready = threading.Event()
        self.error = None
        self.connections_override = connections_override
        super(LiveServerThread, self).__init__()
        return

    def run(self):
        """
        Sets up the live server and databases, and then loops over handling
        http requests.
        """
        if self.connections_override:
            from django.db import connections
            for alias, conn in self.connections_override.items():
                connections[alias] = conn

        try:
            handler = StaticFilesHandler(_MediaFilesHandler(WSGIHandler()))
            for index, port in enumerate(self.possible_ports):
                try:
                    self.httpd = StoppableWSGIServer((
                     self.host, port), QuietWSGIRequestHandler)
                except socket.error as e:
                    if index + 1 < len(self.possible_ports) and e.errno == errno.EADDRINUSE:
                        continue
                    else:
                        raise
                else:
                    self.port = port
                    break

            self.httpd.set_app(handler)
            self.is_ready.set()
            self.httpd.serve_forever()
        except Exception as e:
            self.error = e
            self.is_ready.set()

    def join(self, timeout=None):
        if hasattr(self, b'httpd'):
            self.httpd.shutdown()
            self.httpd.server_close()
        super(LiveServerThread, self).join(timeout)


class LiveServerTestCase(TransactionTestCase):
    """
    Does basically the same as TransactionTestCase but also launches a live
    http server in a separate thread so that the tests may use another testing
    framework, such as Selenium for example, instead of the built-in dummy
    client.
    Note that it inherits from TransactionTestCase instead of TestCase because
    the threads do not share the same transactions (unless if using in-memory
    sqlite) and each thread needs to commit all their transactions so that the
    other thread can see the changes.
    """

    @property
    def live_server_url(self):
        return b'http://%s:%s' % (
         self.server_thread.host, self.server_thread.port)

    @classmethod
    def setUpClass(cls):
        connections_override = {}
        for conn in connections.all():
            if conn.settings_dict[b'ENGINE'].rsplit(b'.', 1)[(-1)] in ('sqlite3', 'spatialite') and conn.settings_dict[b'NAME'] == b':memory:':
                conn.allow_thread_sharing = True
                connections_override[conn.alias] = conn

        specified_address = os.environ.get(b'DJANGO_LIVE_TEST_SERVER_ADDRESS', b'localhost:8081')
        possible_ports = []
        try:
            host, port_ranges = specified_address.split(b':')
            for port_range in port_ranges.split(b','):
                extremes = list(map(int, port_range.split(b'-')))
                assert len(extremes) in (1, 2)
                if len(extremes) == 1:
                    possible_ports.append(extremes[0])
                else:
                    for port in range(extremes[0], extremes[1] + 1):
                        possible_ports.append(port)

        except Exception:
            raise ImproperlyConfigured(b'Invalid address ("%s") for live server.' % specified_address)

        cls.server_thread = LiveServerThread(host, possible_ports, connections_override)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        cls.server_thread.is_ready.wait()
        if cls.server_thread.error:
            cls._tearDownClassInternal()
            raise cls.server_thread.error
        super(LiveServerTestCase, cls).setUpClass()

    @classmethod
    def _tearDownClassInternal(cls):
        if hasattr(cls, b'server_thread'):
            cls.server_thread.join()
        for conn in connections.all():
            if conn.settings_dict[b'ENGINE'].rsplit(b'.', 1)[(-1)] in ('sqlite3', 'spatialite') and conn.settings_dict[b'NAME'] == b':memory:':
                conn.allow_thread_sharing = False

    @classmethod
    def tearDownClass(cls):
        cls._tearDownClassInternal()
        super(LiveServerTestCase, cls).tearDownClass()