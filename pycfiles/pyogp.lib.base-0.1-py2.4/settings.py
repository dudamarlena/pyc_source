# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/settings.py
# Compiled at: 2010-02-07 17:28:31
"""
Contributors can be viewed at:
http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt 

$LicenseInfo:firstyear=2008&license=apachev2$

Copyright 2009, Linden Research, Inc.

Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
    http://www.apache.org/licenses/LICENSE-2.0
or in 
    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt

$/LicenseInfo$
"""

class Settings(object):
    __module__ = __name__

    def __init__(self, quiet_logging=False, spammy_logging=False, log_tests=True):
        """ some lovely configurable settings 

        These are applied application wide, and can be
        overridden at any time in a specific instance
        
        quiet_logging overrides spammy_logging
        """
        self.quiet_logging = quiet_logging
        self.spammy_logging = spammy_logging
        self.HANDLE_PACKETS = True
        self.HANDLE_OUTGOING_PACKETS = False
        self.ENABLE_DEFERRED_PACKET_PARSING = True
        self.LOG_VERBOSE = True
        self.ENABLE_BYTES_TO_HEX_LOGGING = False
        self.ENABLE_CAPS_LOGGING = True
        self.ENABLE_CAPS_LLSD_LOGGING = False
        self.ENABLE_EQ_LOGGING = True
        self.ENABLE_UDP_LOGGING = True
        self.ENABLE_OBJECT_LOGGING = True
        self.LOG_SKIPPED_PACKETS = True
        self.ENABLE_HOST_LOGGING = True
        self.LOG_COROUTINE_SPAWNS = True
        self.PROXY_LOGGING = False
        self.DISABLE_SPAMMERS = True
        self.UDP_SPAMMERS = ['PacketAck', 'AgentUpdate']
        self.REGION_EVENT_QUEUE_POLL_INTERVAL = 1
        if self.spammy_logging:
            self.ENABLE_BYTES_TO_HEX_LOGGING = True
            self.ENABLE_CAPS_LLSD_LOGGING = True
            self.DISABLE_SPAMMERS = False
        if self.quiet_logging:
            self.LOG_VERBOSE = False
            self.ENABLE_BYTES_TO_HEX_LOGGING = False
            self.ENABLE_CAPS_LOGGING = False
            self.ENABLE_CAPS_LLSD_LOGGING = False
            self.ENABLE_EQ_LOGGING = False
            self.ENABLE_UDP_LOGGING = False
            self.LOG_SKIPPED_PACKETS = False
            self.ENABLE_OBJECT_LOGGING = False
            self.ENABLE_HOST_LOGGING = False
            self.LOG_COROUTINE_SPAWNS = False
            self.DISABLE_SPAMMERS = True
        if log_tests:
            self.ENABLE_LOGGING_IN_TESTS = True
        else:
            self.ENABLE_LOGGING_IN_TESTS = False