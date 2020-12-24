# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Support/OscarUtil2.py
# Compiled at: 2008-10-19 12:19:52
"""
=======================
OSCAR Utility functions
=======================
This file includes functions for dealing with OSCAR datatypes and passwords.

This is the second of two utility modules. OscarUtil is the other. Most of
the AIM components require both OscarUtil and OscarUtil2. All the code in this
module was originally written for Twisted or is derived from Twisted code. 

Original Maintainer: U{Paul Swartz<mailto:z3p@twistedmatrix.com>} for Twisted

Modified 12 Jul 2007 by Jinna Lei for Kamaelia.
"""
from __future__ import nested_scopes
import struct, md5
from Kamaelia.Support.OscarUtil import *

def SNAC(fam, sub, data, id=1, flags=[0, 0]):
    """construct a SNAC from the given data"""
    return Double(fam) + Double(sub) + Single(flags[0]) + Single(flags[1]) + Quad(id) + data


def readSNAC(data):
    """puts a SNAC off the wire into a slightly more useable form"""
    header = '!HHBBL'
    try:
        head = [
         list(struct.unpack(header, data[:10]))]
        return head + [data[10:]]
    except struct.error:
        return (
         error, data)


def TLV(type, value):
    """constructs a TLV based on given data"""
    header = '!HH'
    head = struct.pack(header, type, len(value))
    return head + str(value)


def readTLVs(data, count=None):
    """
    takes a string of TLVs and returns a dictionary {TLV type: TLV value}
    Optional keywords:
    - count -- how many TLVs we want to unpack at a time. If count is less than
               the number of TLVs in our string, then we return the dictionary
               plus the remaining TLV string. 
    """
    header = '!HH'
    dict = {}
    while data and len(dict) != count:
        head = struct.unpack(header, data[:4])
        dict[head[0]] = data[4:4 + head[1]]
        data = data[4 + head[1]:]

    if not count:
        return dict
    return (
     dict, data)


def encryptPasswordMD5(password, key):
    """returns a password hash"""
    m = md5.new()
    m.update(key)
    m.update(md5.new(password).digest())
    m.update('AOL Instant Messenger (SM)')
    return m.digest()


def encryptPasswordICQ(password):
    """
    encrypts passwords the old way, relatively insecure way. Not used very often.
    """
    key = [
     243, 38, 129, 196, 57, 134, 219, 146, 113, 163, 185, 230, 83, 122, 149, 124]
    bytes = map(ord, password)
    r = ''
    for i in range(len(bytes)):
        r = r + chr(bytes[i] ^ key[(i % len(key))])

    return r