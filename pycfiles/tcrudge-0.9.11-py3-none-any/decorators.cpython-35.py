# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/app/tcrudge/decorators.py
# Compiled at: 2016-12-08 09:48:39
# Size of source mod 2**32: 734 bytes
"""
Module containing decorators.
"""

def perm_roles(items):
    """
    Check roles from input list. Auth logic is up to user.
    """

    def wrap(f):

        async def func(self, *args, **kw):
            auth = await self.is_auth()
            if auth:
                roles = await self.get_roles()
                valid_permission = False
                for r in roles:
                    if r in items:
                        valid_permission = True
                        break

                if not valid_permission:
                    await self.bad_permissions()
                return await f(self, *args, **kw)
            await self.bad_permissions()

        return func

    return wrap