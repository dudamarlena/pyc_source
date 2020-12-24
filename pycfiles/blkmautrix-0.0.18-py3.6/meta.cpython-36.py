# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/bridge/commands/meta.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 2490 bytes
from typing import Dict, List
from mautrix.types import EventID
from .handler import HelpSection, HelpCacheKey, command_handler, CommandEvent, command_handlers, SECTION_GENERAL

@command_handler(help_section=SECTION_GENERAL, help_text='Cancel an ongoing action.')
async def cancel(evt: CommandEvent) -> EventID:
    if evt.sender.command_status:
        action = evt.sender.command_status['action']
        evt.sender.command_status = None
        return await evt.reply(f"{action} cancelled.")
    else:
        return await evt.reply('No ongoing command.')


@command_handler()
async def unknown_command(evt: CommandEvent) -> EventID:
    return await evt.reply('Unknown command. Try `$cmdprefix+sp help` for help.')


help_cache = {}
help_cache: Dict[(HelpCacheKey, str)]

async def _get_help_text(evt: CommandEvent) -> str:
    cache_key = await evt.get_help_key()
    if cache_key not in help_cache:
        help_sections = {}
        for handler in command_handlers.values():
            if handler.has_help and handler.has_permission(cache_key):
                help_sections.setdefault(handler.help_section, [])
                help_sections[handler.help_section].append(handler.help + '  ')

        help_sorted = sorted((help_sections.items()), key=(lambda item: item[0].order))
        helps = ['#### {}\n{}\n'.format(key.name, '\n'.join(value)) for key, value in help_sorted]
        help_cache[cache_key] = '\n'.join(helps)
    return help_cache[cache_key]


def _get_management_status(evt: CommandEvent) -> str:
    if evt.is_management:
        return 'This is a management room: prefixing commands with `$cmdprefix` is not required.'
    else:
        if evt.is_portal:
            return '**This is a portal room**: you must always prefix commands with `$cmdprefix`.\nManagement commands will not be bridged.'
        return '**This is not a management room**: you must prefix commands with `$cmdprefix`.'


@command_handler(name='help', help_section=SECTION_GENERAL,
  help_text='Show this help message.')
async def help_cmd(evt: CommandEvent) -> EventID:
    return await evt.reply(_get_management_status(evt) + '\n' + await _get_help_text(evt))