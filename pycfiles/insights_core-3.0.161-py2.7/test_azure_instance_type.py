# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_azure_instance_type.py
# Compiled at: 2020-03-25 13:10:41
import pytest, doctest
from insights.parsers import azure_instance_type
from insights.parsers.azure_instance_type import AzureInstanceType
from insights.tests import context_wrap
from insights.parsers import SkipException, ParseException
from insights.core.plugins import ContentException
AZURE_TYPE_1 = 'Standard_L32s'
AZURE_TYPE_2 = 'Standard_NV48s_v3'
AZURE_TYPE_3 = '\n % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current\n                                  Dload  Upload   Total   Spent    Left  Speed\n   0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0\n 100  1126  100  1126    0     0  1374k      0 --:--:-- --:--:-- --:--:-- 1099k\nStandard_NV48s_v3\n'
AZURE_TYPE_DOC = 'Standard_L64s_v2'
AZURE_TYPE_AB_1 = ('\ncurl: (7) Failed to connect to 169.254.169.254 port 80: Connection timed out\n').strip()
AZURE_TYPE_AB_2 = ("\ncurl: (7) couldn't connect to host\n").strip()
AZURE_TYPE_AB_3 = ('\ncurl: (28) connect() timed out!\n').strip()
AZURE_TYPE_AB_4 = ('\n.micro\n').strip()
AZURE_TYPE_AB_5 = ('\nNo module named insights.tools\n').strip()

def test_azure_instance_type_ab_other():
    with pytest.raises(SkipException):
        AzureInstanceType(context_wrap(AZURE_TYPE_AB_1))
    with pytest.raises(SkipException):
        AzureInstanceType(context_wrap(AZURE_TYPE_AB_2))
    with pytest.raises(SkipException):
        AzureInstanceType(context_wrap(AZURE_TYPE_AB_3))
    with pytest.raises(ParseException) as (pe):
        AzureInstanceType(context_wrap(AZURE_TYPE_AB_4))
        assert 'Unrecognized type' in str(pe)
    with pytest.raises(ContentException) as (pe):
        AzureInstanceType(context_wrap(AZURE_TYPE_AB_5))


def test_azure_instance_type_ab_empty():
    with pytest.raises(SkipException):
        AzureInstanceType(context_wrap(''))


def test_azure_instance_type():
    azure = AzureInstanceType(context_wrap(AZURE_TYPE_1))
    assert azure.type == 'Standard'
    assert azure.size == 'L32s'
    assert azure.version is None
    assert azure.raw == 'Standard_L32s'
    azure = AzureInstanceType(context_wrap(AZURE_TYPE_2))
    assert azure.type == 'Standard'
    assert azure.size == 'NV48s'
    assert azure.version == 'v3'
    assert azure.raw == 'Standard_NV48s_v3'
    assert 'NV48s' in str(azure)
    return


def test_azure_instance_type_stats():
    azure = AzureInstanceType(context_wrap(AZURE_TYPE_3))
    assert azure.type == 'Standard'
    assert azure.size == 'NV48s'
    assert azure.version == 'v3'
    assert azure.raw == 'Standard_NV48s_v3'


def test_doc_examples():
    env = {'azure_inst': AzureInstanceType(context_wrap(AZURE_TYPE_DOC))}
    failed, total = doctest.testmod(azure_instance_type, globs=env)
    assert failed == 0