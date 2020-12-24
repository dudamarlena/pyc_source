# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/util/tool_version.py
# Compiled at: 2018-04-20 03:19:42


def remove_version_from_guid(guid):
    """
    Removes version from toolshed-derived tool_id(=guid).
    """
    if '/' not in guid:
        return None
    else:
        last_slash = guid.rfind('/')
        return guid[:last_slash]