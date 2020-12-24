# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe_menu/tests.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 147 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from cms_qe_test import render_plugin
from .cms_plugins import MenuPlugin

def test_render_menu():
    @py_assert0 = '<ul>'
    @py_assert5 = render_plugin(MenuPlugin)
    @py_assert2 = @py_assert0 in @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(render_plugin) if 'render_plugin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(render_plugin) else 'render_plugin', 'py4': @pytest_ar._saferepr(MenuPlugin) if 'MenuPlugin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(MenuPlugin) else 'MenuPlugin'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert5 = None