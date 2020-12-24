# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/test_models.py
# Compiled at: 2020-05-12 11:02:37
# Size of source mod 2**32: 1830 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, numpy as np
from kerasy.models import Sequential
from kerasy.layers import Input, Dense
from kerasy import optimizers
from kerasy import metrics
from kerasy.utils import generate_test_data
from kerasy.utils import CategoricalEncoder
num_classes = 2

def get_test_data():
    (x_train, y_train), _ = generate_test_data(num_train=1000, num_test=200,
      input_shape=(10, ),
      classification=True,
      num_classes=num_classes,
      random_state=123)
    encoder = CategoricalEncoder()
    y_train = encoder.to_onehot(y_train, num_classes)
    return (x_train, y_train)


def _test_build_classification_model(x_train, y_train):
    model = Sequential()
    model.add(Input(input_shape=(x_train.shape[1],)))
    model.add(Dense(10, activation='relu'))
    model.add(Dense((y_train.shape[1]), activation='softmax'))
    model.compile(loss='categorical_crossentropy',
      optimizer='adam',
      metrics=[
     'categorical_accuracy'])
    return model


def test_classification_model():
    x_train, y_train = get_test_data()
    model = _test_build_classification_model(x_train, y_train)
    model.fit(x_train, y_train, epochs=3, batch_size=16, verbose=(-1))
    y_pred = model.predict(x_train)
    scores = [metric.loss(y_pred, y_train) for metric in model.metrics]
    weights = model.get_weights()
    model_ = _test_build_classification_model(x_train, y_train)
    model_.set_weights(weights)
    y_pred_ = model.predict(x_train)
    scores_ = [metric.loss(y_pred_, y_train) for metric in model_.metrics]
    @py_assert1 = np.all
    @py_assert4 = y_pred == y_pred_
    @py_assert8 = @py_assert1(@py_assert4)
    if not @py_assert8:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s == %(py5)s', ), (y_pred, y_pred_)) % {'py3':@pytest_ar._saferepr(y_pred) if 'y_pred' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(y_pred) else 'y_pred',  'py5':@pytest_ar._saferepr(y_pred_) if 'y_pred_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(y_pred_) else 'y_pred_'}
        @py_format10 = 'assert %(py9)s\n{%(py9)s = %(py2)s\n{%(py2)s = %(py0)s.all\n}(%(py7)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py7':@py_format6,  'py9':@pytest_ar._saferepr(@py_assert8)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert4 = @py_assert8 = None
    @py_assert1 = scores == scores_
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (scores, scores_)) % {'py0':@pytest_ar._saferepr(scores) if 'scores' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(scores) else 'scores',  'py2':@pytest_ar._saferepr(scores_) if 'scores_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(scores_) else 'scores_'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None