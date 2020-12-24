# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/Dropbox/c0d3z/python/libs/rbottle/unittests/test_rbottle.py
# Compiled at: 2014-11-30 04:26:32
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, sys
from StringIO import StringIO
import pytest
sys.path = [
 'src/rbottle'] + sys.path
import rbottle
from rbottle import HTTPError

class MockRequest:

    def __init__(self, json):
        self.body = StringIO(json)
        self.forms = {}


def test_decode_json_body():
    rbottle.request = MockRequest('{"hello": "there"}')
    @py_assert1 = rbottle.decode_json_body
    @py_assert3 = @py_assert1()
    @py_assert6 = {'hello': 'there'}
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.decode_json_body\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(rbottle) if 'rbottle' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rbottle) else 'rbottle', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    with pytest.raises(HTTPError):
        rbottle.request = MockRequest('{')
        rbottle.decode_json_body()
    return


def test_encode_json_body():
    @py_assert1 = rbottle.encode_json_body
    @py_assert3 = {'one': 1}
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = '{\n    "one": 1\n}'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.encode_json_body\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0': @pytest_ar._saferepr(rbottle) if 'rbottle' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rbottle) else 'rbottle', 'py9': @pytest_ar._saferepr(@py_assert8), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    return


def test_handle_type_error():

    @rbottle.handle_type_error
    def too_much_parameters(one):
        pass

    with pytest.raises(HTTPError):
        too_much_parameters('one', 'two')

    @rbottle.handle_type_error
    def too_few_parameters(one, two, three):
        pass

    with pytest.raises(HTTPError):
        too_few_parameters('one')

    @rbottle.handle_type_error
    def exactly_right_ammount_of_parameters(one):
        pass

    @py_assert1 = 'one'
    @py_assert3 = exactly_right_ammount_of_parameters(@py_assert1)
    @py_assert5 = @py_assert3 is None
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} is %(py6)s', ), (@py_assert3, None)) % {'py0': @pytest_ar._saferepr(exactly_right_ammount_of_parameters) if 'exactly_right_ammount_of_parameters' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(exactly_right_ammount_of_parameters) else 'exactly_right_ammount_of_parameters', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(None) if 'None' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(None) else 'None'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    return


def test_json_to_params():
    rbottle.request = MockRequest('{"param": 2}')

    @rbottle.json_to_params
    def json_to_params_test(param):
        return param * 2

    @py_assert1 = json_to_params_test()
    @py_assert4 = '4'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(json_to_params_test) if 'json_to_params_test' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(json_to_params_test) else 'json_to_params_test', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    return


def test_json_to_params_no_json_parameter():
    rbottle.request = MockRequest('{"param": 2}')

    @rbottle.json_to_params(return_json=False)
    def json_to_params_test_no_json(param):
        return param * 2

    @py_assert1 = json_to_params_test_no_json()
    @py_assert4 = 4
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(json_to_params_test_no_json) if 'json_to_params_test_no_json' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(json_to_params_test_no_json) else 'json_to_params_test_no_json', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    return


def test_json_to_params_list():
    rbottle.request = MockRequest('[2]')

    @rbottle.json_to_params
    def json_to_params_test(param):
        return param * 2

    @py_assert1 = json_to_params_test()
    @py_assert4 = '4'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(json_to_params_test) if 'json_to_params_test' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(json_to_params_test) else 'json_to_params_test', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    return


def test_json_to_params_value():
    rbottle.request = MockRequest('2')

    @rbottle.json_to_params
    def json_to_params_test(param):
        return param * 2

    @py_assert1 = json_to_params_test()
    @py_assert4 = '4'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(json_to_params_test) if 'json_to_params_test' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(json_to_params_test) else 'json_to_params_test', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    return


def test_json_to_params_bad_keyword():
    rbottle.request = MockRequest('{"nope": 1}')

    @rbottle.json_to_params
    def json_to_params_test(param):
        return param * 2

    with pytest.raises(HTTPError):
        json_to_params_test()


def test_json_to_data():
    rbottle.request = MockRequest('2')

    @rbottle.json_to_data
    def json_to_data_test(data):
        return data * 2

    @py_assert1 = json_to_data_test()
    @py_assert4 = '4'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(json_to_data_test) if 'json_to_data_test' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(json_to_data_test) else 'json_to_data_test', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    return


def test_json_to_data_no_json_parameter():
    rbottle.request = MockRequest('2')

    @rbottle.json_to_data(return_json=False)
    def json_to_data_test(data):
        return data * 2

    @py_assert1 = json_to_data_test()
    @py_assert4 = 4
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(json_to_data_test) if 'json_to_data_test' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(json_to_data_test) else 'json_to_data_test', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    return


def test_json_to_data_error_too_few():
    rbottle.request = MockRequest('2')

    @rbottle.json_to_data
    def json_to_data_test():
        pass

    with pytest.raises(HTTPError):
        json_to_data_test()


def test_json_to_data_error_too_many():
    rbottle.request = MockRequest('2')

    @rbottle.json_to_data
    def json_to_data_test(one, two):
        pass

    with pytest.raises(HTTPError):
        json_to_data_test()


def test_form_to_params():
    rbottle.request = MockRequest('""')
    rbottle.request.forms = {'param': 2}

    @rbottle.form_to_params
    def form_to_params_test(param):
        return param * 2

    @py_assert1 = form_to_params_test()
    @py_assert4 = '4'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(form_to_params_test) if 'form_to_params_test' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(form_to_params_test) else 'form_to_params_test', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    return


def test_form_to_params_no_json_parameter():
    rbottle.request = MockRequest('""')
    rbottle.request.forms = {'param': 2}

    @rbottle.form_to_params(return_json=False)
    def form_to_params_test(param):
        return param * 2

    @py_assert1 = form_to_params_test()
    @py_assert4 = 4
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(form_to_params_test) if 'form_to_params_test' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(form_to_params_test) else 'form_to_params_test', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    return