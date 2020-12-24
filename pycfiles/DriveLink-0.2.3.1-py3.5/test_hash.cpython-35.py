# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_hash.py
# Compiled at: 2017-09-17 22:49:36
# Size of source mod 2**32: 1427 bytes
from drivelink.hash import hash
from drivelink.hash import frozen_hash
from pytest import raises
from sys import version_info
test_items = {0: 0, 
 12: 12, 
 int(1e+16): 1e+16, 
 'a': 91634880152443617534842621287039938041581081254914058002978601050179556493499, 
 '123': 75263518707598184987916378021939673586055614731957507592904438851787542395619, 
 (0, 1, 2): 33822245971830441941584207765618803954591506626161146963614155313748171978276, 
 frozenset([0, 1, 2]): 72252079842091549505691736167086842307551715296043210784274131111424579773361, 
 1.7: 102609002710774119684446456160999458779848467669243989954385827560691142573442}
if version_info[0] == 3:
    test_items_hash = 80464813933747159092944765465151020510175839874325703127380790964538975558201
else:
    test_items_hash = 24470064747263512444326284945774938095155026949908835271795139482934800708844

def test_hash():
    for item, soln in test_items.items():
        print(hash(item))
        if not hash(item) == soln:
            raise AssertionError

    with raises(TypeError):
        assert hash(test_items) == test_items_hash


def test_frozen_hash():
    for item in test_items.keys():
        if not frozen_hash(item) == hash(item):
            raise AssertionError

    print(frozen_hash(test_items))
    assert frozen_hash(test_items) == test_items_hash