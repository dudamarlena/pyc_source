# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_kdump.py
# Compiled at: 2019-05-16 13:41:33
import pytest
from insights.parsers import kdump, ParseException
from insights.tests import context_wrap
KDUMP_WITH_NORMAL_COMMENTS = ('\n# this is a comment\n\nssh kdumpuser@10.209.136.62\npath /kdump/raw\ncore_collector makedumpfile -c --message-level 1 -d 31\n').strip()
KDUMP_WITH_INLINE_COMMENTS = ('\nnfs4 10.209.136.62:/kdumps\npath /kdump/raw #some path stuff\ncore_collector makedumpfile -c --message-level 1 -d 31\n').strip()
KDUMP_WITH_EQUAL = ('\nnfs 10.209.136.62:/kdumps\npath /kdump/raw #some path stuff\ncore_collector makedumpfile -c --message-level 1 -d 31\nsome_var "blah=3"\noptions bonding mode=active-backup miimon=100\n').strip()
KDUMP_WITH_BLACKLIST = '\npath /var/crash\ncore_collector makedumpfile -c --message-level 1 -d 24\ndefault shell\nblacklist vxfs\nblacklist vxportal\nblacklist vxted\nblacklist vxcafs\nblacklist fdd\nignore_me\n'
KDUMP_WITH_NET = ('\nnet user@raw.server.com\npath /var/crash\n').strip()
KDUMP_MATCH_1 = ('\nnet user@raw.server.com\npath /var/crash\n').strip()

def test_with_normal_comments():
    context = context_wrap(KDUMP_WITH_NORMAL_COMMENTS)
    kd = kdump.KDumpConf(context)
    expected = '# this is a comment'
    assert expected == kd.comments[0]
    assert not kd.is_nfs()
    assert kd.is_ssh()
    assert not kd.using_local_disk


def test_with_inline_comments():
    context = context_wrap(KDUMP_WITH_INLINE_COMMENTS)
    kd = kdump.KDumpConf(context)
    expected = 'path /kdump/raw #some path stuff'
    assert expected == kd.inline_comments[0]
    assert '/kdump/raw' == kd['path']
    assert kd.is_nfs()
    assert not kd.is_ssh()
    assert not kd.using_local_disk


def test_with_equal():
    context = context_wrap(KDUMP_WITH_EQUAL)
    kd = kdump.KDumpConf(context)
    expected = '"blah=3"'
    assert expected == kd['some_var']
    assert 'options' in kd.data
    assert isinstance(kd.data['options'], dict)
    assert 'bonding' in kd.data['options']
    assert 'mode=active-backup miimon=100' == kd.data['options']['bonding']
    assert kd.options('bonding') == 'mode=active-backup miimon=100'
    assert kd.is_nfs()
    assert not kd.is_ssh()
    assert not kd.using_local_disk


def test_get_hostname():
    context = context_wrap(KDUMP_WITH_EQUAL)
    kd = kdump.KDumpConf(context)
    assert '10.209.136.62' == kd.hostname
    context = context_wrap(KDUMP_MATCH_1)
    kd = kdump.KDumpConf(context)
    assert 'raw.server.com' == kd.hostname


def test_get_ip():
    context = context_wrap(KDUMP_WITH_EQUAL)
    kd = kdump.KDumpConf(context)
    assert '10.209.136.62' == kd.ip
    context = context_wrap(KDUMP_MATCH_1)
    kd = kdump.KDumpConf(context)
    assert kd.ip is None
    return


def test_blacklist_repeated():
    context = context_wrap(KDUMP_WITH_BLACKLIST)
    kd = kdump.KDumpConf(context)
    assert 'blacklist' in kd.data
    assert kd.data['blacklist'] == ['vxfs', 'vxportal', 'vxted', 'vxcafs', 'fdd']
    assert not kd.is_nfs()
    assert not kd.is_ssh()
    assert kd.using_local_disk


