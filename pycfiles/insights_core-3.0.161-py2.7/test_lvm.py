# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_lvm.py
# Compiled at: 2019-05-16 13:41:33
from __future__ import print_function
from insights.parsers import lvm
WARNINGS_CONTENT = ('\nWARNING\nvalid data 1\nChecksum Error\nvalid data 2\n  Failed to write\n  Attempt To Close Device\nvalid data 3\n').strip()
WARNINGS_FOUND = ('\nWARNING\nChecksum Error\n  Failed to write\n  Attempt To Close Device\n').strip()

def test_find_warnings():
    data = [ l for l in lvm.find_warnings(WARNINGS_CONTENT.splitlines()) ]
    assert len(data) == len(WARNINGS_FOUND.splitlines())
    assert data == WARNINGS_FOUND.splitlines()


def compare_partial_dicts(result, expected):
    """
    Make sure all the keys in expected are matched by keys in result, and
    that the values stored in those keys match.  Result can contain more
    items than expected - those are ignored.

    Used in the test_lvs, test_pvs and test_vgs tests.
    """
    mismatches = 0
    for k in expected.keys():
        if not result[k] == expected[k]:
            print(('Failed for key {k}, {r} != {e}').format(k=k, r=result[k], e=expected[k]))
            mismatches += 1

    return mismatches == 0