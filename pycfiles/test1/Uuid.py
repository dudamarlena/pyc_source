# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Lib\Uuid.py
# Compiled at: 2004-08-05 16:57:32
"""
Functions for generating and comparing Universal Unique Identifiers
(UUIDs), based on ideas from e2fsprogs.

A UUID is essentially a 128-bit random number that has a string
representation of 28 hexadecimal digits, hyphenated in groups of
8-4-4-12. The value could be greater than the number of atoms in the
universe; it's extremely unlikely that the same number would ever be
generated twice.

UUIDs are defined by ISO/IEC 11578:1996 (Remote Procedure Call)
and The Open Group's DCE 1.1 (Distributed Computing Environment) spec
(the ISO version was based on an earlier version of the DCE spec).
See http://www.opengroup.org/onlinepubs/009629399/apdxa.htm#tagcjh_20
for the current version, and also see the expired IETF Internet-Draft
http://www.opengroup.org/dce/info/draft-leach-uuids-guids-01.txt for
a version with more informative prose and examples.

Copyright 2004 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
import socket
from Random import GetRandomBytes

def GenerateUuid():
    """Returns a new UUID as a long int"""
    result = GetRandomBytes(16)
    result = result[:6] + chr(ord(result[6]) & 79 | 64) + result[7:8] + chr(ord(result[8]) & 191 | 128) + result[9:]
    res = 0
    for i in range(16):
        res = (res << 8) + ord(result[i])

    return res


def UuidAsString(uuid):
    """
    Formats a long int representing a UUID as a UUID string:
    32 hex digits in hyphenated groups of 8-4-4-4-12.
    """
    s = '%032x' % uuid
    return '%s-%s-%s-%s-%s' % (s[0:8], s[8:12], s[12:16], s[16:20], s[20:])


def CompareUuids(u1, u2):
    """Compares, as with cmp(), two UUID strings case-insensitively"""
    return cmp(u1.upper(), u2.upper())