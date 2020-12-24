# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/datasets/test_mnist.py
# Compiled at: 2020-05-11 02:12:54
# Size of source mod 2**32: 349 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from kerasy.datasets import mnist

def test_load_data():
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    num_train, *img_shape_train = x_train.shape
    num_test, *img_shape_test = x_test.shape
    @py_assert1 = img_shape_test == img_shape_train
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (img_shape_test, img_shape_train)) % {'py0':@pytest_ar._saferepr(img_shape_test) if 'img_shape_test' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(img_shape_test) else 'img_shape_test',  'py2':@pytest_ar._saferepr(img_shape_train) if 'img_shape_train' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(img_shape_train) else 'img_shape_train'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert2 = len(y_train)
    @py_assert4 = @py_assert2 == num_train
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, num_train)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(y_train) if 'y_train' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(y_train) else 'y_train',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(num_train) if 'num_train' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(num_train) else 'num_train'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None
    @py_assert2 = len(y_test)
    @py_assert4 = @py_assert2 == num_test
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, num_test)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(y_test) if 'y_test' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(y_test) else 'y_test',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(num_test) if 'num_test' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(num_test) else 'num_test'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None