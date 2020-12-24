# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/test_regularizers.py
# Compiled at: 2020-05-10 08:29:38
# Size of source mod 2**32: 2061 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from kerasy.models import Sequential
from kerasy.layers import Input, Dense
from kerasy import regularizers
from kerasy import metrics
from kerasy.utils import generate_test_data
from kerasy.utils import CategoricalEncoder
num_classes = 2
metric = metrics.get('categorical_accuracy')

def get_test_data():
    (x_train, y_train), _ = generate_test_data(num_train=1000, num_test=200,
      input_shape=(10, ),
      classification=True,
      num_classes=num_classes,
      random_state=123)
    encoder = CategoricalEncoder()
    y_train = encoder.to_onehot(y_train, num_classes)
    return (x_train, y_train)


def _test_regularizer(regularizer, target=0.75):
    regularizer = regularizers.get(regularizer)
    x_train, y_train = get_test_data()
    model = Sequential()
    model.add(Input(input_shape=(x_train.shape[1],)))
    model.add(Dense(10, activation='relu', kernel_regularizer=regularizer))
    model.add(Dense((y_train.shape[1]), activation='softmax', kernel_regularizer=regularizer))
    model.compile(loss='categorical_crossentropy',
      optimizer='adam',
      metrics=[
     metric])
    model.fit(x_train, y_train, epochs=10, batch_size=16, verbose=(-1))
    y_pred = model.predict(x_train)
    score = metric.loss(y_pred, y_train)
    @py_assert1 = score >= target
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('>=', ), (@py_assert1,), ('%(py0)s >= %(py2)s', ), (score, target)) % {'py0':@pytest_ar._saferepr(score) if 'score' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(score) else 'score',  'py2':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return model.layers[(-1)].kernel


none_kernel = _test_regularizer('none')

def test_l1():
    l1 = regularizers.L1(lambda1=0.01)
    l1_kernel = _test_regularizer(l1)
    @py_assert1 = l1.loss
    @py_assert4 = @py_assert1(none_kernel)
    @py_assert8 = l1.loss
    @py_assert11 = @py_assert8(l1_kernel)
    @py_assert6 = @py_assert4 >= @py_assert11
    if not @py_assert6:
        @py_format13 = @pytest_ar._call_reprcompare(('>=', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.loss\n}(%(py3)s)\n} >= %(py12)s\n{%(py12)s = %(py9)s\n{%(py9)s = %(py7)s.loss\n}(%(py10)s)\n}', ), (@py_assert4, @py_assert11)) % {'py0':@pytest_ar._saferepr(l1) if 'l1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l1) else 'l1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(none_kernel) if 'none_kernel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(none_kernel) else 'none_kernel',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(l1) if 'l1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l1) else 'l1',  'py9':@pytest_ar._saferepr(@py_assert8),  'py10':@pytest_ar._saferepr(l1_kernel) if 'l1_kernel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l1_kernel) else 'l1_kernel',  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert11 = None


def test_l2():
    l2 = regularizers.L2(lambda2=0.01)
    l2_kernel = _test_regularizer(l2)
    @py_assert1 = l2.loss
    @py_assert4 = @py_assert1(none_kernel)
    @py_assert8 = l2.loss
    @py_assert11 = @py_assert8(l2_kernel)
    @py_assert6 = @py_assert4 >= @py_assert11
    if not @py_assert6:
        @py_format13 = @pytest_ar._call_reprcompare(('>=', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.loss\n}(%(py3)s)\n} >= %(py12)s\n{%(py12)s = %(py9)s\n{%(py9)s = %(py7)s.loss\n}(%(py10)s)\n}', ), (@py_assert4, @py_assert11)) % {'py0':@pytest_ar._saferepr(l2) if 'l2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l2) else 'l2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(none_kernel) if 'none_kernel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(none_kernel) else 'none_kernel',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(l2) if 'l2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l2) else 'l2',  'py9':@pytest_ar._saferepr(@py_assert8),  'py10':@pytest_ar._saferepr(l2_kernel) if 'l2_kernel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l2_kernel) else 'l2_kernel',  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert11 = None


def test_l1l2():
    l1l2 = regularizers.L1L2(lambda1=0.01, lambda2=0.01)
    l1l2_kernel = _test_regularizer(l1l2)
    @py_assert1 = l1l2.loss
    @py_assert4 = @py_assert1(none_kernel)
    @py_assert8 = l1l2.loss
    @py_assert11 = @py_assert8(l1l2_kernel)
    @py_assert6 = @py_assert4 >= @py_assert11
    if not @py_assert6:
        @py_format13 = @pytest_ar._call_reprcompare(('>=', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.loss\n}(%(py3)s)\n} >= %(py12)s\n{%(py12)s = %(py9)s\n{%(py9)s = %(py7)s.loss\n}(%(py10)s)\n}', ), (@py_assert4, @py_assert11)) % {'py0':@pytest_ar._saferepr(l1l2) if 'l1l2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l1l2) else 'l1l2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(none_kernel) if 'none_kernel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(none_kernel) else 'none_kernel',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(l1l2) if 'l1l2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l1l2) else 'l1l2',  'py9':@pytest_ar._saferepr(@py_assert8),  'py10':@pytest_ar._saferepr(l1l2_kernel) if 'l1l2_kernel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l1l2_kernel) else 'l1l2_kernel',  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert11 = None