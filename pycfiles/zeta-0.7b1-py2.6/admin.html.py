# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/projects/admin.html.py
# Compiled at: 2010-07-10 01:45:23
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278740723.656763
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/projects/admin.html'
_template_uri = '/derived/projects/admin.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['hd_script', 'bd_script', 'bd_body']
page_tooltips = [
 [
  'Help',
  'Only project administrator can access this page. Use this page to,\nconfigure project, add/modify/remove project milestones, components and\nversions. Setup project teams and team-permissions.\n'],
 [
  'Project',
  'Upload project logo and icon which will be used where ever relevant.\nOne such case is the header element in the layout, where the project logo\nis displayed on top-right corner of the page. Tickets, wiki pages,\nversion controls, reviews are always associated with a project.\n'],
 [
  'Components',
  'Divide project into components, assigining owner to each one of them.\nTickets can be associated with a component.\n'],
 [
  'Milestones',
  "Create and describe milestones with due-date. Milestones can be closed by\n'cancelling' or 'completing' it and providing a closing remark.\nTickets can be associated with project milestone.\n"],
 [
  'Versions',
  'Versions can be used to track release, both internal and external.\nTickets can be associated with project version.\n'],
 [
  'Teams',
  'Team names are common to all projects. Project\'s administrator\ncan assign user as part of one or more team, one can view\nteam as a role the user is expected to play in the project.\n<br/>\nProject-wise permission are managed via teams.  Registered users \nwho are not associated with a project (i.e) who are not\npart of a project\'s team will be classified as \'non-members\'\n(a special team created by default). Thus the administrator can\nmanage the permissions to these users via \'non-members\'.\n<a href="/help/pms">Know more about permission system</a>\n'],
 [
  'Timeline',
  "Timeline of project's administrative activities."]]

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
        __M_writer('\n\n\n\n')
        __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_hd_script(context):
    context.caller_stack._push_frame()
    try:
        map = context.get('map', UNDEFINED)
        c = context.get('c', UNDEFINED)
        parent = context.get('parent', UNDEFINED)
        h = context.get('h', UNDEFINED)
        str = context.get('str', UNDEFINED)
        x = context.get('x', UNDEFINED)
        sorted = context.get('sorted', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        __M_writer(escape(parent.hd_script()))
        __M_writer('\n\n    <script type="text/javascript">\n    ')
        project_id = c.project and c.project.id or ''
        projusers = map(lambda x: {'val': x, 'txt': x}, sorted(c.projusers))
        adminuser = c.project.admin.username
        __M_writer('\n\n    /* Gotcha : The *_oncomplete and refresh_* functions are globally scoped\n     * since they are required across several callbacks.\n     */\n    projusers = ')
        __M_writer(h.json.dumps(projusers))
        __M_writer(';\n    adminuser = ')
        __M_writer(h.json.dumps(adminuser))
        __M_writer(';\n\n    // Data store fetch on-complete for `pcomplist`\n    function pcomplist_oncomplete( items, req ) {\n        this.items = items;\n        var pcomps  = pcomplist.itemValues( [\'id\', \'componentname\'] );\n        var selpcomp_updt = dojo.query( \'div#prjcomponents select#updtpcomp\')[0];\n        var options = dojo.map( pcomps, "return {val:item[0], txt:item[1]}" );\n        dojo.publish( \'updtpcomp\', [ options, selpcomp_updt.value ] );\n        dojo.publish( \'rmpcomp\', [ options, null ] );\n        refresh_pcompdetail();\n        dojo.publish( \'flash\', [ \'hide\' ] );\n    }\n    function refresh_pcompdetail() {\n        var selpcomp_updt = dojo.query( \'div#prjcomponents select#updtpcomp\')[0];\n        var pcomp  = pcomplist.itembyID( selpcomp_updt.value );\n        if ( pcomp ) {\n            var id    = pcomplist.store.getValue( pcomp, \'id\' );\n            var name  = pcomplist.store.getValue( pcomp, \'componentname\' );\n            var owner = pcomplist.store.getValue( pcomp, \'owner\' );\n            var desc  = pcomplist.store.getValue( pcomp, \'description\' );\n\n            dojo.query( \'input[name=component_id]\', form_updatepcomp\n                      )[0].value = id;\n            dojo.query( \'input[name=componentname]\', form_updatepcomp\n                      )[0].value = name;\n            dojo.query( \'span[name=ownername]\', form_updatepcomp\n                      )[0].innerHTML = owner;\n            dojo.query( \'textarea[name=description]\', form_updatepcomp\n                      )[0].value = desc;\n            dojo.publish( \'updtpcompowners\', [ projusers, owner ]);\n            dijit.byId( "updtpcompdesc" ).resize();\n        }\n    }\n    function projcomp() {\n        /* Setup component selection */\n        var selpcomp_updt    = dojo.query( \'div#prjcomponents select#updtpcomp\')[0];\n        function updtpcomp_onchange( e ) {\n            refresh_pcompdetail();\n            dojo.stopEvent(e);\n        }\n        new ZSelect( selpcomp_updt, \'updtpcomp\', updtpcomp_onchange )\n    }\n\n    // Data store fetch on-complete for `mstnlist`\n    function mstnlist_oncomplete( items, req ) {\n        this.items = items;\n        var mstns   = mstnlist.itemValues( [\'id\', \'milestone_name\' ] );\n        var options = dojo.map( mstns, "return {val:item[0], txt:item[1]}" );\n        var selmstn_updt = dojo.query( \'div#prjmilestones select#updtmstn\')[0];\n        dojo.publish( \'updtmstn\', [ options, selmstn_updt.value ] );\n        dojo.publish( \'rmmstn\', [ options, null ] );\n        refresh_mstndetail();\n        dojo.publish( \'flash\', [ \'hide\' ] );\n    }\n    function refresh_mstndetail() {\n        var selmstn_updt = dojo.query( \'div#prjmilestones select#updtmstn\')[0];\n        var mstn = mstnlist.itembyID( selmstn_updt.value );\n        var duedate = dijit.byId( \'updtduedate\' );\n        if ( mstn ) {\n            var id       = mstnlist.store.getValue( mstn, \'id\' );\n            var name     = mstnlist.store.getValue( mstn, \'milestone_name\' );\n            var due_date = mstnlist.store.getValues( mstn, \'due_date\' );\n            var desc     = mstnlist.store.getValue( mstn, \'description\' );\n            var closr    = mstnlist.store.getValue( mstn, \'closing_remark\' );\n            var mstatus  = mstnlist.store.getValue( mstn, \'status\' );\n\n            dojo.query( \'input[name=milestone_id]\', form_updatemstn\n                      )[0].value = id;\n            dojo.query( \'input[name=milestone_name]\', form_updatemstn\n                      )[0].value = name;\n            if( due_date.length ) {\n                dd = new Date( due_date[0], due_date[1]-1, due_date[2] );\n                duedate.setValue( dd );\n            } else {\n                duedate.setValue( \'\' );\n            }\n\n            dojo.query( \'textarea[name=description]\', form_updatemstn\n                      )[0].value = desc;\n            dijit.byId( "updtmstndesc" ).resize();\n            cremark = dojo.query( \'textarea[name=closing_remark]\',\n                                  form_updatemstn\n                                )[0]\n            cremark.value = closr;\n            var cancelled = dijit.byId( \'mstnstatus1\' );\n            var completed = dijit.byId( \'mstnstatus2\' );\n            completed.setChecked( false );\n            cancelled.setChecked( false );\n            if ( mstatus == \'cancelled\' ) {\n                cancelled.setChecked( true );\n            } else if ( mstatus == \'completed\' ) {\n                completed.setChecked( true );\n            }\n        }\n    }\n    function projmilestones() {\n        /* Setup milestone selection */\n        var selmstn_updt   = dojo.query( \'div#prjmilestones select#updtmstn\')[0];\n        function updtmstn_onchange( e ) {\n            refresh_mstndetail();\n            dojo.stopEvent(e);\n        }\n        new ZSelect( selmstn_updt, \'updtmstn\', updtmstn_onchange )\n    }\n\n    // Data store fetch on-complete for `verlist`\n    function verlist_oncomplete( items, req ) {\n        this.items = items;\n        var vers = verlist.itemValues( [ \'id\', \'version_name\' ] );\n        var options = dojo.map( vers, "return {val:item[0], txt:item[1]}" );\n        var selver_updt = dojo.query( \'div#prjversions select#updtver\')[0];\n        dojo.publish( \'updtver\', [ options, selver_updt.value ] );\n        dojo.publish( \'rmver\', [ options, null ] );\n        refresh_verdetail();\n        dojo.publish( \'flash\', [ \'hide\' ] );\n    }\n    function refresh_verdetail() {\n        var selver_updt = dojo.query( \'div#prjversions select#updtver\')[0];\n        var ver = verlist.itembyID( selver_updt.value );\n        if ( ver ) {\n            var id   = verlist.store.getValue( ver, \'id\' );\n            var name = verlist.store.getValue( ver, \'version_name\' );\n            var desc = verlist.store.getValue( ver, \'description\' );\n\n            dojo.query( \'input[name=version_id]\', form_updatever\n                      )[0].value = id;\n            dojo.query( \'input[name=version_name]\', form_updatever\n                      )[0].value = name;\n            dojo.query( \'textarea[name=description]\', form_updatever\n                      )[0].value = desc;\n            dijit.byId( "updtverdesc" ).resize();\n        }\n    }\n    function projversions() {\n        /* Setup version selection */\n        var selver_updt = dojo.query( \'div#prjversions select#updtver\')[0];\n        function updtver_onchange( e ) {\n            refresh_verdetail();\n            dojo.stopEvent(e);\n        }\n        new ZSelect( selver_updt, \'updtver\', updtver_onchange )\n    }\n\n    // Data store fetch on-complete for `projectteams`\n    function projectteams_oncomplete( items, req ) {\n        this.items = items;\n        refresh_projuser( \'toadd,todel\' );\n        dojo.publish( \'flash\', [ \'hide\' ] );\n\n        // When ever a fresh list is fetched, re-populate the visual elements\n        // with the fresh project user list.\n        var _projusers = {}\n        for( i=0; i < this.items.length; i++ ) {\n            var item     = this.items[i];\n            var usersids = this.store.getValues( item, \'usersids\' );\n            for( j=0; j < usersids.length; j++ ) {\n                _projusers[usersids[j][1]] = true;\n            }\n        }\n        _projusers= keys( _projusers )\n        _projusers[ _projusers.length ] = adminuser // add project admin\n        _projusers.sort();\n        projusers = dojo.map( _projusers, "return { val: item, txt: item }" )\n        dojo.publish( \'projusers\', [ projusers ] );\n        if( pcomplist.items ) {\n            var selpcomp_updt = dojo.query( \'div#prjcomponents select#updtpcomp\')[0];\n            var pcomp  = pcomplist.itembyID( selpcomp_updt.value );\n            if( pcomp ) {\n                dojo.publish(\n                    \'updtpcompowners\',\n                    [ projusers, pcomplist.store.getValue( pcomp, \'owner\' ) ]\n                );\n            }\n        }\n    }\n    function refresh_projuser( dostr ) {\n        var aselect_tt = dojo.query( \'form#addprjteam select[name=team_type]\' )[0];\n        var ateam = projectteams.itembyID( aselect_tt.value );\n        if( ateam ) {\n            var x_usernames = projectteams.store.getValues( ateam, \'x_usernames\');\n            if( /toadd/.test( dostr )) {\n                dojo.publish(\n                    \'addprojuser\',\n                    [ dojo.map( x_usernames, "return {val:item, txt:item}")]\n                );\n            }\n        }\n\n        var dselect_tt = dojo.query( \'form#delprjteam select[name=team_type]\' )[0];\n        var dteam = projectteams.itembyID( dselect_tt.value );\n        if( dteam ) {\n            var usersids = projectteams.store.getValues( dteam, \'usersids\');\n            if ( /todel/.test( dostr )) {\n                dojo.publish(\n                    \'delprojuser\',\n                    [ dojo.map( usersids, "return {val:item[0], txt:item[1]}" )]\n                );\n            }\n        }\n    }\n\n    // Data store fetch on-complete for `teamperms`\n    function teamperms_oncomplete( items, req ) {\n        this.items = items;\n        refresh_teamperms( \'toadd,todel\' );\n        dojo.publish( \'flash\', [ \'hide\' ] );\n    }\n    function refresh_teamperms( dostr ) {\n        var aselect_tt = dojo.query( \'form#addteamperms select[name=team_type]\')[0];\n        var dselect_tt = dojo.query( \'form#delteamperms select[name=team_type]\')[0];\n        var ateam = teamperms.itembyID( aselect_tt.value );\n        var dteam = teamperms.itembyID( dselect_tt.value );\n        var x_permissions = teamperms.store.getValues( ateam, \'x_permissions\' );\n        var permsids      = teamperms.store.getValues( dteam, \'permsids\' );\n        if( /toadd/.test( dostr )) {\n            dojo.publish(\n                \'addpgtoteam\',\n                [ dojo.map( x_permissions, "return {val:item, txt:item}")]\n            );\n        }\n        if ( /todel/.test( dostr )) {\n            dojo.publish(\n                \'delpgfromteam\',\n                [ dojo.map( permsids, "return {val:item[0], txt:item[1]}" )]\n            );\n        }\n    }\n\n    function padmin_forms() {\n        /* Initial Fetching of JSON objects */\n        make_ifrs_pcomplist( \'')
        __M_writer(h.url_pcomplist)
        __M_writer("' );\n        make_ifrs_mstnlist( '")
        __M_writer(h.url_mstnlist)
        __M_writer("' );\n        make_ifrs_verlist( '")
        __M_writer(h.url_verlist)
        __M_writer("' );\n        make_ifrs_projectteams( '")
        __M_writer(h.url_projectteams)
        __M_writer("' );\n        make_ifrs_teamperms( '")
        __M_writer(h.url_teamperms)
        __M_writer('\' );\n\n        pcomplist.fetch({ onComplete : pcomplist_oncomplete,\n                          sort : [ { attribute : \'componentname\' } ]\n                        })\n        mstnlist.fetch({ onComplete : mstnlist_oncomplete,\n                         sort : [ { attribute : \'milestone_name\' } ]\n                       });\n        verlist.fetch({ onComplete : verlist_oncomplete,\n                        sort : [ { attribute : \'version_name\' } ]\n                      });\n        projectteams.fetch({ onComplete : projectteams_oncomplete });\n        teamperms.fetch({ onComplete : teamperms_oncomplete });\n\n        /* Setup tabs */\n        new zeta.ConfigTabs({\n            id: "patabs",\n            tabs: dojo.query( "div[name=patab]" )\n            }, dojo.query( "div[name=patabs]" )[0]\n        )\n        \n        /* Project Logo */\n        new zeta.Attachments(\n            { user: [ \'')
        __M_writer(escape(str(c.authuser.id)))
        __M_writer("', '")
        __M_writer(escape(c.authuser.username))
        __M_writer("' ],\n              id: 'logoattachblk',\n              addform: [ 'addprjlogo', '")
        __M_writer(h.suburl_addprjlogo)
        __M_writer("' ],\n              delform: [ 'delprjlogo', '")
        __M_writer(h.suburl_delprjlogo)
        __M_writer("' ],\n              attachon: [ '")
        __M_writer(escape(str(project_id)))
        __M_writer("', 'project_id' ],\n              editable: ")
        __M_writer(escape([0, 1][(c.logo_editable == True)]))
        __M_writer(",\n              url: '")
        __M_writer(h.url_prjlrefresh)
        __M_writer("',\n              attachs: ")
        __M_writer(h.json.dumps(c.logoattach))
        __M_writer(',\n              label: \'Project logo\'\n            }, dojo.query( "div[name=projlogo]" )[0]\n        )\n\n        /* Project Icon */\n        new zeta.Attachments(\n            { user: [ \'')
        __M_writer(escape(str(c.authuser.id)))
        __M_writer("', '")
        __M_writer(escape(c.authuser.username))
        __M_writer("' ],\n              id: 'iconattachblk',\n              addform: [ 'addprjicon', '")
        __M_writer(h.suburl_addprjicon)
        __M_writer("' ],\n              delform: [ 'delprjicon', '")
        __M_writer(h.suburl_delprjicon)
        __M_writer("' ],\n              attachon: [ '")
        __M_writer(escape(str(project_id)))
        __M_writer("', 'project_id' ],\n              editable: ")
        __M_writer(escape([0, 1][(c.icon_editable == True)]))
        __M_writer(",\n              url: '")
        __M_writer(h.url_prjirefresh)
        __M_writer("',\n              attachs: ")
        __M_writer(h.json.dumps(c.iconattach))
        __M_writer(',\n              label: \'Project icon\'\n              }, dojo.query( "div[name=projicon]" )[0]\n        )\n\n        projcomp();\n        projmilestones();\n        projversions();\n    }\n\n    </script>\n')
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
        __M_writer('\n\n    <script type="text/javascript">\n        dojo.addOnLoad( padmin_forms );\n        dojoaddOnLoad( \'initform_projfav\' );\n        dojoaddOnLoad( \'initform_projectinfo\' );\n        dojoaddOnLoad( \'initform_createpcomp\' );\n        dojoaddOnLoad( \'initform_updatepcomp\' );\n        dojoaddOnLoad( \'initform_rmpcomp\' );\n        dojoaddOnLoad( \'initform_createmstn\' );\n        dojoaddOnLoad( \'initform_updatemstn\' );\n        dojoaddOnLoad( \'initform_rmmstn\' );\n        dojoaddOnLoad( \'initform_createver\' );\n        dojoaddOnLoad( \'initform_updatever\' );\n        dojoaddOnLoad( \'initform_rmver\' );\n        dojoaddOnLoad( \'initform_addprjteam\' );\n        dojoaddOnLoad( \'initform_delprjteam\' );\n        dojoaddOnLoad( \'initform_addteamperms\' );\n        dojoaddOnLoad( \'initform_delteamperms\' );\n\n        dojo.addOnLoad( setup_userpanes );\n        dojo.addOnLoad( adjust_upheight );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bd_body(context):
    context.caller_stack._push_frame()
    try:
        forms = _mako_get_namespace(context, 'forms')
        capture = context.get('capture', UNDEFINED)
        c = context.get('c', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')
        h = context.get('h', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        ctxt_title = "'%s' - Administration" % c.project.projectname
        fav = capture(elements.favoriteicon, 'favproj')
        tline = capture(elements.iconlink, h.url_projadmtimeline, 'timeline', title='Timeline')
        ctxt_spans = [fav, '<span class="fggray fntbold">%s</span>' % ctxt_title]
        rspans = [tline]
        __M_writer('\n    ')
        __M_writer(escape(elements.mainnav()))
        __M_writer('\n    ')
        __M_writer(escape(elements.contextnav(ctxt_spans, tooltips=page_tooltips, rspans=rspans)))
        __M_writer('\n    <div id="bdy" class="w100">\n')
        if c.userpanes:
            __M_writer('    <div class="panel1">\n')
        else:
            __M_writer('    <div class="fullpanel1">\n')
        __M_writer('\n    ')
        __M_writer(escape(forms.form_projfav(c.authuser, c.project, h.suburl_projfav, c.isfavorite and 'delfavuser' or 'addfavuser')))
        __M_writer('\n\n    <div class="m10">\n    <div name="patabs">\n        <div id="projectinfo" class="dispnone" name="patab" title="Project"\n             selected="true">\n            <div name="projlogo"></div>\n            <div name="projicon"></div>\n            <div class="bclear ml50">\n            ')
        __M_writer(escape(forms.form_projectinfo(c.authuser, c.project, c.licensenames, c.usernames, h.url_license, h.suburl_projectinfo)))
        __M_writer('\n            </div>\n        </div>\n        <div id="prjcomponents" class="dispnone" name="patab" title="Components">\n            <div class="disptrow w100 mt20">\n                <div class="disptcell vtop ml10" style="width : 20em;">\n                    <b>New component : </b></div>\n                <div class="disptcell">\n                    ')
        __M_writer(escape(forms.form_createpcomp(c.authuser, c.project, c.projusers, h.suburl_createpcomp)))
        __M_writer('\n                </div>\n            </div>\n            <hr class="bclear mt20"></hr>\n            <div class="disptrow w100 mt20">\n                <div class="disptcell vtop ml10" style="width : 20em;">\n                    <b>Update component : </b></div>\n                <div class="disptcell">\n                    ')
        __M_writer(escape(forms.form_updatepcomp(c.authuser, c.project, c.projusers, c.pcomplist, h.suburl_updatepcomp)))
        __M_writer('\n                </div>\n            </div>\n            <hr class="bclear mt20"></hr>\n            <div class="disptcell w100 mt20">\n                <div class="disptcell vtop ml10" style="width : 20em;">\n                    <b>Remove components : </b></div>\n                <div class="disptcell">\n                    ')
        __M_writer(escape(forms.form_rmpcomp(c.authuser, c.project, h.suburl_rmpcomp)))
        __M_writer('\n                </div>\n            </div>\n        </div>\n        <div id="prjmilestones" class="dispnone" name="patab" title="Milestones">\n            <div class="disptrow w100 mt20">\n                <div class="disptcell vtop ml10" style="width : 20em;">\n                    <b>New milestone : </b></div>\n                <div class="disptcell">\n                    ')
        __M_writer(escape(forms.form_createmstn(c.authuser, c.project, h.suburl_createmstn)))
        __M_writer('\n                </div>\n            </div>\n            <hr class="bclear mt20"></hr>\n            <div class="disptrow w100 mt20">\n                <div class="disptcell vtop ml10" style="width : 20em;">\n                    <b>Update milestone : </b></div>\n                <div class="disptcell">\n                    ')
        __M_writer(escape(forms.form_updatemstn(c.authuser, c.project, c.mstnlist, h.suburl_updatemstn)))
        __M_writer('\n                </div>\n            </div>\n            <hr class="bclear mt20"></hr>\n            <div class="disptrow w100 mt20">\n                <div class="disptcell vtop ml10" style="width : 20em;">\n                    <b>Remove milestone : </b></div>\n                <div class="disptcell">\n                    ')
        __M_writer(escape(forms.form_rmmstn(c.authuser, c.project, h.suburl_rmmstn)))
        __M_writer('\n                </div>\n            </div>\n        </div>\n        <div id="prjversions" class="dispnone" name="patab" title="Versions">\n            <div class="disptrow w100 mt20">\n                <div class="disptcell vtop ml10" style="width : 20em;">\n                    <b>New version : </b></div>\n                <div class="disptcell">\n                    ')
        __M_writer(escape(forms.form_createver(c.authuser, c.project, h.suburl_createver)))
        __M_writer('\n                </div>\n            </div>\n            <hr class="bclear mt20"></hr>\n            <div class="disptrow w100 mt20">\n                <div class="disptcell vtop ml10" style="width : 20em;">\n                    <b>Update version : </b></div>\n                <div class="disptcell">\n                    ')
        __M_writer(escape(forms.form_updatever(c.authuser, c.project, c.verlist, h.suburl_updatever)))
        __M_writer('\n                </div>\n            </div>\n            <hr class="bclear mt20"></hr>\n            <div class="disptrow w100 mt20">\n                <div class="disptcell vtop ml10" style="width : 20em;">\n                    <b>Remove versions : </b></div>\n                <div class="disptcell">\n                    ')
        __M_writer(escape(forms.form_rmver(c.authuser, c.project, h.suburl_rmver)))
        __M_writer('\n                </div>\n            </div>\n        </div>\n        <div id="prjteams" class="dispnone" name="patab" title="Teams">\n            <div class="disptrow w100 mt20">\n                <div class="disptcell vtop ml10" style="width : 20em;">\n                    <b>Add users to team : </b></div>\n                <div class="disptcell">\n                    ')
        __M_writer(escape(forms.form_addprjteam(c.authuser, c.project, c.teamtypes, c.defteamtype, c.x_teamusers, h.suburl_addprjteam)))
        __M_writer('\n                </div>\n            </div>\n            <hr class="bclear mt20"></hr>\n            <div class="disptrow w100 mt20">\n                <div class="disptcell vtop ml10" style="width : 20em;">\n                    <b>Remove users from team : </b></div>\n                <div class="disptcell">\n                    ')
        __M_writer(escape(forms.form_delprjteam(c.authuser, c.project, c.teamtypes, c.defteamtype, c.teamusers, h.suburl_delprjteam)))
        __M_writer('\n                </div>\n            </div>\n        </div>\n        <div id="prjpermissions" class="dispnone" name="patab" title="Permissions">\n            <div class="disptrow w100 mt20">\n                <div class="disptcell vtop ml10" style="width : 20em;">\n                    <b>Add permissions to team : </b></div>\n                <div class="disptcell">\n                    ')
        __M_writer(escape(forms.form_addteamperms(c.authuser, c.project, c.teamtypes_p, c.defteamtype, c.x_teampgroups, h.suburl_addteamperms)))
        __M_writer('\n                </div>\n            </div>\n            <hr class="bclear mt20"></hr>\n            <div class="disptrow w100 mt20">\n                <div class="disptcell vtop ml10" style="width : 20em;">\n                    <b>Remove permissions from team : </b></div>\n                <div class="disptcell">\n                    ')
        __M_writer(escape(forms.form_delteamperms(c.authuser, c.project, c.teamtypes_p, c.defteamtype, c.teampgroups, h.suburl_delteamperms)))
        __M_writer('\n                </div>\n            </div>\n        </div>\n    </div>\n    </div>\n\n    </div>\n')
        if c.userpanes:
            __M_writer('    <div class="panel2">')
            __M_writer(escape(elements.user_panes(c.userpanes)))
            __M_writer('</div>\n')
        __M_writer('    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()