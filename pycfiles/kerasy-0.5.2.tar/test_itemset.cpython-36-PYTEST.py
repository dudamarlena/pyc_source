# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/search/test_itemset.py
# Compiled at: 2020-05-13 01:22:06
# Size of source mod 2**32: 1018 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, numpy as np
from kerasy.search.itemset import FrequentSet
from kerasy.search.itemset import create_one_hot
num_transactions = 100
num_data = 1000

def get_test_data():
    data_idx = np.arange(num_data)
    rnd = np.random.RandomState(123)
    retail = [rnd.choice(a=data_idx, size=size, replace=False) for size in rnd.randint(1, (num_data / 10), size=num_transactions)]
    database, idx2data = create_one_hot(retail)
    return (database, idx2data)


def test_all_itemset(path='itemset.png', threshold=10):
    database, idx2data = get_test_data()
    model = FrequentSet(threshold=threshold)
    model.fit(database, method='all')
    @py_assert1 = model.export_graphviz
    @py_assert5 = @py_assert1(path, class_names=idx2data)
    if not @py_assert5:
        @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.export_graphviz\n}(%(py3)s, class_names=%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(model) if 'model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(model) else 'model',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(path) if 'path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(path) else 'path',  'py4':@pytest_ar._saferepr(idx2data) if 'idx2data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(idx2data) else 'idx2data',  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert5 = None
    os.remove(path)


def test_closed_itemset(path='itemset.png', threshold=10):
    database, idx2data = get_test_data()
    model = FrequentSet(threshold=threshold)
    model.fit(database, method='closed')
    @py_assert1 = model.export_graphviz
    @py_assert5 = @py_assert1(path, class_names=idx2data)
    if not @py_assert5:
        @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.export_graphviz\n}(%(py3)s, class_names=%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(model) if 'model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(model) else 'model',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(path) if 'path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(path) else 'path',  'py4':@pytest_ar._saferepr(idx2data) if 'idx2data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(idx2data) else 'idx2data',  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert5 = None
    os.remove(path)