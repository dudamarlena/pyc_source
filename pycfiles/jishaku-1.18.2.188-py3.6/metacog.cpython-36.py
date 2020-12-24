# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jishaku/metacog.py
# Compiled at: 2020-03-05 23:53:06
# Size of source mod 2**32: 1125 bytes
"""
jishaku.metacog
~~~~~~~~~~~~~~~

The metaclass definitions for the Jishaku cog.

:copyright: (c) 2020 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""
from discord.ext import commands

class GroupCogMeta(commands.CogMeta):
    __doc__ = '\n    A CogMeta metaclass that sets all unparented (non-nested) Commands under it as children\n    of a global Group.\n\n    This allows Jishaku to place all of its commands under a group, while maintaining the ability\n    to override individual subcommands in subclasses.\n\n    The Group will be inserted as an attribute of the resulting Cog under its function name.\n    '

    def __new__(cls, *args, **kwargs):
        group = kwargs.pop('command_parent')
        new_cls = (super().__new__)(cls, *args, **kwargs)
        for subcommand in new_cls.__cog_commands__:
            if subcommand.parent is None:
                subcommand.parent = group
                subcommand.__original_kwargs__['parent'] = group

        new_cls.__cog_commands__.append(group)
        setattr(new_cls, group.callback.__name__, group)
        return new_cls