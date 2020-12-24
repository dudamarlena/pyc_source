# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_meminfo.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import meminfo
from insights.tests import context_wrap
import pytest
MEMINFO = ('\nMemTotal:        8009912 kB\nMemFree:          538760 kB\nMemAvailable:    6820236 kB\nBuffers:          157048 kB\nCached:          4893932 kB\nSwapCached:          120 kB\nActive:          2841500 kB\nInactive:        2565560 kB\nActive(anon):     311596 kB\nInactive(anon):   505800 kB\nActive(file):    2529904 kB\nInactive(file):  2059760 kB\nUnevictable:           0 kB\nMlocked:               0 kB\nSwapTotal:       3145724 kB\nSwapFree:        3136352 kB\nDirty:               140 kB\nWriteback:             0 kB\nAnonPages:        355484 kB\nMapped:            51988 kB\nShmem:            461316 kB\nSlab:            1982652 kB\nSReclaimable:    1945228 kB\nSUnreclaim:        37424 kB\nKernelStack:        3568 kB\nPageTables:         8504 kB\nNFS_Unstable:          0 kB\nBounce:                0 kB\nWritebackTmp:          0 kB\nCommitLimit:     7150680 kB\nCommitted_AS:    1218948 kB\nVmallocTotal:   34359738367 kB\nVmallocUsed:      122268 kB\nVmallocChunk:   34359607064 kB\nHardwareCorrupted:     0 kB\nAnonHugePages:    135168 kB\nHugePages_Total:       0\nHugePages_Free:        0\nHugePages_Rsvd:        0\nHugePages_Surp:        0\nHugepagesize:       2048 kB\nDirectMap4k:       71664 kB\nDirectMap2M:     8316928 kB\n').strip()

def test_meminfo():
    values = []
    for l in MEMINFO.splitlines():
        values.append(l.split()[1].strip())

    m = meminfo.MemInfo(context_wrap(MEMINFO))
    actual = [
     m.total, m.free, m.available, m.buffers, m.cached, m.swap.cached,
     m.active, m.inactive, m.anon.active, m.anon.inactive, m.file.active,
     m.file.inactive, m.unevictable, m.mlocked, m.swap.total, m.swap.free,
     m.dirty, m.writeback, m.anon.pages, m.mapped, m.shmem, m.slab.total,
     m.slab.reclaimable, m.slab.unreclaimable, m.kernel_stack, m.page_tables,
     m.nfs_unstable, m.bounce, m.writeback_tmp, m.commit.limit, m.commit.total,
     m.vmalloc.total, m.vmalloc.used, m.vmalloc.chunk, m.corrupted,
     m.huge_pages.anon, m.huge_pages.total, m.huge_pages.free,
     m.huge_pages.reserved, m.huge_pages.surplus, m.huge_pages.size,
     m.direct_map.kb, m.direct_map.mb]
    for i in range(len(actual)):
        assert isinstance(actual[i], int), "Line %d's value is not an int: %s" % (i, type(actual[i]))
        assert actual[i] == int(values[i]) * 1024, 'Line %d failed to match' % i

    assert m.swap.used == (int(values[14]) - int(values[15]) - int(values[5])) * 1024
    assert m.used == 7650459648


MEMINFO_SHORT = '\nMemTotal:        8009912 kB\nMemAvailable:    6820236 kB\n'

def test_meminfo_short():
    m = meminfo.MemInfo(context_wrap(MEMINFO_SHORT))
    with pytest.raises(TypeError):
        assert m.swap.used is None
    with pytest.raises(TypeError):
        assert m.used is None
    return


def test_using_huge_pages():
    t = [
     'AnonHugePages:    135168 kB',
     'HugePages_Total:       0']
    m = meminfo.MemInfo(context_wrap(t))
    assert not m.huge_pages.using
    assert m.huge_pages.using_transparent
    t = [
     'AnonHugePages:    0 kB',
     'HugePages_Total:  123456',
     'HugePages_Rsvd:     4096']
    m = meminfo.MemInfo(context_wrap(t))
    assert m.huge_pages.using
    assert not m.huge_pages.using_transparent
    assert m.huge_pages.total == 123456
    assert m.huge_pages.reserved == 4096