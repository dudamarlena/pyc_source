# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/projects/ticket.html.py
# Compiled at: 2010-07-10 02:09:35
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278742175.850561
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/projects/ticket.html'
_template_uri = '/derived/projects/ticket.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['status_delimiter', 'ticket_details', 'hd_links', 'hd_script', 'status_block', 'bd_body', 'show_ticket', 'status_flow', 'bd_script']
page_tooltips = [
 [
  'Help',
  "Tickets are helpful to track bugs, tasks, requirements etc ...\n<br/>\nThe three main attributes of a ticket are <b>type, status, severity</b>.\nType should give an idea about why? and what? of a ticket. Status actually\ntracks the flow of work or activity happening on a ticket. Severity, well tells\nhow severe the ticket is to the project (synonymous to priority).\n<br/>\nEvery ticket status change should provide the next status of the ticket and\ndue-date to act on the ticket state. The user who changes the ticket status\nwill become the new owner of the ticket.\n<br/>\nIf, in case the changed ticket status actually expects a response from a user\nother than the ticket owner, it can be indicated so using 'promptuser'\nattribute.\n<br/>\nUse ticket id, where ever the ticket needs to be referenced.\n"],
 [
  'Attachments',
  'Upload attachments by clicking on the iconized title. Clicking on the\nsame once again will hide it. Delete attachments by clicking on the cross-wire.\nUpload any number of attachments files to ticket.\n<br/><br/>\nEvery attached file, will have its "id" in paranthesis. Use the id value when\nrefering to the attachment.\n'],
 [
  'Tags',
  'Tag a ticket by clicking on the iconized title. Delete tags by clicking on\nthe cross-wire. Tag names should be 2 or more characters\n'],
 [
  'Favorites',
  "Registered users can pick ticket(s) as their favorite, provided the user\nhas got 'TICKET_VIEW' permission"],
 [
  'Vote',
  'Registered users can up-vote or down-vote a ticket.']]

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
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_status_delimiter(context, ts, actualdt=None):
    context.caller_stack._push_frame()
    try:
        int = context.get('int', UNDEFINED)
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        abs = context.get('abs', UNDEFINED)
        repr = context.get('repr', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        if ts[2]:
            due_date = ts[2].astimezone(h.timezone(c.authuser.timezone))
            diffdt = due_date - actualdt
            diffdays = int(repr(diffdt.days))
            if 0 <= diffdays:
                diffby = 'beaten by ' + h.olderby(diffdays)
                difffg = 'fggreen'
            else:
                diffby = 'overrun by ' + h.olderby(abs(diffdays))
                difffg = 'fgred'
        else:
            diffby = '-'
            difffg = 'fggray'
        __M_writer('\n    <div>\n        <div>\n            <div style="width : 49%; height: 1em; border-right: 2px solid #f2f2f2;"> \n            </div>\n        </div>\n        <div class="')
        __M_writer(escape(difffg))
        __M_writer(' p2">')
        __M_writer(escape(diffby))
        __M_writer('</div>\n        <div>\n            <div style="width : 49%; height: 1em; border-right: 2px solid #f2f2f2"> \n            </div>\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_ticket_details(context, tckdet):
    context.caller_stack._push_frame()
    try:
        forms = _mako_get_namespace(context, 'forms')
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        abs = context.get('abs', UNDEFINED)
        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        due_date = tckdet.get('due_date', '')
        statusname = tckdet['status']
        parent_id = tckdet.get('parent', '')
        blockers = (', ').join([ str(b) for b in c.blockers ])
        blocking = (', ').join([ str(b) for b in c.blocking ])
        children = (', ').join([ str(child) for child in c.children ])
        flash_schedule = ''
        flashfg = ''
        if due_date:
            due_date = due_date.astimezone(h.timezone(c.authuser.timezone))
            daysleft = due_date.astimezone(h.timezone('UTC')) - h.timezone('UTC').localize(h.dt.datetime.utcnow())
            if statusname not in c.ticketresolv:
                if daysleft < h.dt.timedelta(0) and statusname not in c.ticketresolv:
                    flash_schedule = '( Schedule overun by %s )' % h.olderby(abs(daysleft.days))
                    flashfg = 'fgred'
                else:
                    flash_schedule = '( %s left )' % h.olderby(daysleft.days)
                    flashfg = 'fggreen'
        tckcreator = c.ticketstatus[0][4]
        __M_writer('\n    <div class="w100 ralign fgcrimson fntbold pr10">\n        Created by, <a href="')
        __M_writer(escape(h.url_foruser(tckcreator)))
        __M_writer('">')
        __M_writer(escape(tckcreator))
        __M_writer('</a>,\n        on ')
        __M_writer(escape(c.ticket.created_on.strftime('%a, %b %d, %Y')))
        __M_writer('\n    </div>\n    <div class="disptable">\n        <div class="disptrow">\n            <div class="p5 disptcell">\n                <span class="">Summary</span>\n            </div>\n            <div class="p5 disptcell">\n                ')
        summary = tckdet['summary']
        __M_writer('\n                <span name="summary" class="fntbold inedit">')
        __M_writer(summary)
        __M_writer('</span>\n            </div>\n        </div>\n    </div>\n    <hr></hr>\n')
        if c.tckeditable:
            __M_writer('        <span class="togglest floatr pointer fgblue">Change-status</span>\n')
        __M_writer('    <div class="viewst">\n    <div class="disptable">\n        <div class="disptrow">\n            <div class="p5 disptcell">\n                <span class="">status</span>\n            </div>\n            <div class="p5 disptcell">\n                <span name="tck_statusname" class="fntbold undrln">\n                    ')
        __M_writer(escape(statusname.upper()))
        __M_writer('</span>\n            </div>\n            <div class="p5 disptcell">\n                <span class="">Duedate</span>\n            </div>\n            <div class="p5 disptcell">\n                <span name="due_date" class="fntbold">\n                    ')
        __M_writer(escape(due_date and due_date.strftime('%a, %b %d, %Y') or '-'))
        __M_writer('\n                </span>\n            </div>\n            <div class="p5 disptcell">\n                <span class="">Owner</span>\n            </div>\n            <div class="p5 disptcell">\n                <span name="owner" class="fntbold">')
        __M_writer(escape(tckdet['owner']))
        __M_writer('</span>\n            </div>\n            <div class="p5 ml50 disptcell">\n                <span class="')
        __M_writer(escape(flashfg))
        __M_writer('" >')
        __M_writer(escape(flash_schedule))
        __M_writer('</span>\n            </div>\n        </div>\n    </div>\n    </div>\n    <div class="changest dispnone">\n        ')
        __M_writer(escape(forms.form_changetckst(c.authuser, c.project, c.ticket, tckdet['status'], due_date and due_date.strftime('%m/%d/%Y') or '-', h.suburl_changetckst, c.tck_statusnames)))
        __M_writer('\n    </div>\n    <hr></hr>\n    <div class="floatr pl10 m5 pr10"\n         style="border-left : 2px solid crimson">\n        <b class="dispblk undrln pb10">Reference</b>\n        ')
        parent = tckdet['parent']
        __M_writer('\n        <div>\n')
        if parent:
            __M_writer('        <a href="')
            __M_writer(escape(h.url_forticket(h.maptckproj(parent), parent)))
            __M_writer('"\n           >')
            __M_writer(escape(parent))
            __M_writer('</a>\n')
        __M_writer('        </div>\n        <div>\n')
        for tck in c.children:
            __M_writer('            <a href="')
            __M_writer(escape(h.url_forticket(h.maptckproj(tck), tck)))
            __M_writer('"\n               class="mr5">')
            __M_writer(escape(tck))
            __M_writer('</a>\n')

        __M_writer('        </div>\n        <div>\n')
        for tck in c.blockers:
            __M_writer('            <a href="')
            __M_writer(escape(h.url_forticket(h.maptckproj(tck), tck)))
            __M_writer('"\n               class="mr5">')
            __M_writer(escape(tck))
            __M_writer('</a>\n')

        __M_writer('        </div>\n        <div>\n')
        for tck in c.blocking:
            __M_writer('            <a href="')
            __M_writer(escape(h.url_forticket(h.maptckproj(tck), tck)))
            __M_writer('"\n               class="mr5">')
            __M_writer(escape(tck))
            __M_writer('</a>\n')

        __M_writer('        </div>\n    </div>\n    <div class="disptable">\n        <div class="disptrow">\n            <div class="p5 disptcell">\n                <span class="">Type</span>\n            </div>\n            <div class="p5 disptcell">\n                <span name="tck_typename" class="fntbold inedit">\n                    ')
        __M_writer(escape(tckdet['type']))
        __M_writer('</span>\n            </div>\n            <div class="p5 disptcell">\n                <span class="">&ensp;Severity</span>\n            </div>\n            <div class="p5 disptcell">\n                <span name="tck_severityname" class="fntbold inedit">\n                    ')
        __M_writer(escape(tckdet['severity']))
        __M_writer('</span>\n            </div>\n        </div>\n        <div class="disptrow">\n            <div class="p5 disptcell">\n                <span class="">Component</span>\n            </div>\n            <div class="p5 disptcell">\n                <span name="component_id" class="fntbold inedit">\n                    ')
        __M_writer(escape(tckdet['compname']))
        __M_writer('</span>\n            </div>\n            <div class="p5 disptcell">\n                <span class="">&ensp;Milestone</span>\n            </div>\n            <div class="p5 disptcell">\n                <span name="milestone_id" class="fntbold inedit">\n                    ')
        __M_writer(escape(tckdet['mstnname']))
        __M_writer('</span>\n            </div>\n            <div class="p5 disptcell">\n                <span class="">&ensp;Version</span>\n            </div>\n            <div class="p5 disptcell">\n                <span name="version_id" class="fntbold inedit">\n                    ')
        __M_writer(escape(tckdet['vername']))
        __M_writer('</span>\n            </div>\n        </div>\n        <div class="disptrow">\n            <div class="p5 disptcell">\n                <span class="">Prompting</span>\n            </div>\n            <div class="p5 disptcell">\n                <span name="promptuser" class="fntbold inedit">\n                    ')
        __M_writer(escape(tckdet['promptuser']))
        __M_writer('</span>\n            </div>\n        </div>\n        <div class="disptrow">\n            <div class="p5 disptcell">\n                <span class="">Parent</span>\n            </div>\n            <div class="p5 disptcell">\n                <span name="parent_id" class="fntbold inedit">\n                    ')
        __M_writer(escape(tckdet['parent']))
        __M_writer('</span>\n            </div>\n            <div class="p5 disptcell">\n                <span class="">&ensp;Children</span>\n            </div>\n            <div class="p5 disptcell">\n                <span class="fntbold">')
        __M_writer(escape(children))
        __M_writer('</span>\n            </div>\n        </div>\n        <div class="disptrow">\n            <div class="p5 disptcell">\n                <span class="">Blockers</span>\n            </div>\n            <div class="p5 disptcell">\n                <span name="blockedby_ids" class="fntbold inedit">')
        __M_writer(escape(blockers))
        __M_writer('</span>\n            </div>\n            <div class="p5 disptcell">\n                <span class="">&ensp;Blocking</span>\n            </div>\n            <div class="p5 disptcell">\n                <span name="blocking_ids" class="fntbold inedit">')
        __M_writer(escape(blocking))
        __M_writer('</span>\n            </div>\n        </div>\n    </div>\n    <hr></hr>\n    <div class="p5">\n        <span class="describe floatr pointer fgblue">Describe</span>\n        <div class="fntbold">Description</div>\n        <div name="descriptionhtml" class="">\n            ')
        __M_writer(tckdet['descriptionhtml'])
        __M_writer('\n        </div>\n        <div name="descriptionform" class="dispnone">\n            ')
        __M_writer(escape(forms.form_tckdescription(c.authuser, c.project, h.suburl_configtck, t=c.ticket)))
        __M_writer('\n        </div>\n    </div>\n    <script type="text/javascript">\n        dojo.addOnLoad( function () {\n            dojo.connect(\n                dojo.query( \'span.describe\' )[0],\n                \'onclick\',\n                function( e ) {\n                    dojo.toggleClass( dojo.query( \'div[name=descriptionhtml]\' )[0],\n                                      \'dispnone\', true );\n                    dojo.toggleClass( dojo.query( \'div[name=descriptionform]\' )[0],\n                                      \'dispnone\', false );\n                    dojo.stopEvent( e );\n                }\n            );\n        })\n    </script>\n    ')
        __M_writer(escape(forms.form_tcksummary(c.authuser, c.project, h.suburl_configtck, t=c.ticket)))
        __M_writer('\n    ')
        __M_writer(escape(forms.form_tcktype(c.authuser, c.project, h.suburl_configtck, t=c.ticket)))
        __M_writer('\n    ')
        __M_writer(escape(forms.form_tckseverity(c.authuser, c.project, h.suburl_configtck, t=c.ticket)))
        __M_writer('\n    ')
        __M_writer(escape(forms.form_tckcomponent(c.authuser, c.project, h.suburl_configtck, t=c.ticket)))
        __M_writer('\n    ')
        __M_writer(escape(forms.form_tckmilestone(c.authuser, c.project, h.suburl_configtck, t=c.ticket)))
        __M_writer('\n    ')
        __M_writer(escape(forms.form_tckversion(c.authuser, c.project, h.suburl_configtck, t=c.ticket)))
        __M_writer('\n    ')
        __M_writer(escape(forms.form_tckpromptuser(c.authuser, c.project, h.suburl_configtck, t=c.ticket)))
        __M_writer('\n    ')
        __M_writer(escape(forms.form_tckparent(c.authuser, c.project, h.suburl_configtck, t=c.ticket)))
        __M_writer('\n    ')
        __M_writer(escape(forms.form_tckblockedby(c.authuser, c.project, h.suburl_configtck, t=c.ticket)))
        __M_writer('\n    ')
        __M_writer(escape(forms.form_tckblocking(c.authuser, c.project, h.suburl_configtck, t=c.ticket)))
        __M_writer('\n')
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
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        dict = context.get('dict', UNDEFINED)
        str = context.get('str', UNDEFINED)
        parent = context.get('parent', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        __M_writer(escape(parent.hd_script()))
        __M_writer('\n\n    <script type="text/javascript">\n    /********** Setup Ticket Grid **************/\n    ')
        ticket_id = c.ticket and c.ticket.id or ''
        tckeditable = c.tckeditable and 'true' or 'false'
        __M_writer('\n\n    // Add empty component, milestone, version for select options\n    components  = ')
        __M_writer(h.json.dumps(dict(c.pcomponents + [('', '')])))
        __M_writer('\n    milestones  = ')
        __M_writer(h.json.dumps(dict(c.pmilestones + [('', '')])))
        __M_writer('\n    versions    = ')
        __M_writer(h.json.dumps(dict(c.pversions + [('', '')])))
        __M_writer('\n\n    tck_typenames= ')
        __M_writer(h.json.dumps(c.tck_typenames))
        __M_writer('\n    tck_severitynames= ')
        __M_writer(h.json.dumps(c.tck_severitynames))
        __M_writer('\n    projusers   = ')
        __M_writer(h.json.dumps(c.projusers))
        __M_writer('\n\n    tckccodes   = ')
        __M_writer(c.tckccodes)
        __M_writer("\n\n    function setup_ticket() {\n        var div_zticketpage= dojo.query( 'div.zticketpage' )[0];\n        var div_tcomments  = dojo.query( 'div#tcomments' )[0];\n\n        /* Setup the wiki goto list */\n        select_goto( dojo.query( '#selectticket' )[0] );\n\n        make_ifrs_tckcomments( '")
        __M_writer(h.url_tckcomments)
        __M_writer("',\n                               items_tckcomments );\n        make_ifrs_tckrcomments( '")
        __M_writer(h.url_tckrcomments)
        __M_writer("' );\n\n        /* Attachments */\n        new zeta.Attachments(\n                { user: [ '")
        __M_writer(escape(str(c.authuser.id)))
        __M_writer("', '")
        __M_writer(escape(c.authuser.username))
        __M_writer("' ],\n                  id: 'tckattachblk',\n                  addform: [ 'addtckattachs', '")
        __M_writer(h.suburl_addtckattachs)
        __M_writer("' ],\n                  delform: [ 'deltckattachs', '")
        __M_writer(h.suburl_deltckattachs)
        __M_writer("' ],\n                  attachon: [ '")
        __M_writer(escape(str(ticket_id)))
        __M_writer("', 'ticket_id' ],\n                  editable: ")
        __M_writer(escape([0, 1][(c.att_editable == True)]))
        __M_writer(",\n                  url: '")
        __M_writer(h.url_tckattachments)
        __M_writer("',\n                  attachs: ")
        __M_writer(h.json.dumps(c.attachs))
        __M_writer(',\n                  clsdisplayitem: "dispblk"\n                }, dojo.query( "div[name=tattachblk]" )[0]\n            )\n        /* Tags */\n        new zeta.Tags(\n                { user: [ \'')
        __M_writer(escape(str(c.authuser.id)))
        __M_writer("', '")
        __M_writer(escape(c.authuser.username))
        __M_writer("' ],\n                  id: 'tcktagblk',\n                  addform: [ 'addtcktags', '")
        __M_writer(h.suburl_addtcktags)
        __M_writer("' ],\n                  delform: [ 'deltcktags', '")
        __M_writer(h.suburl_deltcktags)
        __M_writer("' ],\n                  tagon: [ '")
        __M_writer(escape(str(ticket_id)))
        __M_writer("', 'ticket_id' ],\n                  editable: ")
        __M_writer(escape([0, 1][(c.tag_editable == True)]))
        __M_writer(",\n                  url: '")
        __M_writer(h.url_tcktags)
        __M_writer("',\n                  tags: ")
        __M_writer(h.json.dumps(c.tags))
        __M_writer('\n                }, dojo.query( "div[name=ttagblk]" )[0]\n            )\n        /* Comment list */\n        new zeta.CommentContainer({\n                ifrs_comments: tckcomments,\n                ifrs_rcomments: tckrcomments,\n                crformid: \'createtcmt\',\n                rpformid: \'replytcmt\',\n                edformid: \'updatetcmt\',\n                sortby: \'ticket_comment_id\',\n                identity: \'ticket_comment_id\'\n            }, div_tcomments );\n\n        // Widgetify forms for inline editing.\n        if( ')
        __M_writer(escape(tckeditable))
        __M_writer(" ) {\n            new zeta.Form({ normalsub: true, formid: 'tcksummary' });\n            new zeta.Form({ normalsub: true, formid: 'tcktype' });\n            new zeta.Form({ normalsub: true, formid: 'tckseverity' });\n            new zeta.Form({ normalsub: true, formid: 'tckcomponent' });\n            new zeta.Form({ normalsub: true, formid: 'tckmilestone' });\n            new zeta.Form({ normalsub: true, formid: 'tckversion' });\n            new zeta.Form({ normalsub: true, formid: 'tckpromptuser' });\n            new zeta.Form({ normalsub: true, formid: 'tckparent' });\n            new zeta.Form({ normalsub: true, formid: 'tckblockedby' });\n            new zeta.Form({ normalsub: true, formid: 'tckblocking' });\n            new zeta.Form({ normalsub: true, formid: 'tckdescription' });\n\n            function createtstat_onsubmit( e ) {\n                submitform( form_createtstat, e );\n                dojo.stopEvent(e);\n                update_colorcode();\n            }\n            new zeta.Form({ onsubmit: createtstat_onsubmit,\n                            formid: 'createtstat' });\n        }\n\n        /* Inline Editing */\n        function update_colorcode() {\n            var st = form_createtstat ?\n                     dojo.query( 'select[name=tck_statusname]', form_createtstat\n                             )[0].value\n                     : null;\n            var sv = form_tckseverity ?\n                     dojo.query( 'input[name=tck_severityname]', form_tckseverity\n                             )[0].value\n                     : null;\n            var ty = form_tcktype ?\n                     dojo.query( 'input[name=tck_typename]', form_tcktype\n                             )[0].value\n                     : null;\n            var tckdetail = {\n                tck_statusname : st,\n                tck_severityname : sv,\n                tck_typename : ty,\n            }\n            var bgcolor = tckcolorcode( tckdetail, tckccodes );\n            dojo.publish( 'tckbrd_chbg', [ 'tckboard', bgcolor ] );\n        }\n\n        var inlines = []\n        if( ")
        __M_writer(escape(tckeditable))
        __M_writer(' ) {\n            inlines = dojo.query( \'span.inedit\', div_zticketpage );\n        }\n        function inline_onchange( formnode, field, value ) {\n            // Translate the component name into id\n            if( field == \'component_id\' ) {\n                value = keyforvalue( components, value );\n            } else if ( field == \'milestone_id\' ) {\n                value = keyforvalue( milestones, value );\n            } else if ( field == \'version_id\' ) {\n                value = keyforvalue( versions, value );\n            }\n            dojo.query( \'input[name=\' + field + \']\', formnode \n                      )[0].value = value;\n            submitform( formnode );\n            update_colorcode();\n        }\n        dojo.forEach(\n            inlines,\n            function (item) {\n                var name     = dojo.attr( item, \'name\' );\n                var formnode = null;\n                if ( name == \'summary\' ) {\n                    new dijit.InlineEditBox({\n                        editor : "dijit.form.TextBox",\n                        onChange  : dojo.hitch(\n                                        null, inline_onchange,\n                                        form_tcksummary, \'summary\' \n                                    ),\n                        width : \'40em\',\n                        renderAsHtml: true\n                    }, item )        \n                } else if ( name == \'tck_typename\' ) {\n                    var store = create_ifrs_store( tck_typenames );\n                    new dijit.InlineEditBox({\n                        editor : "dijit.form.FilteringSelect",\n                        onChange  : dojo.hitch(\n                                        null, inline_onchange,\n                                        form_tcktype, \'tck_typename\'\n                                    ),\n                        editorParams : { class: "fntbold", store: store }\n                    }, item )        \n                } else if ( name == \'tck_severityname\' ) {\n                    var store = create_ifrs_store( tck_severitynames );\n                    new dijit.InlineEditBox({\n                        editor : "dijit.form.FilteringSelect",\n                        onChange  : dojo.hitch(\n                                        null, inline_onchange,\n                                        form_tckseverity, \'tck_severityname\'\n                                    ),\n                        editorParams : { store : store }\n                    }, item )        \n                } else if ( name == \'component_id\' ) {\n                    var store = create_ifrs_store( values(components).sort() );\n                    new dijit.InlineEditBox({\n                        editor : "dijit.form.FilteringSelect",\n                        onChange  : dojo.hitch(\n                                        null, inline_onchange,\n                                        form_tckcomponent, \'component_id\'\n                                    ),\n                        editorParams : { store : store }\n                    }, item )        \n                } else if ( name == \'milestone_id\' ) {\n                    var store = create_ifrs_store( values(milestones).sort() );\n                    new dijit.InlineEditBox({\n                        editor : "dijit.form.FilteringSelect",\n                        onChange  : dojo.hitch(\n                                        null, inline_onchange,\n                                        form_tckmilestone, \'milestone_id\'\n                                    ),\n                        editorParams : { store : store }\n                    }, item )        \n                } else if ( name == \'version_id\' ) {\n                    var store = create_ifrs_store( values(versions).sort());\n                    new dijit.InlineEditBox({\n                        editor : "dijit.form.FilteringSelect",\n                        onChange  : dojo.hitch(\n                                        null, inline_onchange,\n                                        form_tckversion, \'version_id\'\n                                    ),\n                        editorParams : { store : store }\n                    }, item )        \n                } else if ( name == \'promptuser\' ) {\n                    var store = create_ifrs_store( projusers );\n                    new dijit.InlineEditBox({\n                        editor : "dijit.form.FilteringSelect",\n                        onChange  : dojo.hitch(\n                                        null, inline_onchange,\n                                        form_tckpromptuser, \'promptuser\'\n                                    ),\n                        editorParams : { store : store }\n                    }, item )        \n                } else if ( name == \'parent_id\' ) {\n                    new dijit.InlineEditBox({\n                        editor : "dijit.form.TextBox",\n                        onChange  : dojo.hitch(\n                                        null, inline_onchange,\n                                        form_tckparent, \'parent_id\'\n                                    )\n                    }, item )        \n                } else if ( name == \'blockedby_ids\' ) {\n                    new dijit.InlineEditBox({\n                        editor : "dijit.form.TextBox",\n                        onChange  : dojo.hitch(\n                                        null, inline_onchange,\n                                        form_tckblockedby, \'blockedby_ids\'\n                                    )\n                    }, item )        \n                } else if ( name == \'blocking_ids\' ) {\n                    new dijit.InlineEditBox({\n                        editor : "dijit.form.TextBox",\n                        onChange  : dojo.hitch(\n                                        null, inline_onchange,\n                                        form_tckblocking, \'blocking_ids\'\n                                    )\n                    }, item )        \n                }\n                /*\n                else if ( name == \'description\' ) {\n                    new dijit.InlineEditBox({\n                        editor : "dijit.form.Textarea",\n                        onChange  : dojo.hitch(\n                                        null, inline_onchange,\n                                        form_tckdescription, \'description\'\n                                    )\n                    }, item )\n                }\n                */\n            }\n        );\n\n        /* Change status */\n        var span_togglest = dojo.query( "span.togglest" );\n        if( span_togglest.length ){\n            dojo.connect(\n                span_togglest[0],\n                \'onclick\',\n                function( e ) {\n                    dojo.toggleClass( dojo.query( \'div.changest\' )[0],\n                                      \'dispnone\', false );\n                    dojo.toggleClass( dojo.query( \'div.viewst\' )[0],\n                                      \'dispnone\', true );\n                    dojo.stopEvent( e );\n                }\n            );\n        }\n\n        /* Graph and Tree */\n        toggler(\n            dojo.query( \'span[name=depgraph]\' )[0],\n            dojo.query( \'div[name=graph]\' )[0],\n            \'Hide\', \'Graph\', true,\n            function( n_trigger, n, v_text, h_text ) { // Onshow\n                var n_obj = dojo.query( \'object\', n )[0];\n                var b_obj = dojo.coords( n_obj );\n                var b_par = dojo.coords( n_obj.parentNode );\n                dojo.style(\n                    n_obj,\n                    { marginLeft : ((b_par.w - b_obj.w) / 2)+\'px\' }\n                );\n                console.log( (b_par.w - b_obj.w) / 2 )\n            }\n        )\n        toggler(\n            dojo.query( \'span[name=hiertree]\' )[0],\n            dojo.query( \'div[name=tree]\' )[0],\n            \'Hide\', \'Tree\', true,\n            function( n_trigger, n, v_text, h_text ) { // Onshow\n                var n_obj = dojo.query( \'object\', n )[0];\n                var b_obj = dojo.coords( n_obj );\n                var b_par = dojo.coords( n_obj.parentNode );\n                dojo.style(\n                    n_obj,\n                    { marginLeft : ((b_par.w - b_obj.w) / 2)+\'px\' }\n                );\n            }\n        )\n    }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_status_block(context, ts, refdt):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        created_on = h.timezone(c.authuser.timezone).localize(ts[3])
        before = refdt - created_on
        stfg = ts[1] in c.ticketresolv and 'fggray' or 'fgblue'
        ownername = ts[4]
        __M_writer('\n    <div class="p3">\n        <div class="')
        __M_writer(escape(stfg))
        __M_writer(' p2 fntbold">')
        __M_writer(escape(ts[1]))
        __M_writer('</div>\n        <div class="p2">by, <a href="')
        __M_writer(escape(h.url_foruser(ownername)))
        __M_writer('">')
        __M_writer(escape(ownername))
        __M_writer('</a></div>\n        <div class="p2">\n            ')
        __M_writer(escape(created_on.strftime('%a, %b %d, %Y')))
        __M_writer('\n        </div>\n    </div>\n')
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
        str = context.get('str', UNDEFINED)

        def show_ticket():
            return render_show_ticket(context)

        __M_writer = context.writer()
        __M_writer('\n    ')
        searchbox = capture(forms.form_searchbox, c.authuser, 'searchticket', 'Search-ticket', h.suburl_search, c.searchfaces)
        sel_tck = capture(forms.form_selectticket, c.authuser, c.seltickets, c.ticket and str(c.ticket.id) or '')
        if c.tckeditable:
            newtck = '<span class="ml10 fwnormal fntsmall">                        <a href="%s" title="Create a new ticket">                        Create</a></span>' % h.url_ticketcreate
        else:
            newtck = '<span></span>'
        fav = capture(elements.favoriteicon, 'favtck')
        charts = capture(elements.iconlink, h.url_ticketcharts, 'barchart', title='Ticket analytics')
        tline = capture(elements.iconlink, h.url_tcktimeline, 'timeline', title='Timeline for ticket')
        __M_writer('\n    ')
        __M_writer(escape(elements.mainnav()))
        __M_writer('\n    ')
        __M_writer(escape(elements.contextnav([fav, searchbox, sel_tck, newtck], rspans=[
         charts, tline], tooltips=page_tooltips)))
        __M_writer('\n    <div id="bdy" class="w100">\n')
        if c.authusername == 'anonymous' or not c.userpanes:
            __M_writer('        <div class="fullpanel1">\n')
        else:
            __M_writer('        <div class="panel1">\n')
        __M_writer('            <div>\n')
        if c.authorized:
            __M_writer('                    ')
            __M_writer(escape(forms.form_tckfav(c.authuser, c.project, c.ticket, h.suburl_tckfav, c.isuserfavorite and 'delfavuser' or 'addfavuser')))
            __M_writer('\n                    ')
            __M_writer(escape(forms.form_votetck(c.authuser, c.project, c.ticket, h.suburl_votetck, c.upvotes, c.downvotes, c.currvote)))
            __M_writer('\n')
        __M_writer('                ')
        __M_writer(escape(show_ticket()))
        __M_writer('\n            </div>\n        </div> \n')
        if c.authusername != 'anonymous' and c.userpanes:
            __M_writer('        <div class="panel2">')
            __M_writer(escape(elements.user_panes(c.userpanes)))
            __M_writer('</div>\n')
        __M_writer('    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_show_ticket(context):
    context.caller_stack._push_frame()
    try:
        forms = _mako_get_namespace(context, 'forms')
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)

        def status_flow(tckstat):
            return render_status_flow(context, tckstat)

        def ticket_details(tckdet):
            return render_ticket_details(context, tckdet)

        __M_writer = context.writer()
        __M_writer('\n    ')
        tckdet = c.ticketdetail
        tckccodes = h.json.loads(c.tckccodes)
        bgcolor = h.tckcolorcode({'tck_statusname': tckdet['status'], 'tck_severityname': tckdet['severity'], 
           'tck_typename': tckdet['type']}, tckccodes)
        resolved = tckdet['status'] in c.ticketresolv and 'strike' or ''
        __M_writer('\n    <div class="zticketpage mr5">\n        <div class="pb2" style="height: 1.5em; border-bottom : 1px solid gray">\n            <div class="floatl">\n                <span class="fntbold ')
        __M_writer(escape(resolved))
        __M_writer(' ml10 mr10" style="font-size: 125%">\n                    Ticket ')
        __M_writer(escape(c.ticket.id))
        __M_writer(' :\n                </span>\n                <span name="tckvote"></span>\n            </div>\n            <div class="floatr dispinln">\n                <span name="depgraph" title="Ticket dependency graph"\n                      class="fgblue pointer mr5">Graph</span>\n                <span name="hiertree" title="Parent-children hierarchy"\n                      class="fgblue pointer mr5">Tree</span>\n                <a class="nodec mr5" href="#comments">Comments</a>\n            </div>\n        </div>\n        <div>\n            <div class="floatl" style="width:200px;">\n                <div>\n                    <div name="tattachblk"></div>\n                </div>\n                <div class="bclear">\n                    <div name="ttagblk"></div>\n                </div>\n                <div class="ml10 fntbold bclear">\n                    <a href="')
        __M_writer(escape(h.url_tagcloud))
        __M_writer('">Visit tag cloud ...</a>\n                </div>\n            </div>\n\n            <div class="calign vtop floatr"\n                 style="width : 150px; border-left : 4px solid #f2f2f2;">\n                ')
        __M_writer(escape(status_flow(c.ticketstatus)))
        __M_writer('\n            </div>\n\n            <div style="margin: 0px 150px 0px 200px;">\n                <div class="">\n                    <div name="graph" class="ml10 mr20 pt10 dispnone">\n                        <div class="bgaliceblue">\n                            <h4 class="">Dependency graph</h4>\n                        </div>\n                        <div style="max-width: 100%;\n                                    max-height: 400px; overflow: auto;">\n                        <object data="')
        __M_writer(escape(h.url_ticketgraph))
        __M_writer('" class="ml20"\n                                type="image/svg+xml"></object>\n                        </div>\n                    </div>\n                    <div name="tree" class="ml10 mr20 pt10 dispnone">\n                        <div class="bgaliceblue">\n                            <h4 class="">Task tree</h4>\n                        </div>\n                        <div style="max-width: 100%;\n                                    max-height: 400px; overflow: auto;">\n                        <object data="')
        __M_writer(escape(h.url_tickettree))
        __M_writer('" class="ml20"\n                                type="image/svg+xml"></object>\n                        </div>\n                    </div>\n                </div>\n\n                <div class="ml10 mr10">\n                    <div class="m2 p5 br5"\n                         style="border: 1px solid gray; top : 1.2em;\n                         margin-left: 0px; background: ')
        __M_writer(escape(bgcolor))
        __M_writer('"\n                         name="tckboard">\n                        ')
        __M_writer(escape(ticket_details(c.ticketdetail)))
        __M_writer('\n                    </div>\n                </div>\n\n                <div class="commentbox ml10 mr10">\n                    <div><a name="comments"></a></div>\n                    <div id="tcomments" class="" class="mt20"> </div>\n                    <div id="createtcmt_cntnr" style="border: 1px dotted gray"\n                         class="dispnone mb10 pl3 pt3 w80">\n                        <div class="posr fntbold">Add your comment :</div>\n                        ')
        __M_writer(escape(forms.form_createtcmt(c.authuser, c.project, c.ticket, h.suburl_createtcmt)))
        __M_writer('\n                    </div>\n                    <div id="updatetcmt_cntnr" style="border: 1px dotted gray"\n                         class="dispnone ml10 mr10 w80">\n                        ')
        __M_writer(escape(forms.form_updatetcmt(c.authuser, c.project, c.ticket, h.suburl_updatetcmt)))
        __M_writer('\n                    </div>\n                    <div id="replytcmt_cntnr" style="border: 1px dotted gray"\n                         class="dispnone ml10 mr10 w80">\n                        ')
        __M_writer(escape(forms.form_replytcmt(c.authuser, c.project, c.ticket, h.suburl_replytcmt)))
        __M_writer('\n                    </div>\n                </div>\n            </div>\n        </div>\n    </div>\n\n    <script type="text/javascript">\n        items_tckcomments = ')
        __M_writer(c.items_tckcomments)
        __M_writer('\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_status_flow(context, tckstat):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)

        def status_delimiter(ts, actualdt=None):
            return render_status_delimiter(context, ts, actualdt)

        def status_block(ts, refdt):
            return render_status_block(context, ts, refdt)

        __M_writer = context.writer()
        __M_writer('\n    ')
        tss = tckstat
        tss.reverse()
        currdt = h.timezone(c.authuser.timezone).localize(h.dt.datetime.utcnow())
        nextdt = h.timezone(c.authuser.timezone).localize(tss[0][3])
        __M_writer('\n    <div class="p3" style="border-bottom: 2px solid #f2f2f2;">\n        <div class="fntbold">Status Flow</div>\n        <div>(in reverse chonology)</div>\n    </div>\n    ')
        __M_writer(escape(status_block(tss[0], currdt)))
        __M_writer('\n')
        for ts in tss[1:]:
            __M_writer('        ')
            __M_writer(escape(status_delimiter(ts, nextdt)))
            __M_writer('\n        ')
            nextdt = h.timezone(c.authuser.timezone).localize(ts[3])
            __M_writer('\n        ')
            __M_writer(escape(status_block(ts, currdt)))
            __M_writer('\n')

        return ''
    finally:
        context.caller_stack._pop_frame()

    return


def render_bd_script(context):
    context.caller_stack._push_frame()
    try:
        parent = context.get('parent', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        __M_writer(escape(parent.bd_script()))
        __M_writer('\n\n    <script type="text/javascript">\n        dojo.addOnLoad( setup_ticket );\n        dojo.addOnLoad( function() {\n            dojo.subscribe(\n                \'tckbrd_chbg\',\n                function( name, bgcolor ) {\n                    n = dojo.query( \'div[name=\'+name+\']\' )[0];\n                    dojo.style( n, { background : bgcolor });\n                }\n            );\n        });\n        dojoaddOnLoad( \'initform_tckfav\' );\n        dojoaddOnLoad( \'initform_votetck\' );\n\n        dojo.addOnLoad( setup_userpanes );\n        dojo.addOnLoad( adjust_upheight );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()