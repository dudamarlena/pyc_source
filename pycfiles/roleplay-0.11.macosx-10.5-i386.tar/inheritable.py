# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.5/site-packages/roleplay/inheritable.py
# Compiled at: 2008-01-14 08:27:42
"""
    roleplay.inheritable:

        Base class with method versions of does() and has_role().

        You don't really have to inherit from this class, you can just as well
        import the function versions from the roleplay top-level module.

            from roleplay import does, has_role

        However, if you already have a common base class for all your objects, or you
        maintain a metaclass, this module could be the thing for you.

    author: Ask Solem <askh@opera.com>
    Copyright (c) Ask Solem. Released under the Modified BSD-license, see the
    LICENSE file for a full copy of the license.

"""
__version__ = '0.11'
__author__ = 'Ask Solem <askh@opera.com'
__authority__ = 'pypi:ASK'
import roleplay.keyword

class RoleObject(object):
    """
        Base class with method versions of does() and has_role().

        Example usage:

            from some.module import SomeRole

            class MyClass(RoleObject):
                
                def __init__(self):
                    self.has_role(SomeRole)

                def do_something(self):

                    # Test if we support the SomeRole role, if so we get    
                    # extra functonality.
                    if self.does('SomeRole'):
                        self.some_method_SomeRole_defines()

    """

    def has_role(self, role, **kwargs):
        """
            Method version of roleplay.has_role

            %{role} must be class, not object instance.

            Example:

                self.has_role(RoleClass)
        """
        roleplay.keyword.has_role(self, role, **kwargs)

    def does(self, role):
        """
            Method version of roleplay.does

            Returns True if this class supports the role.

            %(role) can be instance, class or string.

            Example:

                has_comment_support = self.does('Comments')
        """
        roleplay.keyword.does(self, role)