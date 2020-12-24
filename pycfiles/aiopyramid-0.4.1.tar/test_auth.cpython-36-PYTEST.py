# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/housl/workspaces/develop/aiopyramid/tests/test_auth.py
# Compiled at: 2014-12-06 00:25:57
# Size of source mod 2**32: 2275 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, asyncio, pytest
from pyramid import testing
from aiopyramid.helpers import spawn_greenlet, synchronize

@pytest.yield_fixture
def web_request():
    request = testing.DummyRequest()
    yield request


class TestAuthentication:

    @pytest.yield_fixture
    def wrapped_policy(self):
        from pyramid.authentication import CallbackAuthenticationPolicy
        from aiopyramid.auth import authn_policy_factory

        @asyncio.coroutine
        def callback(userid, request):
            yield from asyncio.sleep(0.1)
            return ['test_user']
            if False:
                yield None

        class TestAuthenticationPolicy(CallbackAuthenticationPolicy):

            def __init__(self, callback):
                self.callback = callback
                self.debug = True

            def unauthenticated_userid(self, request):
                return 'theone'

        yield authn_policy_factory(TestAuthenticationPolicy, callback)

    def call_authn_policy_methods(self, policy, request):
        @py_assert1 = policy.unauthenticated_userid
        @py_assert4 = @py_assert1(request)
        @py_assert7 = 'theone'
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.unauthenticated_userid\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(policy) if 'policy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(policy) else 'policy',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(request) if 'request' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request) else 'request',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None
        @py_assert1 = policy.authenticated_userid
        @py_assert4 = @py_assert1(request)
        @py_assert7 = 'theone'
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.authenticated_userid\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(policy) if 'policy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(policy) else 'policy',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(request) if 'request' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request) else 'request',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None
        @py_assert1 = policy.effective_principals
        @py_assert4 = @py_assert1(request)
        @py_assert7 = [
         'system.Everyone', 'system.Authenticated', 'theone', 'test_user']
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.effective_principals\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(policy) if 'policy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(policy) else 'policy',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(request) if 'request' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request) else 'request',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None

    @asyncio.coroutine
    def yield_from_authn_policy_methods(self, policy, request):
        @py_assert0 = yield from policy.unauthenticated_userid(request)
        @py_assert3 = 'theone'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = yield from policy.authenticated_userid(request)
        @py_assert3 = 'theone'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = yield from policy.effective_principals(request)
        @py_assert3 = [
         'system.Everyone', 'system.Authenticated', 'theone', 'test_user']
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        if False:
            yield None

    def test_wrapper_in_sync(self, wrapped_policy, web_request):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(spawn_greenlet(self.call_authn_policy_methods, wrapped_policy, web_request))

    def test_wrapper_in_coroutine(self, wrapped_policy, web_request):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(spawn_greenlet(synchronize(self.yield_from_authn_policy_methods), wrapped_policy, web_request))