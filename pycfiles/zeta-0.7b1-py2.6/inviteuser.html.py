# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/userpage/inviteuser.html.py
# Compiled at: 2010-07-12 02:07:54
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278914874.27435
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/userpage/inviteuser.html'
_template_uri = '/derived/userpage/inviteuser.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['hd_script', 'bd_script', 'bd_body']
page_tooltips = [
 [
  'Help',
  'User invitation must be enabled in <b>site-admin->siteConfig</b>.\nIf any registered user are to be allowed to invite, again configure the same \nin site-admin->siteConfig <br/>\nProvide the email-id of the person you wish to invite.\n']]

def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]


def _mako_generate_namespaces(context):
    ns = runtime.Namespace('forms', context._clean_inheritance_tokens(), templateuri='/component/forms.html', callables=None, calling_uri=_template_uri, module=None)
    context.namespaces[(__name__, 'forms')] = ns
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
        __M_writer('\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n\n\n')
        __M_writer('\n\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_hd_script(context):
    context.caller_stack._push_frame()
    try:
        parent = context.get('parent', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        __M_writer(escape(parent.hd_script()))
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
        __M_writer('\n\n    <script type="text/javascript">\n        dojo.addOnLoad( setup_userpanes );\n        dojo.addOnLoad( adjust_upheight );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bd_body(context):
    context.caller_stack._push_frame()
    try:
        forms = _mako_get_namespace(context, 'forms')
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')
        __M_writer = context.writer()
        __M_writer('\n    ')
        pagebartext = 'Invite a user to your site'
        __M_writer('\n    ')
        __M_writer(escape(elements.pagebar(pagebartext, tooltips=page_tooltips)))
        __M_writer('\n    <div id="bdy">\n')
        if c.authusername == 'anonymous' or not c.userpanes:
            __M_writer('        <div id="userpreference" class="fullpanel1">\n')
        else:
            __M_writer('        <div id="userpreference" class="panel1">\n')
        __M_writer('    <div class="m10">\n        <div class="ml50 mr50">\n')
        if c.usercaninvite:
            __M_writer('                ')
            __M_writer(escape(forms.form_inviteuser(c.authuser, h.suburl_inviteuser)))
            __M_writer('\n')
        else:
            __M_writer('                <div class="fgcrimson" style="font-size: 120%">\n                    Contact site administrator enable invitation.\n                </div>\n')
        __M_writer('        </div>\n    </div>\n    </div>\n')
        if c.authusername != 'anonymous' and c.userpanes:
            __M_writer('        <div class="panel2">')
            __M_writer(escape(elements.user_panes(c.userpanes)))
            __M_writer('</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()