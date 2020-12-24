# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/ML/test_boosting.py
# Compiled at: 2020-05-12 05:22:23
# Size of source mod 2**32: 3196 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, numpy as np
from kerasy.ML.boosting import L2Boosting
from kerasy.models import Sequential
from kerasy.layers import Input, Dense
from kerasy import metrics
from kerasy.utils import generate_test_data
from kerasy.utils import CategoricalEncoder
num_models = 5

def get_test_regression_data():
    (x_train, y_train), _ = generate_test_data(num_train=1000, num_test=200,
      input_shape=(10, ),
      output_shape=(1, ),
      classification=False,
      random_state=123)
    return (x_train, y_train)


def get_test_classification_data():
    num_classes = 2
    (x_train, y_train), _ = generate_test_data(num_train=1000, num_test=200,
      input_shape=(10, ),
      num_classes=num_classes,
      classification=True,
      random_state=123)
    encoder = CategoricalEncoder()
    y_train = encoder.to_onehot(y_train, num_classes)
    return (x_train, y_train)


def _test_adaboost():
    metric = metrics.get('categorical_accuracy')
    x_train, y_train = get_test_classification_data()
    Models = []
    weak_model_losses = []
    for _ in range(num_models):
        model = Sequential()
        model.add(Input(input_shape=(x_train.shape[1],)))
        model.add(Dense(10, activation='relu'))
        model.add(Dense((y_train.shape[1]), activation='softmax'))
        model.compile(loss='categorical_crossentropy',
          optimizer='adam',
          metrics=[
         metric])
        model.fit(x_train, y_train, epochs=3, batch_size=16, verbose=(-1))
        weak_model_losses.append(metric.loss(model.predict(x_train), y_train))
        Models.append(model)

    boosting = AdaBoost(Models)
    boosting.fit(x_train, y_train, verbose=(-1))
    y_boosting_pred = boosting.predict(x_train)
    boosting_loss = metric.loss(y_boosting_pred, y_train)
    @py_assert4 = min(weak_model_losses)
    @py_assert1 = boosting_loss <= @py_assert4
    if not @py_assert1:
        @py_format6 = @pytest_ar._call_reprcompare(('<=', ), (@py_assert1,), ('%(py0)s <= %(py5)s\n{%(py5)s = %(py2)s(%(py3)s)\n}', ), (boosting_loss, @py_assert4)) % {'py0':@pytest_ar._saferepr(boosting_loss) if 'boosting_loss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(boosting_loss) else 'boosting_loss',  'py2':@pytest_ar._saferepr(min) if 'min' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(min) else 'min',  'py3':@pytest_ar._saferepr(weak_model_losses) if 'weak_model_losses' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(weak_model_losses) else 'weak_model_losses',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert4 = None


def test_l2boosting():
    metric = metrics.get('mse')
    x_train, y_train = get_test_regression_data()
    Models = []
    weak_model_losses = []
    for _ in range(num_models):
        model = Sequential()
        model.add(Input(input_shape=(x_train.shape[1],)))
        model.add(Dense(10, activation='relu'))
        model.add(Dense((y_train.shape[1]), activation='linear'))
        model.compile(loss='mean_squared_error',
          optimizer='adam',
          metrics=[
         metric])
        model.fit(x_train, y_train, epochs=3, batch_size=16, verbose=(-1))
        weak_model_losses.append(metric.loss(model.predict(x_train), y_train))
        Models.append(model)

    boosting = L2Boosting(Models)
    boosting.fit(x_train, y_train, verbose=(-1))
    y_boosting_pred = boosting.predict(x_train)
    boosting_loss = metric.loss(y_boosting_pred, y_train)
    @py_assert4 = min(weak_model_losses)
    @py_assert1 = boosting_loss <= @py_assert4
    if not @py_assert1:
        @py_format6 = @pytest_ar._call_reprcompare(('<=', ), (@py_assert1,), ('%(py0)s <= %(py5)s\n{%(py5)s = %(py2)s(%(py3)s)\n}', ), (boosting_loss, @py_assert4)) % {'py0':@pytest_ar._saferepr(boosting_loss) if 'boosting_loss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(boosting_loss) else 'boosting_loss',  'py2':@pytest_ar._saferepr(min) if 'min' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(min) else 'min',  'py3':@pytest_ar._saferepr(weak_model_losses) if 'weak_model_losses' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(weak_model_losses) else 'weak_model_losses',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert4 = None