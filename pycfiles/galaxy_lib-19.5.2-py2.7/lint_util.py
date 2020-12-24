# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/tools/lint_util.py
# Compiled at: 2018-04-20 03:19:42


def is_datasource(tool_xml):
    """Returns true if the tool is a datasource tool"""
    return tool_xml.getroot().attrib.get('tool_type', '') == 'data_source'