# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/duwei/PycharmProjects/kafkaka/kafkaka/util.py
# Compiled at: 2014-12-22 22:57:20
import binascii

def crc32(data):
    return binascii.crc32(data) & 4294967295