# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/socek/projects/impaf/core/build/lib/impaf/controller/tests/test_json.py
# Compiled at: 2015-06-17 12:23:17
# Size of source mod 2**32: 356 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pytest import fixture
from ..json import JsonController
from .test_controller import ControllerFixtures

class TestJsonController(ControllerFixtures):

    @fixture
    def controller(self, mroot_factory, mrequest):
        return JsonController(mroot_factory, mrequest)

    def test_normal_run(self, controller):
        @py_assert1 = controller()
        @py_assert4 = {}
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(controller) if 'controller' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(controller) else 'controller', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None