# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/attachs/add.html.py
# Compiled at: 2010-07-12 03:17:35
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278919055.276139
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/attachs/add.html'
_template_uri = '/derived/attachs/add.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['hd_script', 'bd_script', 'bd_body']
page_tooltips = [
 [
  'Help',
  'Add a new attachment that are not associated with any thing'],
 [
  'Attachments',
  'List of attachments (files) stored in this site. If you have the permission\nyou can edit <b>summary</b> and <b>tag</b> fields'],
 [
  'Charts',
  'Charts are plotted for\n<ul>\n    <li>user Vs files-attached Vs total-payload-uploaded</li>\n    <li>files Vs no-of-downloads</li>\n    <li>attachments Vs uploaded-time-line</li>\n    <li>attachments Vs tags</li>\n</ul>\n'],
 [
  'Timeline',
  'Log of updates done to all attachments.']]

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
        capture = context.get('capture', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        pagebartext = 'Add Attachments'
        attachs = '<div class="floatl mt4 ml10 fwnormal fntsmall">' + '<a href="%s">Attachments</a></div>' % h.url_attachments
        tline = capture(elements.iconlink, h.url_attachtline, 'timeline', title='Attachment Timeline')
        charts = capture(elements.iconlink, h.url_attachcharts, 'barchart', title='Analytics on file attachments')
        __M_writer('\n    ')
        __M_writer(escape(elements.pagebar(pagebartext, [attachs], rspans=[charts, tline], tooltips=page_tooltips)))
        __M_writer('\n    <div id="bdy" class="w100">\n')
        if c.userpanes:
            __M_writer('    <div id="addattach" class="panel1">\n')
        else:
            __M_writer('    <div id="addattach" class="fullpanel1">\n')
        __M_writer('        <div class="disptable">\n        <div class="disptrow">\n            <div class="disptcell">\n                ')
        __M_writer(escape(forms.form_addattachs(c.authuser, h.suburl_addattachs)))
        __M_writer('\n            </div>\n            <div class="disptcell">\n                ')
        __M_writer(escape(elements.helpboard('\n                    Add attachment that is not associated with license,\n                    project, ticket, wiki etc ...\n                    <br></br>\n                    Primarily useful for adding attachments and linking /\n                    referring them else where.\n                ')))
        __M_writer('\n            </div>\n        </div>\n        </div>\n    </div>\n')
        if c.userpanes:
            __M_writer('    <div class="panel2">')
            __M_writer(escape(elements.user_panes(c.userpanes)))
            __M_writer('</div>\n')
        __M_writer('    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()