# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/narani/Projects/django-zen-queries/zen_queries/__init__.py
# Compiled at: 2020-03-13 12:50:55
# Size of source mod 2**32: 301 bytes
from zen_queries.decorators import queries_disabled, queries_dangerously_enabled, QueriesDisabledError
import zen_queries.render as render
from zen_queries.template_response import TemplateResponse, SimpleTemplateResponse
from zen_queries.utils import fetch
__version__ = '1.1.0'