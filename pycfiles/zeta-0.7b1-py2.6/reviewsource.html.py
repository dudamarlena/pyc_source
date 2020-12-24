# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/projects/reviewsource.html.py
# Compiled at: 2010-07-12 03:42:26
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278920546.037784
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/projects/reviewsource.html'
_template_uri = '/derived/projects/reviewsource.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['reviewsource', 'revwsourceline', 'hd_links', 'hd_script', 'bd_body', 'hd_styles', 'bd_script']
page_tooltips = [
 [
  'Help',
  'Review comments can be added interactively while viewing the reviewed item.\nIf able to detect a previous version for reviewing file, you can find that\nmodified lines are color-highlighted to indicate the difference from previous\nversion. Color hightlighting are only indicative of changes made.'],
 [
  'Author',
  "<em>Author</em> can add comments, comment's nature and also\nreponsible for taking actions on all review comments."],
 [
  'Moderator',
  "<em>Moderator</em> can add comments, comment's nature and is responsible\nfor approving actions taken on review comments. Once all the comments are\napprove, the moderator can close the review."],
 [
  'Participant',
  '<em>Participants</em> can comment and reply to other paticipants\ncomment.'],
 [
  'Timeline',
  'Timeline gives a log of all updates done to Review(s).']]
import xml.etree.cElementTree as et
from pygments.formatters import HtmlFormatter

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
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n\n')
        __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_reviewsource(context):
    context.caller_stack._push_frame()
    try:
        capture = context.get('capture', UNDEFINED)
        c = context.get('c', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')
        h = context.get('h', UNDEFINED)
        forms = _mako_get_namespace(context, 'forms')
        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        closed = c.review.closed and 'strike' or ''
        __M_writer('\n    <div id="prjrevwsource" class="mr5">\n        <div class="pb2 posr" style="border-bottom : 1px solid gray">\n            <span class="fntbold ml5">')
        __M_writer(escape(c.cnt_comments))
        __M_writer('</span>\n            <span class="fntbold fggray">Comments</span> |\n            <span class="fntbold">')
        __M_writer(escape(c.cnt_pending))
        __M_writer('</span>\n            <span class="fntbold fgcrimson">Pending</span>\n            <span class="posa" style="right : 0px">\n                <span>[ <a href="')
        __M_writer(escape(h.url_review))
        __M_writer('">View-onlycomments</a> ]</span>\n            </span>\n        </div>\n        <div class="disptable w100">\n        <div class="disptrow">\n            <div class="disptcell vtop"\n                 style="width : 13%; border-right : 2px solid #f2f2f2;">\n                ')
        __M_writer(escape(elements.showpeople()))
        __M_writer('\n                <div class="mr5">\n                    <div name="rattachblk"></div>\n                </div>\n                <div class="bclear mr5">\n                    <div name="rtagblk"></div>\n                </div>\n            </div>\n            <div class="disptcell">\n                <h3 class="')
        __M_writer(escape(closed))
        __M_writer('" style="margin : 5px 0px 0px 10px">\n                    Review ')
        __M_writer(escape(c.review.id))
        __M_writer(' \n                    <span class="fggray">\n                    ( ')
        __M_writer(escape('%s, ver:%s' % (c.review.resource_url, c.review.version)))
        __M_writer(' )\n                    </span>\n                </h3>\n                <div class="pt10">\n                    <div id="creatercmt_cntnr" \n                         class="bclear dispnone ml10 mr10 mb10 pt3">\n')
        if c.revwcmtable:
            __M_writer('                        <div class="ml10 bgwhite br4" style="border: 1px dotted gray">\n                            ')
            __M_writer(escape(forms.form_creatercmt(c.authuser, c.project, c.review, h.suburl_creatercmt, c.naturenames)))
            __M_writer('\n                        </div>\n')
        __M_writer('                    </div>\n                    <div id="replyrcmt_cntnr" style="border: 1px dotted gray"\n                         class="dispnone ml10 mr10 w80">\n                        ')
        __M_writer(escape(forms.form_replyrcmt(c.authuser, c.project, c.review, h.suburl_replyrcmt)))
        __M_writer('\n                    </div>\n                    <div id="processrcmt_cntnr" style="border: 1px dotted gray"\n                         class="dispnone ml10 mr10 w80">\n                        ')
        __M_writer(escape(forms.form_processrcmt(c.authuser, c.project, c.review, h.suburl_processrcmt)))
        __M_writer('\n                    </div>\n                </div>\n                <div class="revwsource ml10">\n                    ')
        import re
        cont = ('\n').join([ l for l in c.revwsource ])
        conthtml = h.syntaxhl(cont, lexbyfile=c.review.resource_url)
        htmllines = re.search('<pre>((.|[\\r\\n])*)</pre>', conthtml).groups()[0].splitlines()
        lineno = 1
        bgcmtadd = c.revwcmtable and 'bgcmtadd' or ''
        __M_writer('\n                    <table class="highlight w100">\n')
        for l in htmllines:
            __M_writer('                        ')
            bg = lineno in c.cmtsatpos and 'bgrevwcmts' or ''
            if c.diffpri == None:
                lnobg = 'bgyellow1'
            elif lineno in c.diffpri:
                lnobg = 'bgyellow1'
            elif c.diffsec and lineno in c.diffsec:
                lnobg = 'bgred1'
            else:
                lnobg = 'bgaliceblue'
            __M_writer('\n                        <tr class="w100">\n                            <td class="')
            __M_writer(escape(bg))
            __M_writer(' hoverhighlight pointer p2 calign vmiddle"\n                                style="width: 17px; padding-left: 17px;">\n                            </td>\n                            <td class="')
            __M_writer(escape(bgcmtadd))
            __M_writer(' hoverhighlight pointer p2 calign vmiddle"\n                                style="width: 17px; padding-left: 17px;">\n                            </td>\n                            <td class="pl5 pr5 ralign ')
            __M_writer(escape(lnobg))
            __M_writer(' p2"\n                                style="border-right: 1px solid gray;\n                                       border-bottom: 1px solid gray;">\n                                ')
            __M_writer(escape(lineno))
            __M_writer('\n                            </td>\n                            <td class="pl5 pr5 pt2 pb2">\n                                <pre>')
            __M_writer(l)
            __M_writer('</pre>\n                                <div class="addcmt mb5 w100"></div>\n                                <div class="cmts"><div>\n                            </td>\n                        </tr>\n                        ')
            lineno += 1
            __M_writer('\n')

        __M_writer('                    </table>\n                </div>\n            </div>\n        </div>\n        </div>\n    </div>\n    <script type="text/javascript">\n    ')
        review_id = c.review and c.review.id or ''
        __M_writer('\n\n    w_rcontainers = {}\n    revwcmtable   = ')
        __M_writer(escape(c.revwcmtable and 'true' or 'false'))
        __M_writer("\n    function setup_reviewsource() {\n        var div_prjrevwsource   = dojo.byId( 'prjrevwsource' );\n\n        new zeta.Form({ formid : 'processrcmt' });\n\n        /* Attachments */\n        new zeta.Attachments(\n                { user: [ '")
        __M_writer(escape(str(c.authuser.id)))
        __M_writer("', '")
        __M_writer(escape(c.authuser.username))
        __M_writer("' ],\n                  id: 'revwattachblk',\n                  addform: [ 'addrevattachs', '")
        __M_writer(h.suburl_addrevattachs)
        __M_writer("' ],\n                  delform: [ 'delrevattachs', '")
        __M_writer(h.suburl_delrevattachs)
        __M_writer("' ],\n                  attachon: [ '")
        __M_writer(escape(str(review_id)))
        __M_writer("', 'review_id' ],\n                  editable: ")
        __M_writer(escape([0, 1][(c.att_editable == True)]))
        __M_writer(",\n                  url: '")
        __M_writer(h.url_revwattachments)
        __M_writer("',\n                  attachs: ")
        __M_writer(h.json.dumps(c.attachs))
        __M_writer(',\n                  clsdisplayitem: "dispblk"\n                }, dojo.query( "div[name=rattachblk]" )[0]\n            )\n\n        /* Tags */\n        new zeta.Tags({ user: [ \'')
        __M_writer(escape(str(c.authuser.id)))
        __M_writer("', '")
        __M_writer(escape(c.authuser.username))
        __M_writer("' ],\n                  id: 'revwtagblk',\n                  addform: [ 'addrevtags', '")
        __M_writer(h.suburl_addrevtags)
        __M_writer("' ],\n                  delform: [ 'delrevtags', '")
        __M_writer(h.suburl_delrevtags)
        __M_writer("' ],\n                  tagon: [ '")
        __M_writer(escape(str(review_id)))
        __M_writer("', 'review_id' ],\n                  editable: ")
        __M_writer(escape([0, 1][(c.tag_editable == True)]))
        __M_writer(",\n                  url: '")
        __M_writer(h.url_revwtags)
        __M_writer("',\n                  tags: ")
        __M_writer(h.json.dumps(c.tags))
        __M_writer('\n                }, dojo.query( "div[name=rtagblk]" )[0]\n            )\n\n        // For each review line.\n        var tr_lines   = dojo.query( \'.revwsource table tr\', div_prjrevwsource )\n        var crcntnr    = dojo.query( \'#creatercmt_cntnr\' )[0];\n        var rpcntnr    = dojo.query( \'#replyrcmt_cntnr\' )[0];\n        if( crcntnr ) {\n            crcntnr.n_trig = null;\n            crcntnr.parentNode.removeChild( crcntnr )\n            rpcntnr.parentNode.removeChild( rpcntnr );\n        }\n\n        function wipe_crcntnr() {\n            crcntnr.parentNode ? \n                crcntnr.parentNode.removeChild( crcntnr ) \n                : null;\n        }\n        function commentforpos( position, n_trig, n_tr, e ) {\n            if( dojo.hasClass( n_trig, \'bgcmtadd\' ) ) {\n                var i_pos   = dojo.query( \'input[name=position]\', form_creatercmt \n                                        )[0];\n                wipe_crcntnr();\n                dojo.place( crcntnr, n_tr.childNodes[7].childNodes[3], \'first\' )\n                dojo.toggleClass( crcntnr, \'dispnone\', false );\n                dojo.toggleClass( n_trig, \'bgcmtadd\', false ); \n                dojo.toggleClass( n_trig, \'bgcmtadd_hide\', true ); \n                i_pos.value = position;\n                crcntnr.n_trig = n_trig\n            } else if ( crcntnr ) {\n                wipe_crcntnr();\n                dojo.toggleClass( n_trig, \'bgcmtadd\', true ); \n                dojo.toggleClass( n_trig, \'bgcmtadd_hide\', false ); \n            }\n            dojo.stopEvent(e);\n        }\n        function onshow_cmts( position, n_tr, n_cmts ) {\n            if( w_rcontainers[position] ) {\n                w_rcontainers[position].ifrs_rcomments.store.close();\n                w_rcontainers[position].ifrs_rcomments.fetch();\n            } else {\n                make_ifrs_revwrcomments(\n                    \'')
        __M_writer(h.url_revwrcomments)
        __M_writer("' + '&position='+position )\n                w = new zeta.RCommentContainer({\n                    ifrs_rcomments : revwrcomments,\n                    rpform: form_replyrcmt,\n                    prform: form_processrcmt,\n                    rpcntnr: rpcntnr,\n                    ref_nature: ")
        __M_writer(capture(forms.select_revwnature, c.naturenames))
        __M_writer(',\n                    ref_action: ')
        __M_writer(capture(forms.select_revwaction, c.actionnames))
        __M_writer(',\n                    moderated: ')
        __M_writer(escape([0, 1][(c.revwmoderated == True)]))
        __M_writer(',\n                    authored: ')
        __M_writer(escape([0, 1][(c.revwauthored == True)]))
        __M_writer(',\n                    revwcmtable: ')
        __M_writer(escape([0, 1][(c.revwcmtable == True)]))
        __M_writer(",\n                    sortby: 'review_comment_id',\n                    identity: 'review_comment_id'\n                    }, n_cmts.childNodes[0] );\n                w_rcontainers[position] = w;\n            }\n        }\n        for( i=0 ; i < tr_lines.length ; i++ ) {\n            var n_tr      = tr_lines[i];\n            var n_cmticon = n_tr.childNodes[1]\n            var n_cmts    = n_tr.childNodes[7].childNodes[5]; \n            if( revwcmtable ) {\n                dojo.connect(\n                    n_tr.childNodes[3], 'onclick',\n                    dojo.partial( commentforpos, i+1, n_tr.childNodes[3], n_tr )\n                );\n            }\n\n            toggler( n_cmticon, n_cmts, \n                     n_cmticon.innerHTML, \n                     n_cmticon.innerHTML, true,\n                     dojo.partial( onshow_cmts, i+1, n_tr, n_cmts )\n                   );\n        }\n    }\n    </script>\n\n")
        return ''
    finally:
        context.caller_stack._pop_frame()

    return


def render_revwsourceline(context, position, line, cmtsatpos):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n')
        bg = position in cmtsatpos and 'bgrevwcmts' or ''
        esc = line and '' or '&ensp;'
        plus = c.revwcmtable and '+' or ''
        __M_writer('\n<tr><td class="hoverhighlight pointer"><div class="')
        __M_writer(escape(bg))
        __M_writer('">&ensp;</div></td><td class="hoverhighlight fgblue pointer fntbold p2">')
        __M_writer(escape(plus))
        __M_writer('</td><td class="fggray p2">')
        __M_writer(escape(position))
        __M_writer('</td><td class="p2"><div class="mb5" style="font-family: monospace, fixed;">')
        __M_writer(escape(line))
        __M_writer(esc)
        __M_writer('</div><div class="addcmt mb5"></div><div class="cmts"><div></div></div></td></tr>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_hd_links(context):
    context.caller_stack._push_frame()
    try:
        parent = context.get('parent', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        __M_writer(escape(parent.hd_links()))
        __M_writer('\n')
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
        elements = _mako_get_namespace(context, 'elements')

        def reviewsource():
            return render_reviewsource(context)

        h = context.get('h', UNDEFINED)
        forms = _mako_get_namespace(context, 'forms')
        __M_writer = context.writer()
        __M_writer('\n    ')
        sel_revw = capture(forms.form_selectrevw, c.authuser, c.revwlist, c.review and c.review.resource_url or '')
        sel_rset = capture(forms.form_selectrset, c.authuser, c.rsetlist, c.reviewset and c.reviewset.name or '')
        fav = capture(elements.favoriteicon, 'favrevw')
        searchbox = capture(forms.form_searchbox, c.authuser, 'searchreview', 'Search-review', h.suburl_search, c.searchfaces)
        if c.revweditable:
            newrevw = '<span class="ml10 fwnormal fntsmall">' + '<a href="' + h.url_revwcreate + '">Create</a>' + '</span>'
        else:
            newrevw = ''
        revwsets = '<span class="ml10 fwnormal fntsmall">                     <a href="%s" title="List of reviews sets">                     Reviewsets</a></span>' % h.url_reviewsets
        charts = capture(elements.iconlink, h.url_revwcharts, 'barchart', title='Review analytics')
        tline = capture(elements.iconlink, h.url_revwtimeline, 'timeline', title='Timeline')
        __M_writer('\n    ')
        __M_writer(escape(elements.mainnav()))
        __M_writer('\n    ')
        __M_writer(escape(elements.contextnav([fav, searchbox, sel_revw, sel_rset,
         newrevw, revwsets], rspans=[charts, tline], tooltips=page_tooltips)))
        __M_writer('\n\n    <div id="bdy" class="w100">\n')
        if c.authusername == 'anonymous' or not c.userpanes:
            __M_writer('        <div class="fullpanel1">\n')
        else:
            __M_writer('        <div class="panel1">\n')
        __M_writer('            <div>\n')
        if c.authorized:
            __M_writer('                    ')
            __M_writer(escape(forms.form_revwfav(c.authuser, c.project, c.review, h.suburl_revwfav, c.isuserfavorite and 'delfavuser' or 'addfavuser')))
            __M_writer('\n')
        __M_writer('                ')
        __M_writer(escape(reviewsource()))
        __M_writer('\n            </div>\n        </div> \n')
        if c.authusername != 'anonymous' and c.userpanes:
            __M_writer('        <div class="panel2">')
            __M_writer(escape(elements.user_panes(c.userpanes)))
            __M_writer('</div>\n')
        __M_writer('    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_hd_styles(context):
    context.caller_stack._push_frame()
    try:
        parent = context.get('parent', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        __M_writer(escape(parent.hd_styles()))
        __M_writer('\n    <style type="text/css">\n        ')
        __M_writer(escape(HtmlFormatter().get_style_defs('.highlight')))
        __M_writer('\n')
        __M_writer('        .highlighttable td.linenos { padding : 3px }\n        .highlighttable td.code { padding : 3px }\n    </style>\n')
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
        __M_writer('\n\n    <script type="text/javascript">\n        dojo.addOnLoad( function() {\n            var n_select = dojo.query( \'#selectrevw\' )[0];\n            n_select ? select_goto( n_select ) : null;\n        });\n        dojo.addOnLoad( setup_participants );\n        dojo.addOnLoad( setup_reviewsource );\n\n        dojo.addOnLoad( setup_userpanes );\n        dojo.addOnLoad( adjust_upheight );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()