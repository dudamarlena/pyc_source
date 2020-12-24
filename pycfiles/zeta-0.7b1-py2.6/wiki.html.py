# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/projects/wiki.html.py
# Compiled at: 2010-07-10 01:41:43
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278740503.520597
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/projects/wiki.html'
_template_uri = '/derived/projects/wiki.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['bd_body', 'hd_links', 'show_wikipage', 'hd_script', 'wiki_talkpage', 'wiki_edit', 'wiki_diff', 'bd_script', 'wiki_history']
page_tooltips = [
 [
  'Help',
  'Each wiki page is rendered with html translated wiki document and gives simple\nstatistical details for the page. Download a wiki page as text, pdf, html or\nps file.\n'],
 [
  'Comments',
  'Discussions on wiki document'],
 [
  'History',
  'List of previous versions of a wiki page and color coded differences\nbetween them.\n'],
 [
  'Attachments',
  'Upload attachments by clicking on the iconized title. Clicking on the\nsame once again will hide it. Delete attachments by clicking on the cross-wire.\nUpload any number of files.\n<br/>\nEvery attached file, will have its "id" in paranthesis. Use the id value when\nrefering to the attachment.\n'],
 [
  'Tags',
  'Tag a wiki page by clicking on the iconized title. Delete tags by clicking\non the cross-wire. Tag names should be 2 or more characters.\n'],
 [
  'Markups',
  '\n<table style="border-collapse: separate; border-spacing: 5px">\n<tr>\n<td>Text-Markup </td>\n<td>\n    <div class="disptrow">\n    <div class="disptcell">\n        &ensp;&ensp;\'\' <b>bold</b> \'\' &ensp;&ensp;// <em>italic</em> //\n        &ensp;&ensp;__ <u>underline</u> __\n        &ensp;&ensp;^^ <sup>super-script</sup> ^^\n        &ensp;&ensp;,, <sub>super-script</sub> ,,\n        &ensp;&ensp;\'/ <b><em>bold-italic</em></b> \'/\n        &ensp;&ensp;\'_ <b><u>bold-underline</u></b> \'_\n    </div></div>\n    <div class="disptrow">\n    <div class="disptcell">\n        &ensp;&ensp;/_ <em><u>italic-underline</u></em> /_\n        &ensp;&ensp;\'/_ <b><em><u>super-script</u></em></b> \'/_\n        &ensp;&ensp;~? escape one character \n        &ensp;&ensp;\\\n escape newline \n        &ensp;&ensp;\\\\ line break\n    </div></div>\n</td>\n</tr>\n<tr>\n<td>Links and anchor </td>\n<td>\n    &ensp;&ensp;[[ href | text ]] &ensp;&ensp;[[ *href_in_newwindow | text ]]\n    &ensp;&ensp;[[ $anchor | text ]] &ensp;&ensp;[[ +image | text ]]\n</td>\n</tr>\n<tr>\n<td>Heading </td>\n<td>&ensp;&ensp;=, ==, ===, ====, =====, for upto five levels of sub-headings</td>\n</tr>\n<tr>\n<td>Horizontal-rule </td><td>&ensp;&ensp;----</td>\n</tr>\n<tr>\n<td>Block-Markup</td>\n    <div class="disptrow">\n    <div class="disptcell">&ensp;&ensp;*{1,5} for upto 5 levels of unordered list</div>\n    </div>\n    <div class="disptrow">\n    <div class="disptcell">&ensp;&ensp;#{1,5} for upto 5 levels of ordered list </div>\n    </div>\n    <div class="disptrow">\n    <div class="disptcell">\n        &ensp;&ensp;>{1,5} for upto 5 levels of block-quoted text.</div>\n    </div>\n</tr>\n</table>\n<br/>\nTo know more about macros, extensions, zetalinks and several other features\nvisit <a href="/help/zwiki/ZWiki">here</a>.\n'],
 [
  'Favorites',
  'Registered users can pick wikipage(s) as their favorite.'],
 [
  'Vote',
  'Registered users can up-vote or down-vote a wiki page.']]

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


