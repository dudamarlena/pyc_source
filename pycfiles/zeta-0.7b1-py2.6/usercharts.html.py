# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/userpage/usercharts.html.py
# Compiled at: 2010-07-18 04:24:13
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1279441453.751309
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/userpage/usercharts.html'
_template_uri = '/derived/userpage/usercharts.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['hd_script', 'bd_script', 'bd_body']
page_tooltips = [
 [
  'Help',
  'Charts are plotted for\n<ul>\n    <li>pie chart for project wise activities</li>\n</ul>\n'],
 [
  'Timeline',
  'Log of updates done to all license.']]
chartoptions = [
 'chart12']

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
    ns = runtime.Namespace('charts', context._clean_inheritance_tokens(), templateuri='/component/charts.html', callables=None, calling_uri=_template_uri, module=None)
    context.namespaces[(__name__, 'charts')] = ns
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
        __M_writer('\n    \n    <script type="text/javascript">\n    var zcharts = {};\n    function setup_charts() {\n        var currcntnr = dojo.query( \'[name=chart12]\' )[0];\n        setup_chart12();\n        dojo.toggleClass( currcntnr, \'dispnone\', false );\n        zcharts[\'currchart\'] = zcharts.chart12.init();\n        zcharts[\'currcntnr\'] = currcntnr;\n        selectchart( dojo.byId( \'selchart\' ), zcharts );\n    }\n    </script>\n')
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
        __M_writer('\n\n    <script type="text/javascript">\n        dojo.addOnLoad( setup_charts );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bd_body(context):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')
        charts = _mako_get_namespace(context, 'charts')
        capture = context.get('capture', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        pagebartext = 'Charts and Analytics'
        users = '<div class="floatl mt4 ml10 fwnormal fntsmall">' + '<a href="%s">Users</a></div>' % h.url_usershome
        usersgmap = '<div class="floatl mt4 ml10 fwnormal fntsmall">' + '<a href="%s">OnGooglemap</a></div>' % h.url_usersgmap
        mytickets = '<div class="floatl mt4 ml10 fwnormal fntsmall">' + '<a href="%s">MyTickets</a></div>' % h.url_mytickets
        tline = capture(elements.iconlink, h.url_usertline, 'timeline', title='Timeline')
        __M_writer('\n    ')
        __M_writer(escape(elements.pagebar(pagebartext, [users, usersgmap, mytickets], rspans=[
         tline], tooltips=page_tooltips)))
        __M_writer('\n    <div id="bdy" class="w100">\n')
        if c.userpanes:
            __M_writer('    <div id="usercharts" class="panel1">\n')
        else:
            __M_writer('    <div id="usercharts" class="fullpanel1">\n')
        __M_writer('\n        ')
        __M_writer(escape(charts.selectcharts(chartoptions, 'chart12')))
        __M_writer('\n        ')
        __M_writer(escape(charts.chart12(c.chart12_data)))
        __M_writer('\n\n    </div>\n')
        if c.userpanes:
            __M_writer('    <div class="panel2">')
            __M_writer(escape(elements.user_panes(c.userpanes)))
            __M_writer('</div>\n')
        __M_writer('    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()