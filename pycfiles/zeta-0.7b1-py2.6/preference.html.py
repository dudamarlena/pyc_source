# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/userpage/preference.html.py
# Compiled at: 2010-07-12 02:07:19
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278914839.901272
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/userpage/preference.html'
_template_uri = '/derived/userpage/preference.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['hd_script', 'bd_script', 'bd_body']
page_tooltips = [
 [
  'Help',
  'User preference'],
 [
  'User Home',
  'Snatpshot of user activity and statistics'],
 [
  'Users',
  'List of registered users, and their summary'],
 [
  'GoogleMap',
  'If enable in site-admin -> site-config, watch yourself and your friends in\ngooglemap'],
 [
  'MyTickets',
  'All tickets that user participates in, across projects'],
 [
  'Timeline',
  'Timeline of user activity']]

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
        __M_writer('\n\n')
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
        str = context.get('str', UNDEFINED)
        parent = context.get('parent', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        __M_writer(escape(parent.hd_script()))
        __M_writer('\n\n    <script type="text/javascript">\n        function preference_forms() {\n            var div_accinfo = dojo.byId( "accinfo" );\n\n            /* User photo attachment */\n            new zeta.Attachments(\n                { user: [ \'')
        __M_writer(escape(str(c.authuser.id)))
        __M_writer("', '")
        __M_writer(escape(c.authuser.username))
        __M_writer("' ],\n                  id: 'photoattachblk',\n                  addform: [ 'userphoto', '")
        __M_writer(h.suburl_adduserphoto)
        __M_writer("' ],\n                  delform: [ 'deluserphoto', '")
        __M_writer(h.suburl_deluserphoto)
        __M_writer("' ],\n                  editable: ")
        __M_writer(escape([0, 1][(c.photo_editable == True)]))
        __M_writer(",\n                  url: '")
        __M_writer(h.url_userprefresh)
        __M_writer("',\n                  label: 'Upload Photo',\n                  attachs: ")
        __M_writer(h.json.dumps(c.photoattach))
        __M_writer("\n                }, div_accinfo.childNodes[1]\n            );\n\n            /* User icon attachment */\n            new zeta.Attachments(\n                { user: [ '")
        __M_writer(escape(str(c.authuser.id)))
        __M_writer("', '")
        __M_writer(escape(c.authuser.username))
        __M_writer("' ],\n                  id: 'iconattachblk',\n                  addform: [ 'usericon', '")
        __M_writer(h.suburl_addusericon)
        __M_writer("' ],\n                  delform: [ 'delusericon', '")
        __M_writer(h.suburl_delusericon)
        __M_writer("' ],\n                  editable: ")
        __M_writer(escape([0, 1][(c.icon_editable == True)]))
        __M_writer(",\n                  url: '")
        __M_writer(h.url_userirefresh)
        __M_writer("',\n                  label: 'Upload Icon',\n                  attachs: ")
        __M_writer(h.json.dumps(c.iconattach))
        __M_writer('\n                }, div_accinfo.childNodes[3]\n            );\n\n            new zeta.ConfigTabs({\n                id: "preftabs",\n                tabs: dojo.query( "div[name=preftab]" )\n                }, dojo.query( "div[name=preftabs]" )[0]\n            );\n\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bd_script(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        parent = context.get('parent', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        __M_writer(escape(parent.bd_script()))
        __M_writer('\n\n')
        if c.googlemaps:
            __M_writer('    <script\n        src="http://maps.google.com/maps?file=api&amp;v=2.x&amp;key=')
            __M_writer(escape(c.googlemaps))
            __M_writer('"\n        type="text/javascript">\n    </script>\n\n    <script type="text/javascript">\n        var map         = null;\n        var geocoder    = null;\n        var fulladdress = "')
            __M_writer(escape(c.fulladdress))
            __M_writer('"\n        var username    = "')
            __M_writer(escape(c.authusername))
            __M_writer('"\n        function init_gmap() {\n            rc = creategmap( "useringmap", 400, 400 )\n            map      = rc[0];\n            geocoder = rc[1];\n            marker = showAddress( username, fulladdress, fulladdress );\n        }\n    </script>\n')
        __M_writer('\n    <script type="text/javascript">\n        dojo.addOnLoad( preference_forms );\n        dojo.addOnLoad( initform_accountinfo );\n        dojo.addOnLoad( initform_updtpass );\n        dojoaddOnLoad( \'init_gmap\' );\n\n        dojo.addOnLoad( setup_userpanes );\n        dojo.addOnLoad( adjust_upheight );\n    </script>\n')
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
        pagebartext = 'User preference (%s)' % c.authusername
        users = '<div class="floatl mt4 ml10 fwnormal fntsmall">' + '<a href="%s">Users</a></div>' % h.url_usershome
        uhome = '<div class="floatl mt4 ml10 fwnormal fntsmall">' + '<a href="%s">Homepage</a></div>' % h.url_userhome
        usersgmap = '<div class="floatl mt4 ml10 fwnormal fntsmall">' + '<a href="%s">OnGooglemap</a></div>' % h.url_usersgmap
        mytickets = '<div class="floatl mt4 ml10 fwnormal fntsmall">' + '<a href="%s">MyTickets</a></div>' % h.url_mytickets
        charts = capture(elements.iconlink, h.url_usercharts, 'barchart', title='Analytics on %s' % c.username)
        tline = capture(elements.iconlink, h.url_usertline, 'timeline', title='Timeline')
        __M_writer('\n    ')
        __M_writer(escape(elements.pagebar(pagebartext, [uhome, users, usersgmap, mytickets], rspans=[
         charts, tline], tooltips=page_tooltips)))
        __M_writer('\n    <div id="bdy">\n')
        if c.authusername == 'anonymous' or not c.userpanes:
            __M_writer('        <div id="userpreference" class="fullpanel1">\n')
        else:
            __M_writer('        <div id="userpreference" class="panel1">\n')
        __M_writer('    <div class="m10">\n    <div name="preftabs">\n        <div id="accinfo" class="dispnone" name="preftab" title="AccountInfo"\n             selected="true">\n            <div name="photoattachs"></div>\n            <div name="iconattachs"></div>\n            <div class="disptable bclear ml50">\n            <div class="disptrow">\n                <div class="disptcell w50 vtop">\n                ')
        __M_writer(escape(forms.form_accountinfo(c.authuser, h.suburl_accountinfo)))
        __M_writer('\n                </div>\n                <div class="disptcell" style="padding-left: 50px;">\n                    <div id="useringmap" class="fggray2 p5"\n                         style="border: 2px solid gray; width: 400px; height: 400px;">\n                         want to see you in google maps ? Enable `googlemaps` in\n                         site-admin->siteConfig\n                    </div>\n                </div>\n            </div>\n            </div>\n        </div>\n        <div id="chpass" class="dispnone" name="preftab" title="ChangePassword">\n            ')
        __M_writer(escape(forms.form_updtpass(c.authuser, h.suburl_updtpass)))
        __M_writer('\n        </div>\n    </div>\n    </div>\n    </div>\n')
        if c.authusername != 'anonymous' and c.userpanes:
            __M_writer('        <div class="panel2">')
            __M_writer(escape(elements.user_panes(c.userpanes)))
            __M_writer('</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()