def render_bd_body(context):
    context.caller_stack._push_frame()
    try:
        capture = context.get('capture', UNDEFINED)
        c = context.get('c', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')
        h = context.get('h', UNDEFINED)
        forms = _mako_get_namespace(context, 'forms')

        def show_wikipage():
            return render_show_wikipage(context)

        def wiki_history():
            return render_wiki_history(context)

        def wiki_edit():
            return render_wiki_edit(context)

        def wiki_diff():
            return render_wiki_diff(context)

        def wiki_talkpage():
            return render_wiki_talkpage(context)

        __M_writer = context.writer()
        __M_writer('\n    ')
        sel_wp = capture(forms.form_selectwikipage, c.authuser, c.wikipagenames, c.wikipagename or '')
        searchbox = capture(forms.form_searchbox, c.authuser, 'searchwiki', 'Search-wiki', h.suburl_search, c.searchfaces)
        fav = capture(elements.favoriteicon, 'favwiki')
        tindex = '<span class="ml10 fwnormal fntsmall">' + '<a href="%s" title="Index of wiki pages">                    Titleindex</a></span>' % h.url_wikititleindex
        refr = capture(elements.iconlink, h.url_translatewiki, 'refresh', classes='mr5', title='Bring this wiki-html upto-date')
        charts = capture(elements.iconlink, h.url_wikicharts, 'barchart', title='Wiki charts')
        tline = capture(elements.iconlink, h.url_wikitimeline, 'timeline', title='Timeline for wiki page')
        __M_writer('\n    ')
        __M_writer(escape(elements.mainnav()))
        __M_writer('\n    ')
        __M_writer(escape(elements.contextnav([fav, searchbox, sel_wp, tindex], rspans=[
         refr, charts, tline], tooltips=page_tooltips)))
        __M_writer('\n    <div id="bdy" class="w100">\n')
        if c.authusername == 'anonymous' or not c.userpanes:
            __M_writer('        <div class="fullpanel1">\n')
        else:
            __M_writer('        <div class="panel1">\n')
        __M_writer('            <div>\n')
        if c.authorized:
            __M_writer('                    ')
            __M_writer(escape(forms.form_wikifav(c.authuser, c.project, c.wiki, h.suburl_wikifav, c.isuserfavorite and 'delfavuser' or 'addfavuser')))
            __M_writer('\n')
        __M_writer('\n')
        if c.wikiedit:
            __M_writer('                    ')
            __M_writer(escape(wiki_edit()))
            __M_writer('\n')
        elif c.whistory:
            __M_writer('                    ')
            __M_writer(escape(wiki_history()))
            __M_writer('\n')
        elif c.wikidiff:
            __M_writer('                    ')
            __M_writer(escape(wiki_diff()))
            __M_writer('\n')
        elif c.wtalkpage:
            __M_writer('                    ')
            __M_writer(escape(wiki_talkpage()))
            __M_writer('\n')
        elif c.wikipage or c.wcnt:
            if c.authorized:
                __M_writer('                        ')
                __M_writer(escape(forms.form_votewiki(c.authuser, c.project, c.wiki, h.suburl_votewiki, c.upvotes, c.downvotes, c.currvote)))
                __M_writer('\n')
            __M_writer('                    ')
            __M_writer(escape(show_wikipage()))
            __M_writer('\n')
        __M_writer('            </div>\n        </div> \n')
        if c.authusername != 'anonymous' and c.userpanes:
            __M_writer('        <div class="panel2">')
            __M_writer(escape(elements.user_panes(c.userpanes)))
            __M_writer('</div>\n')
        __M_writer('    </div>\n')
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


def render_show_wikipage(context):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        author = c.wcnt.author
        created_on = h.utc_2_usertz(c.wcnt.created_on, c.authuser.timezone)
        __M_writer('\n    <div class="zwikipage mr5">\n        <div class="posr pb2" style="height: 1.25em; border-bottom : 1px solid gray">\n            <div class="floatl">\n                <span name="wikivote"></span>\n            </div>\n            <div class="floatr">\n                <span name="wdownload" title="Download in different formats"\n                      class="fntbold fgblue pointer">\n                    download<span class="fntxsmall vmiddle"> &#9660;</span>\n                </span>\n                <span name="wvermenu" title="Goto previous version of document"\n                      class="ml5 fntbold fgblue pointer">\n                    ver<span class="fntxsmall vmiddle"> &#9660;</span>\n                </span>\n                <a class="ml5" title="Create review entry for this document"\n                   href="')
        __M_writer(escape(h.url_reviewwiki))
        __M_writer('">Review</a>\n                <a class="ml5" title="Discuss this document"\n                   href="')
        __M_writer(escape(h.url_wtalkpage))
        __M_writer('">Talkpage</a>\n')
        if c.wikieditable:
            __M_writer('                <a class="ml5" href="')
            __M_writer(escape(h.url_wikiedit))
            __M_writer('">Edit</a>\n')
        __M_writer('                <a class="ml5" title="Watch document history"\n                   href="')
        __M_writer(escape(h.url_whistory))
        __M_writer('">History</a>\n            </div>\n        </div>\n        <div class="ml10 mr10">\n            <div class="floatr" style="width: 250px;">\n                <div class="br4 ml10" style="border : 1px dotted gray;">\n                    <div class="p3 fntbold bggray1">\n                        Page Info\n                        <div class="floatr fggray fntitalic">\n                            Version ')
        __M_writer(escape(c.wcnt.id))
        __M_writer('\n                        </div>\n                    </div>\n                    <div class="p3 calign">\n                        document type,\n                        <span class="fgLCoral fntbold">\n                            ')
        __M_writer(escape(c.wiki.type.wiki_typename))
        __M_writer('</span>\n                    </div>\n                    <div class="p3 calign">\n                        last edited by,\n                        <a class="fntbold" href="')
        __M_writer(escape(h.url_foruser(author)))
        __M_writer('"\n                           >')
        __M_writer(escape(author))
        __M_writer(' </a>\n                    </div>\n                    <div class="p3 calign"\n                         title="')
        __M_writer(escape(created_on.strftime('%b %d, %Y, %r')))
        __M_writer('">\n                        last edited on,\n                        <span class="fggreen fntbold">\n                             ')
        __M_writer(escape(created_on.strftime('%b %d, %Y')))
        __M_writer('</span>\n                    </div>\n                </div>\n\n                <div class="br4 ml10 mt5 fntbold" style="border : 1px dotted gray;">\n                    <div class="p3 bggray1">Authors </div>\n                    <table class="w100">\n')
        for (auth, count) in c.wikiauthors.iteritems():
            __M_writer('                        <tr>\n                         <td class="p3 calign" style="border: none;">\n                            <a href="')
            __M_writer(escape(h.url_foruser(auth)))
            __M_writer('">')
            __M_writer(escape(auth))
            __M_writer('</a>\n                        </td>\n                        <td class="p3 fggray lalign" style="border: none;">\n                            ')
            __M_writer(escape(count))
            __M_writer(' edits\n                        </td>\n                        </tr>\n')

        __M_writer('                    </table>\n                </div>\n                <div>\n                    <div name="wattachblk"></div>\n                </div>\n                <div class="bclear">\n                    <div name="wtagblk"></div>\n                </div>\n                <div class="ml10 fntbold bclear">\n                    <a href="')
        __M_writer(escape(h.url_tagcloud))
        __M_writer('">Visit tag cloud ...</a>\n                </div>\n            </div>\n\n            <div style="margin-right: 250px">\n                <div>\n                    ')
        __M_writer(c.wikihtml)
        __M_writer('\n                </div>\n            </div>\n\n        </div>\n    </div>\n\n    <script type="text/javascript">\n    ')
        wiki_id = c.wiki and c.wiki.id or ''
        __M_writer("\n    function setup_wikipage() {\n\n        /* Setup the wiki version menu */\n        var wvMenu=null;\n        var vernode    = dojo.query( 'span[name=wvermenu]' )[0];\n        var wversions  = ")
        __M_writer(h.json.dumps(c.wversions))
        __M_writer(';\n\n        if ( vernode ) {\n            wvMenu = new zeta.Menu({ \n                            targetNodes   : [ vernode ],\n                            style: { fontSize: \'small\',\n                                     color: \'blue\',\n                                     minWidth: \'2em\'\n                                   }\n                         });\n            dojo.forEach( wversions,\n                function( ver ) {\n                    wverurl = \'<a href="\' + ver[0] + \'">\' + ver[1] + \'</a>\'\n                    wvMenu.addChild(\n                        new zeta.MenuItem(\n                            { content: wverurl, class: \'fntbold hoverhighlight\' }\n                        )\n                    );\n                }\n            );\n        }\n\n        /* Setup wiki download menu */\n        var wdMenu=null;\n        var dwnnode    = dojo.query( \'span[name=wdownload]\' )[0];\n        var wdownload  = ')
        __M_writer(h.json.dumps(c.wdownload))
        __M_writer(';\n\n        if( dwnnode ) {\n            wdMenu = new zeta.Menu({ \n                            targetNodes   : [ dwnnode ],\n                            style: { fontSize: \'small\',\n                                     fontStyle: \'italic\',\n                                     color: \'crimson\',\n                                     minWidth: \'5em\'\n                                   }\n                         });\n            dojo.forEach( wdownload,\n                function( d ) {\n                    wdurl = \'<a href="\' + d[0] + \'">\' + d[1] + \'</a>\'\n                    wdMenu.addChild(\n                        new zeta.MenuItem(\n                            { content: wdurl, class: \'fntbold, hoverhighlight\' }\n                        )\n                    );\n                }\n            );\n        }\n\n\n        /* Attachments */\n        new zeta.Attachments(\n                { user: [ \'')
        __M_writer(escape(str(c.authuser.id)))
        __M_writer("', '")
        __M_writer(escape(c.authuser.username))
        __M_writer("' ],\n                  id: 'wikiattachblk',\n                  addform: [ 'addwikiattachs', '")
        __M_writer(h.suburl_addwikiattachs)
        __M_writer("' ],\n                  delform: [ 'delwikiattachs', '")
        __M_writer(h.suburl_delwikiattachs)
        __M_writer("' ],\n                  attachon: [ '")
        __M_writer(escape(str(wiki_id)))
        __M_writer("', 'wiki_id' ],\n                  editable: ")
        __M_writer(escape([0, 1][(c.att_editable == True)]))
        __M_writer(",\n                  url: '")
        __M_writer(h.url_wikiattachments)
        __M_writer("',\n                  attachs: ")
        __M_writer(h.json.dumps(c.attachs))
        __M_writer(',\n                  clsdisplayitem: "dispblk"\n                }, dojo.query( "div[name=wattachblk]" )[0]\n            )\n        /* Tags */\n        new zeta.Tags(\n                { user: [ \'')
        __M_writer(escape(str(c.authuser.id)))
        __M_writer("', '")
        __M_writer(escape(c.authuser.username))
        __M_writer("' ],\n                  id: 'wikitagblk',\n                  addform: [ 'addwikitags', '")
        __M_writer(h.suburl_addwikitags)
        __M_writer("' ],\n                  delform: [ 'delwikitags', '")
        __M_writer(h.suburl_delwikitags)
        __M_writer("' ],\n                  tagon: [ '")
        __M_writer(escape(str(wiki_id)))
        __M_writer("', 'wiki_id' ],\n                  editable: ")
        __M_writer(escape([0, 1][(c.tag_editable == True)]))
        __M_writer(",\n                  url: '")
        __M_writer(h.url_wikitags)
        __M_writer("',\n                  tags: ")
        __M_writer(h.json.dumps(c.tags))
        __M_writer('\n                }, dojo.query( "div[name=wtagblk]" )[0]\n            )\n        linkencode();\n    }\n    </script>\n')
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


def render_wiki_talkpage(context):
    context.caller_stack._push_frame()
    try:
        forms = _mako_get_namespace(context, 'forms')
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <div class="zwikitalkpage mr5">\n        <div class="pb2 posr ralign" style="border-bottom : 1px solid gray">\n            <a class="mr5" href="')
        __M_writer(escape(h.url_wikipage))
        __M_writer('">Page</a>\n        </div>\n        <div class="commentbox bclear ml20 mr20">\n            <div class="bclear"><a name="comments"></a></div>\n            <div id="wcomments" class="bclear" class="mt20"></div>\n            <div id="createwcmt_cntnr" style="border: 1px dotted gray"\n                 class="dispnone bclear mb10 pl3 pt3 w80">\n                ')
        __M_writer(escape(forms.form_createwcmt(c.authuser, c.wiki, h.suburl_createwcmt)))
        __M_writer('\n            </div>\n            <div id="updatewcmt_cntnr" style="border: 1px dotted gray"\n                 class="dispnone ml10 mr10 w80">\n                ')
        __M_writer(escape(forms.form_updatewcmt(c.authuser, c.wiki, h.suburl_updatewcmt)))
        __M_writer('\n            </div>\n            <div id="replywcmt_cntnr" style="border: 1px dotted gray"\n                 class="dispnone ml10 mr10 w80">\n                ')
        __M_writer(escape(forms.form_replywcmt(c.authuser, c.wiki, h.suburl_replywcmt)))
        __M_writer('\n            </div>\n        </div>\n    </div>\n\n    <script type="text/javascript">\n    items_wikicomments  = ')
        __M_writer(c.items_wikicomments)
        __M_writer("\n    function setup_talkpage() {\n        var div_wcomments   = dojo.query( 'div#wcomments' )[0];\n\n        make_ifrs_wikicomments( '")
        __M_writer(h.url_wikicomments)
        __M_writer("', items_wikicomments )\n        make_ifrs_wikircomments('")
        __M_writer(h.url_wikircomments)
        __M_writer("' )\n\n        /* Comment list */\n        new zeta.CommentContainer({\n                ifrs_comments: wikicomments,\n                ifrs_rcomments: wikircomments,\n                crformid: 'createwcmt',\n                rpformid: 'replywcmt',\n                edformid: 'updatewcmt',\n                sortby: 'wiki_comment_id',\n                identity: 'wiki_comment_id'\n            }, div_wcomments );\n    }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_wiki_edit(context):
    context.caller_stack._push_frame()
    try:
        forms = _mako_get_namespace(context, 'forms')
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <div class="zwikiedit mr5">\n        <div class="pb2 posr ralign" style="border-bottom : 1px solid gray">\n            <a href="')
        __M_writer(escape(h.url_wikipage))
        __M_writer('">Page</a>\n            <a class="ml5 mr5" href="')
        __M_writer(escape(h.url_whistory))
        __M_writer('">History</a>\n        </div>\n        <div class="dispnone mt10 ml10 mr10">\n            <fieldset style="background: #F4F4F4 url(/preview_bg.png) repeat scroll 0">\n                <legend>Preview( <a href="#edit">edit</a> )</legend>\n                <div class="ml10 mr10 wikipreview"></div>\n            </fieldset>\n            <br></br>\n            <hr></hr>\n        </div>\n        <div class="mt10">\n            <a name="edit"></a>\n            ')
        __M_writer(escape(forms.form_wikicontent(c.authuser, c.wiki, c.wcnt, h.suburl_wikiedit, h.url_wikipage)))
        __M_writer('\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_wiki_diff(context):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')
        __M_writer = context.writer()
        __M_writer('\n    <div class="zwikidiff mr5">\n        <div class="pb2 posr ralign" style="border-bottom : 1px solid gray">\n            <a href="')
        __M_writer(escape(h.url_wikipage))
        __M_writer('">Page</a>\n            <a class="ml5 mr5" href="')
        __M_writer(escape(h.url_whistory))
        __M_writer('">History</a>\n        </div>\n        <div class="ml10 mr10 mt10">\n            ')
        __M_writer(escape(elements.difftable(c.oldver, c.newver, c.wcnt_oldver.text.splitlines(), c.wcnt_newver.text.splitlines())))
        __M_writer('\n        </div>\n    </div>\n')
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
        __M_writer('\n\n    <script type="text/javascript">\n        dojo.addOnLoad( function() {\n            /* Setup the wiki goto list */\n            select_goto( dojo.query( \'#selectwikipage\' )[0] );\n        });\n        dojoaddOnLoad( \'setup_talkpage\' );\n        dojoaddOnLoad( \'setup_wikipage\' );\n        dojoaddOnLoad( \'initform_wikifav\' );\n        dojoaddOnLoad( \'initform_votewiki\' );\n        dojoaddOnLoad( \'initform_wikicont\' );\n        dojoaddOnLoad( \'initform_wikidiff\' );\n\n        dojo.addOnLoad( setup_userpanes );\n        dojo.addOnLoad( adjust_upheight );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_wiki_history(context):
    context.caller_stack._push_frame()
    try:
        forms = _mako_get_namespace(context, 'forms')
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <div class="zwikihistory mr5">\n        <div class="pb2 posr ralign" style="border-bottom : 1px solid gray">\n            <a class="mr5" href="')
        __M_writer(escape(h.url_wikipage))
        __M_writer('">Page</a>\n        </div>\n        <div class="ml10 mr10 mt10">\n            ')
        __M_writer(escape(forms.form_wikidiff(c.authuser, c.wiki, h.url_wikidiff, c.wikicontents)))
        __M_writer('\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()