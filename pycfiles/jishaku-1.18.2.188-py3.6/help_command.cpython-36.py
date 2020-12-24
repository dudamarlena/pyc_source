# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jishaku/help_command.py
# Compiled at: 2020-03-05 23:53:06
# Size of source mod 2**32: 2306 bytes
"""
jishaku.help_command
~~~~~~~~~~~~~~~~~~~~

HelpCommand subclasses with jishaku features

:copyright: (c) 2020 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""
from discord.ext import commands
from jishaku.paginators import PaginatorEmbedInterface, PaginatorInterface

class DefaultPaginatorHelp(commands.DefaultHelpCommand):
    __doc__ = '\n    A subclass of :class:`commands.DefaultHelpCommand` that uses a PaginatorInterface for pages.\n    '

    def __init__(self, **options):
        paginator = options.pop('paginator', commands.Paginator(max_size=1985))
        (super().__init__)(paginator=paginator, **options)

    async def send_pages(self):
        destination = self.get_destination()
        interface = PaginatorInterface((self.context.bot), (self.paginator), owner=(self.context.author))
        await interface.send_to(destination)


class DefaultEmbedPaginatorHelp(commands.DefaultHelpCommand):
    __doc__ = '\n    A subclass of :class:`commands.DefaultHelpCommand` that uses a PaginatorEmbedInterface for pages.\n    '

    async def send_pages(self):
        destination = self.get_destination()
        interface = PaginatorEmbedInterface((self.context.bot), (self.paginator), owner=(self.context.author))
        await interface.send_to(destination)


class MinimalPaginatorHelp(commands.MinimalHelpCommand):
    __doc__ = '\n    A subclass of :class:`commands.MinimalHelpCommand` that uses a PaginatorInterface for pages.\n    '

    def __init__(self, **options):
        paginator = options.pop('paginator', commands.Paginator(prefix=None, suffix=None, max_size=1985))
        (super().__init__)(paginator=paginator, **options)

    async def send_pages(self):
        destination = self.get_destination()
        interface = PaginatorInterface((self.context.bot), (self.paginator), owner=(self.context.author))
        await interface.send_to(destination)


class MinimalEmbedPaginatorHelp(commands.MinimalHelpCommand):
    __doc__ = '\n    A subclass of :class:`commands.MinimalHelpCommand` that uses a PaginatorEmbedInterface for pages.\n    '

    async def send_pages(self):
        destination = self.get_destination()
        interface = PaginatorEmbedInterface((self.context.bot), (self.paginator), owner=(self.context.author))
        await interface.send_to(destination)