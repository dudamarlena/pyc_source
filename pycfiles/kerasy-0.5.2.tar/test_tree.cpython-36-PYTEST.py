# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/ML/test_tree.py
# Compiled at: 2020-05-12 22:52:53
# Size of source mod 2**32: 1243 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os
from kerasy.ML.tree import DecisionTreeClassifier
from kerasy.utils import cluster_accuracy
from kerasy.utils import generateWholeCakes
num_samples = 200
num_classes = 5
max_depths = [1, 2, 4, 8]

def get_test_data():
    x_train, y_train = generateWholeCakes(num_classes=num_classes, num_samples=num_samples,
      r_low=1,
      r_high=5,
      same=False,
      seed=0)
    return (x_train, y_train)


def test_decision_tree(target=0.75, path='decision_tree.png'):
    x_train, y_train = get_test_data()
    for i, max_depth in enumerate(sorted(max_depths)):
        model = DecisionTreeClassifier(criterion='gini', max_depth=max_depth,
          random_state=0)
        model.fit(x_train, y_train)
        y_pred = model.predict(x_train)
        score = cluster_accuracy(y_pred, y_train)
        @py_assert1 = []
        @py_assert4 = 0
        @py_assert3 = i == @py_assert4
        @py_assert0 = @py_assert3
        if not @py_assert3:
            @py_assert10 = prev_score <= score
            @py_assert0 = @py_assert10
        if not @py_assert0:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s == %(py5)s', ), (i, @py_assert4)) % {'py2':@pytest_ar._saferepr(i) if 'i' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(i) else 'i',  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = '%(py7)s' % {'py7': @py_format6}
            @py_assert1.append(@py_format8)
            if not @py_assert3:
                @py_format12 = @pytest_ar._call_reprcompare(('<=', ), (@py_assert10,), ('%(py9)s <= %(py11)s', ), (prev_score, score)) % {'py9':@pytest_ar._saferepr(prev_score) if 'prev_score' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(prev_score) else 'prev_score',  'py11':@pytest_ar._saferepr(score) if 'score' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(score) else 'score'}
                @py_format14 = '%(py13)s' % {'py13': @py_format12}
                @py_assert1.append(@py_format14)
            @py_format15 = @pytest_ar._format_boolop(@py_assert1, 1) % {}
            @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
            raise AssertionError(@pytest_ar._format_explanation(@py_format17))
        @py_assert0 = @py_assert1 = @py_assert3 = @py_assert4 = @py_assert10 = None
        prev_score = score
        @py_assert1 = model.export_graphviz
        @py_assert4 = @py_assert1(out_file=path)
        if not @py_assert4:
            @py_format6 = 'assert %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.export_graphviz\n}(out_file=%(py3)s)\n}' % {'py0':@pytest_ar._saferepr(model) if 'model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(model) else 'model',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(path) if 'path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(path) else 'path',  'py5':@pytest_ar._saferepr(@py_assert4)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert4 = None
        os.remove(path)

    @py_assert1 = score >= target
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('>=', ), (@py_assert1,), ('%(py0)s >= %(py2)s', ), (score, target)) % {'py0':@pytest_ar._saferepr(score) if 'score' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(score) else 'score',  'py2':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None