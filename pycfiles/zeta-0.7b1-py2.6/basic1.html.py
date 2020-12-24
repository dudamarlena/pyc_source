# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/base/basic1.html.py
# Compiled at: 2010-07-15 09:09:56
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1279199396.891979
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/base/basic1.html'
_template_uri = '/base/basic1.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['hd_meta', 'bd_metanav', 'hd_title', 'hd_links', 'hd_script', 'bd_body', 'bd_header', 'hd_styles', 'bd_footer', 'bd_breadcrumbs', 'bd_script']

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


def render_body(context, **pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        self = context.get('self', UNDEFINED)
        config = context.get('config', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n\n')
        __M_writer('\n')
        __M_writer('\n')
        __M_writer('\n\n<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">\n\n<html>\n    <head>\n        ')
        __M_writer(escape(self.hd_title()))
        __M_writer('\n        ')
        __M_writer(escape(self.hd_meta()))
        __M_writer('\n        ')
        __M_writer(escape(self.hd_links()))
        __M_writer('\n        ')
        __M_writer(escape(self.hd_styles()))
        __M_writer('\n        ')
        __M_writer(escape(self.hd_script()))
        __M_writer('\n    </head>\n    <body class="tundra">\n        ')
        disclaimer = config['zeta.hdisclaimer']
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([ (__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['disclaimer'] if __M_key in __M_locals_builtin_stored ]))
        __M_writer('\n')
        if disclaimer:
            __M_writer('            <div class="fntsmall fntbold fgred bgred1 calign">')
            __M_writer(escape(disclaimer))
            __M_writer('</div>\n')
        __M_writer('        ')
        __M_writer(escape(self.bd_metanav()))
        __M_writer('\n        ')
        __M_writer(escape(self.bd_header()))
        __M_writer('\n        ')
        __M_writer(escape(self.bd_breadcrumbs()))
        __M_writer('\n        ')
        __M_writer(escape(self.bd_body()))
        __M_writer('\n        ')
        __M_writer(escape(self.bd_footer()))
        __M_writer('\n        ')
        __M_writer(escape(self.bd_script()))
        __M_writer('\n    </body>\n</html>\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_hd_meta(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bd_metanav(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <div id="metanav" class="ralign fntsmall">\n        ')
        __M_writer(escape(c.authusername))
        __M_writer(' |\n        ')
        bar = ' '
        __M_writer('\n')
        for m in c.metanavs:
            if m.type == 'link':
                __M_writer('                ')
                __M_writer(escape(bar))
                __M_writer(' <a style="margin: 0;" title="')
                __M_writer(escape(m.title))
                __M_writer('" href="')
                __M_writer(escape(m.href))
                __M_writer('">')
                __M_writer(escape(m.text))
                __M_writer('</a>\n                ')
                bar = '|'
                __M_writer('\n')
            elif m.type == 'pointer':
                __M_writer('                ')
                __M_writer(escape(bar))
                __M_writer(' <span name="')
                __M_writer(escape(m.text))
                __M_writer('" class="fntsmall pointer fgblue">\n                            ')
                __M_writer(escape(m.text))
                __M_writer('<span class="fntxsmall vmiddle"> &#9660;</span></span>\n                ')
                bar = '|'
                __M_writer('\n')
            else:
                __M_writer('                &#9830;\n                ')
                bar = ' '
                __M_writer('\n')

        __M_writer('    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_hd_title(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <title>')
        __M_writer(escape(c.title))
        __M_writer('</title>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_hd_links(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n    <link href="/zdojo/release/dojo/resources/dojo.css" rel="stylesheet" type="text/css"></link>\n    <link href="/zdojo/ztundra.css" rel="stylesheet" type="text/css"></link>\n    <link href="/zdojo/zdojo.css" rel="stylesheet" type="text/css"></link>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_hd_script(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n    <script src="/zdojo/release/dojo/dojo.js" type="text/javascript"></script>\n    <script type="text/javascript">\n        // TODO : This function graciously fails handler subscription. Eventually this\n        //        should be removed ...\n        function dojoaddOnLoad( fnstr ) {\n            //try {\n            //    dojo.addOnLoad( fn );\n            //} catch( err ) { console.log( err )}\n            fn = dojo.getObject( fnstr )\n            if( typeof fn == \'function\' ) {\n                dojo.addOnLoad( fn );\n            }\n        };\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bd_body(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bd_header(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')
        h = context.get('h', UNDEFINED)
        forms = _mako_get_namespace(context, 'forms')
        getattr = context.get('getattr', UNDEFINED)
        config = context.get('config', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        __M_writer(escape(elements.flashmessages()))
        __M_writer('\n')
        if config['zeta.pageheader']:
            __M_writer('        <div id="lthead" class="w100">\n        <div class="disptable w100"></div>\n        <div class="disptrow">\n            <div class="disptcell vtop pr5">\n                <div id="sitelogo">\n                <a class="nodec fggray fntcaption" href="')
            __M_writer(escape(h.url_site))
            __M_writer('"><img alt="logo" style="max-width: 300px; max-height: 75px;" src="')
            __M_writer(escape(c.sitelogo))
            __M_writer('"></img></a>\n                </div>\n            </div>\n\n            <div class="disptcell vtop pt5 pb5">\n                ')
            __M_writer(escape(forms.form_searchbox(c.authuser, 'searchzeta', 'Search-Site', h.suburl_searchzeta)))
            __M_writer('\n            </div>\n\n            <div class="disptcell vmiddle w100"></div>\n\n            <div class="disptcell vtop pt5 pb5">\n')
            if c.project:
                __M_writer('                    ')
                __M_writer(escape(forms.form_searchbox(c.authuser, 'searchproject', 'Search-project', h.suburl_search, [
                 (
                  'project', c.project.projectname)])))
                __M_writer('\n')
            __M_writer('            </div>\n\n\n            <div class="disptcell vtop pl5">\n                <div id="prjlogo">\n')
            if c.project and getattr(h, 'url_prj', None):
                __M_writer('                    <a class="nodec fggray fntcaption" href="')
                __M_writer(escape(h.url_prj))
                __M_writer('"><img alt="logo" style="max-width: 300px; max-height: 75px;" src="')
                __M_writer(escape(c.prjlogo))
                __M_writer('"></img></a>\n')
            else:
                __M_writer('                    <div class="vmiddle fggray2 fntcaption p10 calign"></div>\n')
            __M_writer('                </div>\n            </div>\n        </div>\n        </div>\n        </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()

    return


def render_hd_styles(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bd_footer(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <div class="bclear" id="footer">\n        <hr style="margin-bottom: 0px"></hr>\n        <a class="floatl" href="')
        __M_writer(escape(c.zetalink))
        __M_writer('"><img width="110" height="45" src="')
        __M_writer(escape(c.zetalogo))
        __M_writer('"></img></a>\n        <div class="floatl" style="font-size: 11px; height : 45px">\n            <div class="ml5 calign" style="height : 22px; border-bottom : 4px solid Gainsboro">\n                <span style="vertical-align : -6px;">version : </span>\n                <span class="fntbold" style="vertical-align : -6px;">')
        __M_writer(escape(c.zetaversion))
        __M_writer('</span>\n            </div>\n            <div class="ml5 pt2" style="height : 22px;">\n                <span class="fntbold" style="color: skyblue">SKR</span>\n                <span class="fntbold" style="color: black">Farms (P) Ltd</span>\n            </div>\n        </div>\n        <div class="floatr fntbold bgblue1 brbl5 brbr5">\n        <table><tr>\n            <td class="p5 calign vmiddle">\n                <div>Z Links</div>\n            </td>\n            <td class="p5" style="border-left: 1px solid gray;">\n                <div><a target="_blank" class="fgcrimson"\n                        title="Track Zeta development activities"\n                        href="http://dev.discoverzeta.com"\n                        >zeta-development</a></div>\n                <div><a target="_blank" class="fgcrimson"\n                        title="Discuss with us"\n                        href="http://groups.google.com/group/zeta-discuss"\n                        >zeta-mailinglist</a>\n            </td>\n            <td class="p5">\n                <div><a target="_blank" class="fgcrimson"\n                        title="Our commercial site"\n                        href="mailto:support@discoverzeta.com"\n                        >Support</a></div>\n                <div><a target="_blank" class="fgcrimson"\n                        title="Our commercial site"\n                        href="http://discoverzeta.com/pricing"\n                        >Pricing</a></div>\n            </td>\n        </tr></table>\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bd_breadcrumbs(context):
    context.caller_stack._push_frame()
    try:
        session = context.get('session', UNDEFINED)
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')
        request = context.get('request', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        e = request.environ
        bd = session.get('breadcrumbs', [])
        hrefs = h.urlpathcrumbs(e['PATH_INFO'], e['HTTP_HOST'], e['SCRIPT_NAME'])
        node = lambda text, ref: '<a class="mr10 fgred nodec" href="%s">%s</a>' % (
         ref, text)
        __M_writer('\n')
        if c.authorized:
            __M_writer('        <div class="ralign fntsmall" style="margin : 4px;">\n')
            for (text, ref) in hrefs[:-1]:
                __M_writer('                ')
                __M_writer(escape(elements.iconize(node(text, ref), 'arrow_right', classes='floatl', styles='padding-left: 8px')))
                __M_writer('\n')

            if hrefs:
                __M_writer('                ')
                __M_writer(escape(elements.iconize(hrefs[(-1)][0], 'arrow_right', classes='floatl fggray', styles='padding-left: 8px')))
                __M_writer('\n')
            for (title, href) in bd:
                __M_writer('                <a class="ml10" href="')
                __M_writer(escape(href))
                __M_writer('">')
                __M_writer(escape(title))
                __M_writer('</a>\n')

            __M_writer('            &ensp;\n        </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bd_script(context):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        getattr = context.get('getattr', UNDEFINED)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <script src="/zdojo/release/dijit/dijit.js" type="text/javascript"></script>\n    <script src="/zdojo/release/dojox/grid/DataGrid.js" type="text/javascript"></script>\n\n    <script src="/zdojo/zlib.js" type="text/javascript"></script>\n    <script src="/zdojo/zwidgets.js" type="text/javascript"></script>\n\n')
        __M_writer('    <script src="/jquery-1.4.2.min.js" type="text/javascript"></script>\n    <script src="/highcharts/highcharts.js" type="text/javascript"></script>\n    <script src="/highcharts/scripts.js" type="text/javascript"></script>\n    <script src="/zhighcharts.js" type="text/javascript"></script>\n    <!--[if IE]>\n        <script type="text/javascript" src="/highcharts/excanvas.compiled.js"></script>\n    <![endif]-->\n\n')
        if h.webanalytics and not getattr(c, 'skipga', False):
            __M_writer('        ')
            __M_writer(h.webanalytics)
            __M_writer('\n')
        __M_writer('\n    <script type="text/javascript">\n        // Common initialization routine\n        function init_zeta() {\n            dojo.subscribe( \'flash\', null, flashmsghandler );\n        }\n\n        // Initialize quick-links\n        function qlinks_menu() {\n            var qlMenu;\n            var tgtnodes = dojo.query( \'div#metanav span[name=quick-links]\' )[0];\n            var quicklinks = ')
        __M_writer(h.json.dumps(h.quicklinks))
        __M_writer(';\n\n            if ( tgtnodes ) {\n                pMenu = new zeta.Menu({\n                                targetNodes   :[ tgtnodes ],\n                                style: { fontSize: \'small\', width: \'6em\', color: \'blue\' }\n                        });\n                dojo.forEach( quicklinks,\n                    function( ql ) {\n                        purl = \'<a href="\' + ql[1] + \'">\' + ql[0] + \'</a>\'\n                        pMenu.addChild( new zeta.MenuItem(\n                                            { content: purl, class: \'fntbold hoverhighlight\' }\n                                      ));\n                    }\n                );\n            }\n        }\n\n        // Initialize project menu\n        function project_menu() {\n            var pMenu;\n            var tgtnodes = dojo.query( \'div#metanav span[name=myprojects]\' )[0];\n            var myprojects = ')
        __M_writer(h.json.dumps(h.projectlinks))
        __M_writer(';\n\n            if ( tgtnodes ) {\n                pMenu = new zeta.Menu({\n                                targetNodes   :[ tgtnodes ],\n                                style: { fontSize: \'small\',\n                                         color: \'blue\',\n                                       }\n                        });\n                pMenu.addChild(\n                    new zeta.MenuItem(\n                        { content: \'<a href="')
        __M_writer(escape(h.url_createprj))
        __M_writer('">New-project</a>\',\n                          class: \'hoverhighlight\' }\n                    )\n                );\n                pMenu.addChild( new zeta.MenuItem({ content: \'<hr></hr>\' }));\n                dojo.forEach( myprojects,\n                    function( p ) {\n                        purl = \'<a href="\' + p[1] + \'">\' + p[0] + \'</a>\'\n                        pMenu.addChild( new zeta.MenuItem(\n                                            { content: purl, class: \'fntbold hoverhighlight\' }\n                                      ));\n                    }\n                );\n                pMenu.addChild( new zeta.MenuItem({ content: \'<hr></hr>\' }));\n                pMenu.addChild( new zeta.MenuItem(\n                                    { content: \'<a href="')
        __M_writer(escape(h.url_projindex))
        __M_writer('">List-all</a>\',\n                                      class: \'hoverhighlight\'\n                                    }\n                              ));\n            }\n        }\n\n        dojo.addOnLoad( init_zeta );\n        dojo.addOnLoad( qlinks_menu );\n        dojo.addOnLoad( project_menu );\n\n        // Handlers for other elements in derived files.\n        dojoaddOnLoad( \'pagebartooltip\' );\n        dojoaddOnLoad( \'contexttooltip\' );\n\n        // Handler for search box.\n        dojo.addOnLoad( function() {\n            dojo.forEach( dojo.query( "span[name=searchbox] input[type=text]" ),\n                function( n ) {\n                    dojo.toggleClass( n, \'fggray2\', true );\n                    dojo.connect( n, \'onfocus\',\n                                  function( e ) {\n                                      dojo.attr( n, \'helpstr\', n.value );\n                                      n.value = \'\';\n                                      dojo.toggleClass( n, \'fggray2\', false );\n                                  }\n                                );\n                    dojo.connect( n, \'onblur\',\n                                  function( e ) {\n                                      n.value = dojo.attr( n, \'helpstr\' );\n                                      dojo.toggleClass( n, \'fggray2\', true );\n                                  }\n                                );\n                }\n            );\n        });\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()