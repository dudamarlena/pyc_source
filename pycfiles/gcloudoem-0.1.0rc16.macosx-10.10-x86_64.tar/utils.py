# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rstuart/.pyenv/versions/gcloudoem/lib/python2.7/site-packages/gcloudoem/utils.py
# Compiled at: 2015-04-20 22:18:08
import re
VERSION_PICKLE_KEY = '_gcloudoem_version'
re_camel_case = re.compile('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))')

def camel_case_to_spaces(value):
    """Splits CamelCase and converts to lower case. Also strips leading and trailing whitespace."""
    return re_camel_case.sub(' \\1', value).strip().lower()