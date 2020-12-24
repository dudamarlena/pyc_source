# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/userpage/usersgmap.html.py
# Compiled at: 2010-07-12 02:07:50
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278914870.967039
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/userpage/usersgmap.html'
_template_uri = '/derived/userpage/usersgmap.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['hd_script', 'bd_script', 'bd_body']
page_tooltips = [
 [
  'Help',
  'If enabled in site-admin -> site-config, watch yourself and your friends in\ngooglemap'],
 [
  'Users',
  'List of all registered users and their summary'],
 [
  'Timeline',
  'Timeline of users activity']]

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
        __M_writer('\n\n')
        __M_writer('\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n\n\n')
        __M_writer('\n\n')
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
        __M_writer('\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bd_script(context):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        parent = context.get('parent', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        __M_writer(escape(parent.bd_script()))
        __M_writer('\n\n')
        if c.googlemaps:
            __M_writer('    <script\n        src="http://maps.google.com/maps?file=api&amp;v=2.x&amp;key=')
            __M_writer(escape(c.googlemaps))
            __M_writer('"\n        type="text/javascript">\n    </script>\n\n    <script type="text/javascript">\n        var map       = null;\n        var geocoder  = null;\n        var useraddrs = ')
            __M_writer(h.json.dumps(c.useraddrs))
            __M_writer('\n        function init_gmap() {\n            rc = creategmap( "useringmap", 1000, 600 ) // width, height\n            map      = rc[0];\n            geocoder = rc[1];\n            dojo.forEach(\n                useraddrs,\n                function( uaddr ) {\n                    console.log( uaddr );\n                    uaddr[uaddr.length] = showAddress( uaddr[0], uaddr[1], uaddr[1] );\n                }\n            );\n        }\n    </script>\n')
        __M_writer('\n    <script type="text/javascript">\n        dojoaddOnLoad( \'init_gmap\' );\n\n        dojo.addOnLoad( setup_userpanes );\n        dojo.addOnLoad( adjust_upheight );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bd_body(context):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')
        capture = context.get('capture', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        pagebartext = 'Users on google map'
        users = '<div class="floatl mt4 ml10 fwnormal fntsmall">' + '<a href="%s">Users</a></div>' % h.url_usershome
        charts = capture(elements.iconlink, h.url_userscharts, 'barchart', title='Analytics on users')
        tline = capture(elements.iconlink, h.url_usertline, 'timeline', title='Timeline')
        __M_writer('\n    ')
        __M_writer(escape(elements.pagebar(pagebartext, [users], rspans=[
         charts, tline], tooltips=page_tooltips)))
        __M_writer('\n    <div id="bdy">\n')
        if c.authusername == 'anonymous' or not c.userpanes:
            __M_writer('        <div id="userpreference" class="fullpanel1">\n')
        else:
            __M_writer('        <div id="userpreference" class="panel1">\n')
        __M_writer('    <div class="m10">\n        <div id="useringmap" class="fggray2 p5"\n             style="border: 2px solid gray; width: 100% height: 800px;">\n             want to see users in google maps ? Enable `googlemaps` in\n             site-admin->siteConfig\n        </div>\n    </div>\n    </div>\n    </div>\n')
        if c.authusername != 'anonymous' and c.userpanes:
            __M_writer('        <div class="panel2">')
            __M_writer(escape(elements.user_panes(c.userpanes)))
            __M_writer('</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()