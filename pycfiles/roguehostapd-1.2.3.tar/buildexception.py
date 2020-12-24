# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/toupload/roguehostapd/roguehostapd/buildutil/buildexception.py
# Compiled at: 2018-02-24 04:48:29
"""
Module defines the custom exceptions for building hostapd
"""

class SharedLibMissError(Exception):
    """
    Define the Netlink shared library missing exception
    """

    def __init__(self, libname, packages):
        """
        Initialize the NetlinkMissError object
        param self: A SharedLibMissError object
        param libname: Required library name
        param packages: The packages required by the lib
        type self: SharedLibMissError
        type libname: str
        type packages: list
        return: None
        rtype: None
        """
        super(SharedLibMissError, self).__init__(libname, packages)
        self.libname = libname
        self.packages = packages