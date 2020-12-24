# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Support/OscarUtil.py
# Compiled at: 2008-10-19 12:19:52
"""
=======================
OSCAR Utility functions
=======================
This file includes functions for packing and unpacking binary data and defines
some constants useful for dealing with OSCAR.

This is the first of two utility modules. OscarUtil2 is the other. Most AIM
code requires both this module and OscarUtil2. 

Credit goes to Alexandr Shutko for errorCodes dictionary (and for writing an
excellent guide on the OSCAR protocol). You can find the original table at
`this page <http://iserverd.khstu.ru/oscar/auth_failed.html>`_.
"""
import struct

def Single(num):
    """convenience method for "struct.pack('!B', num')" """
    return struct.pack('!B', num)


def Double(num):
    """convenience method for "struct.pack('!H, num')" """
    return struct.pack('!H', num)


def Quad(num):
    """convenience method for "struct.pack('!Q', num')" """
    return struct.pack('!i', num)


def unpackDoubles(data):
    """convenience method for "struct.unpack('!%iH' % (len(data)/2), data)" """
    fmt = '!%iH' % (len(data) / 2)
    return struct.unpack(fmt, data)


def unpackSingles(data):
    """convenience method for "struct.unpack('!%iB' % len(data), data)" """
    return struct.unpack('!%iB' % len(data), data)


def printWireshark(text):
    """prints a string of binary data in Wireshark format."""
    data = unpackSingles(text)
    data = ('00 ' * 12 + '%02x ' * len(data)) % data
    while len(data) > 48:
        print data[:24], ' ', data[24:48]
        data = data[48:]

    print data[:24],
    if len(data) > 24:
        print ' ', data[24:]


class selfClass(object):
    """
    selfClass() -> selfClass object.

    Calling selfClass.sendSnac(fam, sub, binaryData) causes the corresponding
    SNAC to be printed in Wireshark format. Used to debug AIM component methods.
    """

    def sendSnac(self, fam, sub, text):
        """constructs the SNAC and prints resulting binary data like a Wireshark
        packet dump."""
        snac = SNAC(fam, sub, text)
        printWireshark(snac)


errorCodes = {1: 'Invalid nick or password', 2: 'Service temporarily unavailable', 
   3: 'All other errors', 
   4: 'Incorrect nick or password, re-enter', 
   5: 'Mismatch nick or password, re-enter', 
   6: 'Internal client error (bad input to authorizer)', 
   7: 'Invalid account', 
   8: 'Deleted account', 
   9: 'Expired account', 
   10: 'No access to database', 
   11: 'No access to resolver', 
   12: 'Invalid database fields', 
   13: 'Bad database status', 
   14: 'Bad resolver status', 
   15: 'Internal error', 
   16: 'Service temporarily offline', 
   17: 'Suspended account', 
   18: 'DB send error', 
   19: 'DB link error', 
   20: 'Reservation map error', 
   21: 'Reservation link error', 
   22: 'The users num connected from this IP has reached the maximum', 
   23: 'The users num connected from this IP has reached the maximum (reservation)', 
   24: 'Rate limit exceeded (reservation). Please try to reconnect in a few minutes', 
   25: 'User too heavily warned', 
   26: 'Reservation timeout', 
   27: 'You are using an older version of ICQ. Upgrade required', 
   28: 'You are using an older version of ICQ. Upgrade recommended', 
   29: 'Rate limit exceeded. Please try to reconnect in a few minutes', 
   30: "Can't register on the ICQ network. Reconnect in a few minutes", 
   32: 'Invalid SecurID', 
   34: 'Account suspended because of your age (age < 13)'}

def readTLV08(tlvdata):
    """returns tuple ("error", error message) when given TLV 0x08"""
    (code,) = struct.unpack('!H', tlvdata)
    return ('error', errorCodes[code])


RATE_ID_WIDTH = 2
RATE_WINSIZE_WIDTH = 4
RATE_CLEAR_WIDTH = 4
RATE_ALERT_WIDTH = 4
RATE_LIMIT_WIDTH = 4
RATE_DISCONNECT_WIDTH = 4
RATE_CURRENT_WIDTH = 4
RATE_MAX_WIDTH = 4
RATE_LASTTIME_WIDTH = 4
RATE_CURRENTSTATE_WIDTH = 1
STATUS_MISC_WEBAWARE = 1
STATUS_MISC_SHOWIP = 2
STATUS_MISC_BIRTHDAY = 8
STATUS_MISC_WEBFRONT = 32
STATUS_MISC_DCDISABLED = 256
STATUS_MISC_DCAUTH = 4096
STATUS_MISC_DCCONT = 8192
STATUS_ONLINE = 0
STATUS_AWAY = 1
STATUS_DND = 2
STATUS_NA = 4
STATUS_OCCUPIED = 16
STATUS_FREE4CHAT = 32
STATUS_INVISIBLE = 256
AUTH_SERVER = 'login.oscar.aol.com'
AIM_PORT = 5190
AIM_MD5_STRING = 'AOL Instant Messenger (SM)'
CLIENT_ID_STRING = 'Kamaelia/AIM'
CHANNEL_NEWCONNECTION = 1
CHANNEL_SNAC = 2
CHANNEL_FLAPERROR = 3
CHANNEL_CLOSECONNECTION = 4
CHANNEL_KEEPALIVE = 5
RATE_CLASS_LEN = 2 + 32 + 1
FLAP_HEADER_LEN = 6