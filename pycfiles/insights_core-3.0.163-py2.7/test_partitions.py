# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_partitions.py
# Compiled at: 2019-11-14 13:57:46
import doctest, pytest
from insights.parsers import SkipException
from insights.parsers import partitions
from insights.parsers.partitions import Partitions
from insights.tests import context_wrap
PARTITIONS_CONTENT = ('\nmajor minor  #blocks  name\n\n   8       16 1384120320 sdb\n   8        0    3701760 sda\n   8       32 2621440000 sdc\n\n 253        0 1384120320 dm-0\n   8       48 2726297600 sdd\n 253        1 2621440000 dm-1\n   8       64 1384120320 sde\n 253        2 2726297600 dm-2\n   8       96 2621440000 sdg\n   8       80   52428800 sdf\n   8      112 2726297600 sdh\n   8      128  209715200 sdi\n   8      144 1384120320 sdj\n 253        3   52428800 dm-3\n 253        4  209715200 dm-4\n   8      160 1384120320 sdk\n   8      176 2621440000 sdl\n   8      192 2621440000 sdm\n 253        5    1048576 dm-5\n 253        6   51379200 dm-6\n   8      224 2726297600 sdo\n   8      208 2726297600 sdn\n   8      240   52428800 sdp\n  65        0   52428800 sdq\n  65       16  209715200 sdr\n  65       32  209715200 sds\n  65       48   52428800 sdt\n  65       64  209715200 sdu\n 253        7   15728640 dm-7\n 253        8   16777216 dm-8\n 253        9   31457280 dm-9\n 253       10   10485760 dm-10\n 253       11    4194304 dm-11\n 253       12  104857600 dm-12\n 253       13    5242880 dm-13\n 253       14    6287360 dm-14\n 253       15    3145728 dm-15\n 253       16 2726281216 dm-16\n 253       17 1069531136 dm-17\n').strip()
INVALID_PARTITIONS_CONTENT = ('\nmajor minor  #blocks  name\n\n   8       16 1384120320\n   8        0    3701760 sda\n   8       32 2621440000 sdc\n').strip()
EMPTY_CONTENT = ('\n').strip()
SAMPLE_INPUT = ('\nmajor minor  #blocks  name\n\n   3     0   19531250 hda\n   3     1     104391 hda1\n   3     2   19422585 hda2\n 253     0   22708224 dm-0\n 253     1     524288 dm-1\n').strip()

def test_partitions():
    info = Partitions(context_wrap(PARTITIONS_CONTENT))
    assert 'dm-2' in info
    dm_2 = info['dm-2']
    assert dm_2.get('major') == '253'
    assert dm_2.get('minor') == '2'
    assert dm_2.get('blocks') == '2726297600'
    assert 'dm-18' not in info
    p_list = [ i for i in info ]
    assert p_list[2] in info
    assert len(p_list) == 39
    assert info['dm-17'] == {'major': '253', 'minor': '17', 'blocks': '1069531136', 'name': 'dm-17'}


def test_partitions_invalid_data():
    output = Partitions(context_wrap(INVALID_PARTITIONS_CONTENT))
    assert len(output) == 2
    assert 'sda' in output
    assert 'sdc' in output


def test_empty_content():
    with pytest.raises(SkipException) as (exc):
        Partitions(context_wrap(EMPTY_CONTENT))
    assert 'Empty content' in str(exc)


def test_partitions_doc_examples():
    env = {'partitions_info': Partitions(context_wrap(SAMPLE_INPUT))}
    failed, total = doctest.testmod(partitions, globs=env)
    assert failed == 0