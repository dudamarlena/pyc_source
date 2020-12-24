# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/kgb/tests/test_spy_agency.py
# Compiled at: 2020-04-10 23:22:42
"""Unit tests for kgb.agency.SpyAgency."""
from __future__ import unicode_literals
from contextlib import contextmanager
from kgb.agency import SpyAgency
from kgb.tests.base import MathClass, TestCase

class SpyAgencyTests(TestCase):
    """Unit tests for kgb.agency.SpyAgency."""

    def test_spy_on(self):
        """Testing SpyAgency.spy_on"""
        obj = MathClass()
        spy = self.agency.spy_on(obj.do_math)
        self.assertEqual(self.agency.spies, set([spy]))

    def test_unspy(self):
        """Testing SpyAgency.unspy"""
        obj = MathClass()
        orig_do_math = obj.do_math
        spy = self.agency.spy_on(obj.do_math)
        self.assertEqual(self.agency.spies, set([spy]))
        self.assertTrue(hasattr(obj.do_math, b'spy'))
        self.agency.unspy(obj.do_math)
        self.assertEqual(self.agency.spies, set())
        self.assertFalse(hasattr(obj.do_math, b'spy'))
        self.assertEqual(obj.do_math, orig_do_math)

    def test_unspy_all(self):
        """Testing SpyAgency.unspy_all"""
        obj = MathClass()
        orig_do_math = obj.do_math
        spy1 = self.agency.spy_on(obj.do_math)
        spy2 = self.agency.spy_on(MathClass.class_do_math)
        self.assertEqual(self.agency.spies, set([spy1, spy2]))
        self.assertTrue(hasattr(obj.do_math, b'spy'))
        self.assertTrue(hasattr(MathClass.class_do_math, b'spy'))
        self.agency.unspy_all()
        self.assertEqual(self.agency.spies, [])
        self.assertEqual(obj.do_math, orig_do_math)
        self.assertEqual(MathClass.class_do_math, self.orig_class_do_math)
        self.assertFalse(hasattr(obj.do_math, b'spy'))
        self.assertFalse(hasattr(MathClass.class_do_math, b'spy'))


