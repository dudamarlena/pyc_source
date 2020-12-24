# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/client/permissions.py
# Compiled at: 2010-02-09 00:00:15
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
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