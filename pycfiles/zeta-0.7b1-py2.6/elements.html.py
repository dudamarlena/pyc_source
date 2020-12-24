# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/component/elements.html.py
# Compiled at: 2010-07-09 03:04:59
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278659099.91111
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/component/elements.html'
_template_uri = '/component/elements.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['attachments', 'diff_row', 'captiontextarea', 'captcha', 'delete_row', 'titleindex', 'helpboard', 'pagebar', 'attachdownloads', 'timeline_view', 'favoriteicon', 'showpeople', 'replace_row', 'timeline', 'mainnav', 'tag_spans', 'lictable1', 'attach_spans', 'flashmessages', 'equal_row', 'insert_row', 'difftable', 'user_panes', 'iconize', 'userdetails', 'contextnav', 'iconlink']
iconmap = {'addattach': '/zetaicons/add_attach.png', 
   'addtag': '/zetaicons/tag_green_add.png', 
   'attach': '/zetaicons/attach.png', 
   'project': '/zetaicons/project.png', 
   'projects': '/zetaicons/projects.png', 
   'relation': '/zetaicons/user_link.png', 
   'tag': '/zetaicons/tag_green.png', 
   'team': '/zetaicons/group_link.png', 
   'users': '/zetaicons/group.png', 
   'user': '/zetaicons/user.png', 
   'trash': '/zetaicons/bin.png', 
   'refresh': '/zetaicons/arrow_refresh.png', 
   'servergo': '/zetaicons/server_go.png', 
   'plus_exp': '/zetaicons/plus_exp.gif', 
   'arrow_right': '/zetaicons/arrow_right.png', 
   'timeline': '/zetaicons/time.png', 
   'tooltips': '/zetaicons/tooltips.png', 
   'barchart': '/zetaicons/chart_bar.png', 
   'commentadd': '/zetaicons/comment_add.png'}

def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]


def _mako_generate_namespaces(context):
    ns = runtime.Namespace('forms', context._clean_inheritance_tokens(), templateuri='/component/forms.html', callables=None, calling_uri=_template_uri, module=None)
    context.namespaces[(__name__, 'forms')] = ns
    return


