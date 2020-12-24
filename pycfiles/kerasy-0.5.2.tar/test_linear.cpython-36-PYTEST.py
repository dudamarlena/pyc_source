# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/ML/test_linear.py
# Compiled at: 2020-05-12 12:16:01
# Size of source mod 2**32: 1126 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from kerasy.ML.linear import LinearRegression, LinearRegressionRidge, LinearRegressionLASSO
from kerasy.utils import generateSin
from kerasy.utils import root_mean_squared_error
num_samples = 30

def get_test_data():
    x_train, y_train = generateSin(num_samples, xmin=0,
      xmax=1,
      seed=0)
    return (x_train, y_train)


def _test_linear_polynomial(Model, num_feature_arr=[
 1, 2, 4, 8], **kwargs):
    x_train, y_train = get_test_data()
    for i, num_features in enumerate(sorted(num_feature_arr)):
        model = Model(basis='polynomial', exponent=range(1, num_features + 1), **kwargs)
        model.fit(x_train, y_train)
        y_pred = model.predict(x_train)
        score = root_mean_squared_error(y_pred, y_train)
        @py_assert1 = []
        @py_assert4 = 0
        @py_assert3 = i == @py_assert4
        @py_assert0 = @py_assert3
        if not @py_assert3:
            @py_assert10 = prev_score >= score
            @py_assert0 = @py_assert10
        if not @py_assert0:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s == %(py5)s', ), (i, @py_assert4)) % {'py2':@pytest_ar._saferepr(i) if 'i' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(i) else 'i',  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = '%(py7)s' % {'py7': @py_format6}
            @py_assert1.append(@py_format8)
            if not @py_assert3:
                @py_format12 = @pytest_ar._call_reprcompare(('>=', ), (@py_assert10,), ('%(py9)s >= %(py11)s', ), (prev_score, score)) % {'py9':@pytest_ar._saferepr(prev_score) if 'prev_score' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(prev_score) else 'prev_score',  'py11':@pytest_ar._saferepr(score) if 'score' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(score) else 'score'}
                @py_format14 = '%(py13)s' % {'py13': @py_format12}
                @py_assert1.append(@py_format14)
            @py_format15 = @pytest_ar._format_boolop(@py_assert1, 1) % {}
            @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
            raise AssertionError(@pytest_ar._format_explanation(@py_format17))
        @py_assert0 = @py_assert1 = @py_assert3 = @py_assert4 = @py_assert10 = None
        prev_score = score


def test_linear():
    _test_linear_polynomial(LinearRegression)


def test_linear_ridge():
    _test_linear_polynomial(LinearRegressionRidge)


def test_linear_lasss():
    _test_linear_polynomial(LinearRegressionLASSO)