# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jishaku/modules.py
# Compiled at: 2020-03-05 23:53:06
# Size of source mod 2**32: 2490 bytes
"""
jishaku.modules
~~~~~~~~~~~~~~

Functions for managing and searching modules.

:copyright: (c) 2020 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""
import pathlib, typing, pkg_resources
from braceexpand import UnbalancedBracesError, braceexpand
from discord.ext import commands
__all__ = ('find_extensions_in', 'resolve_extensions', 'package_version', 'ExtensionConverter')

def find_extensions_in(path: typing.Union[(str, pathlib.Path)]) -> list:
    """
    Tries to find things that look like bot extensions in a directory.
    """
    if not isinstance(path, pathlib.Path):
        path = pathlib.Path(path)
    if not path.is_dir():
        return []
    else:
        extension_names = []
        for subpath in path.glob('*.py'):
            parts = subpath.with_suffix('').parts
            if parts[0] == '.':
                parts = parts[1:]
            extension_names.append('.'.join(parts))

        for subpath in path.glob('*/__init__.py'):
            parts = subpath.parent.parts
            if parts[0] == '.':
                parts = parts[1:]
            extension_names.append('.'.join(parts))

        return extension_names


def resolve_extensions(bot: commands.Bot, name: str) -> list:
    """
    Tries to resolve extension queries into a list of extension names.
    """
    exts = []
    for ext in braceexpand(name):
        if ext.endswith('.*'):
            module_parts = ext[:-2].split('.')
            path = (pathlib.Path)(*module_parts)
            exts.extend(find_extensions_in(path))
        else:
            if ext == '~':
                exts.extend(bot.extensions)
            else:
                exts.append(ext)

    return exts


def package_version(package_name: str) -> typing.Optional[str]:
    """
    Returns package version as a string, or None if it couldn't be found.
    """
    try:
        return pkg_resources.get_distribution(package_name).version
    except (pkg_resources.DistributionNotFound, AttributeError):
        return


class ExtensionConverter(commands.Converter):
    __doc__ = '\n    A converter interface for resolve_extensions to match extensions from users.\n    '

    async def convert(self, ctx: commands.Context, argument) -> list:
        try:
            return resolve_extensions(ctx.bot, argument)
        except UnbalancedBracesError as exc:
            raise commands.BadArgument(str(exc))