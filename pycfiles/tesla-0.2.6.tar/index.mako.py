# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danjac/petprojects/tesla/tests/output/AuthProjectName/data/templates/index.mako.py
# Compiled at: 2007-09-06 07:54:41
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
_magic_number = 2
_modified_time = 1189079681.40786
_template_filename = '/Users/danjac/petprojects/tesla/tests/output/AuthProjectName/authprojectname/templates/index.mako'
_template_uri = '/index.mako'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = None
_exports = []

def render_body(context, **pageargs):
    context.caller_stack.push_frame()
    try:
        __M_locals = dict(pageargs=pageargs)
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        context.write('<html>\n<body>\n')
        if h.has_permission('add_users'):
            context.write('<div>Add user</div>\n')
        if c.auth_user:
            context.write('<div>Post</div>\n')
        context.write('</body>\n</html>')
        return ''
    finally:
        context.caller_stack.pop_frame()