# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/siteadmin/siteadmin.html.py
# Compiled at: 2010-07-16 08:52:00
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1279284720.419865
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/siteadmin/siteadmin.html'
_template_uri = '/derived/siteadmin/siteadmin.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['hd_script', 'bd_script', 'bd_body']
page_tooltips = [
 [
  'Help',
  "All the site-level customization and configuration are done in this page.\nEven if these configurations where done via the '.ini' file while app-setup,\nit can be modified here.\n"],
 [
  'Site-info',
  'This tab contains read-only information about application deployment.'],
 [
  'Site-config',
  "This tab contains global configuration fields. <b>Do not\nedit these fields if you don't know what you are doing. </b> Values entered\nhere are applicable throughout the application"],
 [
  'User-Management',
  'Users can be assigned site level permissions. These permissions does not\ncontrol access to project specific resources, instead it provides permission\nmanagement to site resources like license, guest-wiki etc...\nTo manage permissions for project resources, use the respective project\'s \nadmin tab. <a href="/help/pms">Know</a> more about Zeta\'s permission management\nsystem \n<br/><br/>\nDisabling users doesn\'t allow them to logging into the site.\n'],
 [
  'Project-Management',
  "\nEnabling and disabling projects doesn't have any effect now. This option is \nleft to address future requirements.\n"],
 [
  'Permissions',
  'Application resources are catagorised (like ticket, wiki ...) and governed by\ntheir respective permission names. These permission names can be seen in\nALL-CAPITALS. To help the administrators in adding and removing permissions,\n<b>permission grouping</b> feature is provided. Site-admin can add or remove\npermission names to permission groups. Permission groups should have names in\nall-small letters. <a href="/help/pms">Know</a> more about Zeta\'s permission\nmanagement system \n']]

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
        parent = context.get('parent', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        __M_writer(escape(parent.hd_script()))
        __M_writer('\n\n    <script type="text/javascript">\n\n    // Refresh select-options for user permissions\n    function refresh_userperms() {\n        var seluser_addpg = dojo.query( \'form#adduserperms select#addtouser\' )[0];\n        var seluser_delpg = dojo.query( \'form#deluserperms select#delfromuser\' )[0];\n\n        // Refresh addable permissions for currently selected users.\n        var u = userperms.itembyID( seluser_addpg.value );\n        if( u ) {\n            var x_permissions = userperms.store.getValues( u, \'x_permissions\').sort();\n            dojo.publish(\n                \'adduserpg\',\n                [ dojo.map( x_permissions, "return {val:item, txt:item}") ]\n            )\n        }\n\n        // Refresh removable permissions for currently selected users.\n        var u = userperms.itembyID( seluser_delpg.value );\n        if( u ) {\n            var permissions= userperms.store.getValues( u, \'permissions\').sort();\n            dojo.publish(\n                \'deluserpg\',\n                [ dojo.map( permissions, "return {val:item, txt:item}") ]\n            )\n        }\n    }\n    // Data store fetch on-complete for `userperms`\n    function userperms_oncomplete( items, req ) {\n        this.items = items;\n        refresh_userperms();\n        dojo.publish( \'flash\', [ \'hide\' ] );\n    }\n\n    // Data store fetch on-complete for `userstatus`\n    function userstatus_oncomplete( items, req ) {\n        this.items = items;\n        this.items[0].usernames = \n                this.store.getValues( this.items[0], \'usernames\' ).sort();\n        this.items[1].usernames = \n                this.store.getValues( this.items[1], \'usernames\' ).sort();\n\n        /* Refresh the view */\n        var enb_usernames = this.store.getValues(\n                                    this.itembyID( \'enabled\' ),\n                                    \'usernames\'\n                            );\n        var dis_usernames = this.store.getValues( \n                                    this.itembyID( \'disabled\' ),\n                                    \'usernames\'\n                            );\n        // ?? Seems to be a place holder ??\n        dojo.publish(\n            \'disable_user\',\n            [ dojo.map( enb_usernames, "return {val:item, txt:item}" ) ]\n        );\n        dojo.publish(\n            \'enable_user\',\n            [ dojo.map( dis_usernames, "return {val:item, txt:item}" ) ]\n        );\n        dojo.publish( \'flash\', [ \'hide\' ] );\n    }\n\n    // Data store fetch on-complete for `projectstatus`\n    function projectstatus_oncomplete( items, req ) {\n        this.items = items;\n        items[0].projectnames = this.store.getValues( items[0], \'projectnames\' \n                                                    ).sort();\n        items[1].projectnames = this.store.getValues( items[1], \'projectnames\' \n                                                    ).sort();\n\n        /* Refresh the view */\n        var enb_projnames = this.store.getValues(\n                                    this.itembyID( \'enabled\' ),\n                                    \'projectnames\'\n                            );\n        var dis_projnames = this.store.getValues( \n                                    this.itembyID( \'disabled\' ),\n                                    \'projectnames\'\n                            );\n        // ?? Seems to be a place holder ??\n        dojo.publish(\n            \'disable_project\',\n            [ dojo.map( enb_projnames, "return {val:item, txt:item}" ) ]\n        );\n        dojo.publish(\n            \'enable_project\',\n            [ dojo.map( dis_projnames, "return {val:item, txt:item}" ) ]\n        );\n        dojo.publish( \'flash\', [ \'hide\' ] );\n    }\n\n    // Data store fetch on-complete for `pgmap`\n    function pgmap_oncomplete( refresh_pglist, items, req ) {\n        this.items = items;\n        if ( refresh_pglist ) {\n            options = dojo.map( this.itemValues([\'perm_group\', \'pg_id\' ]).sort(),\n                                "return {val:item[1], txt:item[0]}" );\n            dojo.publish( \'pglist\', [ options ] );\n        }\n        refresh_perms();\n        dojo.publish( \'flash\', [ \'hide\' ] );\n    }\n    function refresh_perms() {\n        var select_pglist= dojo.query( \'select#pglist\' )[0];\n        var upg_id = dojo.query( \'form#updatepg input[name=perm_group_id]\' )[0];\n        var upg_pg = dojo.query( \'form#updatepg input[name=perm_group]\' )[0];\n        var apg_id = dojo.query( \'form#addpntopg input[name=perm_group_id]\' )[0];\n        var dpg_id = dojo.query( \'form#delpnfrompg input[name=perm_group_id]\' )[0];\n        var pg     = pgmap.itembyID( Number(select_pglist.value) );\n        if( pg ) {\n            var x_permnames = pgmap.store.getValues( pg, \'x_permnames\' ).sort();\n            var permnames   = pgmap.store.getValues( pg, \'permnames\' ).sort();\n            var pg_id    = pgmap.store.getValue( pg, \'pg_id\');\n            upg_pg.value = pgmap.store.getValue( pg, \'perm_group\');\n            upg_id.value = pg_id;\n            apg_id.value = pg_id;\n            dpg_id.value = pg_id;\n            dojo.publish(\n                \'addpntopg\',\n                [ dojo.map( x_permnames, "return {val:item, txt:item}" )]\n            );\n            dojo.publish(\n                \'delpnfrompg\',\n                [ dojo.map( permnames, "return {val:item, txt:item}" )]\n            );\n        }\n    }\n\n    function sadmin_forms() {\n        new zeta.ConfigTabs({\n                id: "satabs",\n                tabs: dojo.query( "div[name=satab]" )\n                }, dojo.query( "div[name=satabs]" )[0]\n            )\n        \n        userperms.fetch({\n            onComplete : userperms_oncomplete,\n            sort       : [{ attribute : \'username\' }]\n        });\n        pgmap.fetch({\n             onComplete : dojo.partial( pgmap_oncomplete, true ),\n             sort       : [{ attribute : \'perm_group\' }]\n        });\n    }\n    </script>\n')
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
        __M_writer('\n\n    <script type="text/javascript">\n        make_ifrs_pgmap();\n        make_ifrs_userperms();\n        make_ifrs_userstatus();\n        make_ifrs_projectstatus();\n        dojo.addOnLoad( sadmin_forms );\n        dojo.addOnLoad( initform_system );\n        dojo.addOnLoad( initform_adduserperms );\n        dojo.addOnLoad( initform_deluserperms );\n        dojo.addOnLoad( initform_userenb );\n        dojo.addOnLoad( initform_userdis );\n        dojo.addOnLoad( initform_prjenb );\n        dojo.addOnLoad( initform_prjdis );\n        dojo.addOnLoad( initform_createpg );\n        dojo.addOnLoad( initform_perms );\n\n        dojo.addOnLoad( setup_userpanes );\n        dojo.addOnLoad( adjust_upheight );\n    </script>\n')
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
        sorted = context.get('sorted', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        sp_usernames = c.usernames[:]
        'admin' in sp_usernames and sp_usernames.remove('admin')
        'anonymous' in sp_usernames and sp_usernames.remove('anonymous')
        pagebartext = '%s Site-Administration' % c.sitename
        tline = capture(elements.iconlink, h.url_sitetline, 'timeline', title='Site Timeline')
        __M_writer('\n    ')
        __M_writer(escape(elements.pagebar(pagebartext, rspans=[tline], tooltips=page_tooltips)))
        __M_writer('\n    <div id="bdy" class="w100">\n')
        if c.authusername == 'anonymous' or not c.userpanes:
            __M_writer('        <div id="sadmintabs" class="fullpanel1">\n')
        else:
            __M_writer('        <div id="sadmintabs" class="panel1">\n')
        __M_writer('    <div class="m10">\n    <div class="pb5">\n        <a href="')
        __M_writer(escape(h.url_uploadsitelogo))
        __M_writer('">Upload-sitelogo</a>\n    </div>\n    <div name="satabs">\n        <div id="siteinfo" class="dispnone" name="satab" title="SiteInfo"\n             selected="true">\n            ')
        __M_writer(escape(forms.form_systeminfo(c.authuser, c.sysentries, h.suburl_system)))
        __M_writer('</div>\n        <div id="siteconfig" class="dispnone" name="satab" title="SiteConfig"\n             selected="true">\n            ')
        __M_writer(escape(forms.form_systemconfig(c.authuser, c.sysentries, h.suburl_system)))
        __M_writer('</div>\n        <div id="usermng" class="dispnone" name="satab" title="Users">\n            <div class="disptrow w100 mt20">\n                <div class="disptcell ml10" style="width : 25em;">\n                    <b>Add permission groups to user : </b></div>\n                <div class="disptcell">\n                    ')
        __M_writer(escape(forms.form_add_userpermissions(c.authuser, sp_usernames, h.suburl_adduserperms, c.defuserperms[0], c.defuserperms[2])))
        __M_writer('\n                </div>\n                <div class="disptcell" style="padding-left: 50px; width: 15em;">\n                    ')
        __M_writer(escape(elements.helpboard('\n                        Manage site administration permissions for registered\n                        users. To know more about the purpose of each permissions\n                        <a href="/help/pms#Site-level%20Permissions">visit here</a>\n                    ')))
        __M_writer('\n                </div>\n            </div>\n            <hr class="bclear mt20"></hr>\n            <div class="disptrow w100 mt20">\n                <div class="disptcell ml10" style="width : 25em;">\n                    <b>Delete permission groups from user : </b></div>\n                <div class="disptcell">\n                    ')
        __M_writer(escape(forms.form_del_userpermissions(c.authuser, sp_usernames, h.suburl_deluserperms, c.defuserperms[0], c.defuserperms[1])))
        __M_writer('\n                </div>\n            </div>\n            <hr class="bclear mt20"></hr>\n            <div class="disptrow w100 mt20">\n                <div class="disptcell ml10" style="width : 25em;">\n                    <b>Enable users : </b></div>\n                <div class="disptcell">\n                    ')
        __M_writer(escape(forms.form_user_enable(c.authuser, h.suburl_enusers, sorted(c.userstatus['disabled']))))
        __M_writer('\n                </div>\n                <div class="disptcell" style="padding-left: 50px; width: 15em;">\n                    ')
        __M_writer(escape(elements.helpboard('\n                        By Disabling users site-administrators can prevent\n                        users from logging into the system. Enabling back,\n                        restores the user account\n                    ')))
        __M_writer('\n                </div>\n            </div>\n            <hr class="bclear mt20"></hr>\n            <div class="disptrow w100 mt20">\n                <div class="disptcell ml10" style="width : 25em;">\n                    <b>Disable users : </b></div>\n                <div class="disptcell">\n                    ')
        __M_writer(escape(forms.form_user_disable(c.authuser, h.suburl_disusers, sorted(c.userstatus['enabled']))))
        __M_writer('\n                </div>\n            </div>\n        </div>\n        <div id="projectmng" class="dispnone" name="satab" title="Projects">\n            <div class="disptrow w100 mt20">\n                <div class="disptcell ml10" style="width : 15em;">\n                    <b>Enable Projects : </b></div>\n                <div class="disptcell">\n                    ')
        __M_writer(escape(forms.form_project_enable(c.authuser, h.suburl_enprojects, sorted(c.projectstatus['disabled']))))
        __M_writer('\n                </div>\n                <div class="disptcell" style="padding-left: 50px; width: 15em;">\n                    ')
        __M_writer(escape(elements.helpboard('\n                        Disabling / Enabling project does not have any effect,\n                        as of now. Watch\n                        <a href="mailto:support@discoverzeta.com"\n                            >support@discoverzeta.com</a> for latest\n                        updates.\n                    ')))
        __M_writer('\n                </div>\n            </div>\n            <hr class="bclear mt20"></hr>\n            <div class="disptrow w100 mt20">\n                <div class="disptcell ml10" style="width : 15em;">\n                    <b>Disable Projects : </b></div>\n                <div class="disptcell">\n                    ')
        __M_writer(escape(forms.form_project_disable(c.authuser, h.suburl_disprojects, sorted(c.projectstatus['enabled']))))
        __M_writer('\n                </div>\n            </div>\n        </div>\n        <div id="userperms" class="dispnone" name="satab" title="Permissions">\n            <div class="disptrow w100 mt20">\n                <div class="disptcell ml10" style="width : 17em;">\n                    <b>Create permission group : </b></div>\n                <div class="disptcell">\n                    ')
        __M_writer(escape(forms.form_createpg(c.authuser, c.permnames, h.suburl_createpg)))
        __M_writer('\n                </div>\n                <div class="disptcell" style="padding-left: 50px; width: 15em;">\n                    ')
        __M_writer(escape(elements.helpboard('\n                        During installation time and subsequently when\n                        user base gets expanded, it might be convenient to\n                        logically group permissions and reduce the labour of\n                        adding or removing permissions from users / teams.\n                        Permission groups are merely a convenience feature.\n                    ')))
        __M_writer('\n                </div>\n            </div>\n            <hr class="bclear mt20"></hr>\n            <div class="disptrow w100 mt20">\n                <div class="disptcell ml10" style="width : 17em;">\n                    <b>Update Permission group : </b></div>\n                <div class="disptcell">\n                    ')
        __M_writer(escape(forms.form_updatepg(c.authuser, h.suburl_updatepg, h.suburl_addpntopg, h.suburl_delpnfrompg)))
        __M_writer('\n                </div>\n            </div>\n        </div>\n        <div id="license" class="dispnone" name="satab" title="License">\n            <div class="p5">\n                <a title="Create new license"\n                   href="')
        __M_writer(escape(h.url_crlic))
        __M_writer('">New license</a>\n            </div>\n            ')
        __M_writer(escape(elements.lictable1(c.licenselist, c.liceditable)))
        __M_writer('\n            <div name="rmlic" class="dispnone">\n                ')
        __M_writer(escape(forms.form_removelic_h(c.authuser, h.suburl_rmlic)))
        __M_writer('\n            </div>\n        </div>\n    </div>\n    </div>\n    </div>\n')
        if c.authusername != 'anonymous' and c.userpanes:
            __M_writer('        <div class="panel2">')
            __M_writer(escape(elements.user_panes(c.userpanes)))
            __M_writer('</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()