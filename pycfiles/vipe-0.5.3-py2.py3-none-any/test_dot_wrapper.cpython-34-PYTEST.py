# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/iis_cr/vipe/vipe/graphviz/test/test_dot_wrapper.py
# Compiled at: 2016-02-15 13:44:30
# Size of source mod 2**32: 1250 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
__author__ = 'Mateusz Kobos mkobos@icm.edu.pl'
import pytest
from vipe.graphviz.dot_wrapper import DotBuilderWrapper
from vipe.graphviz.importance_score_map import ImportanceScoreMap, DetailLevel
from vipe.pipeline.pipeline import Node

class TestDotBuilderWrapper:

    def test_nodes_with_the_same_name_are_disallowed(self):
        importance_map = ImportanceScoreMap(DetailLevel.medium)
        builder = DotBuilderWrapper(importance_map, True, True)
        builder.add_node('n1', Node('Java', {}, {}))
        builder.add_node('n2', Node('Java', {}, {}))
        with pytest.raises(Exception):
            builder.add_node('n1', 'Java', Node({}, {}))