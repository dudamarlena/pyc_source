# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_parted.py
# Compiled at: 2019-05-16 13:41:33
"""
``test parted``
===============
"""
import pytest
from insights.parsers import ParseException
from insights.parsers.parted import PartedL
from insights.tests import context_wrap
PARTED_DATA = ('\nModel: Virtio Block Device (virtblk)\nDisk /dev/vda: 9664MB\nSector size (logical/physical): 512B/512B\nPartition Table: msdos\nDisk Flags:\n\nNumber  Start   End     Size    Type     File system  Flags\n 1      1049kB  525MB   524MB   primary  xfs          boot\n 2      525MB   9664MB  9138MB  primary               lvm\n').strip()
PARTED_DATA_NO_SECTOR_SPLIT = '\nModel: Virtio Block Device (virtblk)\nDisk /dev/vda: 9664MB\nSector size (logical/physical): 512B\nPartition Table: msdos\nDisk Flags:\n\nNumber  Start   End     Size    Type     File system  Flags\n 1      1049kB  525MB   524MB   primary  xfs          boot\n 2      525MB   9664MB  9138MB  primary               lvm\n'
PARTED_DATA_2 = ('\nModel: IBM 2107900 (scsi)\nDisk /dev/sdet: 2147MB\nSector size (logical/physical): 512B/512B\nPartition Table: msdos\n\nNumber  Start   End     Size    Type     File system  Flags\n 1      32.3kB  2580kB  2548kB  primary\n').strip()
PARTED_DATA_3 = ('\nModel: DELL PERC H710 (scsi)\nDisk /dev/sda: 292GB\nSector size (logical/physical): 512B/512B\nPartition Table: msdos\n\nNumber  Start   End     Size    Type      File system  Flags\n 1      32.3kB  526MB   526MB   primary   ext3         boot\n 2      526MB   9114MB  8587MB  primary   linux-swap\n 3      9114MB  12.3GB  3224MB  primary   ext3\n 4      12.3GB  292GB   280GB   extended\n 5      12.3GB  254GB   241GB   logical   ext3\n 6      254GB   281GB   26.8GB  logical   ext3\n 7      281GB   285GB   4294MB  logical   ext3\n 8      285GB   288GB   3224MB  logical   ext3\n 9      288GB   290GB   2147MB  logical   ext3\n10      290GB   292GB   2147MB  logical   ext3\n').strip()

def test_parted():
    context = context_wrap(PARTED_DATA)
    results = PartedL(context)
    assert results is not None
    assert results.get('model') == 'Virtio Block Device (virtblk)'
    assert results.disk == '/dev/vda'
    assert results.get('size') == '9664MB'
    assert results.get('sector_size') == '512B/512B'
    assert results.logical_sector_size == '512B'
    assert results.physical_sector_size == '512B'
    assert results.get('partition_table') == 'msdos'
    assert results.get('disk_flags') is None
    partitions = results.partitions
    assert len(partitions) == 2
    assert partitions[0].number == '1'
    assert partitions[0].start == '1049kB'
    assert partitions[0].end == '525MB'
    assert partitions[0].size == '524MB'
    assert partitions[0].file_system == 'xfs'
    assert partitions[0].get('name') is None
    assert partitions[0].type == 'primary'
    assert partitions[0].flags == 'boot'
    assert results.boot_partition is not None
    assert results.boot_partition.number == '1'
    assert partitions[1].get('file_system') == ''
    assert partitions[1].get('flags') == 'lvm'
    assert partitions[1].get('name') is None
    assert partitions[1].get('number') == '2'
    assert partitions[1].get('start') == '525MB'
    assert partitions[1].get('end') == '9664MB'
    assert partitions[1].get('size') == '9138MB'
    assert partitions[1].get('type') == 'primary'
    context = context_wrap(PARTED_DATA_2)
    results = PartedL(context)
    assert results is not None
    assert results.disk == '/dev/sdet'
    assert len(results.partitions) == 1
    context = context_wrap(PARTED_DATA_3)
    results = PartedL(context)
    assert results is not None
    assert results.disk == '/dev/sda'
    assert results.logical_sector_size == '512B'
    assert results.physical_sector_size == '512B'
    assert len(results.partitions) == 10
    return


PARTED_ERR_DATA = '\nError: /dev/dm-1: unrecognised disk label\n'
PARTED_ERR_DATA_2 = ('\nModel: IBM 2107900 (scsi)\nSector size (logical/physical): 512B/512B\nPartition Table: msdos\n\nNumber  Start   End     Size    Type     File system  Flags\n 1      32.3kB  2580kB  2548kB  primary\n').strip()
PARTED_ERR_DATA_NO_PARTITIONS = '\nModel: Virtio Block Device (virtblk)\nDisk /dev/vda: 9664MB\nSector size (logical/physical): 512B/512B\nPartition Table: msdos\nDisk Flags:\n\n'
PARTED_ERR_DATA_EXCEPTIONS = '\nModel: Virtio Block Device (virtblk)\nDisk /dev/vda: 9664MB\nSector size (logical:physical): 512B:512B\nPartition Table: msdos\nDisk Flags:\n\nNumber  Start   End     Size    Type     File system  Flags\n'

def test_failure_modes():
    context = context_wrap(PARTED_ERR_DATA)
    with pytest.raises(ParseException):
        PartedL(context)
    context = context_wrap(PARTED_ERR_DATA_2)
    with pytest.raises(ParseException):
        PartedL(context)
    results = PartedL(context_wrap(PARTED_DATA_NO_SECTOR_SPLIT))
    assert results is not None
    assert results.disk == '/dev/vda'
    assert results._sector_size is None
    assert results.logical_sector_size is None
    assert results.physical_sector_size is None
    part = PartedL(context_wrap(PARTED_ERR_DATA_NO_PARTITIONS))
    assert part is not None
    assert part.disk == '/dev/vda'
    assert part.data['sector_size'] == '512B/512B'
    assert part.logical_sector_size == '512B'
    assert part.physical_sector_size == '512B'
    assert part.partitions == []
    part = PartedL(context_wrap(PARTED_ERR_DATA_EXCEPTIONS))
    assert part.disk == '/dev/vda'
    assert 'sector_size' not in part.data
    return