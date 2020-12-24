# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/accounts/register.html.py
# Compiled at: 2010-07-12 02:05:21
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278914721.445519
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/accounts/register.html'
_template_uri = '/derived/accounts/register.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['hd_script', 'bd_script', 'bd_body']
page_tooltips = [
 [
  'Registration-form',
  'All form fields are mandatory. Follow the help text \nunder each field and enter valid input. By submitting the form, it\nis implied that you have read the terms-of-service.\n']]

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
        __M_writer('\n\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n\n')
        __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_hd_script(context):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        parent = context.get('parent', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        __M_writer(escape(parent.hd_script()))
        __M_writer('\n\n    <script type="text/javascript">\n        usernames = ')
        __M_writer(h.json.dumps(c.usernames))
        __M_writer(';\n    </script>\n')
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
        __M_writer('\n\n    <script type="text/javascript">\n        dojo.addOnLoad( initform_userreg );\n    </script>\n')
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
        pagebartext = 'Create a new %s account' % c.sitename
        __M_writer('\n    ')
        __M_writer(escape(elements.pagebar(pagebartext, tooltips=page_tooltips)))
        __M_writer('\n    <div id="bdy">\n    <div id="userregister" class="mt20 w100" style="padding : 0 20% 0 0">\n')
        if c.authorized:
            __M_writer('            <div class="disptable w100">\n            <div class="disptrow">\n                <div class="disptcell" style="padding-left: 100px;">\n                    ')
            __M_writer(escape(forms.form_userreg(h.suburl_userreg, c.captcha.urlpath)))
            __M_writer('\n                </div>\n                <div class="disptcell">\n                <div style="width : 25em;">\n                    ')
            __M_writer(escape(elements.helpboard('\n                        <span class="fgred">All fields are mandatory.</span>\n                        <dl>\n                        <dt>username</dt>\n                            <dd>Pick a proper username, you may not be able to\n                            change it later.</dd>\n                        <dt>Terms of Service</dt>\n                            <dd>If `Terms of Service (tos)` it empty, prompt your\n                            site-administrator to add a valid TOS content at\n                            <a href="/tos">tos</a></dd>\n                        </dl>\n                    ')))
            __M_writer('\n                </div>\n                </div>\n            </div>\n            </div>\n')
        else:
            __M_writer('        <div class="fgcrimson m20" style="font-size: 120%">\n            Registration is allowed only by invitation\n        </div>\n')
        __M_writer('    </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()