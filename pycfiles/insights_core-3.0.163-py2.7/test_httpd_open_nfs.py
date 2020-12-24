# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_httpd_open_nfs.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import httpd_open_nfs
from insights.parsers.httpd_open_nfs import HttpdOnNFSFilesCount
from insights.tests import context_wrap
import doctest
http_nfs = ('\n{"http_ids": [1787, 2399], "nfs_mounts": ["/data", "/www"], "open_nfs_files": 1000}\n').strip()

def test_http_nfs():
    httpd_nfs_counting = HttpdOnNFSFilesCount(context_wrap(http_nfs))
    assert len(httpd_nfs_counting.data) == 3
    assert httpd_nfs_counting.http_ids == [1787, 2399]
    assert httpd_nfs_counting.nfs_mounts == ['/data', '/www']
    assert httpd_nfs_counting.data.get('open_nfs_files') == 1000


def test_http_nfs_documentation():
    env = {'httpon_nfs': HttpdOnNFSFilesCount(context_wrap(http_nfs))}
    failed, total = doctest.testmod(httpd_open_nfs, globs=env)
    assert failed == 0