def test_net():
    context = context_wrap(KDUMP_WITH_NET)
    kd = kdump.KDumpConf(context)
    assert 'net' in kd.data
    assert 'path' in kd.data
    assert not kd.using_local_disk
    with pytest.raises(KeyError):
        assert kd[3]


KEXEC_CRASH_SIZE_1 = '134217728'
KEXEC_CRASH_SIZE_2 = '0'
KEXEC_CRASH_SIZE_BAD = ''

def test_kexec_crash_size():
    kcs = kdump.KexecCrashSize(context_wrap(KEXEC_CRASH_SIZE_1))
    assert kcs.size == 134217728
    kcs = kdump.KexecCrashSize(context_wrap(KEXEC_CRASH_SIZE_2))
    assert kcs.size == 0
    kcs = kdump.KexecCrashSize(context_wrap(KEXEC_CRASH_SIZE_BAD))
    assert kcs.size == 0


KDUMP_CRASH_NOT_LOADED = '0'
KDUMP_CRASH_LOADED = '1'
KDUMP_CRASH_LOADED_BAD = ''

def test_loaded():
    ctx = context_wrap(KDUMP_CRASH_LOADED, path='/sys/kernel/kexec_crash_loaded')
    assert kdump.KexecCrashLoaded(ctx).is_loaded


def test_not_loaded():
    ctx = context_wrap(KDUMP_CRASH_NOT_LOADED, path='/sys/kernel/kexec_crash_loaded')
    assert not kdump.KexecCrashLoaded(ctx).is_loaded


def test_loaded_bad():
    ctx = context_wrap(KDUMP_CRASH_LOADED_BAD, path='/sys/kernel/kexec_crash_loaded')
    assert not kdump.KexecCrashLoaded(ctx).is_loaded


KDUMP_LOCAL_FS_1 = ('\next3 UUID=f15759be-89d4-46c4-9e1d-1b67e5b5da82\npath /usr/local/cores\ncore_collector makedumpfile -c --message-level 1 -d 31\n').strip()
KDUMP_LOCAL_FS_UNSUPPORTED_2 = ('\nauto LABEL=/boot\npath /usr/local/cores\ncore_collector makedumpfile -c --message-level 1 -d 31\n').strip()
KDUMP_REMOTE_TARGET_3 = ('\nnet user@raw.server.com\npath /usr/local/cores\ncore_collector makedumpfile -c --message-level 1 -d 31\n').strip()

def test_target():
    kd = kdump.KDumpConf(context_wrap(KDUMP_LOCAL_FS_1))
    assert kd.using_local_disk
    assert kd.target == ('ext3', 'UUID=f15759be-89d4-46c4-9e1d-1b67e5b5da82')
    assert kd['path'] == '/usr/local/cores'
    kd = kdump.KDumpConf(context_wrap(KDUMP_LOCAL_FS_UNSUPPORTED_2))
    assert kd.using_local_disk
    assert kd.target is None
    assert kd['path'] == '/usr/local/cores'
    kd = kdump.KDumpConf(context_wrap(KDUMP_REMOTE_TARGET_3))
    assert not kd.using_local_disk
    assert kd.target == ('net', 'user@raw.server.com')
    return


KDUMP_TARGET_CONFLICT_1 = '\nnet user@raw.server.com\nraw /dev/sda5\n'
KDUMP_TARGET_CONFLICT_2 = '\next4 /dev/sdb1\next4 UUID=f15759be-89d4-46c4-9e1d-1b67e5b5da82\n'

def test_conflict_targets_excptions():
    with pytest.raises(ParseException) as (e_info):
        kdump.KDumpConf(context_wrap(KDUMP_TARGET_CONFLICT_1))
        assert 'More than one target is configured' in str(e_info.value)
    with pytest.raises(ParseException) as (e_info):
        kdump.KDumpConf(context_wrap(KDUMP_TARGET_CONFLICT_2))
        assert 'More than one ext4 type targets' in str(e_info.value)