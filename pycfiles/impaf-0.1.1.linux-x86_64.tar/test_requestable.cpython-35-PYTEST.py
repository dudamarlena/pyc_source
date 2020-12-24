# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/socek/projects/impaf/core/build/lib/impaf/tests/test_requestable.py
# Compiled at: 2015-06-26 14:22:16
# Size of source mod 2**32: 1611 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from mock import MagicMock
from pytest import fixture
from ..requestable import Requestable
from ..requestable import ImpafRequest

class ExampleRequest(ImpafRequest):

    def __init__(self, request):
        self.myrequest = request


class ExampleRequestable(Requestable):

    def _get_request_cls(self):
        return ExampleRequest


class TestRequestable(object):

    @fixture
    def model(self):
        return ExampleRequestable()

    def test_feed_request(self, model):
        request = ExampleRequest(None)
        model.feed_request(request)
        @py_assert1 = model.request
        @py_assert3 = @py_assert1 == request
        if not @py_assert3:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.request\n} == %(py4)s', ), (@py_assert1, request)) % {'py4': @pytest_ar._saferepr(request) if 'request' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request) else 'request', 'py0': @pytest_ar._saferepr(model) if 'model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(model) else 'model', 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None

    def test_feed_request_with_convert(self, model):
        request = MagicMock()
        model.feed_request(request)
        @py_assert1 = model.request
        @py_assert3 = @py_assert1.myrequest
        @py_assert5 = @py_assert3 == request
        if not @py_assert5:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.request\n}.myrequest\n} == %(py6)s', ), (@py_assert3, request)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(model) if 'model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(model) else 'model', 'py6': @pytest_ar._saferepr(request) if 'request' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request) else 'request', 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None

    def test_properties(self, model):
        request = MagicMock()
        model.request = request
        model.request.registry = {'settings': 'settings1', 
         'paths': 'paths1'}
        @py_assert1 = model.registry
        @py_assert5 = request.registry
        @py_assert3 = @py_assert1 is @py_assert5
        if not @py_assert3:
            @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.registry\n} is %(py6)s\n{%(py6)s = %(py4)s.registry\n}', ), (@py_assert1, @py_assert5)) % {'py4': @pytest_ar._saferepr(request) if 'request' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request) else 'request', 'py0': @pytest_ar._saferepr(model) if 'model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(model) else 'model', 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = model.POST
        @py_assert5 = request.POST
        @py_assert3 = @py_assert1 is @py_assert5
        if not @py_assert3:
            @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.POST\n} is %(py6)s\n{%(py6)s = %(py4)s.POST\n}', ), (@py_assert1, @py_assert5)) % {'py4': @pytest_ar._saferepr(request) if 'request' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request) else 'request', 'py0': @pytest_ar._saferepr(model) if 'model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(model) else 'model', 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = model.GET
        @py_assert5 = request.GET
        @py_assert3 = @py_assert1 is @py_assert5
        if not @py_assert3:
            @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.GET\n} is %(py6)s\n{%(py6)s = %(py4)s.GET\n}', ), (@py_assert1, @py_assert5)) % {'py4': @pytest_ar._saferepr(request) if 'request' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request) else 'request', 'py0': @pytest_ar._saferepr(model) if 'model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(model) else 'model', 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = model.matchdict
        @py_assert5 = request.matchdict
        @py_assert3 = @py_assert1 is @py_assert5
        if not @py_assert3:
            @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.matchdict\n} is %(py6)s\n{%(py6)s = %(py4)s.matchdict\n}', ), (@py_assert1, @py_assert5)) % {'py4': @pytest_ar._saferepr(request) if 'request' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request) else 'request', 'py0': @pytest_ar._saferepr(model) if 'model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(model) else 'model', 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = model.route_path
        @py_assert5 = request.route_path
        @py_assert3 = @py_assert1 is @py_assert5
        if not @py_assert3:
            @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.route_path\n} is %(py6)s\n{%(py6)s = %(py4)s.route_path\n}', ), (@py_assert1, @py_assert5)) % {'py4': @pytest_ar._saferepr(request) if 'request' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request) else 'request', 'py0': @pytest_ar._saferepr(model) if 'model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(model) else 'model', 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = model.settings
        @py_assert4 = 'settings1'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.settings\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(model) if 'model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(model) else 'model', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = model.paths
        @py_assert4 = 'paths1'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.paths\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(model) if 'model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(model) else 'model', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None


class TestImpafRequest(object):

    def test_properties(self):
        request = ExampleRequest(None)
        request.registry = {'settings': 'settings1', 
         'paths': 'paths1'}
        @py_assert1 = request.settings
        @py_assert4 = 'settings1'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.settings\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(request) if 'request' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request) else 'request', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = request.paths
        @py_assert4 = 'paths1'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.paths\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(request) if 'request' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request) else 'request', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None