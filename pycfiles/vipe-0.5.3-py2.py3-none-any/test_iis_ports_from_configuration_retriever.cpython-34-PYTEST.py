# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/iis_cr/vipe/vipe/oozie/converter/test/test_iis_ports_from_configuration_retriever.py
# Compiled at: 2016-02-15 13:44:30
# Size of source mod 2**32: 2207 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
__author__ = 'Mateusz Kobos mkobos@icm.edu.pl'
import pytest
from vipe.oozie.converter.iis import PortsFromConfigurationRetriever

def test_simple():
    conf = {'input_document': '1',  'output_document': '2',  'input_person': '3'}
    check('input', conf, {'document': '1',  'person': '3'})
    check('output', conf, {'document': '2'})


def test_single_prefix():
    conf = {'input': '1',  'input_document': '2',  'output': '3'}
    check('output', conf, {'output': '3'})
    with pytest.raises(Exception):
        PortsFromConfigurationRetriever.run('input', conf)


def test_root_ports():
    conf = {'output_metadataimport_root': 'meta_root',  'metadataimport_output_name_document_meta': 'doc_meta', 
     'metadataimport_output_name_document_content': 'doc_content', 
     'output_unrelated_port': 'whatevs', 
     'output_person_root': 'person_root', 
     'person_output_name_name': 'name'}
    check('output', conf, {'metadataimport_document_meta': 'meta_root/doc_meta',  'metadataimport_document_content': 'meta_root/doc_content', 
     'unrelated_port': 'whatevs', 
     'person_name': 'person_root/name'})


def test_root_port_with_missing_port_names():
    conf = {'output_person_root': 'person_root',  'output_unrelated_port': 'whatevs'}
    with pytest.raises(Exception):
        PortsFromConfigurationRetriever.run('output', conf)


def check(type_prefix, configuration, expected):
    actual = PortsFromConfigurationRetriever.run(type_prefix, configuration)
    @py_assert1 = expected == actual
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected, actual)) % {'py0': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2': @pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None