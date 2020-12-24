# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/iis_cr/vipe/vipe/graphviz/test/test_importance_score_map.py
# Compiled at: 2016-02-15 13:44:30
# Size of source mod 2**32: 1797 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
__author__ = 'Mateusz Kobos mkobos@icm.edu.pl'
from vipe.graphviz.importance_score_map import ImportanceScoreMap, DetailLevel
from vipe.pipeline.pipeline import NodeImportance

def test_medium():
    check(DetailLevel.medium, {NodeImportance.lowest: -3,  NodeImportance.very_low: -2, 
     NodeImportance.low: -1, 
     NodeImportance.normal: 0})


def test_highest():
    check(DetailLevel.highest, {NodeImportance.lowest: 0,  NodeImportance.very_low: 1, 
     NodeImportance.low: 2, 
     NodeImportance.normal: 3})


def test_lowest():
    check(DetailLevel.lowest, {NodeImportance.lowest: -5,  NodeImportance.very_low: -4, 
     NodeImportance.low: -3, 
     NodeImportance.normal: -2})


def check(detail_level, expected_importance_scores):
    map_ = ImportanceScoreMap(detail_level)
    for importance, expected_score in expected_importance_scores.items():
        actual_score = map_.get_score(importance)
        @py_assert1 = expected_score == actual_score
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected_score, actual_score)) % {'py0': @pytest_ar._saferepr(expected_score) if 'expected_score' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_score) else 'expected_score',  'py2': @pytest_ar._saferepr(actual_score) if 'actual_score' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual_score) else 'actual_score'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None