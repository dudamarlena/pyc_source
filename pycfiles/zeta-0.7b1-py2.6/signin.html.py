# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/accounts/signin.html.py
# Compiled at: 2010-07-12 02:00:37
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278914437.479143
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/accounts/signin.html'
_template_uri = '/derived/accounts/signin.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['bd_script', 'bd_body']

def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]


def _mako_generate_namespaces(context):
    ns = runtime.Namespace('elements', context._clean_inheritance_tokens(), templateuri='/component/elements.html', callables=None, calling_uri=_template_uri, module=None)
    context.namespaces[(__name__, 'elements')] = ns
    return


def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, '/base/basic1.html', _template_uri)


def render_body(context, **pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer('\n')
        __M_writer('\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bd_script(context):
    context.caller_stack._push_frame()
    try:
        parent = context.get('parent', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        __M_writer(escape(parent.bd_script()))
        __M_writer('\n\n    <script type="text/javascript">\n        dojo.addOnLoad(\n            function() { dojo.query( "input[name=username]" )[0].focus(); }\n        );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bd_body(context):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')
        __M_writer = context.writer()
        __M_writer('\n    ')
        pagebartext = 'Please SignIn'
        flash = c.signinflash or ''
        __M_writer('\n\n    ')
        __M_writer(escape(elements.pagebar(pagebartext)))
        __M_writer('\n    <div id="bdy">\n    <div id="signin" class="w100 mt10">\n        <div class="fgred" style="margin-left: 50px;">')
        __M_writer(escape(flash))
        __M_writer('</div>\n        <form action="%s" method="post">\n        <div class="w100 form">\n            <div class="field">\n                <div class="label" style="width : 8em;">Username :</div>\n                <div class="ftbox">\n                    <input name="username" type="text"></input></div>\n            </div>\n            <div class="field">\n                <div class="label" style="width : 8em;">Password :</div>\n                <div class="ftbox">\n                    <input name="password" type="password"></input></div>\n            </div>\n            <div class="field w100">\n                <div class="label" style="width : 8em;"></div>\n                <div class="fsubmit">\n                    <input name="authform" value="Sign In" type="submit"></input></div>\n            </div>\n        </div>\n        </form>\n        <br/>\n        <div class="mt10 lclear">\n            <a href="')
        __M_writer(escape(h.url_forgotpass))
        __M_writer('">forgot-password</a></div>\n    </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()