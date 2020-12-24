# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/ML/test_decomposition.py
# Compiled at: 2020-05-12 11:00:03
# Size of source mod 2**32: 1864 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, numpy as np
from kerasy.ML.decomposition import PCA, UMAP, tSNE
from kerasy.datasets import mnist
from kerasy.utils import cluster_accuracy
num_mnist = 300
n_components = 5
epochs = 10
seed = 123

def get_test_data():
    (x_train, y_train), _ = mnist.load_data()
    x_train = x_train[:num_mnist].reshape(num_mnist, -1)
    y_train = y_train[:num_mnist]
    return (x_train, y_train)


def _test_decomposition(model, **kwargs):
    x_train, y_train = get_test_data()
    if hasattr(model, 'fit_transform'):
        x_transformed = (model.fit_transform)(x_train, **kwargs)
    else:
        (model.fit)(x_train, **kwargs)
        x_transformed = model.transform(x_train)
    x_transformed = x_transformed.real
    for label in np.unique(y_train):
        center = np.mean((x_transformed[(y_train == label)]), axis=0)
        var_within = np.mean(np.sum((np.square(x_transformed[(y_train == label)] - center)), axis=1))
        var_outside = np.mean(np.sum((np.square(x_transformed[(y_train != label)] - center)), axis=1))
        @py_assert1 = var_outside >= var_within
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('>=', ), (@py_assert1,), ('%(py0)s >= %(py2)s', ), (var_outside, var_within)) % {'py0':@pytest_ar._saferepr(var_outside) if 'var_outside' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(var_outside) else 'var_outside',  'py2':@pytest_ar._saferepr(var_within) if 'var_within' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(var_within) else 'var_within'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None


def test_pca():
    model = PCA(n_components=n_components)
    _test_decomposition(model)


def test_tsne():
    model = tSNE(initial_momentum=0.5,
      final_momoentum=0.8,
      eta=500,
      min_gain=0.1,
      tol=1e-05,
      prec_max_iter=50,
      random_state=seed)
    _test_decomposition(model,
      n_components=n_components,
      epochs=epochs,
      verbose=1)


def test_umap():
    model = UMAP(min_dist=0.1,
      spread=1.0,
      sigma_iter=40,
      sigma_init=1.0,
      sigma_tol=1e-05,
      sigma_lower=0,
      sigma_upper=(np.inf),
      random_state=seed)
    _test_decomposition(model,
      n_components=n_components,
      epochs=epochs,
      init_lr=1,
      verbose=(-1))