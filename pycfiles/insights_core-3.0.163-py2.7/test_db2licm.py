# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_db2licm.py
# Compiled at: 2019-11-14 13:57:46
import doctest, pytest
from insights.parsers import ParseException
from insights.tests import context_wrap
from insights.parsers import db2licm
from insights.parsers.db2licm import DB2Info
INVALID_OUTPUT = ('').strip()
VALID_OUTPUT = ('\nProduct name:                     DB2 Enterprise Server Edition\nLicense type:                     CPU Option\nExpiry date:                      Permanent\nProduct identifier:               db2ese\nVersion information:              9.7\nEnforcement policy:               Soft Stop\nFeatures:\nDB2 Performance Optimization ESE: Not licensed\nDB2 Storage Optimization:         Not licensed\nDB2 Advanced Access Control:      Not licensed\nIBM Homogeneous Replication ESE:  Not licensed\n').strip()
VALID_OUTPUT_MULTIPLE = ('\nProduct name:                     DB2 Enterprise Server Edition\nLicense type:                     CPU Option\nExpiry date:                      Permanent\nProduct identifier:               db2ese\nVersion information:              9.7\nEnforcement policy:               Soft Stop\nFeatures:\nDB2 Performance Optimization ESE: Not licensed\nDB2 Storage Optimization:         Not licensed\nDB2 Advanced Access Control:      Not licensed\nIBM Homogeneous Replication ESE:  Not licensed\n\nProduct name:                     DB2 Connect Server\nExpiry date:                      Expired\nProduct identifier:               db2consv\nVersion information:              9.7\nConcurrent connect user policy:   Disabled\nEnforcement policy:               Soft Stop\n').strip()

def test_valid_command_output_1():
    parser_result = DB2Info(context_wrap(VALID_OUTPUT))
    assert parser_result is not None
    assert parser_result['DB2 Enterprise Server Edition']['License type'] == 'CPU Option'
    assert parser_result['DB2 Enterprise Server Edition']['Expiry date'] == 'Permanent'
    assert parser_result['DB2 Enterprise Server Edition']['Product identifier'] == 'db2ese'
    assert parser_result['DB2 Enterprise Server Edition']['Version information'] == '9.7'
    assert parser_result['DB2 Enterprise Server Edition']['Enforcement policy'] == 'Soft Stop'
    assert parser_result['DB2 Enterprise Server Edition']['DB2 Performance Optimization ESE'] == 'Not licensed'
    assert parser_result['DB2 Enterprise Server Edition']['DB2 Storage Optimization'] == 'Not licensed'
    assert parser_result['DB2 Enterprise Server Edition']['DB2 Advanced Access Control'] == 'Not licensed'
    assert parser_result['DB2 Enterprise Server Edition']['IBM Homogeneous Replication ESE'] == 'Not licensed'
    return


def test_valid_command_output_2():
    parser_result = DB2Info(context_wrap(VALID_OUTPUT_MULTIPLE))
    assert parser_result is not None
    assert parser_result['DB2 Enterprise Server Edition']['License type'] == 'CPU Option'
    assert parser_result['DB2 Enterprise Server Edition']['Expiry date'] == 'Permanent'
    assert parser_result['DB2 Enterprise Server Edition']['Product identifier'] == 'db2ese'
    assert parser_result['DB2 Enterprise Server Edition']['Version information'] == '9.7'
    assert parser_result['DB2 Enterprise Server Edition']['Enforcement policy'] == 'Soft Stop'
    assert parser_result['DB2 Enterprise Server Edition']['DB2 Performance Optimization ESE'] == 'Not licensed'
    assert parser_result['DB2 Enterprise Server Edition']['DB2 Storage Optimization'] == 'Not licensed'
    assert parser_result['DB2 Enterprise Server Edition']['DB2 Advanced Access Control'] == 'Not licensed'
    assert parser_result['DB2 Enterprise Server Edition']['IBM Homogeneous Replication ESE'] == 'Not licensed'
    assert parser_result['DB2 Connect Server']['Expiry date'] == 'Expired'
    assert parser_result['DB2 Connect Server']['Product identifier'] == 'db2consv'
    assert parser_result['DB2 Connect Server']['Version information'] == '9.7'
    assert parser_result['DB2 Connect Server']['Enforcement policy'] == 'Soft Stop'
    assert parser_result['DB2 Connect Server']['Concurrent connect user policy'] == 'Disabled'
    return


def test_invalid_command_output():
    with pytest.raises(ParseException) as (e):
        DB2Info(context_wrap(INVALID_OUTPUT))
    assert 'Unable to parse db2licm info: []' == str(e.value)


def test_db2licm_doc_examples():
    env = {'parser_result': DB2Info(context_wrap(VALID_OUTPUT_MULTIPLE))}
    failed, total = doctest.testmod(db2licm, globs=env)
    assert failed == 0