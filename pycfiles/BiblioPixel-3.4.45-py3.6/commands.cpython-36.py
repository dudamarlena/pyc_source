# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/main/commands.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1039 bytes
import importlib, os, pathlib
from ..project.importer import import_module
from .. import commands
from ..util import log
BP_HEADER = '\nAPPENDIX: ``bp <command> --help`` for each command\n==================================================\n'
BP_TEMPLATE = '``bp {command}``\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n{doc}\n\n{description}\n'
SEPARATOR = '\n------------------------------------\n\n'

def print_help():
    template_file = pathlib.Path(__file__).parent / 'commands.rst.tmpl'
    help_text = template_file.open().read().format(command_count=(len(commands.COMMANDS)),
      commands=(commands.COMMANDS_PRINTABLE))
    log.printer(help_text)
    log.printer(BP_HEADER)
    for command in commands.COMMANDS:
        module = importlib.import_module('bibliopixel.commands.' + command)
        log.printer(BP_TEMPLATE.format(command=command,
          doc=(module.__doc__.strip()),
          description=(getattr(module, 'DESCRIPTION', ''))))


if __name__ == '__main__':
    print_help()