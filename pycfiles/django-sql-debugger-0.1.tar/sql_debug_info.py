# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Catherine/Documents/webprojects/efira_repo/efira/sql_debugger/templatetags/sql_debug_info.py
# Compiled at: 2016-01-24 08:59:09
import json
from django import template
from django.db import connections, connection
from django.conf import settings
register = template.Library()

class SQLDebugInfo(template.Node):

    def render(self, context):
        return json.dumps(connection.queries)


def sql_debug_info(parser, token):
    return SQLDebugInfo()


register.tag('sql_debug_info', sql_debug_info)