# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/rpm_vercmp.py
# Compiled at: 2019-05-16 13:41:33
"""
Nearly direct translation of rpm comparison code in the rpm project at
https://github.com/rpm-software-management/rpm/blob/master/lib/rpmvercmp.c

Handles all of the cases in the rpm test file, including the "buggy" tests
and non-ascii characters.

https://raw.githubusercontent.com/rpm-software-management/rpm/master/tests/rpmvercmp.at
"""
from collections import deque
from itertools import takewhile

def _rpm_vercmp(a, b):
    if a == b:
        return 0
    a = deque([ c if ord(c) < 128 else '.' for c in a ])
    a.append('')
    b = deque([ c if ord(c) < 128 else '.' for c in b ])
    b.append('')
    while a[0] or b[0]:
        for x in [a, b]:
            while x[0] and not x[0].isalnum() and x[0] not in '~^':
                x.popleft()

        if a[0] == '~' or b[0] == '~':
            if a[0] != '~':
                return 1
            if b[0] != '~':
                return -1
            a.popleft()
            b.popleft()
            continue
        if a[0] == '^' or b[0] == '^':
            if not a[0]:
                return -1
            if not b[0]:
                return 1
            if a[0] != '^':
                return 1
            if b[0] != '^':
                return -1
            a.popleft()
            b.popleft()
            continue
        if not a[0] or not b[0]:
            break
        if a[0].isdigit():
            l = deque(takewhile(lambda v: v.isdigit(), a))
            r = deque(takewhile(lambda v: v.isdigit(), b))
            isnum = True
        else:
            l = deque(takewhile(lambda v: v.isalpha(), a))
            r = deque(takewhile(lambda v: v.isalpha(), b))
            isnum = False
        if not l:
            return -1
        if not r:
            if isnum:
                return 1
            return -1
        ll = len(l)
        lr = len(r)
        if isnum:
            for x in [l, r]:
                while x and x[0] == '0':
                    x.popleft()

            lenl = len(l)
            lenr = len(r)
            if lenl > lenr:
                return 1
            if lenr > lenl:
                return -1
        if l > r:
            return 1
        if l < r:
            return -1
        for _ in range(ll):
            a.popleft()

        for _ in range(lr):
            b.popleft()

    if not a[0] and not b[0]:
        return 0
    if not a[0]:
        return -1
    return 1


def rpm_version_compare(left, right):
    if left is right:
        return 0
    le, re = int(left.epoch), int(right.epoch)
    if le < re:
        return -1
    if le > re:
        return 1
    rc = _rpm_vercmp(left.version, right.version)
    if rc != 0:
        return rc
    return _rpm_vercmp(left.release, right.release)