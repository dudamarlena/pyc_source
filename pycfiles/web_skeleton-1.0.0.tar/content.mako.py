# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/yuneta-dev/yuneta/^yunos/yunetamonitor/tags/0.00.aa/.cache/yunetamonitor/htmlrendercode/content.mako.py
# Compiled at: 2015-12-27 13:15:23
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1451240124.000053
_enable_loop = True
_template_filename = '/home/yuneta-dev/yuneta/^yunos/yunetamonitor/yunetamonitor/htmlrendercode/content.mako'
_template_uri = '/yunetamonitor/htmlrendercode/content.mako'
_source_encoding = 'ascii'
_exports = []

def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]


def _mako_generate_namespaces(context):
    ns = runtime.TemplateNamespace('logo', context._clean_inheritance_tokens(), templateuri='templates/logo.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, 'logo')] = ns
    return


def render_body(context, **pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        logo = _mako_get_namespace(context, 'logo')
        list = context.get('list', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n\n<div id="main-content" class="grid-content-class">\n    <header>\n    ')
        __M_writer(unicode(logo.logo()))
        __M_writer('\n    </header>\n\n    <footer>\n        <span style="unicode-bidi:bidi-override; direction: rtl;">\n        ')
        revchars = list('yuneta@yuneta.io')
        revchars.reverse()
        revchars = ('').join(revchars)
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([ (__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['revchars'] if __M_key in __M_locals_builtin_stored ]))
        __M_writer('\n        ')
        __M_writer(unicode(revchars))
        __M_writer('\n        </span>\n    </footer>\n\n</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()