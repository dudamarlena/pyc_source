# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/iis_cr/vipe/vipe/oozie/reader/test/test_graph_serialization.py
# Compiled at: 2016-02-15 13:44:30
# Size of source mod 2**32: 1113 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
__author__ = 'Mateusz Kobos mkobos@icm.edu.pl'
from vipe.common.utils import read_as_string
from vipe.oozie.graph import OozieGraph

def test_simple_java_workflow():
    check('../../test/data/java/workflow.yaml')


def check(yaml_file_path):
    graph1 = OozieGraph.from_yaml_dump(read_as_string(__name__, yaml_file_path))
    yaml_str1 = graph1.to_yaml_dump()
    graph2 = OozieGraph.from_yaml_dump(yaml_str1)
    yaml_str2 = graph2.to_yaml_dump()
    @py_assert1 = yaml_str1 == yaml_str2
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (yaml_str1, yaml_str2)) % {'py0': @pytest_ar._saferepr(yaml_str1) if 'yaml_str1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(yaml_str1) else 'yaml_str1',  'py2': @pytest_ar._saferepr(yaml_str2) if 'yaml_str2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(yaml_str2) else 'yaml_str2'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = graph1 == graph2
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (graph1, graph2)) % {'py0': @pytest_ar._saferepr(graph1) if 'graph1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(graph1) else 'graph1',  'py2': @pytest_ar._saferepr(graph2) if 'graph2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(graph2) else 'graph2'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None