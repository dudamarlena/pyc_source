# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/projects/review.html.py
# Compiled at: 2010-07-12 03:41:15
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278920475.52772
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/projects/review.html'
_template_uri = '/derived/projects/review.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['hd_script', 'reviewcomments', 'bd_body', 'hd_links', 'bd_script']
page_tooltips = [
 [
  'Help',
  'Review - documents, code and wiki pages. Every review created, has an\n<em>author</em>, a <em>moderator</em> and <em>participants</em>.\n'],
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
  'View-withsource',
  'Review comments can be added interactively while viewing the reviewed item.'],
 [
  'Timeline',
  'Timeline gives a log of all updates done to Review(s).']]

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
        __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_reviewcomments(context):
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
        __M_writer('\n    <div id="prjrevwcomments" class="mr5">\n        <div class="pb2 posr" style="border-bottom : 1px solid gray">\n            <span class="fntbold ml5">')
        __M_writer(escape(c.cnt_comments))
        __M_writer('</span>\n            <span class="fntbold fggray">Comments</span> | \n            <span class="fntbold">')
        __M_writer(escape(c.cnt_pending))
        __M_writer('</span>\n            <span class="fntbold fgcrimson">Pending</span>\n            <span class="posa" style="right : 0px">\n                <span>[ <a href="')
        __M_writer(escape(h.url_revwwithsource))
        __M_writer('">View-withsource</a> ]</span>\n            </span>\n        </div>\n        <div class="disptable w100">\n        <div class="disptrow">\n            <div class="disptcell vtop"\n                 style="width : 13%; border-right : 2px solid #f2f2f2;">\n                ')
        __M_writer(escape(elements.showpeople()))
        __M_writer('\n                <div class="mr5">\n                    <div name="rattachblk"></div>\n                </div>\n                <div class="bclear mr5">\n                    <div name="rtagblk"></div>\n                </div>\n            </div>\n            <div class="disptcell">\n                <h3 id="revtitle" class="')
        __M_writer(escape(closed))
        __M_writer('"\n                    style="margin : 5px 0px 0px 10px">\n                    Review ')
        __M_writer(escape(c.review.id))
        __M_writer(' \n                    <span class="fggray">\n                    ( ')
        __M_writer(escape('%s, ver:%s' % (c.review.resource_url, c.review.version)))
        __M_writer(' )\n                    </span>\n                </h3>\n                <div>\n                    <div id="creatercmt_cntnr" \n                         class="bclear ml10 mt5 mb10 pt3 w80">\n')
        if c.revwcmtable:
            __M_writer('                            <div class="fgblue pointer">New review comment</div>\n                            <div class="dispnone ml10" style="border: 1px dotted gray">\n                                ')
            __M_writer(escape(forms.form_creatercmt(c.authuser, c.project, c.review, h.suburl_creatercmt, c.naturenames)))
            __M_writer('\n                            </div>\n')
        __M_writer('                    </div>\n                    <div id="replyrcmt_cntnr" style="border: 1px dotted gray"\n                         class="dispnone ml10 mr10 w80">\n                        ')
        __M_writer(escape(forms.form_replyrcmt(c.authuser, c.project, c.review, h.suburl_replyrcmt)))
        __M_writer('\n                    </div>\n                    <div id="processrcmt_cntnr" style="border: 1px dotted gray"\n                         class="dispnone ml10 mr10 w80">\n                        ')
        __M_writer(escape(forms.form_processrcmt(c.authuser, c.project, c.review, h.suburl_processrcmt)))
        __M_writer('\n                    </div>\n                </div>\n                <div class="revwcomments">\n                </div>\n            </div>\n        </div>\n        </div>\n    </div>\n\n    <script type="text/javascript">\n\n    ')
        review_id = c.review and c.review.id or ''
        __M_writer('\n\n    items_revwrcomments  = ')
        __M_writer(c.items_revwrcomments)
        __M_writer('\n    revwcmtable          = ')
        __M_writer(escape([0, 1][(c.revwcmtable == True)]))
        __M_writer("\n    function setup_revwcomments() {\n        var crcntnr          = dojo.query( '#creatercmt_cntnr' )[0];\n        var rpcntnr          = dojo.query( '#replyrcmt_cntnr' )[0];\n        var prcntnr          = dojo.query( '#processrcmt_cntnr' )[0];\n        var div_revwcomments = dojo.query( 'div.revwcomments' )[0];\n\n        if( revwcmtable ) {\n            toggler( crcntnr.childNodes[1], crcntnr.childNodes[3], \n                     'cancel', 'New review comment', true )\n        }\n\n        make_ifrs_revwrcomments( '")
        __M_writer(h.url_revwrcomments)
        __M_writer("',\n                                 items_revwrcomments )\n\n        new zeta.Form({ formid : 'processrcmt' });\n\n        /* Attachments */\n        new zeta.Attachments(\n                { user: [ '")
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
        __M_writer(',\n                  clsdisplayitem: "dispblk"\n                }, dojo.query( "div[name=rattachblk]" )[0]\n            )\n\n        /* Tags */\n        new zeta.Tags(\n                { user: [ \'')
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
        __M_writer('\n                }, dojo.query( "div[name=rtagblk]" )[0]\n            )\n\n        /* Comments */\n        // Setup adding comments.\n        new zeta.RCommentContainer({\n                ifrs_rcomments : revwrcomments,\n                rpform: form_replyrcmt,\n                prform: form_processrcmt,\n                rpcntnr: rpcntnr,\n                ref_nature: ')
        __M_writer(capture(forms.select_revwnature, c.naturenames))
        __M_writer(',\n                ref_action: ')
        __M_writer(capture(forms.select_revwaction, c.actionnames))
        __M_writer(',\n                moderated: ')
        __M_writer(escape([0, 1][(c.revwmoderated == True)]))
        __M_writer(',\n                authored: ')
        __M_writer(escape([0, 1][(c.revwauthored == True)]))
        __M_writer(',\n                revwcmtable: ')
        __M_writer(escape([0, 1][(c.revwcmtable == True)]))
        __M_writer(",\n                sortby: 'review_comment_id',\n                identity: 'review_comment_id'\n            }, div_revwcomments )\n    }\n    </script>\n")
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

        def reviewcomments():
            return render_reviewcomments(context)

        __M_writer = context.writer()
        __M_writer('\n    ')
        sel_revw = capture(forms.form_selectrevw, c.authuser, c.revwlist, c.review and c.review.resource_url or '')
        sel_rset = capture(forms.form_selectrset, c.authuser, c.rsetlist, c.reviewset and c.reviewset.name or '')
        searchbox = capture(forms.form_searchbox, c.authuser, 'searchreview', 'Search-review', h.suburl_search, c.searchfaces)
        fav = capture(elements.favoriteicon, 'favrevw')
        if c.revweditable:
            newrevw = '<span class="ml10 fwnormal fntsmall">                         <a href="%s" title="Create a new review">                         Create</a></span>' % h.url_revwcreate
        else:
            newrevw = ''
        revwsets = '<span class="ml10 fwnormal fntsmall">                     <a href="%s" title="List of reviews sets">                     Reviewsets</a></span>' % h.url_reviewsets
        charts = capture(elements.iconlink, h.url_revwcharts, 'barchart', title='Review analytics')
        tline = capture(elements.iconlink, h.url_revwtimeline, 'timeline', title='Timeline of reviews')
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
        __M_writer(escape(reviewcomments()))
        __M_writer('\n            </div>\n        </div> \n')
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


def render_bd_script(context):
    context.caller_stack._push_frame()
    try:
        parent = context.get('parent', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        __M_writer(escape(parent.bd_script()))
        __M_writer('\n\n    <script type="text/javascript">\n        dojo.addOnLoad( function() {\n            var n_select = dojo.query( \'#selectrevw\' )[0];\n            n_select ? select_goto( n_select ) : null;\n        });\n        dojo.addOnLoad( setup_participants );\n        dojo.addOnLoad( setup_revwcomments );\n\n        dojo.addOnLoad( setup_userpanes );\n        dojo.addOnLoad( adjust_upheight );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()