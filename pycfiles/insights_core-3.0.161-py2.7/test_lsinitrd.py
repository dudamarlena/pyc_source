# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_lsinitrd.py
# Compiled at: 2019-11-14 13:57:46
import doctest, pytest
from insights.parsers import lsinitrd
from insights.tests import context_wrap
LSINITRD_ALL = ('\nImage: /boot/initramfs-3.10.0-862.el7.x86_64.img: 24M\n========================================================================\nEarly CPIO image\n========================================================================\ndrwxr-xr-x   3 root     root            0 Apr 20 15:58 .\n-rw-r--r--   1 root     root            2 Apr 20 15:58 early_cpio\ndrwxr-xr-x   3 root     root            0 Apr 20 15:58 kernel\ndrwxr-xr-x   3 root     root            0 Apr 20 15:58 kernel/x86\ndrwxr-xr-x   2 root     root            0 Apr 20 15:58 kernel/x86/microcode\n-rw-r--r--   1 root     root        12684 Apr 20 15:58 kernel/x86/microcode/AuthenticAMD.bin\n========================================================================\nVersion: dracut-033-535.el7\n\nArguments: -f\n\ndracut modules:\nbash\nnss-softokn\ni18n\nnetwork\nifcfg\ndrm\nplymouth\ndm\nkernel-modules\nlvm\nresume\nrootfs-block\nterminfo\nudev-rules\nbiosdevname\nsystemd\nusrmount\nbase\nfs-lib\nshutdown\n========================================================================\ndrwxr-xr-x  12 root     root            0 Apr 20 15:58 .\ncrw-r--r--   1 root     root       5,   1 Apr 20 15:57 dev/console\ncrw-r--r--   1 root     root       1,  11 Apr 20 15:57 dev/kmsg\ncrw-r--r--   1 root     root       1,   3 Apr 20 15:57 dev/null\nlrwxrwxrwx   1 root     root            7 Apr 20 15:57 bin -> usr/bin\n========================================================================\n').strip()
LSINITRD_FILTERED = ('\ndrwxr-xr-x   3 root     root            0 Apr 20 15:58 kernel/x86\nVersion: dracut-033-535.el7\ndracut modules:\nkernel-modules\nudev-rules\ndrwxr-xr-x  12 root     root            0 Apr 20 15:58 .\ncrw-r--r--   1 root     root       5,   1 Apr 20 15:57 dev/console\ncrw-r--r--   1 root     root       1,  11 Apr 20 15:57 dev/kmsg\ncrw-r--r--   1 root     root       1,   3 Apr 20 15:57 dev/null\n').strip()
LSINITRD_EMPTY = ''
LSINITRD_BROKEN = ('\ndrwxr-xr-x   3 root     root            0 Apr 20 15:58 kernel/x86\nVersion: dracut-033-535.el7\ndracut modules:\nkernel-modules\nudev-rules\ndrwxr-xr-x  12 root     root            0 Apr 20 15:58 .\ncrw-r--r--   1\ncrw-r-\nc\n').strip()

def test_lsinitrd_empty():
    d = lsinitrd.Lsinitrd(context_wrap(LSINITRD_EMPTY))
    assert len(d.data) == 0
    assert d.search(name__contains='kernel') == []
    assert d.unparsed_lines == []


def test_lsinitrd_filtered():
    d = lsinitrd.Lsinitrd(context_wrap(LSINITRD_FILTERED))
    assert len(d.data) == 5
    assert d.search(name__contains='kernel') == [{'type': 'd', 'perms': 'rwxr-xr-x', 'links': 3, 'owner': 'root', 'group': 'root', 'size': 0, 'date': 'Apr 20 15:58', 'name': 'kernel/x86', 'raw_entry': 'drwxr-xr-x   3 root     root            0 Apr 20 15:58 kernel/x86', 'dir': ''}]
    assert d.unparsed_lines == ['Version: dracut-033-535.el7', 'dracut modules:', 'kernel-modules', 'udev-rules']


def test_lsinitrd_all():
    d = lsinitrd.Lsinitrd(context_wrap(LSINITRD_ALL))
    lsdev = d.search(name__contains='dev')
    assert len(lsdev) == 3
    dev_console = {'type': 'c', 
       'perms': 'rw-r--r--', 'links': 1, 'owner': 'root', 'group': 'root', 'major': 5, 
       'minor': 1, 'date': 'Apr 20 15:57', 'name': 'dev/console', 'dir': '', 'raw_entry': 'crw-r--r--   1 root     root       5,   1 Apr 20 15:57 dev/console'}
    assert dev_console in lsdev
    assert 'dev/kmsg' in [ l['name'] for l in lsdev ]
    assert 'dev/null' in [ l['name'] for l in lsdev ]
    assert len(d.data) == 10
    assert len(d.unparsed_lines) == 32
    assert 'udev-rules' in d.unparsed_lines


def test_lsinitrd_broken():
    """
    For this testcase, ls_parser.parse() will throw an IndexError.
    Assert with this specific error here.
    """
    with pytest.raises(Exception) as (err):
        lsinitrd.Lsinitrd(context_wrap(LSINITRD_BROKEN))
    assert 'list index out of range' in str(err)


def test_lsinitrd_docs():
    failed_count, tests = doctest.testmod(globs={'ls': lsinitrd.Lsinitrd(context_wrap(LSINITRD_FILTERED))})
    assert failed_count == 0