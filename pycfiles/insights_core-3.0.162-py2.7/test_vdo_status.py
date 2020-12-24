# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_vdo_status.py
# Compiled at: 2019-11-14 13:57:46
from insights.parsers import ParseException
from insights.parsers import vdo_status
from insights.parsers.vdo_status import VDOStatus
from insights.tests import context_wrap
import pytest, doctest
INPUT_EXP = ('\nVDO status 2019-07-27 04:40:40-04:00\nrdma-qe-04.lab.bos.redhat.com\n').strip()
INPUT_SIMPLE_EXP = "\nVDO status:\n  Date: '2019-07-27 04:40:40-04:00'\n  Node: rdma-qe-04.lab.bos.redhat.com\nKernel module:\n  Loaded: true\n  Name: kvdo\n  Version information:\n    kvdo version: 6.1.0.153\nConfiguration:\n  File: /etc/vdoconf.yml\n  Last modified: '2019-07-26 05:07:48'\nV??DOs:\n  vdo1:\n     XX: XX\n  vdo2:\n     XX: XX\n\n"
INPUT_STATUS_2 = "\nVDO status:\n  Date: '2019-09-23 02:00:38+02:00'\n  Node: hello_test\nKernel module:\n  Loaded: false\n  Name: kvdo\n  Version information:\n    kvdo version: 6.1.2.41\nConfiguration:\n  File: /etc/vdoconf.yml\n  Last modified: '2018-06-13 16:46:03'\nVDOs:\n  vdoapp1:\n    Acknowledgement threads: 1\n    Activate: enabled\n    Bio rotation interval: 64\n    Bio submission threads: 4\n    Block map cache size: 128M\n    Block map period: 16380\n    Block size: 4096\n    CPU-work threads: 2\n    Compression: enabled\n    Configured write policy: auto\n    Deduplication: enabled\n    Device mapper status: not available\n    Emulate 512 byte: disabled\n    Hash zone threads: 1\n    Index checkpoint frequency: 0\n    Index memory setting: 0.25\n    Index parallel factor: 0\n    Index sparse: disabled\n    Index status: not available\n    Logical size: 466771896K\n    Logical threads: 1\n    Physical size: 450G\n    Physical threads: 1\n    Read cache: disabled\n    Read cache size: 0M\n    Slab size: 2G\n    Storage device: /dev/sdh\n    VDO statistics: not available\n  vdoapp2:\n    Acknowledgement threads: 1\n    Activate: enabled\n    Bio rotation interval: 64\n    Bio submission threads: 4\n    Block map cache size: 128M\n    Block map period: 16380\n    Block size: 4096\n    CPU-work threads: 2\n    Compression: enabled\n    Configured write policy: auto\n    Deduplication: enabled\n    Device mapper status: not available\n    Emulate 512 byte: disabled\n    Hash zone threads: 1\n    Index checkpoint frequency: 0\n    Index memory setting: 0.25\n    Index parallel factor: 0\n    Index sparse: disabled\n    Index status: not available\n    Logical size: 466771896K\n    Logical threads: 1\n    Physical size: 450G\n    Physical threads: 1\n    Read cache: disabled\n    Read cache size: 0M\n    Slab size: 2G\n    Storage device: /dev/sdc\n    VDO statistics: not available\n"
INPUT_STATUS_SIMPLE = "\nVDO status:\n  Date: '2019-07-27 04:40:40-04:00'\n  Node: rdma-qe-04.lab.bos.redhat.com\nKernel module:\n  Loaded: true\n  Name: kvdo\n  Version information:\n    kvdo version: 6.1.0.153\nConfiguration:\n  File: /etc/vdoconf.yml\n  Last modified: '2019-07-26 05:07:48'\nVDOs:\n  vdo1:\n    Acknowledgement threads: 1\n    Activate: enabled\n    Slab size: 2G\n    VDO statistics:\n      /dev/mapper/vdo1:\n        block size: 4096\n        data blocks used: 161863\n        logical blocks: 844568\n        logical blocks used: 844502\n        overhead blocks used: 728175\n        physical blocks: 1572864\n        slab count: 26\n  vdo2:\n    Acknowledgement threads: 1\n    Activate: enabled\n    Slab size: 128M\n    VDO statistics:\n      /dev/mapper/vdo2:\n        block size: 4096\n        data blocks used: 161861\n        logical blocks: 844562\n        logical blocks used: 0\n        overhead blocks used: 728172\n        physical blocks: 1572861\n        slab count: 26\n"
INPUT_EMPTY = ("\nVDO status:\n  Date: '2019-07-25 01:38:47-04:00'\n  Node: rdma-dev-09.lab.bos.redhat.com\nKernel module:\n  Loaded: false\n  Name: kvdo\n  Version information:\n    kvdo version: 6.1.0.153\nConfiguration:\n  File: does not exist\n  Last modified: not available\nVDOs: {}\n").strip()
INPUT_STATUS_FULL = ("\nVDO status:\n  Date: '2019-07-24 20:48:16-04:00'\n  Node: dell-m620-10.rhts.gsslab.pek2.redhat.com\nKernel module:\n  Loaded: true\n  Name: kvdo\n  Version information:\n    kvdo version: 6.1.0.153\nConfiguration:\n  File: /etc/vdoconf.yml\n  Last modified: '2019-07-24 20:47:59'\nVDOs:\n  vdo1:\n    Acknowledgement threads: 1\n    Activate: enabled\n    Bio rotation interval: 64\n    Bio submission threads: 4\n    Block map cache size: 128M\n    Block map period: 16380\n    Block size: 4096\n    CPU-work threads: 2\n    Compression: enabled\n    Configured write policy: auto\n    Deduplication: enabled\n    Device mapper status: 0 8370216 vdo /dev/sda3 albserver online cpu=2,bio=4,ack=1,bioRotationInterval=64\n    Emulate 512 byte: disabled\n    Hash zone threads: 1\n    Index checkpoint frequency: 0\n    Index memory setting: 0.25\n    Index parallel factor: 0\n    Index sparse: disabled\n    Index status: online\n    Logical size: 4185108K\n    Logical threads: 1\n    Physical size: 7G\n    Physical threads: 1\n    Read cache: disabled\n    Read cache size: 0M\n    Slab size: 2G\n    Storage device: /dev/sda3\n    VDO statistics:\n      /dev/mapper/vdo1:\n        1K-blocks: 7340032\n        1K-blocks available: 4191472\n        1K-blocks used: 3148560\n        512 byte emulation: false\n        KVDO module bios used: 74572\n        KVDO module bytes used: 851421880\n        KVDO module peak bio count: 74860\n        KVDO module peak bytes used: 851423752\n        bios acknowledged discard: 0\n        bios acknowledged flush: 0\n        bios acknowledged fua: 0\n        bios acknowledged partial discard: 0\n        bios acknowledged partial flush: 0\n        bios acknowledged partial fua: 0\n        bios acknowledged partial read: 0\n        bios acknowledged partial write: 0\n        bios acknowledged read: 261\n        bios acknowledged write: 0\n        bios in discard: 0\n        bios in flush: 0\n        bios in fua: 0\n        bios in partial discard: 0\n        bios in partial flush: 0\n        bios in partial fua: 0\n        bios in partial read: 0\n        bios in partial write: 0\n        bios in progress discard: 0\n        bios in progress flush: 0\n        bios in progress fua: 0\n        bios in progress read: 0\n        bios in progress write: 0\n        bios in read: 261\n        bios in write: 0\n        bios journal completed discard: 0\n        bios journal completed flush: 0\n        bios journal completed fua: 0\n        bios journal completed read: 0\n        bios journal completed write: 0\n        bios journal discard: 0\n        bios journal flush: 0\n        bios journal fua: 0\n        bios journal read: 0\n        bios journal write: 0\n        bios meta completed discard: 0\n        bios meta completed flush: 0\n        bios meta completed fua: 0\n        bios meta completed read: 3\n        bios meta completed write: 65\n        bios meta discard: 0\n        bios meta flush: 1\n        bios meta fua: 1\n        bios meta read: 3\n        bios meta write: 65\n        bios out completed discard: 0\n        bios out completed flush: 0\n        bios out completed fua: 0\n        bios out completed read: 0\n        bios out completed write: 0\n        bios out discard: 0\n        bios out flush: 0\n        bios out fua: 0\n        bios out read: 0\n        bios out write: 0\n        bios page cache completed discard: 0\n        bios page cache completed flush: 0\n        bios page cache completed fua: 0\n        bios page cache completed read: 0\n        bios page cache completed write: 0\n        bios page cache discard: 0\n        bios page cache flush: 0\n        bios page cache fua: 0\n        bios page cache read: 0\n        bios page cache write: 0\n        block map cache pressure: 0\n        block map cache size: 134217728\n        block map clean pages: 0\n        block map dirty pages: 0\n        block map discard required: 0\n        block map failed pages: 0\n        block map failed reads: 0\n        block map failed writes: 0\n        block map fetch required: 0\n        block map flush count: 0\n        block map found in cache: 0\n        block map free pages: 32768\n        block map incoming pages: 0\n        block map outgoing pages: 0\n        block map pages loaded: 0\n        block map pages saved: 0\n        block map read count: 0\n        block map read outgoing: 0\n        block map reclaimed: 0\n        block map wait for page: 0\n        block map write count: 0\n        block size: 4096\n        completed recovery count: 0\n        compressed blocks written: 0\n        compressed fragments in packer: 0\n        compressed fragments written: 0\n        current VDO IO requests in progress: 0\n        current dedupe queries: 0\n        data blocks used: 0\n        dedupe advice stale: 0\n        dedupe advice timeouts: 0\n        dedupe advice valid: 0\n        entries indexed: 0\n        flush out: 0\n        instance: 0\n        invalid advice PBN count: 0\n        journal blocks batching: 0\n        journal blocks committed: 0\n        journal blocks started: 0\n        journal blocks writing: 0\n        journal blocks written: 0\n        journal commits requested count: 0\n        journal disk full count: 0\n        journal entries batching: 0\n        journal entries committed: 0\n        journal entries started: 0\n        journal entries writing: 0\n        journal entries written: 0\n        logical blocks: 1046277\n        logical blocks used: 0\n        maximum VDO IO requests in progress: 9\n        maximum dedupe queries: 0\n        no space error count: 0\n        operating mode: normal\n        overhead blocks used: 787140\n        physical blocks: 1835008\n        posts found: 0\n        posts not found: 0\n        queries found: 0\n        queries not found: 0\n        read cache accesses: 0\n        read cache data hits: 0\n        read cache hits: 0\n        read only error count: 0\n        read-only recovery count: 0\n        recovery progress (%): N/A\n        reference blocks written: 0\n        release version: 131337\n        saving percent: N/A\n        slab count: 2\n        slab journal blocked count: 0\n        slab journal blocks written: 0\n        slab journal disk full count: 0\n        slab journal flush count: 0\n        slab journal tail busy count: 0\n        slab summary blocks written: 0\n        slabs opened: 0\n        slabs reopened: 0\n        updates found: 0\n        updates not found: 0\n        used percent: 42\n        version: 26\n        write amplification ratio: 0.0\n        write policy: sync\n  vdo2:\n    Acknowledgement threads: 1\n    Activate: enabled\n    Bio rotation interval: 64\n    Bio submission threads: 4\n    Block map cache size: 128M\n    Block map period: 16380\n    Block size: 4096\n    CPU-work threads: 2\n    Compression: enabled\n    Configured write policy: auto\n    Deduplication: enabled\n    Device mapper status: 0 4183912 vdo /dev/sda5 albserver online cpu=2,bio=4,ack=1,bioRotationInterval=64\n    Emulate 512 byte: disabled\n    Hash zone threads: 1\n    Index checkpoint frequency: 0\n    Index memory setting: 0.25\n    Index parallel factor: 0\n    Index sparse: disabled\n    Index status: online\n    Logical size: 2091956K\n    Logical threads: 1\n    Physical size: 5G\n    Physical threads: 1\n    Read cache: disabled\n    Read cache size: 0M\n    Slab size: 2G\n    Storage device: /dev/sda5\n    VDO statistics:\n      /dev/mapper/vdo2:\n        1K-blocks: 5242880\n        1K-blocks available: 2095736\n        1K-blocks used: 3147144\n        512 byte emulation: false\n        KVDO module bios used: 74572\n        KVDO module bytes used: 851421880\n        KVDO module peak bio count: 74860\n        KVDO module peak bytes used: 851423752\n        bios acknowledged discard: 0\n        bios acknowledged flush: 0\n        bios acknowledged fua: 0\n        bios acknowledged partial discard: 0\n        bios acknowledged partial flush: 0\n        bios acknowledged partial fua: 0\n        bios acknowledged partial read: 0\n        bios acknowledged partial write: 0\n        bios acknowledged read: 265\n        bios acknowledged write: 0\n        bios in discard: 0\n        bios in flush: 0\n        bios in fua: 0\n        bios in partial discard: 0\n        bios in partial flush: 0\n        bios in partial fua: 0\n        bios in partial read: 0\n        bios in partial write: 0\n        bios in progress discard: 0\n        bios in progress flush: 0\n        bios in progress fua: 0\n        bios in progress read: 0\n        bios in progress write: 0\n        bios in read: 265\n        bios in write: 0\n        bios journal completed discard: 0\n        bios journal completed flush: 0\n        bios journal completed fua: 0\n        bios journal completed read: 0\n        bios journal completed write: 0\n        bios journal discard: 0\n        bios journal flush: 0\n        bios journal fua: 0\n        bios journal read: 0\n        bios journal write: 0\n        bios meta completed discard: 0\n        bios meta completed flush: 0\n        bios meta completed fua: 0\n        bios meta completed read: 4\n        bios meta completed write: 65\n        bios meta discard: 0\n        bios meta flush: 1\n        bios meta fua: 1\n        bios meta read: 4\n        bios meta write: 65\n        bios out completed discard: 0\n        bios out completed flush: 0\n        bios out completed fua: 0\n        bios out completed read: 0\n        bios out completed write: 0\n        bios out discard: 0\n        bios out flush: 0\n        bios out fua: 0\n        bios out read: 0\n        bios out write: 0\n        bios page cache completed discard: 0\n        bios page cache completed flush: 0\n        bios page cache completed fua: 0\n        bios page cache completed read: 0\n        bios page cache completed write: 0\n        bios page cache discard: 0\n        bios page cache flush: 0\n        bios page cache fua: 0\n        bios page cache read: 0\n        bios page cache write: 0\n        block map cache pressure: 0\n        block map cache size: 134217728\n        block map clean pages: 0\n        block map dirty pages: 0\n        block map discard required: 0\n        block map failed pages: 0\n        block map failed reads: 0\n        block map failed writes: 0\n        block map fetch required: 0\n        block map flush count: 0\n        block map found in cache: 0\n        block map free pages: 32768\n        block map incoming pages: 0\n        block map outgoing pages: 0\n        block map pages loaded: 0\n        block map pages saved: 0\n        block map read count: 0\n        block map read outgoing: 0\n        block map reclaimed: 0\n        block map wait for page: 0\n        block map write count: 0\n        block size: 4096\n        completed recovery count: 0\n        compressed blocks written: 0\n        compressed fragments in packer: 0\n        compressed fragments written: 0\n        current VDO IO requests in progress: 0\n        current dedupe queries: 0\n        data blocks used: 1\n        dedupe advice stale: 0\n        dedupe advice timeouts: 0\n        dedupe advice valid: 0\n        entries indexed: 0\n        flush out: 0\n        instance: 1\n        invalid advice PBN count: 0\n        journal blocks batching: 0\n        journal blocks committed: 0\n        journal blocks started: 0\n        journal blocks writing: 0\n        journal blocks written: 0\n        journal commits requested count: 0\n        journal disk full count: 0\n        journal entries batching: 0\n        journal entries committed: 0\n        journal entries started: 0\n        journal entries writing: 0\n        journal entries written: 0\n        logical blocks: 522989\n        logical blocks used: 3\n        maximum VDO IO requests in progress: 7\n        maximum dedupe queries: 0\n        no space error count: 0\n        operating mode: normal\n        overhead blocks used: 786786\n        physical blocks: 1310720\n        posts found: 0\n        posts not found: 0\n        queries found: 0\n        queries not found: 0\n        read cache accesses: 0\n        read cache data hits: 0\n        read cache hits: 0\n        read only error count: 0\n        read-only recovery count: 0\n        recovery progress (%): N/A\n        reference blocks written: 0\n        release version: 131337\n        saving percent: N/A\n        slab count: 1\n        slab journal blocked count: 0\n        slab journal blocks written: 0\n        slab journal disk full count: 0\n        slab journal flush count: 0\n        slab journal tail busy count: 0\n        slab summary blocks written: 0\n        slabs opened: 0\n        slabs reopened: 0\n        updates found: 0\n        updates not found: 0\n        used percent: 60\n        version: 26\n        write amplification ratio: 0.0\n        write policy: sync\n").strip()

