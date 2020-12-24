# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/userpage/userhome.html.py
# Compiled at: 2010-07-12 02:07:47
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278914867.096977
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/userpage/userhome.html'
_template_uri = '/derived/userpage/userhome.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['reviewstat', 'wikistat', 'hd_script', 'bd_body', 'ticketstat', 'bd_script']
page_tooltips = [
 [
  'Help',
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
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n\n\n')
        __M_writer('\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_reviewstat(context, authoredrevw, modertrevw, particprevw, revwcomments):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n    <div class="m5">\n        Authored <span class="fgcrimson">')
        __M_writer(escape(authoredrevw))
        __M_writer('</span> reviews;\n        Moderated <span class="fgcrimson">')
        __M_writer(escape(modertrevw))
        __M_writer('</span> reviews;\n        Participated in <span class="fgcrimson">')
        __M_writer(escape(particprevw))
        __M_writer('</span> reviews;\n        Commented <span class="fgcrimson">')
        __M_writer(escape(revwcomments))
        __M_writer('</span> times for\n        reviews\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_wikistat(context, wikicomments):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n    <div class="m5">\n        Commented <span class="fgcrimson">')
        __M_writer(escape(wikicomments))
        __M_writer('</span> times for\n        wiki pages\n    </div>\n')
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


def render_bd_body(context):
    context.caller_stack._push_frame()
    try:
        capture = context.get('capture', UNDEFINED)
        c = context.get('c', UNDEFINED)
        set = context.get('set', UNDEFINED)
        h = context.get('h', UNDEFINED)
        list = context.get('list', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')
        __M_writer = context.writer()
        __M_writer('\n    ')
        pagebartext = '%s' % c.user.username
        users = '<div class="floatl mt4 ml10 fwnormal fntsmall">' + '<a href="%s">Users</a></div>' % h.url_usershome
        usersgmap = '<div class="floatl mt4 ml10 fwnormal fntsmall">' + '<a href="%s">OnGooglemap</a></div>' % h.url_usersgmap
        mytickets = '<div class="floatl mt4 ml10 fwnormal fntsmall">' + '<a href="%s">MyTickets</a></div>' % h.url_mytickets
        charts = capture(elements.iconlink, h.url_usercharts, 'barchart', title='Analytics on %s' % c.username)
        tline = capture(elements.iconlink, h.url_usertline, 'timeline', title='Timeline')
        __M_writer('\n    ')
        __M_writer(escape(elements.pagebar(pagebartext, [users, usersgmap, mytickets], rspans=[
         charts, tline], tooltips=page_tooltips)))
        __M_writer('\n    <div id="bdy">\n')
        if c.authusername == 'anonymous' or not c.userpanes:
            __M_writer('        <div id="userpreference" class="fullpanel1">\n')
        else:
            __M_writer('        <div id="userpreference" class="panel1">\n')
        __M_writer('    <div class="m10">\n        <div id="userdetail">\n            ')
        __M_writer(escape(elements.userdetails(c.user, c.user.userinfo, h.url_userphoto)))
        __M_writer('\n        </div>\n        <div class="floatr ml10 pt10" style="width: 30%" >\n            ')
        adminprojects = c.statistics['adminprojects']
        inprojects = c.statistics['inprojects']
        projects = list(set(adminprojects + inprojects.keys()))
        projcomps = {}
        [ projcomps.setdefault(comp.project.projectname, []).append(comp.componentname) for comp in c.user.owncomponents
        ]
        __M_writer('\n            <div class="bgblue1 p5 mb10 br5">\n                <table><tr>\n                    <td class="fntbold p3">Administrator :</td>\n                    <td class="p3">\n                        ')
        __M_writer((', ').join([ '<a href="%s">%s</a>' % (h.url_forproject(p), p) for p in adminprojects
                               ]))
        __M_writer('\n                    </td>\n                </tr></table>\n            </div>\n            <div class="bgblue1 p5 mb10 br5">\n                <div class="fntbold">Project teams :</div>\n                <table class="ml20 mt10">\n')
        for p in inprojects:
            __M_writer('                    <tr>\n                        <td class="p3 fntbold ralign">')
            __M_writer(escape(p))
            __M_writer(' : </td>\n                        <td class="p3 fntitalic">')
            __M_writer(escape((', ').join(inprojects[p])))
            __M_writer('</td>\n                    </tr>\n')

        __M_writer('                </table>\n            </div>\n            <div class="bgblue1 p5 mb10 br5">\n                <div class="fntbold">Own components :</div>\n                <table class="ml20 mt10">\n')
        for (p, comps) in projcomps.iteritems():
            __M_writer('                    <tr>\n                        <td class="p3 fntbold ralign">\n                            <a href="')
            __M_writer(escape(h.url_forproject(p)))
            __M_writer('">')
            __M_writer(escape(p))
            __M_writer(' </a>\n                        </td>\n                        <td class="p3 fntitalic">')
            __M_writer(escape((', ').join(comps)))
            __M_writer('</td>\n                    </tr>\n')

        __M_writer('                </table>\n            </div>\n            <div class="bgblue1 p5 mb10 br5">\n                <table>\n                    <tr>\n                        <td class="p3 fntbold ralign">Files uploaded : </td>\n                        <td class="p3 fntitalic">\n                            <span class="fgcrimson">\n                                ')
        __M_writer(escape(c.statistics['uploadedfiles']))
        __M_writer('\n                            </span>\n                            files\n                        </td>\n                    </tr>\n                    <tr>\n                        <td class="p3 fntbold ralign">Down-voted : </td>\n                        <td class="p3 fntitalic">\n                            <span class="fgcrimson">\n                                ')
        __M_writer(escape(c.statistics['votes']['down']))
        __M_writer('\n                            </span>\n                            times\n                        </td>\n                    </tr>\n                    <tr>\n                        <td class="p3 fntbold ralign">Up-voted : </td>\n                        <td class="p3 fntitalic">\n                            <span class="fgcrimson">\n                                ')
        __M_writer(escape(c.statistics['votes']['up']))
        __M_writer('\n                            </span>\n                            times\n                        </td>\n                    </tr>\n                    <tr>\n                        <td class="p5 fntbold ralign">For tickets : </td>\n                        <td class="p3 fntitalic">\n                            <div>\n                                Participated in\n                                <span class="fgcrimson">\n                                    ')
        __M_writer(escape(c.statistics['tickets']))
        __M_writer('\n                                </span> tickets,\n                            </div>\n                            <div>\n                                providing\n                                <span class="fgcrimson">\n                                    ')
        __M_writer(escape(c.statistics['tckcomments']))
        __M_writer('\n                                </span> comments\n                            </div>\n                        </td>\n                    </tr>\n                    <tr>\n                        <td class="p5 fntbold ralign">For wiki : </td>\n                        <td class="p3 fntitalic">\n                            <div>\n                                commented\n                                <span class="fgcrimson">\n                                    ')
        __M_writer(escape(c.statistics['wikicomments']))
        __M_writer('\n                                </span> times\n                            </div>\n                        </td>\n                    </tr>\n                    <tr>\n                        <td class="p5 fntbold ralign">For review : </td>\n                        <td class="p3 fntitalic">\n                            <div>\n                                Authored\n                                <span class="fgcrimson">\n                                    ')
        __M_writer(escape(c.statistics['authoredrevw']))
        __M_writer('\n                                </span> reviews,\n                            </div>\n                            <div>\n                                moderated\n                                <span class="fgcrimson">\n                                    ')
        __M_writer(escape(c.statistics['modertrevw']))
        __M_writer('\n                                </span> reviews,\n                            </div>\n                            <div>\n                                participated in\n                                <span class="fgcrimson">\n                                    ')
        __M_writer(escape(c.statistics['particprevw']))
        __M_writer('\n                                </span> reviews,\n                            </div>\n                            <div>\n                                providing\n                                <span class="fgcrimson">\n                                    ')
        __M_writer(escape(c.statistics['revwcomments']))
        __M_writer('\n                                </span> comments\n                            </div>\n                        </td>\n                    </tr>\n                </table>\n            </div>\n            <div id="useringmap" class="fggray2 p5 mb10 "\n                 style="border: 2px solid gray; width: 95%; height: 200px;">\n                 want to see users in google maps ? Enable `googlemaps` in\n                 site-admin->siteConfig\n            </div>\n        </div>\n        <div class="floatl timeline ml10" style="width : 65%">\n            <h4 class="bggrn2 br4 p2" >Recent activities</h4>\n            <ul>\n')
        for log in c.logs:
            __M_writer('                <li>\n                    <div class="mt5 mb5 ml3 wsnowrap w100"\n                         style="overflow: hidden;">\n                        <span class="hoverhighlight">\n                            ')
            __M_writer(escape(elements.iconize(log.created_on.strftime('%a, %b %d, %Y'), 'plus_exp', span_name='interface', classes='pointer mr5')))
            __M_writer('\n                        </span>\n                        <span>in ')
            __M_writer(log.itemhtml)
            __M_writer('</span>\n                        <span name="logmsg" class="ml10 fggray">')
            __M_writer(escape(log.log))
            __M_writer('</span>\n                    </div>\n                </li>\n')

        __M_writer('            </ul>\n        </div>\n    </div>\n    </div>\n')
        if c.authusername != 'anonymous' and c.userpanes:
            __M_writer('        <div class="panel2">')
            __M_writer(escape(elements.user_panes(c.userpanes)))
            __M_writer('</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_ticketstat(context, tickets, tckcomments):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n    <div class="m5">\n        Commented <span class="fgcrimson">')
        __M_writer(escape(tckcomments))
        __M_writer('</span> times on tickets\n    </div>\n')
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
            __M_writer(h.json.dumps(c.useraddr))
            __M_writer('\n        function init_gmap() {\n            var cbox = dojo.contentBox( \'useringmap\' );\n            rc = creategmap( "useringmap", cbox.w, cbox.h ); // width, height\n            map      = rc[0];\n            geocoder = rc[1];\n            dojo.forEach(\n                useraddrs,\n                function( uaddr ) {\n                    uaddr[uaddr.length] = showAddress( uaddr[0], uaddr[1], uaddr[1] );\n                }\n            );\n        }\n    </script>\n')
        __M_writer('\n    <script type="text/javascript">\n        dojoaddOnLoad( \'init_gmap\' );\n        dojo.addOnLoad( setup_userpanes );\n        dojo.addOnLoad( adjust_upheight );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()