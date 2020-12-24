# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/tools/linters/stdio.py
# Compiled at: 2018-09-15 08:40:24
"""This module contains a linting functions for tool error detection."""
from .command import get_command

def lint_stdio(tool_source, lint_ctx):
    tool_xml = getattr(tool_source, 'xml_tree', None)
    stdios = tool_xml.findall('./stdio') if tool_xml else []
    if not stdios:
        command = get_command(tool_xml) if tool_xml else None
        if command is None or not command.get('detect_errors'):
            if tool_source.parse_profile() <= '16.01':
                lint_ctx.info('No stdio definition found, tool indicates error conditions with output written to stderr.')
            else:
                lint_ctx.info('No stdio definition found, tool indicates error conditions with non-zero exit codes.')
        return
    if len(stdios) > 1:
        lint_ctx.error('More than one stdio tag found, behavior undefined.')
        return
    else:
        stdio = stdios[0]
        for child in list(stdio):
            if child.tag == 'regex':
                _lint_regex(child, lint_ctx)
            elif child.tag == 'exit_code':
                _lint_exit_code(child, lint_ctx)
            else:
                message = 'Unknown stdio child tag discovered [%s]. '
                message += 'Valid options are exit_code and regex.'
                lint_ctx.warn(message % child.tag)

        return


def _lint_exit_code(child, lint_ctx):
    for key in child.attrib.keys():
        if key not in ('description', 'level', 'range'):
            lint_ctx.warn('Unknown attribute [%s] encountered on exit_code tag.' % key)


def _lint_regex(child, lint_ctx):
    for key in child.attrib.keys():
        if key not in ('description', 'level', 'match', 'source'):
            lint_ctx.warn('Unknown attribute [%s] encountered on regex tag.' % key)