def test_vdo_status2():
    vdo = VDOStatus(context_wrap(INPUT_STATUS_2))
    assert vdo.data['VDOs']['vdoapp1']['VDO statistics'] == 'not available'


def test_vdo_status_exp2_0():
    """
    Here test the examples cause expections
    """
    with pytest.raises(ParseException) as (sc1):
        vdo = VDOStatus(context_wrap(INPUT_STATUS_2))
        vdo.get_physical_blocks_of_vol('vdoapp1')
    assert 'Not available device mapper path in' in str(sc1)


def test_vdo_status_exp2_1():
    """
    Here test the examples cause expections
    """
    with pytest.raises(KeyError) as (sc1):
        vdo = VDOStatus(context_wrap(INPUT_STATUS_2))
        vdo.get_physical_blocks_of_vol('vdoapp999')
    assert 'No key(s) named:' in str(sc1)


def test_vdo_status_simple():
    vdo = VDOStatus(context_wrap(INPUT_STATUS_SIMPLE))
    assert vdo.data['VDO status'] == {'Date': '2019-07-27 04:40:40-04:00', 'Node': 'rdma-qe-04.lab.bos.redhat.com'}
    assert vdo.data['VDOs']['vdo1']['Activate'] == 'enabled'
    assert vdo.data['VDO status']['Date'] == '2019-07-27 04:40:40-04:00'
    assert vdo.data['VDO status']['Node'] == 'rdma-qe-04.lab.bos.redhat.com'
    assert vdo.get_slab_size_of_vol('vdo1') == '2G'
    assert vdo.volumns == ['vdo1', 'vdo2']
    assert vdo.get_physical_blocks_of_vol('vdo1') == 1572864
    assert vdo.get_overhead_used_of_vol('vdo1') == 728175
    assert vdo.get_physical_used_of_vol('vdo1') == 161863
    assert vdo.get_physical_free_of_vol('vdo1') == 682826
    assert vdo.get_logical_blocks_of_vol('vdo1') == 844568
    assert vdo.get_logical_used_of_vol('vdo1') == 844502
    assert vdo.get_logical_free_of_vol('vdo1') == 66


