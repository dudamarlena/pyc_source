# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jishaku/models.py
# Compiled at: 2020-03-05 23:53:06
# Size of source mod 2**32: 875 bytes
"""
jishaku.models
~~~~~~~~~~~~~~

Functions for modifying or interfacing with discord.py models.

:copyright: (c) 2020 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""
import copy, discord
from discord.ext import commands

async def copy_context_with(ctx: commands.Context, *, author=None, channel=None, **kwargs):
    """
    Makes a new :class:`Context` with changed message properties.
    """
    alt_message = copy.copy(ctx.message)
    alt_message._update(kwargs)
    if author is not None:
        alt_message.author = author
    if channel is not None:
        alt_message.channel = channel
    return await ctx.bot.get_context(alt_message, cls=(type(ctx)))