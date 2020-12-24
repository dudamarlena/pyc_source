# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/work/lib/pyenv/versions/3.6.1/envs/maestro/lib/python3.6/site-packages/rest_framework/utils/constants.py
# Compiled at: 2018-10-12 04:41:52
# Size of source mod 2**32: 480 bytes
import re
QUERY_TERMS = {
 'exact', 'iexact', 'contains', 'icontains', 'gt', 'gte', 'lt', 'lte', 'in',
 'startswith', 'istartswith', 'endswith', 'iendswith', 'range', 'year',
 'month', 'day', 'week_day', 'hour', 'minute', 'second', 'isnull', 'search',
 'regex', 'iregex'}
EMPTY_VALUES = (
 None, '', [], (), {})
LOOKUP_SEP = '__'
ALL_FIELDS = '__all__'
FILE_INPUT_CONTRADICTION = object()
REGEX_TYPE = type(re.compile(''))
empty = object()