# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ddanier/work/django/django_hits/tests/test_smoke.py
# Compiled at: 2015-09-10 02:07:46
# Size of source mod 2**32: 669 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest

def test_smoke():
    """Just some basic smoke tests (syntax, app loading)"""
    import django_hits, django_hits.models, django_hits.utils, django_hits.templatetags.hit_tags


def test_system_checks():
    import django
    if django.VERSION >= (1, 7, 0):
        from django.core import checks
        if django.VERSION >= (1, 8, 0):
            @py_assert1 = checks.run_checks
            @py_assert3 = False
            @py_assert5 = @py_assert1(include_deployment_checks=@py_assert3)
            @py_assert7 = not @py_assert5
            if not @py_assert7:
                @py_format8 = (@pytest_ar._format_assertmsg('Some Django system checks failed') + '\n>assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.run_checks\n}(include_deployment_checks=%(py4)s)\n}') % {'py4': @pytest_ar._saferepr(@py_assert3),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(checks) if 'checks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(checks) else 'checks',  'py2': @pytest_ar._saferepr(@py_assert1)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        else:
            @py_assert1 = checks.run_checks
            @py_assert3 = @py_assert1()
            @py_assert5 = not @py_assert3
            if not @py_assert5:
                @py_format6 = (@pytest_ar._format_assertmsg('Some Django system checks failed') + '\n>assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.run_checks\n}()\n}') % {'py4': @pytest_ar._saferepr(@py_assert3),  'py0': @pytest_ar._saferepr(checks) if 'checks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(checks) else 'checks',  'py2': @pytest_ar._saferepr(@py_assert1)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None


@pytest.mark.django_db
def test_db():
    pass