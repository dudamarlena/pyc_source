# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_nvme_core_io_timeout.py
# Compiled at: 2019-05-16 13:41:33
import pytest, doctest
from insights.parsers import nvme_core_io_timeout
from insights.parsers.nvme_core_io_timeout import NVMeCoreIOTimeout
from insights.tests import context_wrap
from insights.parsers import SkipException, ParseException
NVME_CORE_IO_TIMEOUT = '4294967295'
NVME_CORE_IO_TIMEOUT_INVALID_1 = ('\n30\n255\n').strip()
NVME_CORE_IO_TIMEOUT_INVALID_2 = 'FF'

def test_nvme_core_io_timeout_se():
    with pytest.raises(SkipException):
        NVMeCoreIOTimeout(context_wrap(''))
    with pytest.raises(SkipException):
        NVMeCoreIOTimeout(context_wrap(NVME_CORE_IO_TIMEOUT_INVALID_1))


def test_nvme_core_io_timeout_pe():
    with pytest.raises(ParseException) as (pe):
        NVMeCoreIOTimeout(context_wrap(NVME_CORE_IO_TIMEOUT_INVALID_2))
    assert 'Unexpected content' in str(pe)


def test_nvme_core_io_timeout():
    nciotmo = NVMeCoreIOTimeout(context_wrap(NVME_CORE_IO_TIMEOUT))
    assert nciotmo.val == 4294967295


def test_doc_examples():
    env = {'nciotmo': NVMeCoreIOTimeout(context_wrap(NVME_CORE_IO_TIMEOUT))}
    failed, total = doctest.testmod(nvme_core_io_timeout, globs=env)
    assert failed == 0