class TestCaseMixinTests(SpyAgency, TestCase):
    """Unit tests for SpyAgency as a TestCase mixin."""

    def test_spy_on(self):
        """Testing SpyAgency mixed in with spy_on"""
        obj = MathClass()
        self.spy_on(obj.do_math)
        self.assertTrue(hasattr(obj.do_math, b'spy'))
        result = obj.do_math()
        self.assertEqual(result, 3)

    def test_tear_down(self):
        """Testing SpyAgency mixed in with tearDown"""
        obj = MathClass()
        orig_do_math = obj.do_math
        func_dict = obj.do_math.__dict__.copy()
        self.spy_on(obj.do_math)
        self.assertTrue(hasattr(obj.do_math, b'spy'))
        self.assertNotEqual(func_dict, obj.do_math.__dict__)
        self.tearDown()
        self.assertEqual(obj.do_math, orig_do_math)
        self.assertFalse(hasattr(obj.do_math, b'spy'))
        self.assertEqual(func_dict, obj.do_math.__dict__)

    def test_assertHasSpy_with_spy(self):
        """Testing SpyAgency.assertHasSpy with spy"""
        self.spy_on(MathClass.do_math, owner=MathClass)
        self.assertHasSpy(MathClass.do_math)
        self.assertHasSpy(MathClass.do_math.spy)

    def test_assertHasSpy_without_spy(self):
        """Testing SpyAgency.assertHasSpy without spy"""
        with self._check_assertion(b'do_math has not been spied on.'):
            self.assertHasSpy(MathClass.do_math)

    def test_assertSpyCalled_with_called(self):
        """Testing SpyAgency.assertSpyCalled with spy called"""
        obj = MathClass()
        self.spy_on(obj.do_math)
        obj.do_math()
        self.assertSpyCalled(obj.do_math)
        self.assertSpyCalled(obj.do_math.spy)

    def test_assertSpyCalled_without_called(self):
        """Testing SpyAgency.assertSpyCalled without spy called"""
        obj = MathClass()
        self.spy_on(obj.do_math)
        msg = b'do_math was not called.'
        with self._check_assertion(msg):
            self.assertSpyCalled(obj.do_math)
        with self._check_assertion(msg):
            self.assertSpyCalled(obj.do_math.spy)

    def test_assertSpyNotCalled_without_called(self):
        """Testing SpyAgency.assertSpyNotCalled without spy called"""
        obj = MathClass()
        self.spy_on(obj.do_math)
        self.assertSpyNotCalled(obj.do_math)
        self.assertSpyNotCalled(obj.do_math.spy)

    def test_assertSpyNotCalled_with_called(self):
        """Testing SpyAgency.assertSpyNotCalled with spy called"""
        obj = MathClass()
        self.spy_on(obj.do_math)
        obj.do_math(3, b=4)
        obj.do_math(2, b=9)
        msg = b"do_math was called 2 times:\n\nCall 0:\n  args=()\n  kwargs={'a': 3, 'b': 4}\n\nCall 1:\n  args=()\n  kwargs={'a': 2, 'b': 9}"
        with self._check_assertion(msg):
            self.assertSpyNotCalled(obj.do_math)
        with self._check_assertion(msg):
            self.assertSpyNotCalled(obj.do_math.spy)

    def test_assertSpyCallCount_with_expected_count(self):
        """Testing SpyAgency.assertSpyCallCount with expected call count"""
        obj = MathClass()
        self.spy_on(obj.do_math)
        obj.do_math()
        obj.do_math()
        self.assertSpyCallCount(obj.do_math, 2)
        self.assertSpyCallCount(obj.do_math.spy, 2)

    def test_assertSpyCallCount_without_expected_count(self):
        """Testing SpyAgency.assertSpyCallCount without expected call count"""
        obj = MathClass()
        self.spy_on(obj.do_math)
        obj.do_math()
        with self._check_assertion(b'do_math was called 1 time, not 2.'):
            self.assertSpyCallCount(obj.do_math, 2)
        obj.do_math()
        with self._check_assertion(b'do_math was called 2 times, not 3.'):
            self.assertSpyCallCount(obj.do_math.spy, 3)

    def test_assertSpyCalledWith_with_expected_arguments(self):
        """Testing SpyAgency.assertSpyCalledWith with expected arguments"""
        obj = MathClass()
        self.spy_on(obj.do_math)
        obj.do_math(1, b=4)
        obj.do_math(2, b=9)
        self.assertSpyCalledWith(obj.do_math, a=1, b=4)
        self.assertSpyCalledWith(obj.do_math.calls[0], a=1, b=4)
        self.assertSpyCalledWith(obj.do_math.spy, a=2, b=9)
        self.assertSpyCalledWith(obj.do_math.spy.calls[1], a=2, b=9)

    def test_assertSpyCalledWith_without_expected_arguments(self):
        """Testing SpyAgency.assertSpyCalledWith without expected arguments"""
        obj = MathClass()
        self.spy_on(obj.do_math)
        obj.do_math(1, b=4)
        obj.do_math(2, b=9)
        msg = b"No call to do_math was passed args=(), kwargs={'x': 4, 'z': 1}.\n\nThe following calls were recorded:\n\nCall 0:\n  args=()\n  kwargs={'a': 1, 'b': 4}\n\nCall 1:\n  args=()\n  kwargs={'a': 2, 'b': 9}"
        with self._check_assertion(msg):
            self.assertSpyCalledWith(obj.do_math, x=4, z=1)
        with self._check_assertion(msg):
            self.assertSpyCalledWith(obj.do_math.spy, x=4, z=1)
        msg = b"This call to do_math was not passed args=(), kwargs={'x': 4, 'z': 1}.\n\nIt was called with:\n\nargs=()\nkwargs={'a': 1, 'b': 4}"
        with self._check_assertion(msg):
            self.assertSpyCalledWith(obj.do_math.spy.calls[0], x=4, z=1)

    def test_assertSpyLastCalledWith_with_expected_arguments(self):
        """Testing SpyAgency.assertSpyLastCalledWith with expected arguments"""
        obj = MathClass()
        self.spy_on(obj.do_math)
        obj.do_math(1, b=4)
        obj.do_math(2, b=9)
        self.assertSpyLastCalledWith(obj.do_math, a=2, b=9)
        self.assertSpyLastCalledWith(obj.do_math.spy, a=2, b=9)

    def test_assertSpyLastCalledWith_without_expected_arguments(self):
        """Testing SpyAgency.assertSpyLastCalledWith without expected
        arguments
        """
        obj = MathClass()
        self.spy_on(obj.do_math)
        obj.do_math(1, b=4)
        obj.do_math(2, b=9)
        msg = b"The last call to do_math was not passed args=(), kwargs={'a': 1, 'b': 4}.\n\nIt was last called with:\n\nargs=()\nkwargs={'a': 2, 'b': 9}"
        with self._check_assertion(msg):
            self.assertSpyLastCalledWith(obj.do_math, a=1, b=4)
        with self._check_assertion(msg):
            self.assertSpyLastCalledWith(obj.do_math.spy, a=1, b=4)

    def test_assertSpyReturned_with_expected_return(self):
        """Testing SpyAgency.assertSpyReturned with expected return value"""
        obj = MathClass()
        self.spy_on(obj.do_math)
        obj.do_math(1, b=4)
        obj.do_math(2, b=9)
        self.assertSpyReturned(obj.do_math, 5)
        self.assertSpyReturned(obj.do_math.calls[0], 5)
        self.assertSpyReturned(obj.do_math.spy, 11)
        self.assertSpyReturned(obj.do_math.spy.calls[1], 11)

    def test_assertSpyReturned_without_expected_return(self):
        """Testing SpyAgency.assertSpyReturned without expected return value"""
        obj = MathClass()
        self.spy_on(obj.do_math)
        obj.do_math(1, b=4)
        obj.do_math(2, b=9)
        msg = b'No call to do_math returned 100.\n\nThe following values have been returned:\n\nCall 0:\n  5\n\nCall 1:\n  11'
        with self._check_assertion(msg):
            self.assertSpyReturned(obj.do_math, 100)
        with self._check_assertion(msg):
            self.assertSpyReturned(obj.do_math.spy, 100)
        msg = b'This call to do_math did not return 100.\n\nIt returned:\n\n5'
        with self._check_assertion(msg):
            self.assertSpyReturned(obj.do_math.calls[0], 100)

    def test_assertSpyLastReturned_with_expected_return(self):
        """Testing SpyAgency.assertSpyLastReturned with expected return value
        """
        obj = MathClass()
        self.spy_on(obj.do_math)
        obj.do_math(1, b=4)
        obj.do_math(2, b=9)
        self.assertSpyLastReturned(obj.do_math, 11)
        self.assertSpyLastReturned(obj.do_math.spy, 11)

    def test_assertSpyLastReturned_without_expected_return(self):
        """Testing SpyAgency.assertSpyLastReturned without expected return
        value
        """
        obj = MathClass()
        self.spy_on(obj.do_math)
        obj.do_math(1, b=4)
        obj.do_math(2, b=9)
        msg = b'The last call to do_math did not return 5.\n\nIt last returned:\n\n11'
        with self._check_assertion(msg):
            self.assertSpyLastReturned(obj.do_math, 5)
        with self._check_assertion(msg):
            self.assertSpyLastReturned(obj.do_math.spy, 5)

    def test_assertSpyRaised_with_expected_exception(self):
        """Testing SpyAgency.assertSpyRaised with expected exception raised"""

        def _do_math(_self, a, *args, **kwargs):
            if a == 1:
                raise KeyError
            elif a == 2:
                raise ValueError

        obj = MathClass()
        self.spy_on(obj.do_math, call_fake=_do_math)
        try:
            obj.do_math(1)
        except KeyError:
            pass

        try:
            obj.do_math(2)
        except ValueError:
            pass

        self.assertSpyRaised(obj.do_math, KeyError)
        self.assertSpyRaised(obj.do_math.calls[0], KeyError)
        self.assertSpyRaised(obj.do_math.spy, ValueError)
        self.assertSpyRaised(obj.do_math.spy.calls[1], ValueError)

    def test_assertSpyRaised_with_expected_no_exception(self):
        """Testing SpyAgency.assertSpyRaised with expected completions without
        exceptions
        """
        obj = MathClass()
        self.spy_on(obj.do_math)
        obj.do_math(1)
        obj.do_math(2)
        self.assertSpyRaised(obj.do_math, None)
        self.assertSpyRaised(obj.do_math.calls[0], None)
        self.assertSpyRaised(obj.do_math.spy, None)
        self.assertSpyRaised(obj.do_math.spy.calls[1], None)
        return

    def test_assertSpyRaised_without_expected_exception(self):
        """Testing SpyAgency.assertSpyRaised without expected exception raised
        """

        def _do_math(_self, a, *args, **kwargs):
            if a == 1:
                raise KeyError
            elif a == 2:
                raise ValueError

        obj = MathClass()
        self.spy_on(obj.do_math, call_fake=_do_math)
        try:
            obj.do_math(1)
        except KeyError:
            pass

        try:
            obj.do_math(2)
        except ValueError:
            pass

        msg = b'No call to do_math raised AttributeError.\n\nThe following exceptions have been raised:\n\nCall 0:\n  KeyError\n\nCall 1:\n  ValueError'
        with self._check_assertion(msg):
            self.assertSpyRaised(obj.do_math, AttributeError)
        with self._check_assertion(msg):
            self.assertSpyRaised(obj.do_math.spy, AttributeError)
        msg = b'This call to do_math did not raise AttributeError. It raised KeyError.'
        with self._check_assertion(msg):
            self.assertSpyRaised(obj.do_math.calls[0], AttributeError)

    def test_assertSpyRaised_without_raised(self):
        """Testing SpyAgency.assertSpyRaised without any exceptions raised"""
        obj = MathClass()
        self.spy_on(obj.do_math)
        obj.do_math(1)
        obj.do_math(2)
        msg = b'No call to do_math raised an exception.'
        with self._check_assertion(msg):
            self.assertSpyRaised(obj.do_math, AttributeError)
        with self._check_assertion(msg):
            self.assertSpyRaised(obj.do_math.spy, AttributeError)
        msg = b'This call to do_math did not raise an exception.'
        with self._check_assertion(msg):
            self.assertSpyRaised(obj.do_math.spy.calls[0], AttributeError)

    def test_assertSpyLastRaised_with_expected_exception(self):
        """Testing SpyAgency.assertSpyLastRaised with expected exception
        raised
        """

        def _do_math(_self, a, *args, **kwargs):
            if a == 1:
                raise KeyError
            elif a == 2:
                raise ValueError

        obj = MathClass()
        self.spy_on(obj.do_math, call_fake=_do_math)
        try:
            obj.do_math(1)
        except KeyError:
            pass

        try:
            obj.do_math(2)
        except ValueError:
            pass

        self.assertSpyLastRaised(obj.do_math, ValueError)
        self.assertSpyLastRaised(obj.do_math.spy, ValueError)

    def test_assertSpyLastRaised_with_expected_no_exception(self):
        """Testing SpyAgency.assertSpyLastRaised with expected completion
        without raising
        """
        obj = MathClass()
        self.spy_on(obj.do_math)
        obj.do_math(1)
        obj.do_math(2)
        self.assertSpyLastRaised(obj.do_math, None)
        self.assertSpyLastRaised(obj.do_math.spy, None)
        return

    def test_assertSpyLastRaised_without_expected_exception(self):
        """Testing SpyAgency.assertSpyLastRaised without expected exception
        raised
        """

        def _do_math(_self, a, *args, **kwargs):
            if a == 1:
                raise KeyError
            elif a == 2:
                raise ValueError

        obj = MathClass()
        self.spy_on(obj.do_math, call_fake=_do_math)
        try:
            obj.do_math(1)
        except KeyError:
            pass

        try:
            obj.do_math(2)
        except ValueError:
            pass

        msg = b'The last call to do_math did not raise KeyError. It last raised ValueError.'
        with self._check_assertion(msg):
            self.assertSpyLastRaised(obj.do_math, KeyError)
        with self._check_assertion(msg):
            self.assertSpyLastRaised(obj.do_math.spy, KeyError)

    def test_assertSpyLastRaised_without_raised(self):
        """Testing SpyAgency.assertSpyLastRaised without exception raised"""
        obj = MathClass()
        self.spy_on(obj.do_math)
        obj.do_math(1)
        obj.do_math(2)
        msg = b'The last call to do_math did not raise an exception.'
        with self._check_assertion(msg):
            self.assertSpyLastRaised(obj.do_math, KeyError)
        with self._check_assertion(msg):
            self.assertSpyLastRaised(obj.do_math.spy, KeyError)

    def test_assertSpyRaisedMessage_with_expected(self):
        """Testing SpyAgency.assertSpyRaised with expected exception and
        message raised
        """

        def _do_math(_self, a, *args, **kwargs):
            if a == 1:
                raise AttributeError(b'Bad key!')
            elif a == 2:
                raise ValueError(b'Bad value!')

        obj = MathClass()
        self.spy_on(obj.do_math, call_fake=_do_math)
        try:
            obj.do_math(1)
        except AttributeError:
            pass

        try:
            obj.do_math(2)
        except ValueError:
            pass

        self.assertSpyRaisedMessage(obj.do_math, AttributeError, b'Bad key!')
        self.assertSpyRaisedMessage(obj.do_math.calls[0], AttributeError, b'Bad key!')
        self.assertSpyRaisedMessage(obj.do_math.spy, ValueError, b'Bad value!')
        self.assertSpyRaisedMessage(obj.do_math.spy.calls[1], ValueError, b'Bad value!')

    def test_assertSpyRaisedMessage_without_expected(self):
        """Testing SpyAgency.assertSpyRaisedMessage without expected exception
        and message raised
        """

        def _do_math(_self, a, *args, **kwargs):
            if a == 1:
                raise AttributeError(b'Bad key!')
            elif a == 2:
                raise ValueError(b'Bad value!')

        obj = MathClass()
        self.spy_on(obj.do_math, call_fake=_do_math)
        try:
            obj.do_math(1)
        except AttributeError:
            pass

        try:
            obj.do_math(2)
        except ValueError:
            pass

        msg = b'No call to do_math raised AttributeError with message %r.\n\nThe following exceptions have been raised:\n\nCall 0:\n  exception=AttributeError\n  message=%r\n\nCall 1:\n  exception=ValueError\n  message=%r' % (
         b'Bad key...', str(b'Bad key!'), str(b'Bad value!'))
        with self._check_assertion(msg):
            self.assertSpyRaisedMessage(obj.do_math, AttributeError, b'Bad key...')
        with self._check_assertion(msg):
            self.assertSpyRaisedMessage(obj.do_math.spy, AttributeError, b'Bad key...')
        msg = b'This call to do_math did not raise AttributeError with message %r.\n\nIt raised:\n\nexception=AttributeError\nmessage=%r' % (
         b'Bad key...', str(b'Bad key!'))
        with self._check_assertion(msg):
            self.assertSpyRaisedMessage(obj.do_math.calls[0], AttributeError, b'Bad key...')

    def test_assertSpyRaisedMessage_without_raised(self):
        """Testing SpyAgency.assertSpyRaisedMessage without exception raised
        """
        obj = MathClass()
        self.spy_on(obj.do_math)
        obj.do_math(1)
        obj.do_math(2)
        msg = b'No call to do_math raised an exception.'
        with self._check_assertion(msg):
            self.assertSpyRaisedMessage(obj.do_math, KeyError, b'...')
        with self._check_assertion(msg):
            self.assertSpyRaisedMessage(obj.do_math.spy, KeyError, b'...')

    def test_assertSpyLastRaisedMessage_with_expected(self):
        """Testing SpyAgency.assertSpyLastRaised with expected exception and
        message raised
        """

        def _do_math(_self, a, *args, **kwargs):
            if a == 1:
                raise AttributeError(b'Bad key!')
            elif a == 2:
                raise ValueError(b'Bad value!')

        obj = MathClass()
        self.spy_on(obj.do_math, call_fake=_do_math)
        try:
            obj.do_math(1)
        except AttributeError:
            pass

        try:
            obj.do_math(2)
        except ValueError:
            pass

        self.assertSpyLastRaisedMessage(obj.do_math, ValueError, b'Bad value!')
        self.assertSpyLastRaisedMessage(obj.do_math.spy, ValueError, b'Bad value!')

    def test_assertSpyLastRaisedMessage_without_expected(self):
        """Testing SpyAgency.assertSpyLastRaisedMessage without expected exception
        and message raised
        """

        def _do_math(_self, a, *args, **kwargs):
            if a == 1:
                raise AttributeError(b'Bad key!')
            elif a == 2:
                raise ValueError(b'Bad value!')

        obj = MathClass()
        self.spy_on(obj.do_math, call_fake=_do_math)
        try:
            obj.do_math(1)
        except AttributeError:
            pass

        try:
            obj.do_math(2)
        except ValueError:
            pass

        msg = b'The last call to do_math did not raise AttributeError with message %r.\n\nIt last raised:\n\nexception=ValueError\nmessage=%r' % (
         b'Bad key!', str(b'Bad value!'))
        with self._check_assertion(msg):
            self.assertSpyLastRaisedMessage(obj.do_math, AttributeError, b'Bad key!')
        with self._check_assertion(msg):
            self.assertSpyLastRaisedMessage(obj.do_math.spy, AttributeError, b'Bad key!')

    def test_assertSpyLastRaisedMessage_without_raised(self):
        """Testing SpyAgency.assertSpyLastRaisedMessage without exception raised
        """
        obj = MathClass()
        self.spy_on(obj.do_math)
        obj.do_math(1)
        obj.do_math(2)
        msg = b'The last call to do_math did not raise an exception.'
        with self._check_assertion(msg):
            self.assertSpyLastRaisedMessage(obj.do_math, KeyError, b'...')
        with self._check_assertion(msg):
            self.assertSpyLastRaisedMessage(obj.do_math.spy, KeyError, b'...')

    @contextmanager
    def _check_assertion(self, msg):
        """Check that the expected assertion and message is raised.

        Args:
            msg (unicode):
                The assertion message.

        Context:
            The context used to run an assertion.
        """
        with self.assertRaises(AssertionError) as (ctx):
            yield
        self.assertEqual(str(ctx.exception), msg)