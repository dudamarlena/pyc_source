# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Lib\Uuid.py
# Compiled at: 2004-08-05 16:57:32
__doc__ = "\nFunctions for generating and comparing Universal Unique Identifiers\n(UUIDs), based on ideas from e2fsprogs.\n\nA UUID is essentially a 128-bit random number that has a string\nrepresentation of 28 hexadecimal digits, hyphenated in groups of\n8-4-4-12. The value could be greater than the number of atoms in the\nuniverse; it's extremely unlikely that the same number would ever be\ngenerated twice.\n\nUUIDs are defined by ISO/IEC 11578:1996 (Remote Procedure Call)\nand The Open Group's DCE 1.1 (Distributed Computing Environment) spec\n(the ISO version was based on an earlier version of the DCE spec).\nSee http://www.opengroup.org/onlinepubs/009629399/apdxa.htm#tagcjh_20\nfor the current version, and also see the expired IETF Internet-Draft\nhttp://www.opengroup.org/dce/info/draft-leach-uuids-guids-01.txt for\na version with more informative prose and examples.\n\nCopyright 2004 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n"
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