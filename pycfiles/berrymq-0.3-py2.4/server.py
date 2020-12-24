# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/berrymq/jsonrpc/server.py
# Compiled at: 2009-09-08 19:26:33
import sys
if sys.version_info[:2] == (2, 5) or sys.version_info[:2] == (2, 4):
    from server25 import SimpleJSONRPCServer
elif sys.version_info[:2] == (2, 6):
    from server26 import SimpleJSONRPCServer