def test_vdo_status_empty():
    vdo = VDOStatus(context_wrap(INPUT_EMPTY))
    assert vdo.data['VDOs'] == {}
    assert vdo.data['Configuration']['File'] == 'does not exist'
    assert vdo.data['Configuration']['Last modified'] == 'not available'


def test_vdo_status_full():
    vdo = VDOStatus(context_wrap(INPUT_STATUS_FULL))
    assert vdo.data['VDO status']['Date'] == '2019-07-24 20:48:16-04:00'
    assert vdo.data['VDO status']['Node'] == 'dell-m620-10.rhts.gsslab.pek2.redhat.com'
    assert vdo.data['Kernel module']['Name'] == 'kvdo'
    assert vdo.data['Kernel module']['Version information']['kvdo version'] == '6.1.0.153'
    assert vdo.data['Configuration']['File'] == '/etc/vdoconf.yml'
    assert vdo.data['Configuration']['Last modified'] == '2019-07-24 20:47:59'
    assert vdo.data['VDOs']['vdo1']['Acknowledgement threads'] == 1
    assert vdo.data['VDOs']['vdo1']['Device mapper status'] == '0 8370216 vdo /dev/sda3 albserver online cpu=2,bio=4,ack=1,bioRotationInterval=64'
    assert vdo.data['VDOs']['vdo1']['VDO statistics']['/dev/mapper/vdo1']['KVDO module bios used'] == 74572
    assert vdo.get_slab_size_of_vol('vdo1') == '2G'
    assert vdo.volumns == ['vdo1', 'vdo2']
    assert vdo.get_physical_blocks_of_vol('vdo1') == 1835008
    assert vdo.get_overhead_used_of_vol('vdo1') == 787140
    assert vdo.get_physical_used_of_vol('vdo1') == 0
    assert vdo.get_logical_blocks_of_vol('vdo1') == 1046277
    assert vdo.get_logical_used_of_vol('vdo1') == 0
    assert vdo.get_logical_free_of_vol('vdo1') == 1046277
    assert vdo.get_physical_free_of_vol('vdo1') == 1047868
    assert vdo.get_logical_used_of_vol('vdo2') == 3
    assert vdo.get_physical_used_of_vol('vdo2') == 1


def test_vdo_status_documentation():
    """
    Here we test the examples in the documentation automatically using
    doctest.  We set up an environment which is similar to what a rule
    writer might see - a '/usr/bin/vdo status' command output that has
    been passed in as a parameter to the rule declaration.
    """
    env = {'vdo': VDOStatus(context_wrap(INPUT_STATUS_FULL))}
    failed, total = doctest.testmod(vdo_status, globs=env)
    assert failed == 0


def test_vdo_status_exp():
    """
    Here test the examples cause expections
    """
    with pytest.raises(ParseException) as (sc1):
        VDOStatus(context_wrap(INPUT_EXP))
    assert "couldn't parse yaml" in str(sc1)


def test_vdo_status_exp3():
    """
    Here test the examples cause expections
    """
    with pytest.raises(KeyError) as (sc1):
        vdo = VDOStatus(context_wrap(INPUT_STATUS_SIMPLE))
        vdo.get_physical_blocks_of_vol('vdo3')
    assert 'No key(s) named' in str(sc1)