def render_body(context, **pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer('\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n')
        __M_writer('\n\n')
        __M_writer('\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_attachments(context, u, attachments, editable, attachassc=None, aa=None, ua=None, la=None, pa=None, ta=None, ra=None, wa=None):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        sorted = context.get('sorted', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        keys = sorted(attachments.keys())
        __M_writer('\n    <div id="attachments w100" class="br4" style="border: 3px solid #B3CFB3;">\n    <table class="w100">\n        <tr class="bggrn2">\n            <td class="p3 fntbold" style="width: 2%;">id</td>\n            <td class="p3 fntbold" style="width: 20%;">filename</td>\n            <td class="p3 fntbold" style="">summary</td>\n            <td class="p3 fntbold" style="width: 20%;">tags</td>\n            <td class="p3 fntbold" style="width: 7%;">uploader</td>\n')
        if attachassc:
            __M_writer('            <td class="p3 fntbold" style="width: 10em;">attached-to</td>\n')
        __M_writer('            <td class="p3 fntbold" style="width: 8%;">downloads</td>\n        </tr>\n')
        for k in keys:
            __M_writer('            ')
            count = 0
            __M_writer('\n            <tr class="fntitalic bggray2"><td class="p5 fntbold" colspan="7">')
            __M_writer(escape(k))
            __M_writer('</td></tr>\n')
            for att in attachments[k]:
                __M_writer('                ')
                createdon = att[4] and h.utc_2_usertz(att[4], u.timezone).strftime('%a, %b %d, %Y')
                count += 1
                bgrnd = count % 2 == 0 and 'bggray1' or ''
                if attachassc:
                    items = [ h.attachassc2link(item, aa, ua, la, pa, ta, ra, wa) for item in attachassc.get(att[0], []) ]
                else:
                    items = []
                __M_writer('\n                <tr class="')
                __M_writer(escape(bgrnd))
                __M_writer('">\n                    <td class="p5 fggray" style="width: 2%">\n                        <a href="')
                __M_writer(escape(att[7]))
                __M_writer('">')
                __M_writer(escape(att[0]))
                __M_writer('</a>\n                    </td>\n                    <td class="p5 fggray" style="width: 15%">')
                __M_writer(escape(att[1]))
                __M_writer('</td>\n                    <td class="p5" style="">\n                        <span name="summary" attid="')
                __M_writer(escape(att[0]))
                __M_writer('" class="inedit">')
                __M_writer(escape(att[2]))
                __M_writer('</span>\n                    </td>\n                    <td class="p5" style="width: 20%;">\n                        <span name="tags" attid="')
                __M_writer(escape(att[0]))
                __M_writer('" class="inedit">')
                __M_writer(escape(att[6]))
                __M_writer('</span>\n                    </td>\n                    <td class="p5 fggray" style="width: 5%;">\n                        <a href="')
                __M_writer(escape(h.url_foruser(att[5])))
                __M_writer('">')
                __M_writer(escape(att[5]))
                __M_writer('</a>\n                    </td>\n')
                if attachassc:
                    __M_writer('                    <td class="p5 fggray" style="width: 10em;">\n')
                    for (text, href) in items:
                        __M_writer('                            <div class="pl10"><a href="')
                        __M_writer(escape(href))
                        __M_writer('">')
                        __M_writer(escape(text))
                        __M_writer('</a></div>\n')

                    __M_writer('                    </td>\n')
                __M_writer('                    <td class="p5 fggray" style="width: 8%;">')
                __M_writer(escape(att[3]))
                __M_writer('</td>\n                </tr>\n')

        __M_writer('    </table>\n    </div>\n\n    <script type="text/javascript">\n        function editable_attachments() {\n            // Setup forms\n            new zeta.Form({ normalsub: true, formid: \'attachssummary\' });\n            new zeta.Form({ normalsub: true, formid: \'attachstags\' });\n\n            var inlines = dojo.query( \'span.inedit\' );\n\n            function inline_onchange( attid, formnode, field, value ) {\n                dojo.query( \'input[name=\' + field + \']\', formnode \n                          )[0].value = value;\n                dojo.query( \'input[name=attachment_id]\', formnode )[0].value = attid;\n                submitform( formnode );\n            }\n            dojo.forEach(\n                inlines,\n                function(item) {\n                    var name  = dojo.attr( item, \'name\' );\n                    var attid = dojo.attr( item, \'attid\' )   \n                    if ( name == \'summary\' ) {\n                        new dijit.InlineEditBox({\n                            editor: "dijit.form.TextBox",\n                            onChange: dojo.partial(\n                                        inline_onchange, attid, form_attachssummary, \'summary\' \n                                      ),\n                        }, item )        \n                    } else if ( name == \'tags\' ) {\n                        new dijit.InlineEditBox({\n                            editor: "dijit.form.TextBox",\n                            onChange: dojo.partial(\n                                        inline_onchange, attid, form_attachstags, \'tags\'\n                                      )\n                        }, item )        \n                    }\n                }\n            );\n\n        }\n        function setup_attachments() {\n            var editable = ')
        __M_writer(editable and 'true' or 'false')
        __M_writer('\n            if( editable ) {\n                editable_attachments()\n            }\n        }\n        dojo.addOnLoad( setup_attachments );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_diff_row(context, col1, col2, col3, cls):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n    <tr class="')
        __M_writer(escape(cls))
        __M_writer('">\n        <td class="oldver ')
        __M_writer(escape(cls))
        __M_writer('">')
        __M_writer(escape(col1))
        __M_writer('</td>\n        <td class="newver ')
        __M_writer(escape(cls))
        __M_writer('">')
        __M_writer(escape(col2))
        __M_writer('</td>\n        <td class="verdiff ')
        __M_writer(escape(cls))
        __M_writer('">')
        __M_writer(escape(col3))
        __M_writer('</td>\n    </tr>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_captiontextarea(context, text=''):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n    <div class="w100 mb5 fntitalic fntbold fggray">\n        ')
        __M_writer(escape(text))
        __M_writer('\n        <a href="/help/zwiki/ZWiki">Zwiki reference</a>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_captcha(context, url):
    context.caller_stack._push_frame()
    try:
        forms = _mako_get_namespace(context, 'forms')
        __M_writer = context.writer()
        __M_writer('\n    <div class="ftbox">\n        ')
        __M_writer(escape(forms.input_text(name='captcha', id='captcha')))
        __M_writer('\n        <img class="vbottom ml20" src="')
        __M_writer(escape(url))
        __M_writer('"></img>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_delete_row(context, tup, flines, tlines):
    context.caller_stack._push_frame()
    try:
        range = context.get('range', UNDEFINED)

        def diff_row(col1, col2, col3, cls):
            return render_diff_row(context, col1, col2, col3, cls)

        __M_writer = context.writer()
        __M_writer('\n')
        for ln in range(tup[1], tup[2]):
            __M_writer('        ')
            __M_writer(escape(diff_row(ln + 1, '', flines[ln], 'diffdelete')))
            __M_writer('\n')

        return ''
    finally:
        context.caller_stack._pop_frame()


def render_titleindex(context, items, url_for):
    context.caller_stack._push_frame()
    try:
        map = context.get('map', UNDEFINED)
        len = context.get('len', UNDEFINED)
        filter = context.get('filter', UNDEFINED)
        p = context.get('p', UNDEFINED)
        range = context.get('range', UNDEFINED)
        r = context.get('r', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        curdir = []
        __M_writer('\n    <ul class="ml50">\n')
        for (path, text) in items:
            __M_writer('        ')
            parts = filter(None, path.split('/'))
            render = map(lambda r, p: None if r == p else p, curdir, parts)
            while render:
                if render[(-1)] == None:
                    render.pop(-1)
                else:
                    break

            curdir = parts
            ndirs = render and len(render) - 1 or 0
            __M_writer('\n')
            for i in range(ndirs):
                if render[i]:
                    __M_writer('                <li class="fntbold" style="margin-left: ')
                    __M_writer(escape(i * 20))
                    __M_writer('px">\n                    <b>')
                    __M_writer(escape(render[i]))
                    __M_writer('</b>\n                </li>\n')

            __M_writer('        <li class="fntbold" style="margin-left: ')
            __M_writer(escape(ndirs * 20))
            __M_writer('px">\n            <a href="')
            __M_writer(escape(url_for(path)))
            __M_writer('">')
            __M_writer(escape(render[(-1)]))
            __M_writer('</a>\n        </li>\n')

        __M_writer('    </ul>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()

    return


def render_helpboard(context, help='', classes='', styles=''):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n    <div class="helpbrd bgblue1 p10 ')
        __M_writer(escape(classes))
        __M_writer(' br10"\n         style="font-family: Helvetica, sans-serif;\n                ')
        __M_writer(escape(styles))
        __M_writer('">\n        ')
        __M_writer(help)
        __M_writer('\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_pagebar(context, text, spans=[], rspans=[], tooltips=[], *args):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)

        def iconize(spantext, iconname, span_name='', classes='', styles='', title=''):
            return render_iconize(context, spantext, iconname, span_name, classes, styles, title)

        __M_writer = context.writer()
        __M_writer('\n    <div class="pbar fnt83 brtl5 brtr5" \n         style="border-top: 1px solid green; border-left: 1px solid green;\n                border-right: 1px solid green;">\n        <div class="bggrn1 pl1 pr1 pl5 pb5" style="height: 20px">\n')
        if tooltips:
            __M_writer('                <div id=\'trgr_tooltips\' title="Tips on how to use this page" \n                     class="posr floatr mr10 fntnormal fgblue pointer"\n                     style="margin-top: 5px;">\n                    ')
            __M_writer(escape(iconize('', 'tooltips', styles='height: 16px;')))
            __M_writer('\n                </div>\n')
        else:
            __M_writer('                <div id=\'trgr_tooltips\' title="Tips on how to use this page" \n                     class="posr floatr mr20 fntnormal fggray">\n                </div>\n')
        __M_writer('            <div class="floatr pr10" style="margin-top: 4px">\n')
        for span in rspans:
            __M_writer('                ')
            __M_writer(span)
            __M_writer('\n')

        __M_writer('            </div>\n            <div class="floatl" style="margin-top: 4px">')
        __M_writer(escape(text))
        __M_writer('</div>\n            <div class="floatl pl5">\n')
        for span in spans:
            __M_writer('                    ')
            __M_writer(span)
            __M_writer('\n')

        __M_writer('            </div>\n        </div>\n')
        for div_spans in args:
            __M_writer('        <div class="bggrn1 ml1 mr1 pl5 pb2">\n')
            for span in div_spans:
                __M_writer('                ')
                __M_writer(span)
                __M_writer('\n')

            __M_writer('        </div>\n')

        __M_writer('    </div>\n')
        if tooltips:
            __M_writer('        <div id="cont_tooltips"></div>\n')
        __M_writer('\n    <script type="text/javascript">\n        function pagebartooltip() {\n            var n_cont = dojo.byId( \'cont_tooltips\' );\n            var n_trgr = dojo.byId( \'trgr_tooltips\' );\n            if( n_cont ) {\n                new zeta.ToolTips({\n                    n_tooltip : n_trgr,\n                    tooltips: ')
        __M_writer(h.json.dumps(tooltips))
        __M_writer('\n                }, n_cont )\n            }\n        };\n    </script>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_attachdownloads(context, u, attachments):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        count = 0
        values = []
        [ values.extend(v) for v in attachments.values() ]
        __M_writer('\n    <div id="attachments w100" class="br4" style="border: 3px solid #B3CFB3;">\n    <table class="w100">\n        <tr class="bggrn2">\n            <td class="p3 fntbold" style="width: 21%;">filename</td>\n            <td class="p3 fntbold" style="">summary</td>\n            <td class="p3 fntbold" style="width: 7%;">uploader</td>\n            <td class="p3 fntbold" style="width: 10em;;">created-on</td>\n            <td class="p3 fntbold" style="width: 8%;">downloads</td>\n        </tr>\n')
        for att in values:
            __M_writer('            ')
            createdon = att[4] and h.utc_2_usertz(att[4], u.timezone).strftime('%a, %b %d, %Y')
            count += 1
            bgrnd = count % 2 == 0 and 'bggray1' or ''
            __M_writer('\n            <tr class="')
            __M_writer(escape(bgrnd))
            __M_writer('">\n                <td class="p5 fggray" style="width: 15%">\n                    <a href="')
            __M_writer(escape(h.url_for(h.r_attachdownl, id=att[0])))
            __M_writer('">')
            __M_writer(escape(att[1]))
            __M_writer('</a>\n                </td>\n                <td class="p5" style="">\n                    <span name="summary" attid="')
            __M_writer(escape(att[0]))
            __M_writer('" class="inedit">')
            __M_writer(escape(att[2]))
            __M_writer('</span>\n                </td>\n                <td class="p5 fggray" style="width: 5%;">\n                    <a href="')
            __M_writer(escape(h.url_foruser(att[5])))
            __M_writer('">')
            __M_writer(escape(att[5]))
            __M_writer('</a>\n                </td>\n                <td class="p5 fggray" style="width: 10em;">')
            __M_writer(escape(createdon))
            __M_writer('</td>\n                <td class="p5 fggray" style="width: 8%;">')
            __M_writer(escape(att[3]))
            __M_writer('</td>\n            </tr>\n')
            if att[6]:
                __M_writer('            <tr class="fntitalic ')
                __M_writer(escape(bgrnd))
                __M_writer('">\n                <td class="pl5 fntitalic fggreen" colspan="7">\n                    <span>( ')
                __M_writer(escape(att[6]))
                __M_writer(' )</span>\n                </td>\n            </tr>\n')

        __M_writer('    </table>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_timeline_view(context, logs, fromoff, tooff, links, chartid=''):
    context.caller_stack._push_frame()
    try:
        x = context.get('x', UNDEFINED)
        h = context.get('h', UNDEFINED)
        sorted = context.get('sorted', UNDEFINED)

        def timeline(ondt, log):
            return render_timeline(context, ondt, log)

        __M_writer = context.writer()
        __M_writer('\n    ')
        if logs:
            lf = '<span class="fgred">%s</span>' % logs[0].created_on.strftime('%a, %b %d, %Y')
            lt = '<span class="fgred">%s</span>' % logs[(-1)].created_on.strftime('%a, %b %d, %Y')
            logwindow = 'Till %s from %s' % (lf, lt)
        else:
            logwindow = 'No logs'
        slices = h.timeslice(logs)
        slicedt = sorted(slices.keys(), key=lambda x: h.dt.datetime.strptime(x, '%a, %b %d %Y'), reverse=True)
        __M_writer('\n    <div class="timeline ml10 mr10">\n        <br/>\n        <div class="pb2" style="height : 1.5em; border-bottom : 2px solid gray;">\n            <div class="floatr">\n                <a class="rss" href="')
        __M_writer(escape(h.url_rssfeed))
        __M_writer('" rel="nofollow">RSS</a>\n\n')
        if links[0]:
            __M_writer('                    <span class="fntlarge fntbold"><a href="')
            __M_writer(escape(links[0]))
            __M_writer('">&#171;</a></span>\n')
        __M_writer('\n')
        if links[1]:
            __M_writer('                    <span class="fntlarge fntbold ml5"><a href="')
            __M_writer(escape(links[1]))
            __M_writer('">&#8249;</a></span>\n')
        __M_writer('\n                <span class="ml5">')
        __M_writer(escape(fromoff))
        __M_writer('-')
        __M_writer(escape(tooff))
        __M_writer('</span>\n\n')
        if links[2]:
            __M_writer('                    <span class="fntlarge fntbold ml5"><a href="')
            __M_writer(escape(links[2]))
            __M_writer('">&#8250;</a></span>\n')
        __M_writer('\n            </div>\n            <span class="fntbold">')
        __M_writer(logwindow)
        __M_writer('</span>\n            <span name="expand" class="ml10 fgblue pointer">Expand</span>\n        </div>\n        <div class="pl5 pr5">\n')
        if chartid:
            __M_writer('                <div class="floatr p5 bgwhite">\n                    <div class="chartcntnr">\n                        <div id="')
            __M_writer(escape(chartid))
            __M_writer('" class="chart"\n                             style="width: 500px; height: 325px;">\n                        </div>\n                    </div>\n                </div>\n')
        for ondt in slicedt:
            __M_writer('                <ul class="w100">\n')
            for log in slices[ondt]:
                __M_writer('                    ')
                __M_writer(escape(timeline(ondt, log)))
                __M_writer('\n')

            __M_writer('                </ul>\n')

        __M_writer('        </div>\n        <br/>\n        <div class="bclear pb2" style="height : 1.5em; border-bottom : 2px solid gray;">\n            <div class="floatr" style="right : 0px;">\n')
        if links[0]:
            __M_writer('                    <span class="fntlarge fntbold"><a href="')
            __M_writer(escape(links[0]))
            __M_writer('">&#171;</a></span>\n')
        __M_writer('\n')
        if links[1]:
            __M_writer('                    <span class="fntlarge fntbold ml5"><a href="')
            __M_writer(escape(links[1]))
            __M_writer('">&#8249;</a></span>\n')
        __M_writer('\n                <span class="ml5">')
        __M_writer(escape(fromoff))
        __M_writer('-')
        __M_writer(escape(tooff))
        __M_writer('</span>\n\n')
        if links[2]:
            __M_writer('                    <span class="fntlarge fntbold ml5"><a href="')
            __M_writer(escape(links[2]))
            __M_writer('">&#8250;</a></span>\n')
        __M_writer('            </span>\n            <span class="fntbold">&ensp;</span>\n        </div>\n    </div>\n\n    <script type="text/javascript">\n        function logmsg( n, what ) {\n            if( what == \'expand\' ) {\n                dojo.toggleClass( n, \'dispblk\', true );\n                dojo.toggleClass( n, \'wspre\', true );\n                dojo.toggleClass( n, \'ml50\', true );\n            } else {\n                dojo.toggleClass( n, \'dispblk\', false );\n                dojo.toggleClass( n, \'wspre\', false );\n                dojo.toggleClass( n, \'ml50\', false );\n            }\n        }\n\n        function pntr_onclick( n_logmsg, e ) {\n            dojo.hasClass( n_logmsg, \'dispblk\' ) ? \n                logmsg( n_logmsg, \'summary\' ) : logmsg( n_logmsg, \'expand\' ) ;\n            dojo.stopEvent(e);\n        }\n        function setup_timeline() {\n            dojo.setObject( \'span_expand\', dojo.query( \'span[name=expand]\' )[0] );\n            dojo.forEach(\n                dojo.query( \'.tlog\' ),\n                function( n ) {\n                    var n_pntr   = dojo.query( \'span[name=interface]\', n )[0]\n                    var n_logmsg = dojo.query( \'span[name=logmsg]\', n )[0]\n                    dojo.connect(\n                        n_pntr, \'onclick\',\n                        dojo.partial( pntr_onclick, n_logmsg )\n                    );\n                }\n            );\n            dojo.connect(\n                span_expand, \'onclick\', \n                function(e) {\n                    dojo.forEach(\n                        dojo.query( \'span[name=logmsg]\' ),\n                        function( n ) {\n                            if( span_expand.innerHTML == \'Summary\' ) {\n                                logmsg( n, \'summary\' ) \n                            } else {\n                                logmsg( n, \'expand\') ;\n                            }\n                        }\n                    );\n                    span_expand.innerHTML = span_expand.innerHTML == \'Expand\' ?\n                                                \'Summary\' : \'Expand\'\n                    dojo.stopEvent(e);\n                }\n            );\n        }\n        dojo.addOnLoad( setup_timeline );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_favoriteicon(context, name):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n    <span name="')
        __M_writer(escape(name))
        __M_writer('" title="add or delete as your favorite"\n          class="favdeselected ml5 pointer fntlarge"></span>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showpeople(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        set = context.get('set', UNDEFINED)
        h = context.get('h', UNDEFINED)
        list = context.get('list', UNDEFINED)
        forms = _mako_get_namespace(context, 'forms')
        sorted = context.get('sorted', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        participants = [ u.username for u in c.review.participants ]
        x_participants = sorted(list(set(c.usernames).difference(set(participants))))
        'admin' in x_participants and x_participants.remove('admin')
        'anonymous' in x_participants and x_participants.remove('anonymous')
        __M_writer('\n    <div id="revwinfo">\n        <div class="fggray fntbold pt5 pb5 ml10"> Author </div>\n')
        if c.revweditable:
            __M_writer('            <div class="ml20">\n            ')
            __M_writer(escape(forms.form_revwauthor(c.authuser, c.project, c.review, h.suburl_revwauthor, c.projusers)))
            __M_writer('\n            </div>\n')
        else:
            __M_writer('            ')
            authorname = c.review.author and c.review.author.username or '-'
            __M_writer('\n            <div class="ml20">\n')
            if c.review.author:
                __M_writer('                <a href="')
                __M_writer(escape(h.url_foruser(authorname)))
                __M_writer('">')
                __M_writer(escape(authorname))
                __M_writer('</a>\n')
            else:
                __M_writer('                <span>')
                __M_writer(escape(authorname))
                __M_writer('</span>\n')
            __M_writer('            </div>\n')
        __M_writer('        <hr></hr>\n        <div class="fggray fntbold pt5 pb5 ml10"> Moderator </div>\n')
        if c.revweditable:
            __M_writer('            <div class="ml20">\n            ')
            __M_writer(escape(forms.form_revwmoderator(c.authuser, c.project, c.review, h.suburl_revwmoderator, c.projusers)))
            __M_writer('\n            </div>\n')
        else:
            __M_writer('            ')
            moderatorname = c.review.moderator and c.review.moderator.username or '-'
            __M_writer('\n            <div class="ml20">\n')
            if c.review.moderator:
                __M_writer('                <a href="')
                __M_writer(escape(h.url_foruser(moderatorname)))
                __M_writer('">')
                __M_writer(escape(moderatorname))
                __M_writer('</a>\n')
            else:
                __M_writer('                <span>')
                __M_writer(escape(moderatorname))
                __M_writer('</span>\n')
            __M_writer('            </div>\n')
        if c.authuser == c.review.moderator:
            __M_writer('            <div id="revwclosed" class="fgblue pointer ml10 mt5 mb5">\n                ')
            __M_writer(escape(forms.form_closerev(c.authuser, c.project, c.review, h.suburl_closerev)))
            __M_writer('\n            </div>\n')
        __M_writer('        <hr></hr>\n        <div class="fggray fntbold pt5 pb5 ml10"> Participants </div>\n')
        if c.revweditable:
            __M_writer('            <div class="ml20">\n                ')
            __M_writer(escape(forms.form_addparts(c.authuser, c.project, c.review, h.suburl_addparts, x_participants)))
            __M_writer('\n            </div>\n')
        __M_writer('        <div id="listparts" class="ml20 p5" >\n')
        for username in sorted([ u.username for u in c.review.participants ]):
            __M_writer('        <div>\n')
            if c.revweditable:
                __M_writer('            <span username="')
                __M_writer(escape(username))
                __M_writer('"\n                  class="closeparticipant mr5 fgred pointer">x</span>\n')
            __M_writer('            <a href="')
            __M_writer(escape(h.url_foruser(username)))
            __M_writer('">')
            __M_writer(escape(username))
            __M_writer('</a>\n        </div>\n')

        __M_writer('        </div>\n        ')
        __M_writer(escape(forms.form_delparts(c.authuser, c.project, c.review, h.suburl_delparts)))
        __M_writer('\n    </div>\n    <script type="text/javascript">\n        function publish_delpart( username, e ) {\n            dojo.publish( \'delparticipant\', [ username ] );\n            dojo.destroy(\n                dojo.query( \'span[username=\'+username+\']\', dojo.byId( \'listparts\' ) \n                          )[0].parentNode\n            );\n            dojo.stopEvent(e);\n        }\n        function setup_participants() {\n\n            dojoaddOnLoad( \'initform_revwauthor\' );\n            dojoaddOnLoad( \'initform_revwmoderator\' );\n            dojoaddOnLoad( \'initform_closerev\' );\n            dojoaddOnLoad( \'initform_addparts\' );\n            dojoaddOnLoad( \'initform_delparts\' );\n\n            var n_spans = dojo.query(\'div#revwinfo span.closeparticipant\');\n            dojo.forEach( n_spans,\n                function( n ) {\n                    dojo.connect(\n                        n, \'onclick\', \n                        dojo.partial( publish_delpart, dojo.attr( n, \'username\' ))\n                    );\n                }\n            );\n            dojo.subscribe( \n                \'insertparticipant\',\n                function( username ) {\n                    // Create the div\n                    var n_div = dojo.create( \'div\', {}, dojo.byId( \'listparts\' ), \'last\' );\n                    // interface to show and delete the participant.\n                    var n_x = dojo.create( \n                                \'span\', { username : username, innerHTML : \'x \',\n                                          class : "closeparticipant mr5 fgred pointer"\n                                        },\n                                n_div, \'last\'\n                              );\n                    dojo.connect( n_x, \'onclick\', \n                                  dojo.partial( publish_delpart, username ));\n                    dojo.create( \n                        \'a\', { href : url_foruser( username ), innerHTML : username },\n                        n_div, \'last\'\n                    );\n                }\n            );\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_replace_row(context, tup, flines, tlines):
    context.caller_stack._push_frame()
    try:
        range = context.get('range', UNDEFINED)

        def diff_row(col1, col2, col3, cls):
            return render_diff_row(context, col1, col2, col3, cls)

        __M_writer = context.writer()
        __M_writer('\n')
        for ln in range(tup[1], tup[2]):
            __M_writer('        ')
            __M_writer(escape(diff_row(ln + 1, '', flines[ln], 'diffreplace')))
            __M_writer('\n')

        for ln in range(tup[3], tup[4]):
            __M_writer('        ')
            __M_writer(escape(diff_row('', ln + 1, tlines[ln], 'diffreplace')))
            __M_writer('\n')

        return ''
    finally:
        context.caller_stack._pop_frame()


def render_timeline(context, ondt, log):
    context.caller_stack._push_frame()
    try:

        def iconize(spantext, iconname, span_name='', classes='', styles='', title=''):
            return render_iconize(context, spantext, iconname, span_name, classes, styles, title)

        __M_writer = context.writer()
        __M_writer('\n    <li class="tlog">\n        <div class="mt5 mb5 ml3 wsnowrap w100" style="overflow: hidden;">\n            <span class="hoverhighlight">\n                ')
        __M_writer(escape(iconize(ondt, 'plus_exp', span_name='interface', classes='pointer mr5', title='%s' % log.created_on)))
        __M_writer('\n            </span>\n            <span class="ml5">By ')
        __M_writer(log.userhtml)
        __M_writer('</span>\n            <span>in ')
        __M_writer(log.itemhtml)
        __M_writer('</span>\n            <span name="logmsg" class="ml10 fggray">')
        __M_writer(escape(log.log))
        __M_writer('</span>\n        </div>\n    </li>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_mainnav(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <div id="mainnav" class="fnt83" >\n    <table cellspacing="0" cellpadding="0" border="0">\n        <tr>\n')
        for m in c.mainnavs:
            __M_writer('            <th>\n                <div class="curvy4 bggreen"></div>\n                <div class="curvy2 bggreen">\n                    <div class="')
            __M_writer(escape(m.tab))
            __M_writer(' ml2 mr2" style="height: 1px;" ></div>\n                </div>\n                <div class="curvy1 bggreen">\n                    <div class="')
            __M_writer(escape(m.tab))
            __M_writer(' mr1 ml1" style="height: 1px;"></div>\n                </div>\n                <div class="bggreen">\n                    <div class="')
            __M_writer(escape(m.tab))
            __M_writer(' mr1 ml1 pl10 pr10 pb2">\n                        <a class="nodec bb" href="')
            __M_writer(escape(m.href))
            __M_writer('" title="')
            __M_writer(escape(m.title))
            __M_writer('">')
            __M_writer(escape(m.text))
            __M_writer('</a>\n                    </div>\n                </div>\n            </th>\n            <td><div style="width: 10px;"</div></td>\n')

        __M_writer('        </tr>\n    </table>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_tag_spans(context, span_name, form_id, refreshurl):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n    <span class="m2" name="')
        __M_writer(escape(span_name))
        __M_writer('" form_id="')
        __M_writer(escape(form_id))
        __M_writer('" refreshurl="')
        __M_writer(escape(refreshurl))
        __M_writer('">\n    </span>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_lictable1(context, license, editable):
    context.caller_stack._push_frame()
    try:

        def iconize(spantext, iconname, span_name='', classes='', styles='', title=''):
            return render_iconize(context, spantext, iconname, span_name, classes, styles, title)

        __M_writer = context.writer()
        __M_writer('\n    <table class="w100" style="border-collapse : collapse;">\n        <tr>\n            <th class="calign">Id</th>\n            <th class="calign">License name</th>\n            <th class="calign">Projects</th>\n')
        if editable:
            __M_writer('                <th></th>\n')
        __M_writer('        </tr>\n')
        for l in license:
            __M_writer('            ')
            (id, licensename, licurl, editurl, rmurl) = l[:5]
            __M_writer('\n            <tr licensename="')
            __M_writer(escape(licensename))
            __M_writer('">\n                <td class="calign">')
            __M_writer(escape(id))
            __M_writer('</td>\n                <td class="calign"><a class="fntbold" href="')
            __M_writer(escape(licurl))
            __M_writer('">')
            __M_writer(escape(licensename))
            __M_writer('</a></td>\n                <td class="calign">\n')
            for (p, href) in l[5:]:
                __M_writer('                    <div><a href="')
                __M_writer(escape(href))
                __M_writer('">')
                __M_writer(escape(p))
                __M_writer('</a></div>\n')

            __M_writer('                </td>\n')
            if editable:
                __M_writer('                    <td class="calign">\n                        ')
                __M_writer(escape(iconize('', 'trash', span_name='rmlic', classes='fgblue pointer', title='Remove this license')))
                __M_writer('\n                    </td>\n')
            __M_writer('            </tr>\n')

        __M_writer('    </table>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_attach_spans(context, span_name, form_id, refreshurl):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n    <span class="m2" name="')
        __M_writer(escape(span_name))
        __M_writer('" form_id="')
        __M_writer(escape(form_id))
        __M_writer('" refreshurl="')
        __M_writer(escape(refreshurl))
        __M_writer('">\n    </span>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_flashmessages(context):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        allflash = [ '%s' % m for m in h.flash.pop_messages() ]
        errors = [ m.strip(h.ERROR_FLASH) for m in allflash if h.ERROR_FLASH in m ]
        messages = [ m.strip(h.MESSAGE_FLASH) for m in allflash if h.MESSAGE_FLASH in m ]
        allflash = errors + messages
        flashcls = errors and 'bgLSalmon' or messages and 'bgyellow' or ''
        if allflash:
            style = ''
        else:
            style = 'display: none;'
        __M_writer('\n    <div id="flashblk" class="calign m10 flashbind z100" style="')
        __M_writer(escape(style))
        __M_writer('">\n        <div class="flash curvy4 ')
        __M_writer(escape(flashcls))
        __M_writer('"></div>\n        <div class="flash curvy2 ')
        __M_writer(escape(flashcls))
        __M_writer('"></div>\n        <div class="flash curvy1 ')
        __M_writer(escape(flashcls))
        __M_writer('"></div>\n        <div id="flashmsg" class="flash fntsmall fwnormal ')
        __M_writer(escape(flashcls))
        __M_writer('">\n')
        for message in allflash:
            __M_writer('                ')
            __M_writer(escape(message))
            __M_writer('\n')

        __M_writer('        </div>\n        <div class="flash curvy1 ')
        __M_writer(escape(flashcls))
        __M_writer('"></div>\n        <div class="flash curvy2 ')
        __M_writer(escape(flashcls))
        __M_writer('"></div>\n        <div class="flash curvy4 ')
        __M_writer(escape(flashcls))
        __M_writer('"></div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_equal_row(context, tup, flines, tlines):
    context.caller_stack._push_frame()
    try:
        Exception = context.get('Exception', UNDEFINED)

        def diff_row(col1, col2, col3, cls):
            return render_diff_row(context, col1, col2, col3, cls)

        range = context.get('range', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        if tup[2] - tup[1] != tup[4] - tup[3]:
            raise Exception
        len = tup[2] - tup[1]
        __M_writer('\n')
        for ln in range(0, len):
            __M_writer('        ')
            __M_writer(escape(diff_row(tup[1] + ln + 1, tup[3] + ln + 1, flines[(tup[1] + ln)], 'diffequal')))
            __M_writer('\n')

        return ''
    finally:
        context.caller_stack._pop_frame()


def render_insert_row(context, tup, flines, tlines):
    context.caller_stack._push_frame()
    try:
        range = context.get('range', UNDEFINED)

        def diff_row(col1, col2, col3, cls):
            return render_diff_row(context, col1, col2, col3, cls)

        __M_writer = context.writer()
        __M_writer('\n')
        for ln in range(tup[3], tup[4]):
            __M_writer('        ')
            __M_writer(escape(diff_row('', ln + 1, tlines[ln], 'diffinsert')))
            __M_writer('\n')

        return ''
    finally:
        context.caller_stack._pop_frame()


def render_difftable(context, oldver, newver, flines, tlines):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)

        def diff_row(col1, col2, col3, cls):
            return render_diff_row(context, col1, col2, col3, cls)

        def replace_row(tup, flines, tlines):
            return render_replace_row(context, tup, flines, tlines)

        def equal_row(tup, flines, tlines):
            return render_equal_row(context, tup, flines, tlines)

        def delete_row(tup, flines, tlines):
            return render_delete_row(context, tup, flines, tlines)

        def insert_row(tup, flines, tlines):
            return render_insert_row(context, tup, flines, tlines)

        __M_writer = context.writer()
        __M_writer('\n    ')
        m = h.SequenceMatcher(None, flines, tlines)
        __M_writer('\n    <div class="difflegend mt10">\n        <dl>\n            <dt class="unmod"></dt><dd class="ml5">Un-modified</dd>\n            <dt class="del"></dt><dd class="ml5">Deleted</dd>\n            <dt class="ins"></dt><dd class="ml5">Inserted</dd>\n            <dt class="rep"></dt><dd class="ml5">Replaced</dd>\n        </dl>\n    </div>\n    <table class="zwdiff">\n        <thead><tr>\n            <th class="oldver">v')
        __M_writer(escape(oldver))
        __M_writer('</th>\n            <th class="newver">v')
        __M_writer(escape(newver))
        __M_writer('</th>\n            <th class="verdiff">Difference</th>\n        </tr></thead>\n')
        for cluster in m.get_grouped_opcodes():
            __M_writer('            ')
            __M_writer(escape(diff_row('...', '...', '', 'skip')))
            __M_writer('\n')
            for tup in cluster:
                if tup[0] == 'equal':
                    __M_writer('                    ')
                    __M_writer(escape(equal_row(tup, flines, tlines)))
                    __M_writer('\n')
                elif tup[0] == 'delete':
                    __M_writer('                    ')
                    __M_writer(escape(delete_row(tup, flines, tlines)))
                    __M_writer('\n')
                elif tup[0] == 'insert':
                    __M_writer('                    ')
                    __M_writer(escape(insert_row(tup, flines, tlines)))
                    __M_writer('\n')
                elif tup[0] == 'replace':
                    __M_writer('                    ')
                    __M_writer(escape(replace_row(tup, flines, tlines)))
                    __M_writer('\n')

        __M_writer('    </table>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()

    return


def render_user_panes(context, userpanes):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n    <table class="w100"><tr>\n    <td id="collapseup" style="width : 7px;" class="pointer vmiddle inactive">\n        <div style="cursor : default; width : 7px; background-color : transparent;">&#187;<div>\n    </td>\n    <td id="coluserpane">\n        <div class="pt5 w100 pl1pc">\n            <div class="fntsmall w100 ralign">\n                <span id="uprefresh" class="fgblue pointer">refresh</span>\n                &ensp;\n                <span id="upcolexp" class="fgblue pointer">collapse</span>\n            </div>\n\n            <div style="border : thin dotted black; padding : 0px 3px 0 3px; margin : 3px 0px 3px 0;"\n                 class="fntsmall 100" id="adduserpanes">\n')
        for up in userpanes:
            __M_writer('                    <span class="fgblue pointer" title="')
            __M_writer(escape(up))
            __M_writer('">')
            __M_writer(escape(up))
            __M_writer('&ensp;</span>\n')

        __M_writer('            </div>\n\n            <div id=\'userpanes\' class="w100">\n')
        for up in userpanes:
            __M_writer('                <div title="')
            __M_writer(escape(up))
            __M_writer('"></div>\n')

        __M_writer('            </div>\n        </div>\n    </td>\n    </table>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_iconize(context, spantext, iconname, span_name='', classes='', styles='', title=''):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n    ')
        iconfile = iconmap.get(iconname, '')
        __M_writer('\n    <span name="')
        __M_writer(escape(span_name))
        __M_writer('" class="pl18 ')
        __M_writer(escape(classes))
        __M_writer('" title="')
        __M_writer(escape(title))
        __M_writer('"\n          style="')
        __M_writer(escape(styles))
        __M_writer('; background : transparent url(')
        __M_writer(escape(iconfile))
        __M_writer(') no-repeat scroll 0;">\n        ')
        __M_writer(spantext)
        __M_writer('\n    </span>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_userdetails(context, user, userinfo, urlphoto):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        username = user.username
        __M_writer('\n    <div class="p5 w100">\n        <h3 style="border-bottom: 2px solid gray;">\n            ')
        __M_writer(escape('%s %s %s' % (userinfo.firstname, userinfo.middlename, userinfo.lastname)))
        __M_writer('\n        </h3>\n        <div class="disptable w100">\n        <div class="disptrow w100">\n            <div class="disptcell vtop" style="width: 30%">\n                <div class="p3">\n                    <div>')
        __M_writer(escape(user.emailid))
        __M_writer('</div>\n                    <div><span class="fntbold">timezone : </span>\n                        ')
        __M_writer(escape(user.timezone))
        __M_writer('\n                    </div>\n                </div>\n                <div class="mt20 p3">\n                    <span class="fntbold">Registered as :</span>\n                    <a href="')
        __M_writer(escape(h.url_foruser(username)))
        __M_writer('">')
        __M_writer(escape(username))
        __M_writer('</a>\n                </div>\n                <div class="p3">\n                    <span class="fntbold">Registered on :</span>\n                        ')
        __M_writer(escape(userinfo.created_on.strftime('%a, %b %d, %Y')))
        __M_writer('\n                </div>\n            </div>\n            <div class="disptcell vtop" style="width: 30%">\n                <em><b>Address : </b></em> <br></br>\n                <div class="ml20 mt10">\n                    ')
        __M_writer(escape(userinfo.addressline1))
        __M_writer(' <br></br>\n                    ')
        __M_writer(escape(userinfo.addressline2))
        __M_writer(' <br></br>\n                    ')
        __M_writer(escape(userinfo.city))
        __M_writer(' - ')
        __M_writer(escape(userinfo.pincode))
        __M_writer(' <br></br>\n                    ')
        __M_writer(escape(userinfo.state))
        __M_writer(' <br></br>\n                    ')
        __M_writer(escape(userinfo.country))
        __M_writer(' <br></br>\n                </div>\n            </div>\n            <div class="disptcell vtop ralign" style="width: 30%">\n')
        if urlphoto:
            __M_writer('                    <img style="max-width: 200px; max-height: 200px;" src="')
            __M_writer(escape(urlphoto))
            __M_writer('"></img>\n')
        __M_writer('            </div>\n        </div>\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_contextnav(context, spans=[], rspans=[], tooltips=[]):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)

        def iconize(spantext, iconname, span_name='', classes='', styles='', title=''):
            return render_iconize(context, spantext, iconname, span_name, classes, styles, title)

        __M_writer = context.writer()
        __M_writer('\n    <div class="bggrn1 ctxtnav pl5 fnt83 brtr5" style="height: 20px;">\n')
        if tooltips:
            __M_writer('            <div id=\'trgr_tooltips\' title="Tips on how to use this page" \n                 class="posr floatr mt2 mr10 fntsmall fgblue pointer">\n                ')
            __M_writer(escape(iconize('', 'tooltips')))
            __M_writer('\n            </div>\n')
        else:
            __M_writer('            <div id=\'trgr_tooltips\' title="Tips on how to use this page" \n                 class="posr floatr mr10 fntsmall fggray">\n            </div>\n')
        __M_writer('\n        <div class="floatr pr10">\n')
        for span in rspans:
            __M_writer('            ')
            __M_writer(span)
            __M_writer('\n')

        __M_writer('        </div>\n\n')
        for span in spans:
            __M_writer('            ')
            __M_writer(span)
            __M_writer('\n')

        __M_writer('    </div>\n')
        if tooltips:
            __M_writer('        <div id="cont_tooltips"></div>\n')
        __M_writer('\n    <script type="text/javascript">\n        function contexttooltip() {\n            var n_cont = dojo.byId( \'cont_tooltips\' );\n            var n_trgr = dojo.byId( \'trgr_tooltips\' );\n            if( n_cont ) {\n                new zeta.ToolTips({\n                    n_tooltip : n_trgr,\n                    tooltips: ')
        __M_writer(h.json.dumps(tooltips))
        __M_writer('\n                }, n_cont )\n            }\n        };\n    </script>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_iconlink(context, link, iconname, anchor_name='', classes='', styles='', title=''):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n    ')
        iconfile = iconmap.get(iconname, '')
        __M_writer('\n    <a name="')
        __M_writer(escape(anchor_name))
        __M_writer('" class="')
        __M_writer(escape(classes))
        __M_writer(' hoverhighlight br2 p3" title="')
        __M_writer(escape(title))
        __M_writer('" \n       style="')
        __M_writer(escape(styles))
        __M_writer(';" href="')
        __M_writer(escape(link))
        __M_writer('" >\n        <img src="')
        __M_writer(escape(iconfile))
        __M_writer('" class="vmiddle"></img></a>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()