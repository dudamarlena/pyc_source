# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_readlink_mtab.py
# Compiled at: 2019-12-13 11:35:46
import pytest, doctest
from insights.tests import context_wrap
from insights.parsers import readlink_e_mtab, SkipException
REAL_FILE_PATH = ('\n/proc/4578/mounts\n').strip()
BAD_FILE_PATH = ''

def test_doc_examples():
    env = {'mtab': readlink_e_mtab.ReadLinkEMtab(context_wrap(REAL_FILE_PATH))}
    failed, total = doctest.testmod(readlink_e_mtab, globs=env)
    assert failed == 0


def test_readlink_e_mtab():
    mtab = readlink_e_mtab.ReadLinkEMtab(context_wrap(REAL_FILE_PATH))
    assert len(mtab.path) > 0
    assert mtab.path == REAL_FILE_PATH


def test_fail():
    with pytest.raises(SkipException) as (e):
        readlink_e_mtab.ReadLinkEMtab(context_wrap(BAD_FILE_PATH))
    assert 'No Data from command: readlink -e /etc/mtab' in str(e)