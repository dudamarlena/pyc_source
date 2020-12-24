# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/license/lictline.html.py
# Compiled at: 2010-07-12 02:00:45
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278914445.766871
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/license/lictline.html'
_template_uri = '/derived/license/lictline.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['hd_script', 'bd_script', 'bd_body']
page_tooltips = [
 [
  'Help',
  "Use the selectable options in the page bar to navigate to desired \nlicense page. License can be associated with a project (via project's\nadmin page). In the page bar, along with the license name,\n(license-id) will be displayed in paranthesis. Use this 'id' for referring to\nthe license.\n"],
 [
  'Timeline',
  'Timeline gives a log of all updates done to license.']]

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
        __M_writer('\n\n    <script type="text/javascript">\n    ')
        charttitle = (c.license.licensename if c.license else 'license ') + ' activity'
        __M_writer('\n    function setup_charts() {\n        var datatline = ')
        __M_writer(h.json.dumps(c.datatline))
        __M_writer('\n        timelinechart( datatline, Date.UTC( ')
        __M_writer(escape((',').join(c.startdt)))
        __M_writer(" ),\n                       'chart_tline', '")
        __M_writer(escape(charttitle))
        __M_writer("' );\n    }\n    </script>\n")
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
        __M_writer('\n\n    <script type="text/javascript">\n        dojo.addOnLoad( function() {\n            /* License shortcut list */\n            select_goto( dojo.query( \'#viewlicense\' )[0] );\n        });\n        dojo.addOnLoad( setup_charts );\n\n        dojo.addOnLoad( setup_userpanes );\n        dojo.addOnLoad( adjust_upheight );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bd_body(context):
    context.caller_stack._push_frame()
    try:
        forms = _mako_get_namespace(context, 'forms')
        capture = context.get('capture', UNDEFINED)
        c = context.get('c', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')
        h = context.get('h', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        if c.license:
            pagebartext = 'Timeline: %s (%s)' % (c.license.licensename, c.license.id)
        else:
            pagebartext = 'Timeline'
        charts = capture(elements.iconlink, h.url_licensecharts, 'barchart', title='Analytics on license')
        __M_writer('\n    ')
        __M_writer(escape(elements.pagebar(pagebartext, spans=[
         capture(forms.form_licenselist, c.licenselist, c.license and c.license.licensename)], rspans=[
         charts], tooltips=page_tooltips)))
        __M_writer('\n    <div id="bdy" class="w100">\n')
        if c.userpanes:
            __M_writer('    <div id="licensepage" class="panel1">\n')
        else:
            __M_writer('    <div id="licensepage" class="fullpanel1">\n')
        __M_writer('        ')
        __M_writer(escape(elements.timeline_view(c.logs, c.fromoff, c.tooff, c.links, chartid='chart_tline')))
        __M_writer('\n    </div>\n')
        if c.userpanes:
            __M_writer('    <div class="panel2">')
            __M_writer(escape(elements.user_panes(c.userpanes)))
            __M_writer('</div>\n')
        __M_writer('    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()