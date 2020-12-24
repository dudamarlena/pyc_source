# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/tools/linters/command.py
# Compiled at: 2018-04-20 03:19:42
"""This module contains a linting function for a tool's command description.

A command description describes how to build the command-line to execute
from supplied inputs.
"""

def lint_command(tool_xml, lint_ctx):
    """Ensure tool contains exactly one command and check attributes."""
    root = tool_xml.getroot()
    commands = root.findall('command')
    if len(commands) > 1:
        lint_ctx.error('More than one command tag found, behavior undefined.')
        return
    else:
        if len(commands) == 0:
            lint_ctx.error('No command tag found, must specify a command template to execute.')
            return
        command = get_command(tool_xml)
        if 'TODO' in command:
            lint_ctx.warn('Command template contains TODO text.')
        command_attrib = command.attrib
        interpreter_type = None
        for key, value in command_attrib.items():
            if key == 'interpreter':
                interpreter_type = value
            elif key == 'detect_errors':
                detect_errors = value
                if detect_errors not in ('default', 'exit_code', 'aggressive'):
                    lint_ctx.warn('Unknown detect_errors attribute [%s]' % detect_errors)

        interpreter_info = ''
        if interpreter_type:
            interpreter_info = ' with interpreter of type [%s]' % interpreter_type
        if interpreter_type:
            lint_ctx.info("Command uses deprecated 'interpreter' attribute.")
        lint_ctx.info('Tool contains a command%s.' % interpreter_info)
        return


def get_command(tool_xml):
    """Get command XML element from supplied XML root."""
    root = tool_xml.getroot()
    commands = root.findall('command')
    command = None
    if len(commands) == 1:
        command = commands[0]
    return command