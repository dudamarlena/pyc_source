# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/ML/test_svm.py
# Compiled at: 2020-05-13 03:16:16
# Size of source mod 2**32: 811 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from kerasy.ML.svm import hardSVC, SVC
from kerasy.utils import generateWhirlpool
num_samples = 150
max_iter = 10

def get_test_data():
    x_train, y_train = generateWhirlpool(num_samples, xmin=0,
      xmax=4,
      seed=0)
    return (x_train, y_train)


def _test_svm(model, target=0.75):
    x_train, y_train = get_test_data()
    model.fit(x_train, y_train, max_iter=max_iter, sparse_memorize=False, verbose=(-1))
    @py_assert1 = model.accuracy
    @py_assert5 = @py_assert1(x_train, y_train)
    @py_assert7 = @py_assert5 >= target
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('>=', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.accuracy\n}(%(py3)s, %(py4)s)\n} >= %(py8)s', ), (@py_assert5, target)) % {'py0':@pytest_ar._saferepr(model) if 'model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(model) else 'model',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(x_train) if 'x_train' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x_train) else 'x_train',  'py4':@pytest_ar._saferepr(y_train) if 'y_train' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(y_train) else 'y_train',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert5 = @py_assert7 = None


def test_hard_svc():
    model = hardSVC(kernel='gaussian', sigma=1.0)
    _test_svm(model, target=0.75)


def test_soft_svc():
    model = SVC(kernel='gaussian', sigma=1.0, C=10)
    _test_svm(model, target=0.75)