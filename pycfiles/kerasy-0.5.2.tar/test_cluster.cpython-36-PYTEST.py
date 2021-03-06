# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/ML/test_cluster.py
# Compiled at: 2020-05-12 10:12:54
# Size of source mod 2**32: 916 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from kerasy.ML.cluster import DBSCAN
from kerasy.utils import generateWholeCakes
from kerasy.utils import cluster_accuracy
num_clusters = 3
num_samples = 300

def get_test_data():
    x_train, y_train = generateWholeCakes(num_classes=(num_clusters * 2), num_samples=(num_samples * 2),
      r_low=3,
      r_high=10,
      add_noise=False,
      same=True,
      seed=123)
    mask = y_train % 2 == 0
    x_train = x_train[mask]
    y_train = y_train[mask]
    return (x_train, y_train)


def test_dbscan(target=0.75):
    x_train, y_train = get_test_data()
    model = DBSCAN(eps=1)
    y_pred = model.fit_predict(x_train, verbose=(-1))
    @py_assert3 = cluster_accuracy(y_train, y_pred)
    @py_assert5 = @py_assert3 > target
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('>', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} > %(py6)s', ), (@py_assert3, target)) % {'py0':@pytest_ar._saferepr(cluster_accuracy) if 'cluster_accuracy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cluster_accuracy) else 'cluster_accuracy',  'py1':@pytest_ar._saferepr(y_train) if 'y_train' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(y_train) else 'y_train',  'py2':@pytest_ar._saferepr(y_pred) if 'y_pred' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(y_pred) else 'y_pred',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert3 = @py_assert5 = None