# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/shared/vnc_constants.py
# Compiled at: 2016-11-12 07:38:04
"""
    This file defines the constants used in the RFB Protocol, which is
    used by VNC.
"""
RFB_VERSION = 'RFB 003.007\n'
SUPPORTED_AUTH_METHODS = '\x01\x02'
VNC_AUTH = '\x02'
NO_AUTH = '\x01'
AUTH_FAILED = '\x00\x00\x00\x01'
AUTH_SUCCESSFUL = '\x00\x00\x00\x00'