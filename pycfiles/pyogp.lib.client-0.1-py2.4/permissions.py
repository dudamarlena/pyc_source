# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/client/permissions.py
# Compiled at: 2010-02-09 00:00:15
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
from logging import getLogger
logger = getLogger('pyogp.lib.client.permissions')

class PermissionsMask(object):
    """ permissions flags mappings """
    __module__ = __name__
    Transfer = 1 << 13
    Modify = 1 << 14
    Copy = 1 << 15
    Move = 1 << 19
    _None = 0
    All = 2147483647


class PermissionsTarget(object):
    """ who the permissions apply to """
    __module__ = __name__
    Base = 1
    Owner = 2
    Group = 4
    Everyone = 8
    NextOwner = 16


class Permissions(object):
    """ class representing the permissions of an object or inventory item """
    __module__ = __name__

    def __init__(self, BaseMask=None, OwnerMask=None, GroupMask=None, EveryoneMask=None, NextOwnerMask=None):
        """ store the values of the various targets permissions """
        self.BaseMask = BaseMask
        self.OwnerMask = OwnerMask
        self.GroupMask = GroupMask
        self.EveryoneMask = EveryoneMask
        self.NextOwnerMask = NextOwnerMask