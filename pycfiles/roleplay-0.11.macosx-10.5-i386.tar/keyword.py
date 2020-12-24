# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.5/site-packages/roleplay/keyword.py
# Compiled at: 2008-01-14 08:27:42
"""
    roleplay.keyword:

        Apply and test for roles.

    author: Ask Solem <askh@opera.com>
    Copyright (c) Ask Solem. Released under the Modified BSD-license, see the
    LICENSE file for a full copy of the license.
"""
__version__ = '0.11'
__author__ = 'Ask Solem <askh@opera.com'
__authority__ = 'pypi:ASK'
from roleplay.meta import MetaRole
from roleplay.role import Role
DEBUG = 0
DOES_FRAME_STEP_MAX = 2

class DoesOutsideClass(Exception):
    """ does() must be used in a class definiton """
    pass


def has_role(instance, role, **kwargs):
    """
        Applies the role %{role} to your class.

        %{instance} can be either instance or class.
        %{role} must be class, not object instance.

        Example:

        has_role(self, RoleClass)

    """
    role(instance, **kwargs).__buildrole__()


def does(instance, role):
    """
        Returns True if %{instance} supports the role %(role).

        %(class) can be instance, class or string.
        %(role) can be instance, class or string.

        Example:

        has_comment_support = does(self, 'Comments')
    """
    meta = MetaRole()
    return meta.__does__(instance, role)