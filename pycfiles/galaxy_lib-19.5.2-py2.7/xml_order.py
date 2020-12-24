# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/tools/linters/xml_order.py
# Compiled at: 2018-04-20 03:19:42
"""This module contains a linting functions for tool XML block order.

For more information on the IUC standard for XML block order see -
https://github.com/galaxy-iuc/standards.
"""
TAG_ORDER = [
 'description',
 'macros',
 'parallelism',
 'requirements',
 'code',
 'stdio',
 'version_command',
 'command',
 'environment_variables',
 'configfiles',
 'inputs',
 'outputs',
 'tests',
 'help',
 'citations']
DATASOURCE_TAG_ORDER = [
 'description',
 'macros',
 'command',
 'configfiles',
 'inputs',
 'request_param_translation',
 'uihints',
 'outputs',
 'options',
 'help',
 'citations']

def lint_xml_order(tool_xml, lint_ctx):
    tool_root = tool_xml.getroot()
    if tool_root.attrib.get('tool_type', '') == 'data_source':
        _validate_for_tags(tool_root, lint_ctx, DATASOURCE_TAG_ORDER)
    else:
        _validate_for_tags(tool_root, lint_ctx, TAG_ORDER)


def _validate_for_tags(root, lint_ctx, tag_ordering):
    last_tag = None
    last_key = None
    for elem in root:
        tag = elem.tag
        if tag in tag_ordering:
            key = tag_ordering.index(tag)
            if last_key:
                if last_key > key:
                    lint_ctx.warn('Best practice violation [%s] elements should come before [%s]' % (tag, last_tag))
            last_tag = tag
            last_key = key
        else:
            lint_ctx.info('Unknown tag [%s] encountered, this may result in a warning in the future.' % tag)

    return