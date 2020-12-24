# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/component/forms.html.py
# Compiled at: 2010-07-09 03:04:59
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278659099.424059
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/component/forms.html'
_template_uri = '/component/forms.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['form_attachssummary', 'form_createrev', 'form_tckparent', 'form_updatetcmt', 'form_addattachs', 'form_tcksummary', 'form_systeminfo', 'form_tckpromptuser', 'form_addparts', 'form_configticket', 'form_revwfav', 'form_del_userpermissions', 'form_rmver', 'form_createvcs', 'form_addtckfilter', 'input_text', 'form_revwauthor', 'input_password', 'form_updatever', 'form_editsw', 'input_checkbox', 'form_createwcmt', 'input_hidden', 'form_createpcomp', 'form_project_disable', 'form_updaterset', 'multiselect', 'select_revwnature', 'form_deltckfilter', 'form_rmmstn', 'form_delteamperms', 'form_wikifav', 'form_addtorset', 'form_deletemount_e', 'form_addprjperms', 'form_selectticket', 'form_rmpcomp', 'form_configtst', 'form_wikitype', 'label', 'form_creatercmt', 'form_configvcs', 'form_updatemount', 'form_updatepcomp', 'form_tckversion', 'form_updatelicense_h', 'input_radio', 'form_updatepg', 'form_selectsavfilter', 'form_approve_userrelations', 'input_button', 'form_wikicontent', 'form_addprjteam', 'form_user_disable', 'form_deletemount', 'form_createproject', 'form_wikisummary', 'form_inviteuser', 'form_delprjperms', 'form_selectwikipage', 'fieldhelp', 'form_selectfilerevision', 'form_sitelogo', 'form_updatemstn', 'form_createmstn', 'form_project_enable', 'select', 'input_submit', 'form_tckblockedby', 'form_tckseverity', 'form_projfav', 'form_projectinfo', 'form_tckblocking', 'form_selectwikiversion', 'form_updatewcmt', 'form_selectrevw', 'form_createpg', 'form_removelic_h', 'form_configrev', 'form_createmount_e', 'form_selectrset', 'form_createticket', 'form_selectvcs', 'form_licenselist', 'form_addteamperms', 'textarea', 'form_attachstags', 'form_votewiki', 'form_tckdescription', 'form_searchbox', 'form_delparts', 'form_edittck', 'form_userreg', 'form_tckcomponent', 'form_user_enable', 'form_delprjteam', 'form_systemconfig', 'form_tckfav', 'form_createlicense', 'form_tcktype', 'form_updtpass', 'form_tckmilestone', 'form_search', 'form_forgotpass', 'form_createrset', 'form_createtcmt', 'form_delfromrset', 'form_createver', 'form_closerev', 'form_configwiki', 'form_del_userrelations', 'form_votetck', 'input_file', 'form_wikidiff', 'form_createmount', 'form_replyrcmt', 'form_revwmoderator', 'form_replywcmt', 'form_replytcmt', 'form_resetpass', 'form_changetckst', 'input_image', 'form_add_userrelations', 'select_revwaction', 'form_accountinfo', 'form_processrcmt', 'input_reset', 'form_deletevcs', 'form_add_userpermissions']
restrict_kwargs = lambda kwargs, allowed_keys: [ kwargs.pop(k) for k in kwargs.keys() if k not in allowed_keys ]
make_attrs = lambda kwargs: (' ').join([ k + '="' + kwargs[k] + '"' for k in kwargs ])
general_attrs = ['name', 'value', 'id', 'class', 'title', 'style']
inputtext_attrs = general_attrs + ['disabled', 'maxlength', 'readonly', 'size']
inputpass_attrs = general_attrs + ['disabled', 'maxlength', 'size']
inputchkbox_attrs = general_attrs + ['checked', 'disabled']
inputradio_attrs = general_attrs + ['checked', 'disabled']
inputfile_attrs = general_attrs + ['disabled', 'size']
inputbutton_attrs = general_attrs
inputhidden_attrs = general_attrs
inputimage_attrs = general_attrs + ['alt', 'disabled', 'src', 'value']
textarea_attrs = general_attrs + ['rows', 'cols', 'disabled', 'readonly', 'tatype']
select_attrs = general_attrs + ['multiple', 'size', 'disabled']
multiselect_attrs = general_attrs + ['size', 'disabled']
label_attrs = [
 'for']
infofields = [
 'product_name', 'product_version', 'database_version',
 'envpath',
 'sitename', 'siteadmin', 'timezone', 'unicode_encoding']
cnffields = [
 'welcomestring', 'specialtags', 'projteamtypes',
 'tickettypes', 'ticketseverity', 'ticketstatus', 'ticketresolv',
 'wikitypes', 'def_wikitype', 'reviewactions', 'reviewnatures',
 'vcstypes', 'googlemaps', 'strictauth',
 'regrbyinvite', 'invitebyall', 'interzeta', 'userrel_types']

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
        __M_writer('\n')
        __M_writer('\n')
        __M_writer('\n')
        __M_writer('\n')
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
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
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
        __M_writer('\n\n\n')
        __M_writer('\n')
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
        __M_writer('\n\n')
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
        __M_writer('\n\n')
        __M_writer('\n')
        __M_writer('\n\n')
        __M_writer('\n\n\n')
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
        __M_writer('\n\n\n')
        __M_writer('\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_attachssummary(context, u, action):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form id="attachssummary" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='attachment_id')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='summary')))
        __M_writer('\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_createrev(context, u, p, rsets, action, projusers, usernames, forsrc=[], forversion=None):
    context.caller_stack._push_frame()
    try:

        def fieldhelp(help='', fhstyle=''):
            return render_fieldhelp(context, help, fhstyle)

        def input_reset(**kwargs):
            return render_input_reset(context, **kwargs)

        def multiselect(**kwargs):
            return render_multiselect(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        def select(**kwargs):
            return render_select(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        ru_help = 'enter the resource url to be reviewed'
        rv_help = 'nth version to review'
        ra_help = 'author should take action on review comments'
        rsets = [['', '--Select-ReviewSet--']] + rsets
        __M_writer('\n\n    <form id="createrev" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='moderator', value=str(u.username))))
        __M_writer('\n    <div class="form">\n        <div class="field">\n            <div class="label" style="width : 12em;">Review Set :</div>\n            <div class="ftbox">\n                ')
        __M_writer(escape(select(name='rset_id', id='rset_id', options=rsets)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 12em;">Resource Url :</div>\n')
        if forsrc == []:
            __M_writer('                <div class="ftbox" required="true">\n                    ')
            __M_writer(escape(input_text(name='resource_url', id='resource_url')))
            __M_writer('\n                    <br></br>\n                    ')
            __M_writer(escape(fieldhelp(ru_help)))
            __M_writer('\n                </div>\n')
        for rurl in forsrc:
            __M_writer('                <div>\n                ')
            __M_writer(escape(input_text(name='resource_url', value=rurl, readonly='readonly', size='40')))
            __M_writer('\n                </div>\n')

        __M_writer('        </div>\n        <div class="field">\n            <div class="label" style="width : 12em;">Version :</div>\n')
        if forversion:
            __M_writer('                ')
            __M_writer(escape(input_text(name='version', value=str(forversion), readonly='readonly')))
            __M_writer('\n')
        else:
            __M_writer('                <div class="ftbox" regExp="[0-9]*" required="true">\n                    ')
            __M_writer(escape(input_text(name='version', id='version')))
            __M_writer('\n                    <br></br>\n                    ')
            __M_writer(escape(fieldhelp(rv_help)))
            __M_writer('\n                </div>\n')
        __M_writer('        </div>\n        <div class="field">\n            <div class="label" style="width : 12em;">Author :</div>\n            <div class="fselect" required="true">\n                ')
        __M_writer(escape(select(name='author', id='author', options=projusers, opt_selected=u.username)))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(ra_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 12em;">Participants :</div>\n            <div class="fselect vtop">\n                ')
        __M_writer(escape(multiselect(name='participant', id='participant', options=usernames, size='7')))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 12em;"></div>\n            <div class="fsubmit">\n                ')
        __M_writer(escape(input_submit(value='Create')))
        __M_writer('\n                ')
        __M_writer(escape(input_reset(value='Reset')))
        __M_writer('\n            </div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        function initform_createrev() {\n            function createrev_onsubmit( e ) {\n                var msg       = \'\';\n                if ( dijit.byId(\'createrev\').validate() ) {\n                    if (! dojo.attr( dojo.byId( \'author\' ), \'value\' )) {\n                        msg       = \'Provide review author !!\'\n                    }\n                    if (msg) {\n                        dojo.publish( \'flash\', [ \'error\', msg, 2000 ]);\n                        dojo.stopEvent( e );\n                    }\n                } else {\n                    dojo.publish( \'flash\', [ \'error\', "Invalid form fields", 2000 ]);\n                    dojo.stopEvent( e );\n                }\n            }\n            new zeta.Form({ onsubmit : createrev_onsubmit, formid: \'createrev\' })\n\n            var n_rurl = dijit.byId( \'resource_url\' );\n            n_rurl ? n_rurl.focus() : null;\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_tckparent(context, u, p, action, t=None):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form id="tckparent" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='ticket_id', value=t and str(t.id) or '')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='parent_id')))
        __M_writer('\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_updatetcmt(context, u, p, t, action, tcmt=None):
    context.caller_stack._push_frame()
    try:

        def textarea(**kwargs):
            return render_textarea(context, **kwargs)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id=\'updatetcmt\' action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='ticket_id', value=str(t.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='ticket_comment_id', value=tcmt and str(tcmt.id) or '')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='commentby', value=u.username)))
        __M_writer('\n    <div class="w100 form">\n        <div class="w80">\n            ')
        __M_writer(escape(elements.captiontextarea('Use wiki markup to compose ticket comment.')))
        __M_writer('\n            ')
        __M_writer(escape(textarea(name='text', id='upcmt_text', text=tcmt and tcmt.text or '')))
        __M_writer('\n        </div>\n        <div>')
        __M_writer(escape(input_submit(value='Update')))
        __M_writer('</div>\n    </div>\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_addattachs(context, u, action):
    context.caller_stack._push_frame()
    try:

        def input_file(**kwargs):
            return render_input_file(context, **kwargs)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id="addattachs" enctype="multipart/form-data" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 12em;">File :</div>\n            <div class="ffile">\n                ')
        __M_writer(escape(input_file(name='attachfile', id='attachfile', style='width: 40em;')))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 12em;">Summary :</div>\n            <div class="ftbox">\n                ')
        __M_writer(escape(input_text(name='summary', id='summary', style='width: 40em;')))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 12em;"></div>\n            <div class="fsubmit">')
        __M_writer(escape(input_submit(value='Add')))
        __M_writer('</div>\n        </div>\n    </div>\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_tcksummary(context, u, p, action, t=None):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form id="tcksummary" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='ticket_id', value=t and str(t.id) or '')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='summary')))
        __M_writer('\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_systeminfo(context, u, entries, action):
    context.caller_stack._push_frame()
    try:

        def fieldhelp(help='', fhstyle=''):
            return render_fieldhelp(context, help, fhstyle)

        __M_writer = context.writer()
        __M_writer('\n    ')
        help = {'product_name': '', 
           'envpath': '<em>Can be changed ony in the .ini file</em>', 
           'product_version': '', 
           'database_version': '', 
           'sitename': '', 
           'siteadmin': '', 
           'timezone': '', 
           'unicode_encoding': '<em>-- This feature is in development --</em>'}
        import zwiki
        __M_writer('\n\n    <div class="disptable w60 ml50" style="border-collapse: separate; border-spacing: 10px">\n')
        for field in infofields:
            __M_writer('        <div class="disptrow">\n            <div class="disptcell p3 fggray fntbold">')
            __M_writer(escape(field))
            __M_writer('</div>\n            <div class="disptcell p3 fggray">\n                ')
            __M_writer(escape(entries[field]))
            __M_writer('\n')
            if help[field]:
                __M_writer('                    - ')
                __M_writer(escape(fieldhelp(help[field])))
                __M_writer('\n')
            __M_writer('            </div>\n        </div>\n')

        __M_writer('        <div class="disptrow">\n            <div class="disptcell p3 fggray fntbold">zwiki_version</div>\n            <div class="disptcell p3 fggray">\n                ')
        __M_writer(escape(zwiki.VERSION))
        __M_writer('\n            </div>\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_tckpromptuser(context, u, p, action, t=None):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form id="tckpromptuser" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='ticket_id', value=t and str(t.id) or '')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='promptuser')))
        __M_writer('\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_addparts(context, u, p, r, action, usernames):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def select(**kwargs):
            return render_select(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        usernames = [
         '--Add--'] + usernames
        default = '--Add--'
        __M_writer('\n    <form id="addparts" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='review_id', value=str(r.id))))
        __M_writer('\n    ')
        __M_writer(escape(select(name='participant', id='participant', options=usernames, opt_selected=default)))
        __M_writer('\n    </form>\n\n    <script type="text/javascript">\n        function initform_addparts() {\n            new zeta.Form({ formid: \'addparts\' });\n            var n_select = dojo.query( \'select[name=participant]\', form_addparts )[0];\n            // Submit the form on selecting a user.\n            dojo.connect(\n                n_select, \'onchange\',\n                function( e ) {\n                    var n_select = e.currentTarget;\n                    var sr_str = \'select[name=participant] option[value=\'+n_select.value+\']\';\n                    var n_opt  = dojo.query( sr_str, form_addparts )[0];\n                    submitform( form_addparts, e );\n                    dojo.stopEvent( e );\n                    dojo.publish( \'insertparticipant\', [ n_select.value ] );\n                    n_select.removeChild( n_opt );\n                }\n            );\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_configticket(context, u, p, action, t=None):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form id="configtck" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='ticket_id', value=t and str(t.id) or '')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='tck_typename')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='tck_severityname')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='promptuser')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='component_id')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='milestone_id')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='version_id')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='summary')))
        __M_writer('\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_revwfav(context, u, p, r, action, name):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form id=\'revwfav\' class="dispnone" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='review_id', value=str(r.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name=name, value=str(u.username))))
        __M_writer('\n    </form>\n\n    <script type="text/javascript">\n        /* Setup favorite review for user */\n        function initform_revwfav() {\n            var n_span  = dojo.query( "span[name=favrevw]" )[0];\n            var w_form  = new zeta.Form({ normalsub: true, formid: \'revwfav\' });\n            var n_field = dojo.query( "input[name=')
        __M_writer(escape(name))
        __M_writer(']", form_revwfav )[0];\n            if( n_span && n_field ) {\n                new ZFavorite( n_span, form_revwfav, n_field );\n            }\n        }\n        dojo.addOnLoad( initform_revwfav );\n    </script>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_del_userpermissions(context, u, usernames, action, defuser, pgroups):
    context.caller_stack._push_frame()
    try:
        elements = _mako_get_namespace(context, 'elements')

        def multiselect(**kwargs):
            return render_multiselect(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def select(**kwargs):
            return render_select(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id="deluserperms" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 7em;">\n                ')
        __M_writer(escape(elements.iconize('User :', 'user')))
        __M_writer('</div>\n            <div class="fselect vtop"  required="true">\n                ')
        __M_writer(escape(select(name='username', id='delfromuser', options=usernames, opt_selected=defuser, style='width : 15em')))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 7em;">Permissions :</div>\n            <div class="fselect vtop"  required="true">\n                ')
        __M_writer(escape(multiselect(name='perm_group', id='del_perm_group', options=pgroups, size='7', style='width : 15em')))
        __M_writer('</div>\n            <div class="fsubmit" style="margin-left : 50px">')
        __M_writer(escape(input_submit(value='Delete')))
        __M_writer('</div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        /* Initialise deluserperms form */\n        function initform_deluserperms( e ) {\n            seluser_delpg  = dojo.query( \'form#deluserperms select#delfromuser\' )[0];\n            selpg_fromuser = dojo.query( \'form#deluserperms select#del_perm_group\' )[0];\n            new ZSelect( seluser_delpg, null, function( e ) { refresh_userperms() } );\n            new ZSelect( selpg_fromuser, \'deluserpg\', null );\n\n            function deluserperms_onsubmit( e ) {\n                submitform( form_deluserperms, e )\n                dojo.publish( \'flash\', [ \'message\', "Refreshing ..." ] );\n                userperms.store.close();\n                userperms.fetch({\n                    onComplete : userperms_oncomplete,\n                    sort       : [{ attribute : \'username\' }]\n                });\n                dojo.stopEvent( e );\n            }\n            new zeta.Form({ onsubmit : deluserperms_onsubmit, formid : \'deluserperms\' });\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_rmver(context, u, p, action):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def multiselect(**kwargs):
            return render_multiselect(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id="rmver" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 10em;"></div>\n            <div class="ftarea">\n                ')
        __M_writer(escape(multiselect(name='version_id', id='version_id', options=[], size='4', style='width : 20em;')))
        __M_writer('\n                <div>')
        __M_writer(escape(input_submit(value='Delete')))
        __M_writer('</div>\n            </div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        /* Setup version removal */\n        function initform_rmver() {\n            var selver_rmver= dojo.query( \'form#rmver select#version_id\' )[0];\n            new ZSelect( selver_rmver, \'rmver\', null )\n            function rmver_onsubmit( e ) {\n                submitform( form_rmver, e );\n                verlist.store.close();\n                verlist.fetch({\n                    onComplete : verlist_oncomplete,\n                    sort : [ { attribute : \'version_name\' } ]\n                });\n                dojo.stopEvent(e);\n            }\n            new zeta.Form({ onsubmit: rmver_onsubmit, formid : \'rmver\' });\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_createvcs(context, u, p, action, vcs_typenames):
    context.caller_stack._push_frame()
    try:

        def fieldhelp(help='', fhstyle=''):
            return render_fieldhelp(context, help, fhstyle)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        def select(**kwargs):
            return render_select(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        nm_help = 'repository name must be unique'
        __M_writer('\n    <form id="createvcs" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 12em;">Name :</div>\n            <div class="ftbox" required="true">\n                ')
        __M_writer(escape(input_text(name='name', id='name')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(nm_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 12em;">Type :</div>\n            <div class="fselect" required="true">\n                ')
        __M_writer(escape(select(name='vcs_typename', id='vcs_typename', options=vcs_typenames)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 12em;">Root-url :</div>\n            <div class="ftbox" required="true">\n                ')
        __M_writer(escape(input_text(name='rooturl', id='rooturl', size='64', style='width : 30em;')))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 12em;"></div>\n            <div class="fsubmit">')
        __M_writer(escape(input_submit(value='Create')))
        __M_writer('</div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        function initform_createvcs() {\n            new zeta.Form({ formid: \'createvcs\' });\n            dijit.byId( \'name\' ).focus();\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_addtckfilter(context, u, action):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form id="addtckfilter" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(id='filterbyjson', name='filterbyjson')))
        __M_writer('\n    <div class="pt10">\n        ')
        __M_writer(escape(input_text(id='filtername', name='name', style='width: 10em; color: #D6D6D6;', value='Save-This-Filter')))
        __M_writer('\n    </div>\n    </form>\n    <script type="text/javascript">\n        function addtckfilter_onsubmit( e ) {\n            var name    = dojo.attr( dojo.byId( \'filtername\' ), \'value\' );\n            var n_fjson = dojo.byId( \'filterbyjson\' );\n            var valpatt = /^[a-zA-Z]+[a-zA-Z0-9]*$/;\n            dojo.attr( n_fjson, \'value\', dojo.toJson(customquery()) );\n            if( name && n_fjson && valpatt.test( name ) ) {\n                submitform( form_addtckfilter, e );\n            } else {\n                dojo.publish( \'flash\', [ \'error\', "Invalid name", 2000 ]);\n            }\n            dojo.stopEvent( e );\n        }\n        function initform_addtckfilter() {\n            new zeta.Form({ onsubmit: addtckfilter_onsubmit,\n                            formid: \'addtckfilter\' })\n            dojo.connect( dojo.byId( \'filtername\' ), \'onfocus\',\n                function(e) {\n                    dojo.attr( e.target, \'value\', \'\' );\n                    dojo.style( e.target, { color : \'black\' });\n                }\n            );\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_input_text(context, **kwargs):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n    ')
        text = kwargs.pop('text', '')
        restrict_kwargs(kwargs, inputtext_attrs)
        attrs = make_attrs(kwargs)
        __M_writer('\n    <input type="text" ')
        __M_writer(attrs)
        __M_writer('>')
        __M_writer(escape(text))
        __M_writer('</input>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_revwauthor(context, u, p, r, action, projusers):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def select(**kwargs):
            return render_select(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        projusers = [
         [
          '', '--Select-Author--']] + projusers
        if not r.author:
            default = '--Select-Author--'
        elif r.author.username not in projusers:
            default = '--Select-Author--'
        else:
            default = r.author.username
        __M_writer('\n    <form class="dispnone" id="revwauthor" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='review_id', value=str(r.id))))
        __M_writer('\n    ')
        __M_writer(escape(select(name='author', id='author', options=projusers, opt_selected=default)))
        __M_writer('\n    </form>\n\n    <script type="text/javascript">\n        function initform_revwauthor() {\n            new zeta.Form({ formid: \'revwauthor\' });\n            var n_select = dojo.query( \'select[name=author]\', form_revwauthor )[0];\n            // Submit the form on selecting the author\n            dojo.connect( n_select, \'onchange\',\n                          function( e ) {\n                              submitform( form_revwauthor, e );\n                              dojo.stopEvent( e );\n                          }\n            );\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_input_password(context, **kwargs):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n    ')
        restrict_kwargs(kwargs, inputpass_attrs)
        attrs = make_attrs(kwargs)
        __M_writer('\n    <input type="password" ')
        __M_writer(attrs)
        __M_writer('></input>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_updatever(context, u, p, verlist, action):
    context.caller_stack._push_frame()
    try:
        elements = _mako_get_namespace(context, 'elements')

        def textarea(**kwargs):
            return render_textarea(context, **kwargs)

        def fieldhelp(help='', fhstyle=''):
            return render_fieldhelp(context, help, fhstyle)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        def select(**kwargs):
            return render_select(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        vn_help = 'version name must be unique'
        __M_writer('\n\n    <div class="w100 mb10">\n        ')
        __M_writer(escape(select(name='updtver', id='updtver', options=verlist)))
        __M_writer('\n        <hr></hr>\n    </div>\n    <form id="updatever" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='version_id', value='')))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 10em;">Version name :</div>\n            <div class="ftbox" required="true">\n                ')
        __M_writer(escape(input_text(name='version_name', id='updtvername')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(vn_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label vtop" style="width : 10em;">Description : </div>\n            <div class="ftarea" required="true">\n                ')
        __M_writer(escape(elements.captiontextarea('Use wiki markup to compose version description.')))
        __M_writer('\n                ')
        __M_writer(escape(textarea(name='description', id='updtverdesc', cols='50', style='width : 25em')))
        __M_writer('\n                <div>')
        __M_writer(escape(input_submit(value='Update')))
        __M_writer('</div>\n            </div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        function initform_updatever() {\n            /* Setup version detail update */\n            function updatever_onsubmit( e ) {\n                var msg = \'\'\n                if ( dijit.byId(\'updatever\').validate() ) {\n                    if (! dojo.attr( dojo.byId( \'updtverdesc\' ), \'value\' )) {\n                        msg = \'Provide version description !!\'\n                    }\n\n                    if ( msg ) {\n                        dojo.publish( \'flash\', [ \'error\', msg, 2000 ]);\n                    } else {\n                        submitform( form_updatever, e);\n                        verlist.store.close();\n                        verlist.fetch({\n                            onComplete : verlist_oncomplete,\n                            sort : [ { attribute : \'version_name\' } ]\n                        });\n                    }\n                } else {\n                    dojo.publish( \'flash\', [ \'error\', "Invalid form fields", 2000 ]);\n                }\n                dojo.stopEvent(e);\n            }\n            new zeta.Form({ onsubmit: updatever_onsubmit, formid : \'updatever\' });\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_editsw(context, u, sw, action):
    context.caller_stack._push_frame()
    try:
        elements = _mako_get_namespace(context, 'elements')

        def textarea(**kwargs):
            return render_textarea(context, **kwargs)

        h = context.get('h', UNDEFINED)

        def input_reset(**kwargs):
            return render_input_reset(context, **kwargs)

        def input_button(**kwargs):
            return render_input_button(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id=\'editsw\' action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='pathurl', value=sw.path)))
        __M_writer('\n    <div class="w100 form">\n        <div class="field ml20">\n            <div class="ftarea w80" required="true">\n                ')
        __M_writer(escape(elements.captiontextarea('Use wiki markup to compose guest wiki page.')))
        __M_writer('\n                ')
        __M_writer(escape(textarea(name='text', tatype='simpletextarea', id='swtext', text=sw.text, cols='120', rows='30')))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="fsubmit">\n                ')
        __M_writer(escape(input_submit(value='Save & Continue')))
        __M_writer('\n                ')
        __M_writer(escape(input_reset(value='Reset')))
        __M_writer('\n                ')
        __M_writer(escape(input_button(id='preview', value='Preview')))
        __M_writer('\n            </div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        function onpreview( x_form, e ) {\n            var div_wp  = dojo.query( \'.swpreview\' )[0];\n            var ta_wcnt = dijit.byId( \'swtext\' )\n            if ( e.type == \'keyup\' && e.keyCode != dojo.keys.ENTER ) {\n                return;\n            }\n            if ( div_wp && ta_wcnt ) {\n                div_wp.innerHTML = \'\'\n                xhrpost_obj( \'')
        __M_writer(h.url_swpreview)
        __M_writer("',\n                             { 'text' : ta_wcnt.attr( 'value' ) },\n                             'text',\n                             false,\n                             null,\n                             function( resp ) {\n                                    dojo.toggleClass( div_wp.parentNode.parentNode, 'dispnone', false );\n                                    div_wp.innerHTML = resp;\n                             },\n                             null\n                          );\n                dojo.stopEvent( e );\n            }\n        }\n        function initform_editsw() {\n            new zeta.Form({ normalsub: true, formid: 'editsw' });\n            dijit.byId( 'swtext' ).focus();\n\n            // Show preview\n            var x_form = dijit.byId( 'editsw' );\n            var butt_preview = dojo.query( '#preview', x_form.domNode )[0];\n            dojo.connect( butt_preview, 'onclick', dojo.hitch( null, onpreview, x_form ));\n            dojo.connect( butt_preview, 'onkeyup', dojo.hitch( null, onpreview, x_form ));\n        }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_input_checkbox(context, **kwargs):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n    ')
        text = kwargs.pop('text', '')
        restrict_kwargs(kwargs, inputchkbox_attrs)
        attrs = make_attrs(kwargs)
        __M_writer('\n    <input type="checkbox" ')
        __M_writer(attrs)
        __M_writer('></input>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_createwcmt(context, u, w, action):
    context.caller_stack._push_frame()
    try:
        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def textarea(**kwargs):
            return render_textarea(context, **kwargs)

        elements = _mako_get_namespace(context, 'elements')

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id=\'createwcmt\' action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='wiki_id', value=str(w.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='version_id', value=str(w.latest_version))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='commentby', value=u.username)))
        __M_writer('\n    <div class="w100 form">\n        <div class="w80">\n            ')
        __M_writer(escape(elements.captiontextarea('Use wiki markup to compose wiki comment.')))
        __M_writer('\n            ')
        __M_writer(escape(textarea(name='text', id='crwcmt_text')))
        __M_writer('\n        </div>\n        <div>')
        __M_writer(escape(input_submit(value='Add')))
        __M_writer('</div>\n    </div>\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_input_hidden(context, **kwargs):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n    ')
        restrict_kwargs(kwargs, inputhidden_attrs)
        attrs = make_attrs(kwargs)
        __M_writer('\n    <input type="hidden" ')
        __M_writer(attrs)
        __M_writer('></input>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_createpcomp(context, u, p, pusers, action):
    context.caller_stack._push_frame()
    try:
        elements = _mako_get_namespace(context, 'elements')

        def textarea(**kwargs):
            return render_textarea(context, **kwargs)

        def fieldhelp(help='', fhstyle=''):
            return render_fieldhelp(context, help, fhstyle)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        def select(**kwargs):
            return render_select(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        cn_help = 'Component name must be unique'
        __M_writer('\n\n    <form id="createpcomp" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 10em;">Component name :</div>\n            <div class="ftbox" required="true">\n                ')
        __M_writer(escape(input_text(name='componentname', id='crcompname')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(cn_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10em;">Owner :</div>\n            <div class="ftbox">\n                ')
        __M_writer(escape(select(name='owner', id='crowner', options=pusers)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label vtop" style="width : 10em;">Description : </div>\n            <div class="ftarea" required="true">\n                ')
        __M_writer(escape(elements.captiontextarea('Use wiki markup to compose component description.')))
        __M_writer('\n                ')
        __M_writer(escape(textarea(name='description', id='crcompdesc', rows='1', cols='50', style='width : 25em')))
        __M_writer('\n                <div>')
        __M_writer(escape(input_submit(value='Create')))
        __M_writer('</div>\n            </div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        function initform_createpcomp() {\n            var select_puser = dojo.query( \'form#createpcomp select#crowner\' )[0];\n            new ZSelect( select_puser, \'projusers\', null );\n\n            function createpcomp_onsubmit( e ) {\n                var msg = \'\'\n                if ( dijit.byId(\'createpcomp\').validate() ) {\n                    if (! dojo.attr( dojo.byId( \'crowner\' ), \'value\' )) {\n                        msg = \'Provide component owner !!\'\n                    }\n                    if (! dojo.attr( dojo.byId( \'crcompdesc\' ), \'value\' )) {\n                        msg = \'Provide component description !!\'\n                    }\n\n                    if ( msg ) {\n                        dojo.publish( \'flash\', [ \'error\', msg, 2000 ]);\n                    } else {\n                        submitform( form_createpcomp, e);\n                        pcomplist.store.close();\n                        pcomplist.fetch({\n                            onComplete : pcomplist_oncomplete,\n                            sort : [ { attribute : \'componentname\' } ]\n                        })\n                    }\n                } else {\n                    dojo.publish( \'flash\', [ \'error\', "Invalid form fields", 2000 ]);\n                }\n                dojo.stopEvent(e);\n            }\n            new zeta.Form({ onsubmit: createpcomp_onsubmit, formid : \'createpcomp\' });\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_project_disable(context, u, action, eprojects):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def multiselect(**kwargs):
            return render_multiselect(context, **kwargs)

        str = context.get('str', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id="prjdis" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 7em;">\n                ')
        __M_writer(escape(elements.iconize('Projects :', 'projects')))
        __M_writer('</div>\n            <div class="fselect vtop" style="width : 20em;">\n                ')
        __M_writer(escape(multiselect(name='disable_project', id='disable_project', options=eprojects, size='7', style='width : 10em;')))
        __M_writer('</div>\n            <div class="fsubmit ml10">')
        __M_writer(escape(input_submit(value='Disable')))
        __M_writer('</div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        /* Initialise prjdis form */\n        function initform_prjdis() {\n            selproj_dis = dojo.query( \'select#disable_project\' )[0];\n            new ZSelect( selproj_dis, \'disable_project\', null );\n            function prjdis_onsubmit( e ) {\n                submitform( form_prjdis, e );\n                dojo.publish( \'flash\', [ \'message\', "Refreshing ..." ]);\n                projectstatus.store.close();\n                projectstatus.fetch( { onComplete : projectstatus_oncomplete } );\n                dojo.stopEvent( e );\n            }\n            new zeta.Form({ onsubmit : prjdis_onsubmit, formid : \'prjdis\' });\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_updaterset(context, u, p, rs, action, reload):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id=\'updaterset\' action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='rset_id', value=str(rs.id))))
        __M_writer('\n    <div class="form">\n        <div class="field">\n            <div class="label" style="">Update ReviewSet :</div>\n            <div class="ftbox" required=True>\n                ')
        __M_writer(escape(input_text(name='name', id='name', value=rs.name)))
        __M_writer('\n            </div>\n            <div class="fsubmit">\n                ')
        __M_writer(escape(input_submit(value='Update')))
        __M_writer('\n            </div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        function updaterset_onsubmit(e) {\n            var reloadurl = "')
        __M_writer(reload)
        __M_writer('";\n            submitform( form_updaterset, e );\n            dojo.stopEvent(e);\n            if( reloadurl ) { window.location = reloadurl; }\n        }\n        function initform_updaterset() {\n            new zeta.Form({ onsubmit: updaterset_onsubmit, \n                            formid: \'updaterset\' });\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_multiselect(context, **kwargs):
    context.caller_stack._push_frame()
    try:
        unicode = context.get('unicode', UNDEFINED)
        range = context.get('range', UNDEFINED)
        isinstance = context.get('isinstance', UNDEFINED)
        str = context.get('str', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        selected = kwargs.get('opt_selected', '')
        options = kwargs.get('options', [])
        opts_disabled = kwargs.get('opts_disabled', '')
        restrict_kwargs(kwargs, multiselect_attrs)
        attrs = make_attrs(kwargs)
        options = options[:]
        for i in range(len(options)):
            if isinstance(options[i], (str, unicode)):
                options[i] = (
                 options[i], options[i])

        __M_writer('\n    <select multiple="multiple" ')
        __M_writer(attrs)
        __M_writer('>\n')
        for (val, txt) in options:
            __M_writer('            <option value=')
            __M_writer(escape(val))
            __M_writer('\n')
            if selected == txt:
                __M_writer('                selected="selected"\n')
            if txt in opts_disabled:
                __M_writer('                disabled="disabled"\n')
            __M_writer('            >')
            __M_writer(escape(txt))
            __M_writer('</option>\n')

        __M_writer('    </select>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_select_revwnature(context, naturenames):
    context.caller_stack._push_frame()
    try:

        def select(**kwargs):
            return render_select(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        naturenames = [
         [
          '', '--Select-Nature--']] + naturenames
        __M_writer('\n    ')
        __M_writer(escape(select(name='reviewnature', options=naturenames)))
        __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_deltckfilter(context, u, savfilterid, action):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id="deltckfilter" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='tf_id', value=str(savfilterid))))
        __M_writer('\n    ')
        __M_writer(escape(input_submit(value='Delete')))
        __M_writer('\n    </form>\n    <script type="text/javascript">\n        function deltckfilter_onsubmit( e ) {\n            submitform( form_deltckfilter, e );\n            dojo.stopEvent( e );\n        }\n        function initform_deltckfilter() {\n            new zeta.Form({ onsubmit: deltckfilter_onsubmit,\n                            formid: \'deltckfilter\' })\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_rmmstn(context, u, p, action):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def multiselect(**kwargs):
            return render_multiselect(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id="rmmstn" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 10em;"></div>\n            <div class="ftarea">\n                ')
        __M_writer(escape(multiselect(name='milestone_id', id='milestone_id', options=[], size='4', style='width : 20em;')))
        __M_writer('\n                <div>')
        __M_writer(escape(input_submit(value='Delete')))
        __M_writer('</div>\n            </div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        /* Setup milestone removal */\n        function initform_rmmstn() {\n            var selmstn_rmmstn = dojo.query( \'form#rmmstn select#milestone_id\' )[0];\n            new ZSelect( selmstn_rmmstn, \'rmmstn\', null )\n            function rmmstn_onsubmit( e ) {\n                submitform( form_rmmstn, e );\n                mstnlist.store.close();\n                mstnlist.fetch({\n                    onComplete : mstnlist_oncomplete,\n                    sort : [ { attribute : \'milestone_name\' } ]\n                });\n                dojo.stopEvent(e);\n            }\n            new zeta.Form({ onsubmit: rmmstn_onsubmit, formid : \'rmmstn\' });\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_delteamperms(context, u, p, teamtypes, deftt, teampgroups, action):
    context.caller_stack._push_frame()
    try:
        elements = _mako_get_namespace(context, 'elements')

        def multiselect(**kwargs):
            return render_multiselect(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def select(**kwargs):
            return render_select(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id=\'delteamperms\' action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 10em;">\n                ')
        __M_writer(escape(elements.iconize('Team :', 'team')))
        __M_writer('</div>\n            <div class="fselect"  required="true">\n                ')
        __M_writer(escape(select(name='team_type', id='team_type', options=teamtypes, opt_selected=deftt, style='width : 10em')))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label vtop" style="width : 10em;">Permissions :</div>\n            <div class="fselect" required="true">\n                ')
        __M_writer(escape(multiselect(name='projectteam_perm_id', id='projectteam_perm_id', options=teampgroups, size='7', style='width : 15em')))
        __M_writer('</div>\n            <div class="fsubmit" style="margin-left : 50px">')
        __M_writer(escape(input_submit(value='Submit')))
        __M_writer('</div>\n        </div>\n    </div>\n    </form>\n    <script type="text/javascript">\n        /* Setup permission removals to project team */\n        function initform_delteamperms() {\n            var dselect_tt     = dojo.query( \'form#delteamperms select[name=team_type]\'\n                                           )[0];\n            var select_delperm = dojo.query( \'form#delteamperms select#projectteam_perm_id\'\n                                           )[0];\n            new ZSelect( select_delperm, \'delpgfromteam\', null );\n            new ZSelect( dselect_tt, null, function( e ) { refresh_teamperms( \'todel\' ) } );\n            function delteamperms_onsubmit( e ) {\n                submitform( form_delteamperms, e )\n                dojo.publish( \'flash\', [ \'message\', "Refreshing ..." ] );\n                teamperms.store.close();\n                teamperms.fetch({ onComplete : teamperms_oncomplete });\n                dojo.stopEvent( e );\n            }\n            new zeta.Form({ onsubmit: delteamperms_onsubmit, formid : \'delteamperms\' });\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_wikifav(context, u, p, w, action, name):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n\n    <form id=\'wikifav\' class="dispnone" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='wiki_id', value=str(w.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name=name, value=str(u.username))))
        __M_writer('\n    </form>\n\n    <script type="text/javascript">\n        /* Setup favorite wiki for user */\n        function initform_wikifav() {\n            var n_span  = dojo.query( "span[name=favwiki]" )[0];\n            var w_form  = new zeta.Form({ normalsub: true, formid: \'wikifav\' });\n            var n_field = dojo.query( "input[name=')
        __M_writer(escape(name))
        __M_writer(']", form_wikifav )[0];\n            if( n_span && n_field ) {\n                new ZFavorite( n_span, form_wikifav, n_field );\n            }\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_addtorset(context, u, p, rs, action, revwlist, reload=None):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def select(**kwargs):
            return render_select(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        revwlist = [
         [
          '', '--Add Review to Set--']] + revwlist
        __M_writer('\n    <form id=\'addtorset\' action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='rset_id', value=str(rs.id))))
        __M_writer('\n    ')
        __M_writer(escape(select(name='review_id', id='add_review_id', options=revwlist)))
        __M_writer('\n    </form>\n\n    <script type="text/javascript">\n        function initform_addtorset() {\n            var n_selrid = dojo.byId( \'add_review_id\' );\n\n            new zeta.Form({ formid: \'addtorset\' });\n\n            // Submit form on selecting review to add\n            dojo.connect(\n                n_selrid, \'onchange\',\n                function( e ) {\n                    var reloadurl = "')
        __M_writer(reload)
        __M_writer('";\n                    if( n_selrid.value ) { submitform( form_addtorset, e ); }\n                    dojo.stopEvent( e );\n                    if( reloadurl ) { window.location = reloadurl; }\n                }\n            );\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_deletemount_e(context, u, action):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form id="deletemount_e" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='mount_id', id='mount_id')))
        __M_writer('\n    </form>\n\n    <script type="text/javascript">\n        function initform_deletemount_e() {\n            new zeta.Form({ formid: \'deletemount_e\' });\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_addprjperms(context, u, p, projusers, defuser, x_userpgroups, action):
    context.caller_stack._push_frame()
    try:
        elements = _mako_get_namespace(context, 'elements')

        def multiselect(**kwargs):
            return render_multiselect(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def select(**kwargs):
            return render_select(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id=\'addprjperms\' action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 7em;">\n                ')
        __M_writer(escape(elements.iconize('User :', 'user')))
        __M_writer('</div>\n            <div class="fselect"  required="true">\n                ')
        __M_writer(escape(select(name='projuser', options=projusers, opt_selected=defuser, style='width : 10em')))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label vtop" style="width : 7em;">Permissions :</div>\n            <div class="fselect" required="true">\n                ')
        __M_writer(escape(multiselect(name='perm_group', id='perm_group', options=x_userpgroups, size='7', style='width : 15em')))
        __M_writer('</div>\n            <div class="fsubmit" style="margin-left : 50px">')
        __M_writer(escape(input_submit(value='Submit')))
        __M_writer('</div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        /* Setup permission additions to project user */\n        function initform_addprjperms() {\n            var aselect_user   = dojo.query( \'form#addprjperms select[name=projuser]\'\n                                           )[0];\n            var select_addperm = dojo.query( \'form#addprjperms select[name=perm_group]\'\n                                           )[0];\n            new ZSelect( select_addperm, \'addppgtouser\', null );\n            new ZSelect( aselect_user, \'projusers\', function( e ) { refresh_prjperms() } );\n            function addprjperms_onsubmit( e ) {\n                submitform( form_addprjperms, e )\n                dojo.publish( \'flash\', [ \'message\', "Refreshing ..." ] );\n                prjperms.store.close();\n                prjperms.fetch({ onComplete : prjperms_oncomplete,\n                                 sort       : [{ attribute : \'username\' }]\n                              });\n                dojo.stopEvent( e );\n            }\n            new zeta.Form({ onsubmit: addprjperms_onsubmit, formid : \'addprjperms\' });\n        }\n        dojo.addOnLoad( initform_addprjperms );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_selectticket(context, u, ticketlist, default=''):
    context.caller_stack._push_frame()
    try:

        def select(**kwargs):
            return render_select(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        ticketlist = [
         [
          '', '--Select-Ticket--']] + ticketlist
        default = default or '--Select-Ticket--'
        __M_writer('\n    <span class="ml5">\n        ')
        __M_writer(escape(select(name='selectticket', id='selectticket', options=ticketlist, opt_selected=default)))
        __M_writer('\n    </span>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_rmpcomp(context, u, p, action):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def multiselect(**kwargs):
            return render_multiselect(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id="rmpcomp" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 10em;"></div>\n            <div class="ftarea">\n                ')
        __M_writer(escape(multiselect(name='component_id', id='component_id', options=[], size='4', style='width : 20em;')))
        __M_writer('\n                <div>')
        __M_writer(escape(input_submit(value='Delete')))
        __M_writer('</div>\n            </div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        function initform_rmpcomp() {\n            /* Setup component removal */\n            var selpcomp_rmpcomp = dojo.query( \'form#rmpcomp select#component_id\')[0];\n            function rmpcomp_onsubmit( e ) {\n                submitform( form_rmpcomp, e );\n                pcomplist.store.close();\n                pcomplist.fetch({\n                    onComplete : pcomplist_oncomplete,\n                    sort : [ { attribute : \'componentname\' } ]\n                })\n                dojo.stopEvent(e);\n            }\n            new ZSelect( selpcomp_rmpcomp, \'rmpcomp\', null )\n            new zeta.Form({ onsubmit: rmpcomp_onsubmit, formid : \'rmpcomp\' });\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_configtst(context, u, p, action, t=None, ts=None):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form id="configtstat" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='ticket_id', value=t and str(t.id) or '')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='ticket_status_id', value=ts and str(ts.id) or '')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='owner', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='tck_statusname')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='due_date')))
        __M_writer('\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_wikitype(context, u, w, wikitypenames, action):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def select(**kwargs):
            return render_select(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id=\'wikitype\' action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='wiki_id', value=str(w.id))))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="fselect"  required="true">\n                ')
        __M_writer(escape(select(name='wiki_typename', id='wiki_typename', options=wikitypenames, opt_selected=w.type.wiki_typename, style='width : 10em')))
        __M_writer('\n            </div>\n        </div>\n    </div>\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_label(context, labelfor='', text=''):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n    <label for="')
        __M_writer(escape(labelfor))
        __M_writer('" >')
        __M_writer(escape(text))
        __M_writer('</label>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_creatercmt(context, u, p, r, action, naturenames):
    context.caller_stack._push_frame()
    try:
        elements = _mako_get_namespace(context, 'elements')

        def textarea(**kwargs):
            return render_textarea(context, **kwargs)

        def fieldhelp(help='', fhstyle=''):
            return render_fieldhelp(context, help, fhstyle)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        def select(**kwargs):
            return render_select(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        naturenames = [
         '--Select-Nature--'] + naturenames[:]
        pos_help = 'Line number'
        __M_writer('\n    <form id=\'creatercmt\' action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='review_id', value=str(r.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='commentby', value=u.username)))
        __M_writer('\n    <div class="form w100">\n        <div class="field">\n            <div class="label" style="width : 15%;">Position :</div>\n            <div class="ftbox" style="width : 3em;" required="true" regExp="[0-9]*">\n                ')
        __M_writer(escape(input_text(name='position', style='width: 3em;')))
        __M_writer('\n                <em>')
        __M_writer(escape(fieldhelp(pos_help, fhstyle='color: red;')))
        __M_writer('</em>\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 15%;">Nature :</div>\n            <div class="fselect vtop"  style="width : 10em;">\n                ')
        __M_writer(escape(select(name='reviewnature', options=naturenames, opt_selected='--Select-Nature--')))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label vtop"  style="width : 15%;">Comment text :</div>\n            <div class="ftarea" required="true">\n                ')
        __M_writer(escape(elements.captiontextarea('Use wiki markup to compose review comment.')))
        __M_writer('\n                ')
        __M_writer(escape(textarea(name='text', tatype='simpletextarea', id='crrcmt_text', cols='90', rows='1', style='width : 100%')))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 15%;"></div>\n            <div class="fsubmit" style="width : 10em;">')
        __M_writer(escape(input_submit(value='Create')))
        __M_writer('</div>\n        </div>\n    </div>\n    </form>\n    <script type="text/javascript">\n        // Setup review comment creation form\n        function initform_creatercmt() {\n            function creatercmt_onsubmit( e ) {\n                var i_pos = dojo.query( \'input[name=position]\', form_creatercmt )[0];\n                submitform( form_creatercmt, e );\n                dojo.publish( \'flash\', [ \'message\', "Refreshing ..." ] );\n                dojo.publish( \'refreshrcomments\', [ \'creatercmt\', i_pos.value ] );\n                dojo.stopEvent(e);\n            }\n            new zeta.Form({ onsubmit: creatercmt_onsubmit, formid: \'creatercmt\' });\n        }\n        dojo.addOnLoad( initform_creatercmt );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_configvcs(context, u, p, action, v=None):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        t = context.get('t', UNDEFINED)
        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form id="configvcs" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='vcs_id', value=t and str(t.id) or '')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='name')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='rooturl')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='vcs_typename')))
        __M_writer('\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_updatemount(context, u, m, vcslist, contents, action):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def select(**kwargs):
            return render_select(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id="updatemount" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='mount_id', value=str(m.id))))
        __M_writer('\n    <div class="form">\n        <div class="disptrow">\n            <div class="ftbox" required="true">\n                 <em>name</em>')
        __M_writer(escape(input_text(name='name', id='name', value=m.name)))
        __M_writer('\n            </div>\n            <div class="fselect" required="true">\n                ')
        __M_writer(escape(select(name='content', id='content', options=contents, opt_selected=m.content)))
        __M_writer('\n            </div>\n            <div class="fselect" required="true">\n                ')
        __M_writer(escape(select(name='vcs_id', id='vcs_id', options=vcslist, opt_selected=m.vcs.name)))
        __M_writer('\n            </div>\n            <div class="ftbox" required="true">\n                <em>path</em>')
        __M_writer(escape(input_text(name='repospath', value=m.repospath)))
        __M_writer('\n            </div>\n            <div class="pl20 fsubmit">')
        __M_writer(escape(input_submit(value='Update')))
        __M_writer('</div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        function initform_updatemount() {\n            new zeta.Form({ formid: \'updatemount\' });\n            dijit.byId( \'name\' ).focus();\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_updatepcomp(context, u, p, pusers, pcomplist, action):
    context.caller_stack._push_frame()
    try:
        elements = _mako_get_namespace(context, 'elements')

        def textarea(**kwargs):
            return render_textarea(context, **kwargs)

        def fieldhelp(help='', fhstyle=''):
            return render_fieldhelp(context, help, fhstyle)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        def select(**kwargs):
            return render_select(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        cn_help = 'component name must be unique'
        __M_writer('\n\n    <div class="w100 mb10">\n        ')
        __M_writer(escape(select(name='updtpcomp', id='updtpcomp', options=pcomplist)))
        __M_writer('\n        <hr></hr>\n    </div>\n    <form id="updatepcomp" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='component_id', value='')))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 10em;">Component name :</div>\n            <div class="ftbox" required="true">\n                ')
        __M_writer(escape(input_text(name='componentname', id='updtcompname')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(cn_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10em;">Owner :</div>\n            <div class="ftbox">\n                <span class="fggray" name="ownername"></span>&ensp;&ensp;\n                <span>Pick new owner :</span>\n                ')
        __M_writer(escape(select(name='owner', id='updtowner', options=pusers)))
        __M_writer('</div>\n        </div>\n        <div class="field">\n            <div class="label vtop" style="width : 10em;">Description : </div>\n            <div class="ftarea" required="true">\n                ')
        __M_writer(escape(elements.captiontextarea('Use wiki markup to compose component description.')))
        __M_writer('\n                ')
        __M_writer(escape(textarea(name='description', id='updtpcompdesc', cols='50', style='width : 25em')))
        __M_writer('\n                <div>')
        __M_writer(escape(input_submit(value='Update')))
        __M_writer('</div>\n            </div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        /* Setup component detail update */\n        function initform_updatepcomp() {\n            var selpcomp_owner = dojo.query( \'form#updatepcomp select#updtowner\')[0];\n            new ZSelect( selpcomp_owner, \'updtpcompowners\', null ); \n            function updatepcomp_onsubmit( e ) {\n                var msg = \'\'\n                if ( dijit.byId(\'updatepcomp\').validate() ) {\n                    if (! dojo.attr( dojo.byId( \'updtowner\' ), \'value\' )) {\n                        msg = \'Provide component owner !!\'\n                    }\n                    if (! dojo.attr( dojo.byId( \'updtpcompdesc\' ), \'value\' )) {\n                        msg = \'Provide component description !!\'\n                    }\n\n                    if ( msg ) {\n                        dojo.publish( \'flash\', [ \'error\', msg, 2000 ]);\n                    } else {\n                        submitform( form_updatepcomp, e);\n                        pcomplist.store.close();\n                        pcomplist.fetch({\n                            onComplete : pcomplist_oncomplete,\n                            sort : [ { attribute : \'componentname\' } ]\n                        })\n                    }\n                } else {\n                    dojo.publish( \'flash\', [ \'error\', "Invalid form fields", 2000 ]);\n                }\n                dojo.stopEvent(e);\n            }\n            new zeta.Form({ onsubmit: updatepcomp_onsubmit, formid : \'updatepcomp\' });\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_tckversion(context, u, p, action, t=None):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form id="tckversion" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='ticket_id', value=t and str(t.id) or '')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='version_id')))
        __M_writer('\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_updatelicense_h(context, u, l, action):
    context.caller_stack._push_frame()
    try:

        def textarea(**kwargs):
            return render_textarea(context, **kwargs)

        def fieldhelp(help='', fhstyle=''):
            return render_fieldhelp(context, help, fhstyle)

        def input_reset(**kwargs):
            return render_input_reset(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        ln_help = 'licensename must be unique'
        sm_help = 'one line summary'
        src_help = 'license originator'
        __M_writer('\n\n    <form id="updatelic" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='license_id', value=str(l.id))))
        __M_writer('\n    <div class="form 40em">\n        <div class="field pt20">\n            <div class="label" style="width : 12%;">License name :</div>\n            <div class="ftbox" required="true">\n                ')
        __M_writer(escape(input_text(name='licensename', id='licensename', value=l.licensename, size='32', style='width : 15em;')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(ln_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 12%;">Summary :</div>\n            <div class="ftbox" required="true">\n                ')
        __M_writer(escape(input_text(name='summary', id='summary', value=l.summary, size='64', style='width : 30em;')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(sm_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 12%;">Source :</div>\n            <div class="ftbox" required="true">\n                ')
        __M_writer(escape(input_text(name='source', id='source', size='64', value=l.source, style='width : 30em;')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(src_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label vtop" style="width : 12%;">License Text :</div>\n            <div class="ftarea" required="true">\n                ')
        __M_writer(escape(textarea(name='text', tatype='simpletextarea', id='text', cols='90', rows='20', style='width : 100%')))
        __M_writer('\n            </div>\n        </div>\n')
        __M_writer('        <div class="field">\n            <div class="label" style="width : 12%;"></div>\n            <div class="fsubmit">\n                ')
        __M_writer(escape(input_submit(value='Submit')))
        __M_writer('\n                ')
        __M_writer(escape(input_reset(value='Reset')))
        __M_writer('\n            </div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        function updatelic_onsubmit( e ) {\n            if ( dijit.byId( \'updatelic\' ).validate() ) {\n                var lictext = dojo.byId( \'text\' ).value\n                if(! lictext ) {\n                    dojo.publish(\n                        \'flash\', [ \'error\', "License text must be present", 2000 ]\n                    );\n                    dojo.stopEvent( e );\n                }\n            } else {\n                dojo.publish( \'flash\', [ \'error\', "Invalid form fields", 2000 ]);\n                dojo.stopEvent( e );\n            }\n        }\n        function initform_updatelic() {\n            // Connect form-edit (update) handler\n            var n_edit = dojo.query( \'div[name=editlic]\' )[0];\n            var n_view = dojo.query( \'div[name=viewlic]\' )[0];\n            var edit   = dojo.query( \'div.pbar span[name=editlic]\' )[0];\n            if( n_edit && edit ) {\n                dojo.connect(\n                    edit, \'onclick\', \n                    function ( e ) {\n                      var i_text = dojo.query( \'textarea#text\', form_updatelic )[0];\n                      edit.style.display   = \'none\';\n                      n_view.style.display = \'none\';\n                      n_edit.style.display = \'block\';\n                      dijit.byId( \'licensename\' ).focus();\n                    }\n                );\n            }\n            // Instantiate \'updatelic\'\n            new zeta.Form({ onsubmit : updatelic_onsubmit, formid :  \'updatelic\' });\n\n            /* Copy and process the license text */\n            var re         = new RegExp( \'\\n\', \'g\' );\n            var n_lictext  = dojo.query( \'div[name=text]\', n_view )[0];\n            dojo.query(\'textarea#text\', form_updatelic\n                      )[0].value = n_lictext.innerHTML;\n            n_lictext.innerHTML = dojo.query( \'textarea#text\', form_updatelic\n                                            )[0].value.replace( re, \'<br></br>\' );\n            dojo.toggleClass( n_lictext, \'dispnone\', false )\n        }\n        dojo.addOnLoad( initform_updatelic );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_input_radio(context, **kwargs):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n    ')
        text = kwargs.get('text', '')
        restrict_kwargs(kwargs, inputradio_attrs)
        attrs = make_attrs(kwargs)
        __M_writer('\n    <input type="radio" ')
        __M_writer(attrs)
        __M_writer('>')
        __M_writer(escape(text))
        __M_writer('</input>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_updatepg(context, u, action_pg, action_addpn, action_delpn, pgroups=[], defpg='', perms=[], x_perms=[]):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)

        def multiselect(**kwargs):
            return render_multiselect(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        def select(**kwargs):
            return render_select(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        pg_help = ('Minimum 3 characters to max %s characters.' + 'With all characters in small case.') % h.LEN_NAME
        __M_writer('\n\n    <div class="w100 form">\n        <div class="field">\n            <div class="ftbox" style="width : 20em;" required="true">\n                Select group -\n                ')
        __M_writer(escape(select(name='pglist', id='pglist', options=pgroups, opt_selected=defpg)))
        __M_writer('\n                <hr></hr>\n            </div>\n        </div>\n    </div>\n    <form id="updatepg" action="')
        __M_writer(escape(action_pg))
        __M_writer('" method="post">\n    <div class="w100 form">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='perm_group_id', value='')))
        __M_writer('\n        <div class="field">\n            <div class="label" style="width : 11em;">Permission group :</div>\n            <div class="ftbox" style="width : 20em;" required="true">\n                ')
        __M_writer(escape(input_text(name='perm_group', id='updt_perm_group')))
        __M_writer('</div>\n            <div class="fsubmit"  style="width : 5em;">')
        __M_writer(escape(input_submit(value='Change')))
        __M_writer('</div>\n        </div>\n    </div>\n    </form>\n    <form id="addpntopg" action="')
        __M_writer(escape(action_addpn))
        __M_writer('" method="post">\n    <div class="w100 form">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='perm_group_id', value='')))
        __M_writer('\n        <div class="field">\n            <div class="label" style="width : 11em;">Add Permissions :</div>\n            <div class="fselect vtop" style="width : 20em;" required="true">\n                ')
        __M_writer(escape(multiselect(name='perm_name', id='add_perm_name', options=x_perms, size='7', style='width : 17em')))
        __M_writer('</div>\n            <div class="fsubmit" style="width : 5em;">')
        __M_writer(escape(input_submit(value='Add')))
        __M_writer('</div>\n        </div>\n    </div>\n    </form>\n    <form id="delpnfrompg" action="')
        __M_writer(escape(action_delpn))
        __M_writer('" method="post">\n    <div class="w100 form">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='perm_group_id', value='')))
        __M_writer('\n        <div class="field">\n            <div class="label" style="width : 11em;">Delete Permissions :</div>\n            <div class="fselect vtop" style="width : 20em;" required="true">\n                ')
        __M_writer(escape(multiselect(name='perm_name', id='del_perm_name', options=perms, size='7', style='width : 17em')))
        __M_writer('</div>\n            <div class="fsubmit" style="width : 5em;">')
        __M_writer(escape(input_submit(value='Delete')))
        __M_writer('</div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        function initform_perms() {\n            var select_addpn = dojo.query( \'form#addpntopg select#add_perm_name\' )[0];\n            new ZSelect( select_addpn, \'addpntopg\', null );\n\n            var select_delpn = dojo.query( \'form#delpnfrompg select#del_perm_name\' )[0];\n            new ZSelect( select_delpn, \'delpnfrompg\', null );\n\n            var select_pglist= dojo.query( \'select#pglist\' )[0];\n            new ZSelect( select_pglist, \'pglist\', function( e ) { refresh_perms() });\n\n            function perms_onsubmit( formid, e ) {\n                submitform( dojo.getObject( \'form_\'+formid, e ));\n                dojo.publish( \'flash\', [ \'message\', "Refreshing ..." ] );\n                pgmap.store.close() ;\n                pgmap.fetch({\n                    onComplete : dojo.partial( pgmap_oncomplete, (formid == \'updatepg\')),\n                    sort       : [{ attribute : \'perm_group\' }]\n                });\n                dojo.stopEvent(e);\n            }\n            new zeta.Form({ onsubmit : dojo.partial( perms_onsubmit, \'updatepg\' ),\n                            formid : \'updatepg\' });\n            new zeta.Form({ onsubmit : dojo.partial( perms_onsubmit, \'addpntopg\' ),\n                            formid : \'addpntopg\' });\n            new zeta.Form({ onsubmit : dojo.partial( perms_onsubmit, \'delpnfrompg\' ),\n                            formid : \'delpnfrompg\' });\n        } \n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_selectsavfilter(context, u, filterlist, default=''):
    context.caller_stack._push_frame()
    try:

        def select(**kwargs):
            return render_select(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        filterlist = [
         [
          '', '--Select-Filter--']] + filterlist
        default = default or '--Select-Filter--'
        __M_writer('\n    <span class="ml3">\n        ')
        __M_writer(escape(select(name='selsavfilter', id='selsavfilter', options=filterlist, opt_selected=default)))
        __M_writer('\n    </span>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_approve_userrelations(context, u, action):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id="approveuserrels" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    <div class="w100 form">\n        <div class="fchkbox ml10" style="width : 27em;"><div id="aurels"></div></div>\n        <div class="fsubmit ml10">')
        __M_writer(escape(input_submit(value='Approve')))
        __M_writer('</div>\n    </div>\n    </form>\n    <div style="margin-left : 100px;" id="nodata">None</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_input_button(context, **kwargs):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n    ')
        restrict_kwargs(kwargs, inputbutton_attrs)
        attrs = make_attrs(kwargs)
        __M_writer('\n    <input type="button" ')
        __M_writer(attrs)
        __M_writer('></input>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_wikicontent(context, u, w, wcnt, action, pageurl):
    context.caller_stack._push_frame()
    try:
        elements = _mako_get_namespace(context, 'elements')

        def textarea(**kwargs):
            return render_textarea(context, **kwargs)

        h = context.get('h', UNDEFINED)

        def input_reset(**kwargs):
            return render_input_reset(context, **kwargs)

        def input_button(**kwargs):
            return render_input_button(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        sm_help = 'Enter the page summary, max %s characters' % h.LEN_SUMMARY
        __M_writer('\n\n    <form id=\'wikicont\' action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='wiki_id', value=str(w.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='author', value=u.username)))
        __M_writer('\n    <div class="w100 form">\n        <div class="field ml20">\n            <div class="ftarea w80" required="true">\n                ')
        __M_writer(escape(elements.captiontextarea('Use wiki markup.')))
        __M_writer('\n                ')
        __M_writer(escape(textarea(name='text', tatype='simpletextarea', id='wcnttext', text=wcnt and wcnt.text or '', cols='120', rows='30')))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="fsubmit">\n                ')
        __M_writer(escape(input_submit(value='Save & Continue')))
        __M_writer('\n                ')
        __M_writer(escape(input_reset(value='Reset')))
        __M_writer('\n                ')
        __M_writer(escape(input_button(id='preview', value='Preview')))
        __M_writer('\n                <a class="ml10" href="')
        __M_writer(escape(pageurl))
        __M_writer('">Goto-Page</a>\n            </div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        function onpreview( x_form, e ) {\n            var div_wp  = dojo.query( \'.wikipreview\' )[0];\n            var ta_wcnt = dijit.byId( \'wcnttext\' )\n            if ( e.type == \'keyup\' && e.keyCode != dojo.keys.ENTER ) {\n                return;\n            }\n            if ( div_wp && ta_wcnt ) {\n                div_wp.innerHTML = \'\'\n                xhrpost_obj( \'')
        __M_writer(h.url_wikipreview)
        __M_writer("',\n                             { 'text' : ta_wcnt.attr( 'value' ) },\n                             'text',\n                             false,\n                             null,\n                             function( resp ) {\n                                 dojo.toggleClass( div_wp.parentNode.parentNode, 'dispnone', false );\n                                 div_wp.innerHTML = resp;\n                             },\n                             null\n                           );\n                dojo.stopEvent( e );\n            }\n        }\n        function initform_wikicont() {\n            new zeta.Form({ normalsub: true, formid: 'wikicont' });\n            dijit.byId( 'wcnttext' ).focus();\n\n            // Setup preview\n            var x_form = dijit.byId( 'wikicont' );\n            var butt_preview = dojo.query( '#preview', x_form.domNode )[0];\n            dojo.connect( butt_preview, 'onclick', dojo.hitch( null, onpreview, x_form ));\n            dojo.connect( butt_preview, 'onkeyup', dojo.hitch( null, onpreview, x_form ));\n        }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_addprjteam(context, u, p, teamtypes, deftt, x_teamusers, action):
    context.caller_stack._push_frame()
    try:
        elements = _mako_get_namespace(context, 'elements')

        def multiselect(**kwargs):
            return render_multiselect(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def select(**kwargs):
            return render_select(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id=\'addprjteam\' action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 10em;">\n                ')
        __M_writer(escape(elements.iconize('Team :', 'team')))
        __M_writer('</div>\n            <div class="fselect"  required="true">\n                ')
        __M_writer(escape(select(name='team_type', id='team_type', options=teamtypes, opt_selected=deftt, style='width : 10em')))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label vtop" style="width : 10em;">\n                ')
        __M_writer(escape(elements.iconize('Users :', 'users')))
        __M_writer('</div>\n            <div class="fselect" required="true">\n                ')
        __M_writer(escape(multiselect(name='projuser', options=x_teamusers, size='7', style='width : 10em')))
        __M_writer('</div>\n            <div class="fsubmit" style="margin-left : 50px">')
        __M_writer(escape(input_submit(value='Submit')))
        __M_writer('</div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        /* Setup user additions to project team */\n        function initform_addprjteam() {\n            var aselect_tt     = dojo.query( \'form#addprjteam select[name=team_type]\' )[0];\n            var select_adduser = dojo.query( \'form#addprjteam select[name=projuser]\' )[0];\n\n            new ZSelect( aselect_tt, null, function( e ) { refresh_projuser( \'toadd\' ) } );\n            new ZSelect( select_adduser, \'addprojuser\', null );\n\n            function addprjteam_onsubmit( e ) {\n                submitform( form_addprjteam, e )\n                dojo.publish( \'flash\', [ \'message\', "Refreshing ..." ] );\n                // Fetch and update the project team member details.\n                projectteams.store.close();\n                projectteams.fetch({ onComplete : projectteams_oncomplete });\n                dojo.stopEvent( e );\n            }\n            new zeta.Form({ onsubmit: addprjteam_onsubmit, formid : \'addprjteam\' });\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_user_disable(context, u, action, eusers):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def multiselect(**kwargs):
            return render_multiselect(context, **kwargs)

        str = context.get('str', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n\n    <form id="userdis" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 7em;">\n                ')
        __M_writer(escape(elements.iconize('Users :', 'users')))
        __M_writer('</div>\n            <div class="fselect vtop">\n                ')
        __M_writer(escape(multiselect(name='disable_user', id='disable_user', options=eusers, size='7', style='width : 15em;')))
        __M_writer('</div>\n            <div class="fsubmit" style="margin-left : 50px">')
        __M_writer(escape(input_submit(value='Disable')))
        __M_writer('</div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        /* Initialise userdis form */\n        function initform_userdis( e ) {\n            seluser_dis = dojo.query( \'select#disable_user\' )[0];\n            new ZSelect( seluser_dis, \'disable_user\', null );\n            function userdis_onsubmit( e ) {\n                submitform( form_userdis, e );\n                dojo.publish( \'flash\', [ \'message\', "Refreshing ..." ]);\n                userstatus.store.close();\n                userstatus.fetch( { onComplete : userstatus_oncomplete } );\n                dojo.stopEvent( e );\n            }\n            new zeta.Form({ onsubmit : userdis_onsubmit, formid : \'userdis\' });\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_deletemount(context, u, action):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form id="deletemount" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='mount_id', id='del_mountid')))
        __M_writer('\n    </form>\n    <script type="text/javascript">\n        function initform_deletemount() {\n            new zeta.Form({ formid: \'deletemount\' });\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_createproject(context, u, licensenames, projectnames, action):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')

        def textarea(**kwargs):
            return render_textarea(context, **kwargs)

        h = context.get('h', UNDEFINED)

        def fieldhelp(help='', fhstyle=''):
            return render_fieldhelp(context, help, fhstyle)

        def input_reset(**kwargs):
            return render_input_reset(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        def select(**kwargs):
            return render_select(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        pn_help = '<b>"projectname" cannot be changed later</b>'
        sm_help = 'one line summary'
        __M_writer('\n\n    <form id="createprj" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='admin', value=u.username)))
        __M_writer('\n    <div class="form">\n        <div class="field">\n            <div class="label" style="width : 15%">Project name :</div>\n            <div class="ftbox" required="true" regExp="')
        __M_writer(escape(h.RE_PNAME))
        __M_writer('">\n                ')
        __M_writer(escape(input_text(name='projectname', id='projectname')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(pn_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 15%;">Summary :</div>\n            <div class="ftbox" required="true">\n                ')
        __M_writer(escape(input_text(name='summary', id='summary', size='64', style='width : 30em;')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(sm_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 15%;">Admin E-mailid :</div>\n            <div class="ftbox" required="true">\n                ')
        __M_writer(escape(input_text(name='admin_email', id='admin_email', value=u.emailid)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 15%;">License :</div>\n            <div class="fselect" required="true">\n                ')
        __M_writer(escape(select(name='licensename', id='licensename', options=licensenames)))
        __M_writer('\n')
        if c.liceditable:
            __M_writer('                    <a class="ml10 fntitalic" href="')
            __M_writer(escape(h.url_crlic))
            __M_writer('"\n                       title="Create a new license for this project">create-license</a>\n')
        else:
            __M_writer('                    <em title="You don\'t have the permission" \n                        class="pointer ml10 undrln fggray">create-license</em>\n')
        __M_writer('            </div>\n        </div>\n        <div class="field">\n            <div class="label vtop" style="width : 15%;">Description :</div>\n            <div class="ftarea" required="true">\n                ')
        __M_writer(escape(elements.captiontextarea('Use wiki markup to compose project description.')))
        __M_writer('\n                ')
        __M_writer(escape(textarea(name='description', tatype='simpletextarea', id='description', cols='90', rows='20', style='width : 100%')))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 15%;"></div>\n            <div class="fsubmit">\n                ')
        __M_writer(escape(input_submit(value='Submit')))
        __M_writer('\n                ')
        __M_writer(escape(input_reset(value='Reset')))
        __M_writer('\n            </div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        function initform_createproject() {\n            function createprj_onsubmit( e ) {\n                var rg_pname  = dijit.byId(\'projectname\').value;\n                var projnames = ')
        __M_writer(h.json.dumps(projectnames))
        __M_writer(';\n                var stopevent = false;\n                var msg       = \'\';\n                if ( dijit.byId(\'createprj\').validate() ) {\n                    for ( i in projnames ) {\n                        if ( projnames[i] == rg_pname ) {\n                            stopevent = true;\n                            msg       = rg_pname+ \' already exists\'\n                        }\n                    }\n                    if (! dojo.attr( dojo.byId( \'licensename\' ), \'value\' )) {\n                        stopevent = true;\n                        msg       = \'Provide the license for project !!\'\n                    }\n                    if (! dojo.attr( dojo.byId( \'description\' ), \'value\' )) {\n                        stopevent = true;\n                        msg       = \'Project description is a must !!\'\n                    }\n                    if (stopevent) {\n                        dojo.publish( \'flash\', [ \'error\', msg, 2000 ]);\n                        dojo.stopEvent( e );\n                    }\n                } else {\n                    dojo.publish( \'flash\', [ \'error\', "Invalid form fields", 2000 ]);\n                    dojo.stopEvent( e );\n                }\n            }\n            new zeta.Form({ onsubmit : createprj_onsubmit, formid : \'createprj\' });\n            dijit.byId( \'projectname\' ).focus();\n        } \n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_wikisummary(context, u, w, action, summary=''):
    context.caller_stack._push_frame()
    try:

        def fieldhelp(help='', fhstyle=''):
            return render_fieldhelp(context, help, fhstyle)

        un_help = context.get('un_help', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form id=\'wikisummary\' action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='wiki_id', value=str(w.id))))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 7em;">\'Summary :\'</div>\n            <div class="ftbox"  required="true">\n                ')
        __M_writer(escape(input_text(name='summary', id='summary', value=summary)))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(un_help)))
        __M_writer('\n            </div>\n        </div>\n    </div>\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_inviteuser(context, u, action):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        str = context.get('str', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')
        __M_writer = context.writer()
        __M_writer('\n    <form id="inviteuser" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    <div class="form">\n        <div class="field">\n            <div class="label">\n                ')
        __M_writer(escape(elements.helpboard("\n                    provide user's emailid whom you want to invite.\n                ")))
        __M_writer('\n            </div>\n            <div class="ftbox" required="true">\n                ')
        __M_writer(escape(input_text(name='emailid', id='emailid', size='32', style='width : 15em;')))
        __M_writer('\n            </div>\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_delprjperms(context, u, p, projusers, defuser, userpgroups, action):
    context.caller_stack._push_frame()
    try:
        elements = _mako_get_namespace(context, 'elements')

        def multiselect(**kwargs):
            return render_multiselect(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def select(**kwargs):
            return render_select(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id=\'delprjperms\' action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 7em;">\n                ')
        __M_writer(escape(elements.iconize('User :', 'user')))
        __M_writer('</div>\n            <div class="fselect"  required="true">\n                ')
        __M_writer(escape(select(name='projuser', options=projusers, opt_selected=defuser, style='width : 10em')))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label vtop" style="width : 7em;">Permissions :</div>\n            <div class="fselect" required="true">\n                ')
        __M_writer(escape(multiselect(name='project_perm_id', id='project_perm_id', options=userpgroups, size='7', style='width : 15em')))
        __M_writer('</div>\n            <div class="fsubmit" style="margin-left : 50px">')
        __M_writer(escape(input_submit(value='Submit')))
        __M_writer('</div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        function initform_delprjperms() {\n            /* Setup permission removals to project user */\n            var dselect_user   = dojo.query( \'form#delprjperms select[name=projuser]\'\n                                           )[0];\n            var select_delperm = dojo.query( \'form#delprjperms select#project_perm_id\'\n                                           )[0];\n            new ZSelect( select_delperm, \'delppgfromuser\', null );\n            new ZSelect( dselect_user, \'projusers\', function( e ) { refresh_prjperms() } );\n            function delprjperms_onsubmit( e ) {\n                submitform( form_delprjperms, e )\n                dojo.publish( \'flash\', [ \'message\', "Refreshing ..." ] );\n                prjperms.store.close();\n                prjperms.fetch({ onComplete : prjperms_oncomplete,\n                                 sort       : [{ attribute : \'username\' }]\n                              });\n                dojo.stopEvent( e );\n            }\n            new zeta.Form({ onsubmit: delprjperms_onsubmit, formid : \'delprjperms\' });\n        }\n        dojo.addOnLoad( initform_delprjperms );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_selectwikipage(context, u, wikipagenames, default=''):
    context.caller_stack._push_frame()
    try:
        sorted = context.get('sorted', UNDEFINED)

        def select(**kwargs):
            return render_select(context, **kwargs)

        x = context.get('x', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        wikipagenames = sorted(wikipagenames, key=lambda x: x[1])
        wikipagenames = [['', '--Select-Wikipage--']] + wikipagenames
        default = default or '--Select-Wikipage--'
        __M_writer('\n    <span class="ml5">\n        ')
        __M_writer(escape(select(name='selectwikipage', id='selectwikipage', options=wikipagenames, opt_selected=default)))
        __M_writer('\n    </span>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_fieldhelp(context, help='', fhstyle=''):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n    <span class="fhelp" style="')
        __M_writer(escape(fhstyle))
        __M_writer('" >')
        __M_writer(help)
        __M_writer('</span>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_selectfilerevision(context, u, revlist, default=''):
    context.caller_stack._push_frame()
    try:

        def select(**kwargs):
            return render_select(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <span class="ml5">\n        <span style="font-size : small;">File Revision :</span>\n        ')
        __M_writer(escape(select(name='selectfrev', id='selectfrev', options=revlist, opt_selected=default)))
        __M_writer('\n    </span>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_sitelogo(context, u, action):
    context.caller_stack._push_frame()
    try:

        def input_file(**kwargs):
            return render_input_file(context, **kwargs)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id="sitelogo" enctype="multipart/form-data" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 12em;">File :</div>\n            <div class="ffile">\n                ')
        __M_writer(escape(input_file(name='sitelogofile', id='sitelogofile', style='width: 40em;')))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 12em;"></div>\n            <div class="fsubmit">')
        __M_writer(escape(input_submit(value='Upload')))
        __M_writer('</div>\n        </div>\n    </div>\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_updatemstn(context, u, p, mstnlist, action):
    context.caller_stack._push_frame()
    try:
        elements = _mako_get_namespace(context, 'elements')

        def textarea(**kwargs):
            return render_textarea(context, **kwargs)

        def fieldhelp(help='', fhstyle=''):
            return render_fieldhelp(context, help, fhstyle)

        def input_radio(**kwargs):
            return render_input_radio(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        def select(**kwargs):
            return render_select(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        mn_help = 'milestone name must be unique'
        __M_writer('\n\n    <div class="w100 mb20">\n        ')
        __M_writer(escape(select(name='updtmstn', id='updtmstn', options=mstnlist)))
        __M_writer('\n        <hr></hr>\n    </div>\n    <form id="updatemstn" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='milestone_id', value='')))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 10em;">Mileston name :</div>\n            <div class="ftbox" required="true">\n                ')
        __M_writer(escape(input_text(name='milestone_name', id='updtmstnname')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(mn_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10em;">Due date :</div>\n            <div class="fdtbox">\n                ')
        __M_writer(escape(input_text(name='due_date', id='updtduedate')))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label vtop" style="width : 10em;">Description : </div>\n            <div class="ftarea" required="true">\n                ')
        __M_writer(escape(elements.captiontextarea('Use wiki markup to compose milestone description.')))
        __M_writer('\n                ')
        __M_writer(escape(textarea(name='description', id='updtmstndesc', cols='50', style='width : 25em')))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10em;">Mark as : </div>\n            <div class="fradio">\n                ')
        __M_writer(escape(input_radio(name='status', id='mstnstatus1', value='cancelled', text='cancelled')))
        __M_writer('\n                ')
        __M_writer(escape(input_radio(name='status', id='mstnstatus2', value='completed', text='completed')))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10em;">Closing remark : </div>\n            <div class="ftarea">\n                ')
        __M_writer(escape(elements.captiontextarea('Use wiki markup to compose closing_remark.')))
        __M_writer('\n                ')
        __M_writer(escape(textarea(name='closing_remark', id='closing_remark', rows='4', cols='50', style='width : 25em')))
        __M_writer('\n                <div>')
        __M_writer(escape(input_submit(value='Update')))
        __M_writer('</div>\n            </div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        /* setup milestone update */\n        function initform_updatemstn() {\n            function updatemstn_onsubmit( e ) {\n                var msg = \'\'\n                dojo.stopEvent(e);\n                if ( dijit.byId(\'updatemstn\').validate() ) {\n                    if (! dojo.attr( dojo.byId( \'updtmstndesc\' ), \'value\' )) {\n                        msg = \'Provide milestone description !!\'\n                    }\n                    if ( dijit.byId( \'mstnstatus1\' ).checked || \n                         dijit.byId( \'mstnstatus2\' ).checked ) {\n                        if (! dojo.attr( dojo.byId( \'closing_remark\' ), \'value\' )) {\n                            msg = \'Provide closing remark !!\'\n                        }\n                    }\n\n                    if ( msg ) {\n                        dojo.publish( \'flash\', [ \'error\', msg, 2000 ]);\n                    } else {\n                        submitform( form_updatemstn, e);\n                        mstnlist.store.close();\n                        mstnlist.fetch({\n                            onComplete : mstnlist_oncomplete,\n                            sort : [ { attribute : \'milestone_name\' } ]\n                        });\n                    }\n                } else {\n                    dojo.publish( \'flash\', [ \'error\', "Invalid form fields", 2000 ]);\n                }\n            }\n            new zeta.Form({ onsubmit: updatemstn_onsubmit, formid : \'updatemstn\' });\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_createmstn(context, u, p, action):
    context.caller_stack._push_frame()
    try:
        elements = _mako_get_namespace(context, 'elements')

        def textarea(**kwargs):
            return render_textarea(context, **kwargs)

        def fieldhelp(help='', fhstyle=''):
            return render_fieldhelp(context, help, fhstyle)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        mn_help = 'milestone name must be unique'
        __M_writer('\n\n    <form id="createmstn" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 10em;">Milestone name :</div>\n            <div class="ftbox" required="true"> \n                ')
        __M_writer(escape(input_text(name='milestone_name', id='crmstnname')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(mn_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10em;">Due date :</div>\n            <div class="fdtbox">\n                ')
        __M_writer(escape(input_text(name='due_date', id='crduedate')))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label vtop" style="width : 10em;">Description : </div>\n            <div class="ftarea" required="true">\n                ')
        __M_writer(escape(elements.captiontextarea('Use wiki markup to compose milestone description.')))
        __M_writer('\n                ')
        __M_writer(escape(textarea(name='description', id='crmstndesc', rows='1', cols='50', style='width : 25em')))
        __M_writer('\n                <br></br>\n                <div>')
        __M_writer(escape(input_submit(value='Create')))
        __M_writer('</div>\n            </div>\n        </div>\n    </div>\n    </form>\n    \n    <script type="text/javascript">\n        /* setup milestone creation */\n        function initform_createmstn() {\n            function createmstn_onsubmit( e ) {\n                var msg     = \'\'\n                if ( dijit.byId(\'createmstn\').validate() ) {\n                    if (! dojo.attr( dojo.byId( \'crmstndesc\' ), \'value\' )) {\n                        msg = \'Provide milestone description !!\'\n                    }\n\n                    if ( msg ) {\n                        dojo.publish( \'flash\', [ \'error\', msg, 2000 ]);\n                    } else {\n                        submitform( form_createmstn, e);\n                        mstnlist.store.close();\n                        mstnlist.fetch({\n                            onComplete : mstnlist_oncomplete,\n                            sort : [ { attribute : \'milestone_name\' } ]\n                        });\n                    }\n                } else {\n                    dojo.publish( \'flash\', [ \'error\', "Invalid form fields", 2000 ]);\n                }\n                dojo.stopEvent(e);\n            }\n            new zeta.Form({ onsubmit: createmstn_onsubmit, formid : \'createmstn\' });\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_project_enable(context, u, action, dprojects):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def multiselect(**kwargs):
            return render_multiselect(context, **kwargs)

        str = context.get('str', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id="prjenb" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 7em;">\n                ')
        __M_writer(escape(elements.iconize('Projects :', 'projects')))
        __M_writer('</div>\n            <div class="fselect vtop" style="width : 20em;">\n                ')
        __M_writer(escape(multiselect(name='enable_project', id='enable_project', options=dprojects, size='7', style='width : 10em;')))
        __M_writer('</div>\n            <div class="fsubmit ml10">')
        __M_writer(escape(input_submit(value='Enable')))
        __M_writer('</div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        /* Initialise prjenb form */\n        function initform_prjenb() {\n            selproj_enb = dojo.query( \'select#enable_project\' )[0];\n            new ZSelect( selproj_enb, \'enable_project\', null );\n            function prjenb_onsubmit( e ) {\n                submitform( form_prjenb, e );\n                dojo.publish( \'flash\', [ \'message\', "Refreshing ..." ]);\n                projectstatus.store.close();\n                projectstatus.fetch( { onComplete : projectstatus_oncomplete } );\n                dojo.stopEvent( e );\n            }\n            new zeta.Form({ onsubmit : prjenb_onsubmit, formid : \'prjenb\' });\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_select(context, **kwargs):
    context.caller_stack._push_frame()
    try:
        unicode = context.get('unicode', UNDEFINED)
        range = context.get('range', UNDEFINED)
        isinstance = context.get('isinstance', UNDEFINED)
        str = context.get('str', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        selected = kwargs.get('opt_selected', '')
        options = kwargs.get('options', [])
        opts_disabled = kwargs.get('opts_disabled', '')
        restrict_kwargs(kwargs, select_attrs)
        attrs = make_attrs(kwargs)
        options = options[:]
        for i in range(len(options)):
            if isinstance(options[i], (str, unicode)):
                options[i] = (
                 options[i], options[i])

        __M_writer('\n    <select ')
        __M_writer(attrs)
        __M_writer('>\n')
        for (val, txt) in options:
            __M_writer('            <option value="')
            __M_writer(escape(val))
            __M_writer('"\n')
            if selected == txt:
                __M_writer('                selected="selected"\n')
            if txt in opts_disabled:
                __M_writer('                disabled="disabled"\n')
            __M_writer('            >')
            __M_writer(escape(txt))
            __M_writer('</option>\n')

        __M_writer('    </select>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_input_submit(context, **kwargs):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n    ')
        restrict_kwargs(kwargs, inputbutton_attrs)
        attrs = make_attrs(kwargs)
        __M_writer('\n    <input type="submit" ')
        __M_writer(attrs)
        __M_writer('></input>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_tckblockedby(context, u, p, action, t=None):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form id="tckblockedby" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='ticket_id', value=t and str(t.id) or '')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='blockedby_ids')))
        __M_writer('\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_tckseverity(context, u, p, action, t=None):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form id="tckseverity" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='ticket_id', value=t and str(t.id) or '')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='tck_severityname', value=t and t.severity.tck_severityname or '')))
        __M_writer('\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_projfav(context, u, p, action, name):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form id=\'projfav\' class="dispnone" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name=name, value=str(u.username))))
        __M_writer('\n    </form>\n\n    <script type="text/javascript">\n        /* Setup favorite project for user */\n        function initform_projfav() {\n            var n_span  = dojo.query( "span[name=favproj]" )[0];\n            var w_form  = new zeta.Form({ normalsub: true, formid: \'projfav\' });\n            var n_field = dojo.query( "input[name=')
        __M_writer(escape(name))
        __M_writer(']", form_projfav )[0];\n            if( n_span && n_field ) {\n                new ZFavorite( n_span, form_projfav, n_field );\n            }\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_projectinfo(context, u, p, licensenames, usernames, licurl, action):
    context.caller_stack._push_frame()
    try:
        elements = _mako_get_namespace(context, 'elements')

        def textarea(**kwargs):
            return render_textarea(context, **kwargs)

        def fieldhelp(help='', fhstyle=''):
            return render_fieldhelp(context, help, fhstyle)

        def input_reset(**kwargs):
            return render_input_reset(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        def select(**kwargs):
            return render_select(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        sm_help = 'one line summary'
        em_help = 'if left empty, your registered email-id will be used.'
        ml_help = 'project mailing-list as comma separated values'
        ir_help = 'project irc-channels as comma separated values'
        pinfo = p.project_info
        mailinglists = (', ').join([ m.mailing_list for m in p.mailinglists ])
        ircchannels = (', ').join([ i.ircchannel for i in p.ircchannels ])
        __M_writer('\n\n    <form id="updateprj" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='projectname', value=str(p.projectname))))
        __M_writer('\n')
        __M_writer('    ')
        __M_writer(escape(input_hidden(name='expose_project', id='exposed', value=p.projectname)))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 10%;">Summary :</div>\n            <div class="ftbox" required="true">\n                ')
        __M_writer(escape(input_text(name='summary', id='summary', size='64', style='width : 30em;', value=p.summary)))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(sm_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10%;">Admin E-mailid :</div>\n            <div class="ftbox">\n                ')
        __M_writer(escape(input_text(name='admin_email', id='admin_email', value=p.admin_email)))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(em_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label vtop" style="width : 10%;">Description :</div>\n            <div class="ftarea" required="true">\n                ')
        __M_writer(escape(elements.captiontextarea('Use wiki markup to compose project description.')))
        __M_writer('\n                ')
        __M_writer(escape(textarea(name='description', id='description', text=p.project_info.description, style='width : 40em')))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10%;">Admin :</div>\n            <div class="fselect" required="true">\n                ')
        __M_writer(escape(select(name='admin', id='admin', options=usernames, opt_selected=p.admin.username)))
        __M_writer('\n                ')
        __M_writer(escape(fieldhelp('if you are changing the administrator, be sure to refresh the page', fhstyle='font-style: italic; color: red')))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10%;">License :</div>\n            <div class="fselect" required="true">\n                ')
        __M_writer(escape(select(name='licensename', id='licensename', options=licensenames, opt_selected=p.license and p.license.licensename or '')))
        __M_writer('\n                <a class="ml5" href="')
        __M_writer(escape(licurl))
        __M_writer('">view-all-license</a>\n            </div>\n        </div>\n')
        __M_writer('        <div class="field">\n            <div class="label" style="width : 10%;">Mailing-lists :</div>\n            <div class="ftbox">\n                ')
        __M_writer(escape(input_text(name='mailinglists', id='mailinglists', size='64', value=mailinglists)))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(ml_help)))
        __M_writer('\n            </div>\n        </div>\n')
        __M_writer('        <div class="field">\n            <div class="label" style="width : 10%;">Irc-channels :</div>\n            <div class="ftbox">\n                ')
        __M_writer(escape(input_text(name='ircchannels', id='ircchannels', size='64', value=ircchannels)))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(ir_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10%;"></div>\n            <div class="fsubmit">\n                ')
        __M_writer(escape(input_submit(value='Submit')))
        __M_writer('\n                ')
        __M_writer(escape(input_reset(value='Reset')))
        __M_writer('\n            </div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        function updateprj_onsubmit( e ) {\n            var msg       = \'\';\n            if ( dijit.byId(\'updateprj\').validate() ) {\n                if (! dojo.attr( dojo.byId( \'licensename\' ), \'value\' )) {\n                    msg       = \'Provide the license for project !!\'\n                }\n                if (! dojo.attr( dojo.byId( \'description\' ), \'value\' )) {\n                    msg       = \'Project description is a must !!\'\n                }\n            } else {\n                msg = "Invalid form fields"\n            }\n            if (msg) {\n                dojo.publish( \'flash\', [ \'error\', msg, 2000 ]);\n            } else {\n                submitform( form_updateprj, e );\n            }\n            dojo.stopEvent( e );\n        }\n        function initform_projectinfo() {\n            new zeta.Form({ onsubmit : updateprj_onsubmit, formid : \'updateprj\' });\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_tckblocking(context, u, p, action, t=None):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form id="tckblocking" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='ticket_id', value=t and str(t.id) or '')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='blocking_ids')))
        __M_writer('\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_selectwikiversion(context, u, versions, default=''):
    context.caller_stack._push_frame()
    try:

        def select(**kwargs):
            return render_select(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <span class="ml5">\n        ')
        __M_writer(escape(select(name='selectwver', id='selectwver', options=versions, opt_selected=default)))
        __M_writer('\n    </span>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_updatewcmt(context, u, w, action, wcmt=None):
    context.caller_stack._push_frame()
    try:
        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def textarea(**kwargs):
            return render_textarea(context, **kwargs)

        elements = _mako_get_namespace(context, 'elements')

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id=\'updatewcmt\' action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='wiki_id', value=str(w.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='wiki_comment_id', value=wcmt and str(wcmt.id) or '')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='commentby', value=u.username)))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='version_id', value=wcmt and str(wcmt.version_id) or '')))
        __M_writer('\n    <div class="w100 form">\n        <div class="w80">\n            ')
        __M_writer(escape(elements.captiontextarea('Use wiki markup to compose wiki comment.')))
        __M_writer('\n            ')
        __M_writer(escape(textarea(name='text', id='upwcmt_text', text=wcmt and wcmt.text or '')))
        __M_writer('\n        </div>\n        <div>')
        __M_writer(escape(input_submit(value='Update')))
        __M_writer('</div>\n    </div>\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_selectrevw(context, u, revwlist, default=''):
    context.caller_stack._push_frame()
    try:

        def select(**kwargs):
            return render_select(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        revwlist = [
         [
          '', '--Select-Review--']] + revwlist
        default = default or '--Select-Review--'
        __M_writer('\n    <span class="ml5">\n        ')
        __M_writer(escape(select(name='selectrevw', id='selectrevw', options=revwlist, opt_selected=default)))
        __M_writer('\n    </span>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_createpg(context, u, permnames, action):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)

        def fieldhelp(help='', fhstyle=''):
            return render_fieldhelp(context, help, fhstyle)

        def multiselect(**kwargs):
            return render_multiselect(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        pg_help = 'small cased, 2 to max %s characters. ' % h.LEN_NAME
        __M_writer('\n\n    <form id="createpg" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 11em;">Permission group :</div>\n            <div class="ftbox" style="width : 25em;" required="true" regExp="[a-z0-9_.]{2,32}">\n                ')
        __M_writer(escape(input_text(name='perm_group', id='cr_perm_group')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(pg_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 11em;">Permission names :</div>\n            <div class="fselect vtop"  style="width : 25em;" required="true">\n                ')
        __M_writer(escape(multiselect(name='perm_name', id='cr_perm_name', options=permnames, size='7', style='width : 17em')))
        __M_writer('</div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 11em;"></div>\n            <div class="fsubmit" style="width : 25em;">')
        __M_writer(escape(input_submit(value='Create')))
        __M_writer('</div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        function initform_createpg() {\n            function createpg_onsubmit( e ) {\n                submitform( form_createpg, e );\n                dojo.publish( \'flash\', [ \'message\', "Refreshing ..." ] );\n                pgmap.store.close() ;\n                pgmap.fetch({\n                    onComplete : dojo.partial( pgmap_oncomplete, true ),\n                    sort       : [{ attribute : \'perm_group\' }]\n                });\n                dojo.stopEvent(e);\n            }\n            new zeta.Form({ onsubmit : createpg_onsubmit, formid : \'createpg\' });\n        } \n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_removelic_h(context, u, action):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n\n    <form id="rmlic" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='licensename', id='licensename')))
        __M_writer('\n    </form>\n\n    <script type="text/javascript">\n        function initform_rmlic() {\n            function removelic( n_remove, n_tr, e ) {\n                var i_licname = dojo.query( \'input#licensename\' )[0];\n                var n_table   = n_tr.parentNode;\n                i_licname.value = dojo.attr( n_tr, \'licensename\' );\n                submitform( form_rmlic, e );\n                n_table.removeChild( n_tr );\n            }\n            dojo.query( \'span[name=rmlic]\' ).forEach(\n                function( n ) {\n                    dojo.connect(\n                        n, \'onclick\', \n                        dojo.partial( removelic, n, n.parentNode.parentNode )\n                    );\n              }\n            );\n            new zeta.Form({ onsubmit : null, formid : \'rmlic\' });\n        }\n        dojo.addOnLoad( initform_rmlic );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_configrev(context, u, p, action):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form class="dispnone" id="configrev" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='review_id', value='')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='resource_url', id='resource_url', value='')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='version', id='version', value='')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='author', id='author', value='')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='moderator', id='moderator', value='')))
        __M_writer('\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_createmount_e(context, u, v, contents, action):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def select(**kwargs):
            return render_select(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        rp_help = 'relative path to repositories root url'
        __M_writer('\n    <div id="mountpopup" class="dispnone p5 bgaliceblue br4"\n         style="border: 1px solid LightSteelBlue">\n        <form id="createmount_e" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n            ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n            ')
        __M_writer(escape(input_hidden(name='vcs_id', value=str(v.id))))
        __M_writer('\n            ')
        __M_writer(escape(input_hidden(name='repospath', id='repospath')))
        __M_writer('\n            ')
        __M_writer(escape(input_text(name='name', id='name')))
        __M_writer('\n            ')
        __M_writer(escape(select(name='content', id='content', options=contents)))
        __M_writer('\n            ')
        __M_writer(escape(input_submit(value='Create')))
        __M_writer('\n        </form>\n        <div name="close" class="fgblue pointer">close</div>\n    </div>\n\n    <script type="text/javascript">\n        function cme_onsubmit( e ) {\n            var i_name = dojo.byId( \'name\' );\n            var i_content = dojo.byId( \'content\' );\n            if( i_name.value && i_content.value ) {\n                submitform( form_createmount_e, e );\n                dojo.publish( \'mounted\', [] );\n            } else {\n                dojo.publish( \'flash\', [ \'error\', \'Complete the form\', 2000 ]);\n            }\n            dojo.stopEvent( e );\n        }\n        function initform_createmount_e() {\n            new zeta.Form({ formid: \'createmount_e\', onsubmit: cme_onsubmit });\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_selectrset(context, u, rsetlist, default=''):
    context.caller_stack._push_frame()
    try:

        def select(**kwargs):
            return render_select(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        rsetlist = [
         [
          '', '--Select-ReviewSet--']] + rsetlist
        default = default or '--Select-ReviewSet--'
        __M_writer('\n    <span class="ml5">\n        ')
        __M_writer(escape(select(name='selectrset', id='selectrset', options=rsetlist, opt_selected=default)))
        __M_writer('\n    </span>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_createticket(context, u, p, action, tck_typenames, tck_severitynames, projusers, components, milestones, versions):
    context.caller_stack._push_frame()
    try:
        elements = _mako_get_namespace(context, 'elements')

        def textarea(**kwargs):
            return render_textarea(context, **kwargs)

        def fieldhelp(help='', fhstyle=''):
            return render_fieldhelp(context, help, fhstyle)

        str = context.get('str', UNDEFINED)
        sorted = context.get('sorted', UNDEFINED)
        x = context.get('x', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        def select(**kwargs):
            return render_select(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        sm_help = 'one line summary'
        blkby_help = 'comma separated list of <b>ticket ids</b> that are blocking this ticket'
        blkng_help = 'comma separated list of <b>ticket ids</b> that are blockedby this ticket'
        pt_help = 'parent <b>ticket id</b>'
        components = [
         [
          '', '--Select-Component--']] + sorted(components, key=lambda x: x[1])
        milestones = [['', '--Select-Milestone--']] + sorted(milestones, key=lambda x: x[1])
        versions = [['', '--Select-Version--']] + sorted(versions, key=lambda x: x[1])
        projusers = sorted(projusers)
        __M_writer('\n\n    <h3 class="ml10">Create Ticket</h3>\n    <form id="createtck" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    <div class="w100">\n      <div class="posr floatl" style="padding-left : 20px;">\n      <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 15%;">Summary :</div>\n            <div class="ftbox" required="true">\n                ')
        __M_writer(escape(input_text(name='summary', id='summary', size='40', style='width : 25em;')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(sm_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 15%;">type :</div>\n            <div class="fselect" required="true">\n                ')
        __M_writer(escape(select(name='tck_typename', id='tck_typename', options=tck_typenames)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 15%;">severity :</div>\n            <div class="fselect" required="true">\n                ')
        __M_writer(escape(select(name='tck_severityname', id='tck_severityname', options=tck_severitynames)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 20%;">prompt user :</div>\n            <div class="fselect">\n                ')
        __M_writer(escape(select(name='promptuser', id='promptuser', options=projusers, opt_selected=u.username)))
        __M_writer('\n            </div>\n        </div>\n      </div>\n      </div>\n      <div class="posr floatl" style="border-left : 3px solid #d6d6d6;">\n      <div class="w100 form mb10">\n        <div class="field w100">\n          <div class="fselect">\n              <div class="floatl m5">\n                  ')
        __M_writer(escape(select(name='component_id', id='component', options=components, opt_selected='--Select-Component--')))
        __M_writer('\n              </div>\n              <div class="floatl m5">\n                  ')
        __M_writer(escape(select(name='milestone_id', id='milestone', options=milestones, opt_selected='--Select-Milestone--')))
        __M_writer('\n              </div>\n              <div class="floatl m5">\n                  ')
        __M_writer(escape(select(name='version_id', id='version', options=versions, opt_selected='--Select-Version--')))
        __M_writer('\n              </div>\n          </div>\n        </div>\n      </div>\n      <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 20%;">blocked by :</div>\n            <div class="ftbox">\n                ')
        __M_writer(escape(input_text(name='blockedby_ids', id='blockedby_ids')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(blkby_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 20%;">blocking :</div>\n            <div class="ftbox">\n                ')
        __M_writer(escape(input_text(name='blocking_ids', id='blocking_ids')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(blkng_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 20%;">parent ticket:</div>\n            <div class="ftbox">\n                ')
        __M_writer(escape(input_text(name='parent_id', id='parent_id')))
        __M_writer('\n                ( ')
        __M_writer(escape(fieldhelp(pt_help)))
        __M_writer(' )\n            </div>\n        </div>\n      </div>\n      </div>\n      <div class="w100 form bclear" style="padding-left : 20px;">\n        <div class="field">\n            <div class="label vtop" style="width : 7%;">Description : </div>\n            <div class="ftarea" required="true">\n                ')
        __M_writer(escape(elements.captiontextarea('Use wiki markup to compose ticket description.')))
        __M_writer('\n                ')
        __M_writer(escape(textarea(name='description', tatype='simpletextarea', id='description', cols='100', rows='7')))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 7%;"></div>\n            <div class="fsubmit">')
        __M_writer(escape(input_submit(value='Create')))
        __M_writer('</div>\n        </div>\n      </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        function initform_createtck() {\n            function createtck_onsubmit( e ) {\n                var stopevent = false;\n                var msg       = \'\';\n                if ( dijit.byId(\'createtck\').validate() ) {\n                    if (! dojo.attr( dojo.byId( \'tck_typename\' ), \'value\' )) {\n                        stopevent = true;\n                        msg       = \'Provide ticket type !!\'\n                    }\n                    if (! dojo.attr( dojo.byId( \'tck_severityname\' ), \'value\' )) {\n                        stopevent = true;\n                        msg       = \'Project ticket severity !!\'\n                    }\n                    if (stopevent) {\n                        dojo.publish( \'flash\', [ \'error\', msg, 2000 ]);\n                        dojo.stopEvent( e );\n                    }\n                } else {\n                    dojo.publish( \'flash\', [ \'error\', "Invalid form fields", 2000 ]);\n                    dojo.stopEvent( e );\n                }\n            }\n            new zeta.Form({ onsubmit : createtck_onsubmit, formid: \'createtck\' });\n            dijit.byId( \'summary\' ).focus();\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_selectvcs(context, u, vcslist, default=''):
    context.caller_stack._push_frame()
    try:

        def select(**kwargs):
            return render_select(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        vcslist = [
         [
          '', '--Select-Repository--']] + vcslist
        default = default or '--Select-Repository--'
        __M_writer('\n    <span class="ml5">\n        <span style="font-size : small;">Project VCS :</span>\n        ')
        __M_writer(escape(select(name='selectvcs', id='selectvcs', options=vcslist, opt_selected=default)))
        __M_writer('\n    </span>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_licenselist(context, lics, default=''):
    context.caller_stack._push_frame()
    try:

        def select(**kwargs):
            return render_select(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        lics = [
         [
          '', '--Select-License--']] + lics
        default = default or '--Select-License--'
        __M_writer('\n    <span style="margin-left : 10px; font-weight: normal;">\n        ')
        __M_writer(escape(select(name='viewlicense', id='viewlicense', options=lics, opt_selected=default)))
        __M_writer('\n    </span>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_addteamperms(context, u, p, teamtypes, deftt, x_teampgroups, action):
    context.caller_stack._push_frame()
    try:
        elements = _mako_get_namespace(context, 'elements')

        def multiselect(**kwargs):
            return render_multiselect(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def select(**kwargs):
            return render_select(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id=\'addteamperms\' action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 10em;">\n                ')
        __M_writer(escape(elements.iconize('Team :', 'team')))
        __M_writer('</div>\n            <div class="fselect"  required="true">\n                ')
        __M_writer(escape(select(name='team_type', id='team_type', options=teamtypes, opt_selected=deftt, style='width : 10em')))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label vtop" style="width : 10em;">Permissions :</div>\n            <div class="fselect" required="true">\n                ')
        __M_writer(escape(multiselect(name='perm_group', id='perm_group', options=x_teampgroups, size='7', style='width : 15em')))
        __M_writer('</div>\n            <div class="fsubmit" style="margin-left : 50px">')
        __M_writer(escape(input_submit(value='Submit')))
        __M_writer('</div>\n        </div>\n    </div>\n    </form>\n    <script type="text/javascript">\n        /* Setup permission additions to project team */\n        function initform_addteamperms() {\n            var aselect_tt     = dojo.query( \'form#addteamperms select[name=team_type]\'\n                                           )[0];\n            var select_addperm = dojo.query( \'form#addteamperms select[name=perm_group]\'\n                                           )[0];\n            new ZSelect( aselect_tt, null, function( e ) { refresh_teamperms( \'toadd\' ) } );\n            new ZSelect( select_addperm, \'addpgtoteam\', null );\n            function addteamperms_onsubmit( e ) {\n                submitform( form_addteamperms, e )\n                dojo.publish( \'flash\', [ \'message\', "Refreshing ..." ] );\n                teamperms.store.close();\n                teamperms.fetch({ onComplete : teamperms_oncomplete });\n                dojo.stopEvent( e );\n            }\n            new zeta.Form({ onsubmit: addteamperms_onsubmit, formid : \'addteamperms\' });\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_textarea(context, **kwargs):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n    ')
        text = kwargs.pop('text', '')
        restrict_kwargs(kwargs, textarea_attrs)
        attrs = make_attrs(kwargs)
        __M_writer('\n    <textarea ')
        __M_writer(attrs)
        __M_writer('>')
        __M_writer(escape(text))
        __M_writer('</textarea>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_attachstags(context, u, action):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form id="attachstags" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='attachment_id')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='tags')))
        __M_writer('\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_votewiki(context, u, p, w, action, upvotes, downvotes, currvote):
    context.caller_stack._push_frame()
    try:
        vote = context.get('vote', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form id=\'votewiki\' class="dispnone" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='wiki_id', value=str(w.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='votedas', value=vote and vote.votedas or '')))
        __M_writer('\n    </form>\n\n    <script type="text/javascript">\n        /* Setup wiki voting form */\n        function initform_votewiki() {\n            var n_span = dojo.query( "span[name=wikivote]" )[0];\n            if( n_span ) {\n                new zeta.Voting({\n                    upvotes: ')
        __M_writer(escape(upvotes))
        __M_writer(',\n                    downvotes: ')
        __M_writer(escape(downvotes))
        __M_writer(",\n                    currvote: '")
        __M_writer(escape(currvote))
        __M_writer("',\n                    formid: 'votewiki'\n                }, n_span );\n            }\n        }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_tckdescription(context, u, p, action, t=None):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def textarea(**kwargs):
            return render_textarea(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id="tckdescription" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='ticket_id', value=t and str(t.id) or '')))
        __M_writer('\n    ')
        __M_writer(escape(textarea(name='description', tatype='simpletextarea', id='description', text=t.description, rows='10', style='width : 100%')))
        __M_writer('\n    ')
        __M_writer(escape(input_submit(value='Update')))
        __M_writer('\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_searchbox(context, u, id, valasbg, action, faces=[]):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <span name="searchbox">\n        <form id=\'')
        __M_writer(escape(id))
        __M_writer('\' class="dispinln" action="')
        __M_writer(escape(action))
        __M_writer('" method="get">\n')
        for (face, val) in faces:
            __M_writer('                ')
            __M_writer(escape(input_hidden(name=face, value=val)))
            __M_writer('\n')

        __M_writer('            ')
        __M_writer(escape(input_text(name='querystring', value=valasbg)))
        __M_writer('\n        </form>\n    </span>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_delparts(context, u, p, r, action):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form class="dispnone" id="delparts" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='review_id', value=str(r.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='participant')))
        __M_writer('\n    </form>\n\n    <script type="text/javascript">\n        function initform_delparts() {\n            new zeta.Form({ formid: \'delparts\' });\n            dojo.subscribe(\n                \'delparticipant\', \n                function( username ) {\n                    dojo.query( \'input[name=participant]\', form_delparts \n                              )[0].value = username;\n                    submitform( form_delparts );\n                }\n            );\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_edittck(context, u, p, t, action, tck_typenames, tck_severitynames, projusers, components, milestones, versions):
    context.caller_stack._push_frame()
    try:
        elements = _mako_get_namespace(context, 'elements')
        compnentname = context.get('compnentname', UNDEFINED)

        def textarea(**kwargs):
            return render_textarea(context, **kwargs)

        h = context.get('h', UNDEFINED)

        def fieldhelp(help='', fhstyle=''):
            return render_fieldhelp(context, help, fhstyle)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        def select(**kwargs):
            return render_select(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        blkby_help = 'Enter blocking ticket ids as comma separated integer values'
        blkng_help = 'Enter blockedby ticket ids as comma separated integer values'
        pt_help = 'Parent ticket id as integer value'
        sm_help = 'A one line summary'
        ds_help = 'Mininum 6 characters to max %s characters.' % h.LEN_DESCRIBE
        componentname = t.components and t.components[0].componentname
        milestone_name = t.milestones and t.milestones[0].milestone_name
        version_name = t.versions and t.versions[0].version_name
        blockedby = (', ').join([ str(tby.id) for tby in t.blockedby ])
        blocking = (', ').join([ str(tng.id) for tng in t.blocking ])
        parent = t.parent and str(t.parent.id) or ''
        __M_writer('\n    <form id="configtck" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='ticket_id', value=str(t.id))))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 12em;">type :</div>\n            <div class="fselect">\n                ')
        __M_writer(escape(select(name='tck_typename', id='tck_typename', options=tck_typenames, opt_selected=t.type.tck_typename)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 12em;">severity :</div>\n            <div class="fselect">\n                ')
        __M_writer(escape(select(name='tck_severityname', id='tck_severityname', options=tck_severitynames, opt_selected=t.severity.tck_severityname)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 12em;">prompt user :</div>\n            <div class="fselect">\n                ')
        __M_writer(escape(select(name='promptuser', id='promptuser', options=projusers, opt_selected=t.promptuser.username)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 12em;">component :</div>\n            <div class="fselect">\n                ')
        __M_writer(escape(select(name='component_id', id='component', options=components, opt_selected=compnentname)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 12em;">milestone :</div>\n            <div class="fselect">\n                ')
        __M_writer(escape(select(name='milestone_id', id='milestone', options=milestones, opt_selected=milestone_name)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 12em;">version :</div>\n            <div class="fselect">\n                ')
        __M_writer(escape(select(name='version_id', id='version', options=versions, opt_selected=version_name)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 12em;">blocked by :</div>\n            <div class="ftbox">\n                ')
        __M_writer(escape(input_text(name='blockedby_ids', id='blockedby_ids', value=blockedby)))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(blkby_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 12em;">blocking :</div>\n            <div class="ftbox">\n                ')
        __M_writer(escape(input_text(name='blocking_ids', id='blocking_ids', value=blocking)))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(blkng_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 12em;">parent ticket:</div>\n            <div class="ftbox">\n                ')
        __M_writer(escape(input_text(name='parent_id', id='parent_id', value=parent)))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(pt_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 12em;">Summary :</div>\n            <div class="ftbox">\n                ')
        __M_writer(escape(input_text(name='summary', id='summary', value=t.summary, size='64', style='width : 30em;')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(sm_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 12em;">Description</div>\n            <div class="ftarea w50">\n                ')
        __M_writer(escape(elements.captiontextarea('Use wiki markup to compose ticket description.')))
        __M_writer('\n                ')
        __M_writer(escape(textarea(name='description', tatype='simpletextarea', id='description', text=t.description, rows='20', style='width : 100%')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(ds_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 12em;"></div>\n            <div class="fsubmit">')
        __M_writer(escape(input_submit(value='Update')))
        __M_writer('</div>\n        </div>\n    </div>\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_userreg(context, action, url_captcha):
    context.caller_stack._push_frame()
    try:
        elements = _mako_get_namespace(context, 'elements')
        h = context.get('h', UNDEFINED)

        def input_password(**kwargs):
            return render_input_password(context, **kwargs)

        def fieldhelp(help='', fhstyle=''):
            return render_fieldhelp(context, help, fhstyle)

        def input_reset(**kwargs):
            return render_input_reset(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        def select(**kwargs):
            return render_select(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        un_help = 'All small case, between 3 characters to %s characters.' % h.LEN_NAME
        em_help = 'Your communication email id.'
        pw_help = 'Use a password of minimum 4 characters.'
        __M_writer('\n\n    <form id="userreg" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 10em;">Username :</div>\n            <div class="ftbox" style="width : 40em;" required="true" regExp="')
        __M_writer(escape(h.RE_UNAME))
        __M_writer('">\n                ')
        __M_writer(escape(input_text(name='username', id='username')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(un_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10em;">Email-id :</div>\n            <div class="ftbox" style="width : 40em;" required="true" regExp="')
        __M_writer(escape(h.RE_EMAIL))
        __M_writer('">\n                ')
        __M_writer(escape(input_text(name='emailid', id='emailid')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(em_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10em;">Password :</div>\n            <div class="fpass" style="width : 40em;" required="true" regExp="')
        __M_writer(escape(h.RE_PASSWD))
        __M_writer('">\n                ')
        __M_writer(escape(input_password(name='password', id='password')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(pw_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10em;">Confirm password :</div>\n            <div class="fpass" style="width : 40em;" required="true">\n                ')
        __M_writer(escape(input_password(name='confpass', id='confpass')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(pw_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10em;">Timezone :</div>\n            <div class="fselect" style="width : 40em;">\n                ')
        __M_writer(escape(select(name='timezone', id='timezone', options=h.all_timezones, opt_selected='UTC')))
        __M_writer('</div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10em;"></div>\n            <div class="fsubmit">\n                <div>\n                    <a target="_blank" href="')
        __M_writer(escape(h.url_tos))
        __M_writer('">Terms of Service</a>\n                 </div>\n                <div class="pt5 fgcrimson">\n                    By submitting this form, it is implied that you are agreeing\n                    to Terms of Service\n                </div>\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10em;">Captcha :</div>\n            ')
        __M_writer(escape(elements.captcha(url_captcha)))
        __M_writer('\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10em;"></div>\n            <div class="fsubmit" sytle="width : 40em;">\n                ')
        __M_writer(escape(input_submit(value='Submit')))
        __M_writer('\n                ')
        __M_writer(escape(input_reset(value='Reset')))
        __M_writer('\n            </div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        function initform_userreg() {\n            function userreg_onsubmit( e ) {\n                var rg_uname = dijit.byId(\'username\').value;\n                if ( dijit.byId(\'userreg\').validate() ) {\n                    for ( i = 0; i < usernames.length; i++ ) {\n                        if ( usernames[i] == rg_uname ) {\n                            dojo.publish( \'flash\', [ \'error\', rg_uname+\' already exists\', 2000 ]);\n                            dojo.stopEvent( e );\n                         }\n                    }\n                } else {\n                    dojo.publish( \'flash\', [ \'error\', "Invalid form fields", 2000 ]);\n                    dojo.stopEvent( e );\n                }\n            }\n            new zeta.Form({ onsubmit : userreg_onsubmit, formid : \'userreg\' });\n            dijit.byId( \'username\' ).focus();\n        } \n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_tckcomponent(context, u, p, action, t=None):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form id="tckcomponent" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='ticket_id', value=t and str(t.id) or '')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='component_id')))
        __M_writer('\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_user_enable(context, u, action, dusers):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def multiselect(**kwargs):
            return render_multiselect(context, **kwargs)

        str = context.get('str', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n\n    <form id="userenb" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 7em;">\n                ')
        __M_writer(escape(elements.iconize('Users :', 'users')))
        __M_writer('</div>\n            <div class="fselect vtop">\n                ')
        __M_writer(escape(multiselect(name='enable_user', id='enable_user', options=dusers, size='7', style='width : 15em;')))
        __M_writer('</div>\n            <div class="fsubmit" style="margin-left : 50px">')
        __M_writer(escape(input_submit(value='Enable')))
        __M_writer('</div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        /* Initialise userenb form */\n        function initform_userenb( e ) {\n            seluser_enb = dojo.query( \'select#enable_user\' )[0];\n            new ZSelect( seluser_enb, \'enable_user\', null );\n            function userenb_onsubmit( e ) {\n                submitform( form_userenb, e );\n                dojo.publish( \'flash\', [ \'message\', "Refreshing ..." ]);\n                userstatus.store.close();\n                userstatus.fetch( { onComplete : userstatus_oncomplete } );\n                dojo.stopEvent( e );\n            }\n            new zeta.Form({ onsubmit : userenb_onsubmit, formid : \'userenb\' });\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_delprjteam(context, u, p, teamtypes, deftt, teamusers, action):
    context.caller_stack._push_frame()
    try:
        elements = _mako_get_namespace(context, 'elements')

        def multiselect(**kwargs):
            return render_multiselect(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def select(**kwargs):
            return render_select(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id=\'delprjteam\' action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 10em;">\n                ')
        __M_writer(escape(elements.iconize('Team :', 'team')))
        __M_writer('</div>\n            <div class="fselect"  required="true">\n                ')
        __M_writer(escape(select(name='team_type', id='team_type', options=teamtypes, opt_selected=deftt, style='width : 10em')))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label vtop" style="width : 10em;">\n                ')
        __M_writer(escape(elements.iconize('Users :', 'users')))
        __M_writer('</div>\n            <div class="fselect" required="true">\n                ')
        __M_writer(escape(multiselect(name='project_team_id', id='project_team_id', options=teamusers, size='7', style='width : 10em')))
        __M_writer('</div>\n            <div class="fsubmit" style="margin-left : 50px">')
        __M_writer(escape(input_submit(value='Submit')))
        __M_writer('</div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        function initform_delprjteam() {\n            /* Setup user removal from project team */\n            var dselect_tt     = dojo.query( \'form#delprjteam select[name=team_type]\' )[0];\n            var select_deluser = dojo.query( \'form#delprjteam select#project_team_id\' )[0];\n\n            new ZSelect( dselect_tt, null, function( e ) { refresh_projuser( \'todel\' ) } );\n            new ZSelect( select_deluser, \'delprojuser\', null );\n\n            function delprjteam_onsubmit( e ) {\n                submitform( form_delprjteam, e )\n                dojo.publish( \'flash\', [ \'message\', "Refreshing ..." ] );\n                // Fetch and update the project team member details.\n                projectteams.store.close();\n                projectteams.fetch({ onComplete : projectteams_oncomplete });\n                dojo.stopEvent( e );\n            }\n            new zeta.Form({ onsubmit: delprjteam_onsubmit, formid : \'delprjteam\' });\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_systemconfig(context, u, entries, action):
    context.caller_stack._push_frame()
    try:
        Exception = context.get('Exception', UNDEFINED)
        set = context.get('set', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')
        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        if set(infofields + cnffields) != set(entries):
            raise Exception('Mismatch in system fields')
        help = {'welcomestring': "This string will be displayed on the page bar of site's\n                    homepage", 
           'specialtags': 'Some tags are special, in the sense that they will be\n                    interpreted by the application', 
           'projteamtypes': 'Registered users can be part of a project only via a\n                    team. Add team types for all the projects hosted under\n                    this site, <em>non-members</em> denote registered users\n                    who are not part of the project', 
           'tickettypes': 'Tickets can have type, it gives an idea about the\n                    ticket', 
           'ticketseverity': 'Ticket severity should indicate at what priority it\n                    should be addressed. Note that, sometimes important\n                    ticket need not be urgent', 
           'ticketstatus': "And this is how a ticket is tracked, typically a ticket\n                    begins its life as 'new', travels through one of\n                    its different states, that is defined here and finally moves on\n                    to a resolved state.", 
           'ticketresolv': 'Should be a sub-set of ticket-status list, and\n                    indicates that a ticket is resolved upon moving to this\n                    state.', 
           'wikitypes': 'Documents can also can have types, define them here', 
           'def_wikitype': 'Should be present in the list of `wikitypes`. On creating\n                    a wiki page, it is always marked with the default\n                    type', 
           'reviewactions': '<em>Authors</em> must take actions on review comments,\n                    define the type of actions here', 
           'reviewnatures': 'Nature of review comment. Sometimes, marking a comment\n                    as `cosmetic` can avoid lot of debate.', 
           'vcstypes': 'Supported list of version control systems, integratable\n                    with your site.', 
           'googlemaps': '\n                    <a href="http://code.google.com/apis/maps/signup.html">sign-up</a>\n                    google map key for your site and copy the key here. If\n                    left empty, google-maps will not be enabled.', 
           'strictauth': 'Setting this to `True` will completely restrict\n                    anonymous user. This feature is still evolving', 
           'regrbyinvite': 'By default anybody can register in the site. In case\n                    this is not desirable, set `regrbyinvite` to `True`', 
           'invitebyall': 'If `regrbyinvite` is set to `True`, `invitebyall`\n                    defines who can invite new users. By default, only site\n                    administrator can invite, if set to `True` any registered\n                    user under this site can invite new users'}
        __M_writer('\n\n    <div class="w100 calign fgred">\n        All the confguration fields here pertains to entire site,\n        applicable to all projects created in this site\n    </div>\n    <div class="disptable w100">\n    <div class="disptrow">\n        <div class="disptcell w60">\n        <form id="system" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n        ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n        <div class="disptable ml50" style="border-collapse: separate; border-spacing: 10px">\n')
        for field in cnffields:
            __M_writer('            <div class="disptrow">\n                <div class="disptcell fntbold pb20">')
            __M_writer(escape(field))
            __M_writer('</div>\n                <div class="disptcell ftbox pb20">\n                    ')
            __M_writer(escape(input_text(name=field, style='width: 30em;', id='sys_' + field, value=entries[field])))
            __M_writer('\n                </div>\n                <div class="disptcell">\n                <div class="ml10">\n                    ')
            __M_writer(escape(elements.helpboard(help.get(field, ''), styles='padding: 5px')))
            __M_writer('\n                </div>\n                </div>\n            </div>\n')

        __M_writer('            <div class="disptrow">\n                <div class="disptcell"></div>\n                <div class="disptcell">')
        __M_writer(escape(input_submit(value='Update')))
        __M_writer('</div>\n            </div>\n        </div>\n        </form>\n        </div>\n    </div>\n    </div>\n\n    <script type="text/javascript">\n        /* Initialise system form */\n        function initform_system( e ) {\n            new zeta.Form({ normalsub : true, formid : \'system\' });\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_tckfav(context, u, p, t, action, name):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form id=\'tckfav\' class="dispnone" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='ticket_id', value=str(t.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name=name, value=str(u.username))))
        __M_writer('\n    </form>\n\n    <script type="text/javascript">\n        /* Setup favorite ticket for user */\n        function initform_tckfav() {\n            var n_span  = dojo.query( "span[name=favtck]" )[0];\n            var w_form  = new zeta.Form({ normalsub: true, formid: \'tckfav\' });\n            var n_field = dojo.query( "input[name=')
        __M_writer(escape(name))
        __M_writer(']", form_tckfav )[0];\n            if( n_span && n_field ) {\n                new ZFavorite( n_span, form_tckfav, n_field );\n            }\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_createlicense(context, u, action):
    context.caller_stack._push_frame()
    try:

        def textarea(**kwargs):
            return render_textarea(context, **kwargs)

        def fieldhelp(help='', fhstyle=''):
            return render_fieldhelp(context, help, fhstyle)

        def input_reset(**kwargs):
            return render_input_reset(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        ln_help = 'licensename must be unique'
        sm_help = 'one line summary'
        src_help = 'license originator'
        __M_writer('\n\n    <form id="createlic" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    <div class="form 40em">\n        <div class="field pt20">\n            <div class="label" style="width : 12%;">License name :</div>\n            <div class="ftbox" required="true">\n                ')
        __M_writer(escape(input_text(name='licensename', id='licensename', size='32', style='width : 15em;')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(ln_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 12%;">Summary :</div>\n            <div class="ftbox" required="true">\n                ')
        __M_writer(escape(input_text(name='summary', id='summary', size='64', style='width : 30em;')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(sm_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 12%;">Source :</div>\n            <div class="ftbox" required="true">\n                ')
        __M_writer(escape(input_text(name='source', id='source', size='64', style='width : 30em;')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(src_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label vtop"  style="width : 12%;">License Text :</div>\n            <div class="ftarea" required="true">\n                ')
        __M_writer(escape(textarea(name='text', tatype='simpletextarea', id='text', cols='80', rows='20', style='width : 100%')))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 12%;"></div>\n            <div class="fsubmit">\n                ')
        __M_writer(escape(input_submit(value='Submit')))
        __M_writer('\n                ')
        __M_writer(escape(input_reset(value='Reset')))
        __M_writer('\n            </div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        function initform_liccreate() {\n            function createlic_onsubmit( e ) {\n                if ( dijit.byId( \'createlic\' ).validate() ) {\n                    var lictext = dojo.byId( \'text\' ).value\n                    if(! lictext ) {\n                        dojo.publish(\n                            \'flash\', [ \'error\', "License text must be present", 2000 ]\n                        );\n                        dojo.stopEvent( e );\n                    }\n                } else {\n                    dojo.publish( \'flash\', [ \'error\', "Invalid form fields", 2000 ]);\n                    dojo.stopEvent( e );\n                }\n            }\n            new zeta.Form({ onsubmit : createlic_onsubmit, formid : \'createlic\' });\n            dijit.byId( \'licensename\' ).focus();\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_tcktype(context, u, p, action, t=None):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form id="tcktype" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='ticket_id', value=t and str(t.id) or '')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='tck_typename', value=t and t.type.tck_typename or '')))
        __M_writer('\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_updtpass(context, u, action):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)

        def input_password(**kwargs):
            return render_input_password(context, **kwargs)

        def fieldhelp(help='', fhstyle=''):
            return render_fieldhelp(context, help, fhstyle)

        def input_reset(**kwargs):
            return render_input_reset(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        pw_help = 'Should be a minimum of 4 character password.'
        __M_writer('\n\n    <form id="updtpass" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 15em;">Enter new password :</div>\n            <div class="fpass" required="true" regExp="')
        __M_writer(escape(h.RE_PASSWD))
        __M_writer('">\n                ')
        __M_writer(escape(input_password(name='password', id='password')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(pw_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 15em;">Confirm password :</div>\n            <div class="fpass" required="true">\n                ')
        __M_writer(escape(input_password(name='confpass', id='confpass')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(pw_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 15em;"></div>\n            <div class="fsubmit">\n                ')
        __M_writer(escape(input_submit(value='Submit')))
        __M_writer('\n                ')
        __M_writer(escape(input_reset(value='Reset')))
        __M_writer('\n            </div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        function initform_updtpass() {\n            function updtpass_onsubmit( e ) {\n                password = dijit.byId( \'password\' ).value;\n                confpass = dijit.byId( \'confpass\' ).value;\n                if ( password == \'\' ) {\n                    dojo.publish( \'flash\', [ \'error\', "Enter password", 2000 ] );\n                } else if ( password != confpass ) {\n                    dojo.publish( \'flash\', [ \'error\', "Re-type the exact password", 2000 ]\n                    );\n                } else {\n                    submitform( form_updtpass, e );\n                }\n                dijit.byId( \'password\' ).value = \'\';\n                dijit.byId( \'confpass\' ).value = \'\';\n                dojo.stopEvent( e );\n            }\n            new zeta.Form({ onsubmit : updtpass_onsubmit, formid : \'updtpass\' });\n        } \n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_tckmilestone(context, u, p, action, t=None):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form id="tckmilestone" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='ticket_id', value=t and str(t.id) or '')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='milestone_id')))
        __M_writer('\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_search(context, querystring, u, action, allfaces, faces):
    context.caller_stack._push_frame()
    try:
        sorted = context.get('sorted', UNDEFINED)

        def input_checkbox(**kwargs):
            return render_input_checkbox(context, **kwargs)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        project = faces.get('project', '')
        faces = faces.keys()
        __M_writer('\n    <form id=\'searchadv\' action="')
        __M_writer(escape(action))
        __M_writer('" method="get">\n')
        if project:
            __M_writer('            ')
            __M_writer(escape(input_hidden(name='project', value=project)))
            __M_writer('\n')
        __M_writer('        <div class="">\n            <span class="ml20 fntbold fntitalic">Filter By : </span>\n')
        for face in sorted(allfaces.keys()):
            __M_writer('                <span class="mr10">\n                    ')
            checked = face in faces
            __M_writer('\n')
            if checked:
                __M_writer('                        ')
                __M_writer(escape(input_checkbox(name=face, value=allfaces[face], checked='checked')))
                __M_writer(' ')
                __M_writer(escape(face.upper()))
                __M_writer('\n')
            else:
                __M_writer('                        ')
                __M_writer(escape(input_checkbox(name=face, value=allfaces[face])))
                __M_writer(' ')
                __M_writer(escape(face.upper()))
                __M_writer('\n')
            __M_writer('                </span>\n')

        __M_writer('            <span class="mr10">\n                ')
        checked = 'all' in faces
        __M_writer('\n')
        if checked:
            __M_writer('                    ')
            __M_writer(escape(input_checkbox(name='all', value='1', checked='checked')))
            __M_writer(' ALL\n')
        else:
            __M_writer('                    ')
            __M_writer(escape(input_checkbox(name='all', value='1')))
            __M_writer(' ALL\n')
        __M_writer('            </span>\n        </div>\n        <div class="mt10 ml50">\n            ')
        __M_writer(escape(input_text(id='facetedsr', name='querystring', value=querystring)))
        __M_writer('\n            ')
        __M_writer(escape(input_submit(value='Search')))
        __M_writer('\n        </div>\n    </form>\n\n    <script type="text/javascript">\n        function initform_searchadv() {\n            n = dojo.byId( \'facetedsr\' );\n            n.focus();\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_forgotpass(context, action):
    context.caller_stack._push_frame()
    try:
        elements = _mako_get_namespace(context, 'elements')

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id="forgotpass" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    <div class="form">\n        <div class="field">\n            <div class="label">\n                ')
        __M_writer(escape(elements.helpboard('\n                    Enter the email id that you have registered with us\n                ')))
        __M_writer('\n            </div>\n            <div class="ftbox" required="true">\n                ')
        __M_writer(escape(input_text(name='emailid', id='emailid', size='32', style='width : 15em;')))
        __M_writer('\n            </div>\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_createrset(context, u, p, action, reload):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id=\'createrset\' action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    <div class="form">\n        <div class="field">\n            <div class="label" style="">New ReviewSet :</div>\n            <div class="ftbox" required=True>\n                ')
        __M_writer(escape(input_text(name='name', id='name')))
        __M_writer('\n            </div>\n            <div class="fsubmit">\n                ')
        __M_writer(escape(input_submit(value='Create')))
        __M_writer('\n            </div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        function createrset_onsubmit(e) {\n            var reloadurl = "')
        __M_writer(reload)
        __M_writer('";\n            submitform( form_createrset, e );\n            dojo.stopEvent(e);\n            if( reloadurl) { window.location = reloadurl; }\n        }\n        function initform_createrset() {\n            new zeta.Form({ onsubmit: createrset_onsubmit, \n                            formid: \'createrset\' });\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_createtcmt(context, u, p, t, action):
    context.caller_stack._push_frame()
    try:

        def textarea(**kwargs):
            return render_textarea(context, **kwargs)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id=\'createtcmt\' action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='ticket_id', value=str(t.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='commentby', value=u.username)))
        __M_writer('\n    <div class="w100 form">\n        <div class="w80">\n            ')
        __M_writer(escape(elements.captiontextarea('Use wiki markup to compose ticket comment.')))
        __M_writer('\n            ')
        __M_writer(escape(textarea(name='text', id='crtcmt_text')))
        __M_writer('\n        </div>\n        <div>')
        __M_writer(escape(input_submit(value='Add')))
        __M_writer('</div>\n    </div>\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_delfromrset(context, u, p, rs, action, revwlist, reload=None):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def select(**kwargs):
            return render_select(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        revwlist = [
         [
          '', '--Remove Review from Set--']] + revwlist
        __M_writer('\n    <form id=\'delfromrset\' action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='rset_id', value=str(rs.id))))
        __M_writer('\n    ')
        __M_writer(escape(select(name='review_id', id='del_review_id', options=revwlist)))
        __M_writer('\n    </form>\n\n    <script type="text/javascript">\n        function initform_delfromrset() {\n            var n_selrid = dojo.byId( \'del_review_id\' );\n\n            new zeta.Form({ formid: \'delfromrset\' });\n\n            // Submit form on selecting review to remove\n            dojo.connect(\n                n_selrid, \'onchange\',\n                function( e ) {\n                    var reloadurl = "')
        __M_writer(reload)
        __M_writer('";\n                    if( n_selrid.value ) { submitform( form_delfromrset, e ); }\n                    dojo.stopEvent( e );\n                    if( reloadurl ) { window.location = reloadurl; }\n                }\n            );\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_createver(context, u, p, action):
    context.caller_stack._push_frame()
    try:
        elements = _mako_get_namespace(context, 'elements')

        def textarea(**kwargs):
            return render_textarea(context, **kwargs)

        def fieldhelp(help='', fhstyle=''):
            return render_fieldhelp(context, help, fhstyle)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        vn_help = 'version name must be unique'
        __M_writer('\n\n    <form id="createver" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 10em;">Version name :</div>\n            <div class="ftbox" required="true">\n                ')
        __M_writer(escape(input_text(name='version_name', id='crvername')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(vn_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label vtop" style="width : 10em;">Description : </div>\n            <div class="ftarea" required="true">\n                ')
        __M_writer(escape(elements.captiontextarea('Use wiki markup to compose version description.')))
        __M_writer('\n                ')
        __M_writer(escape(textarea(name='description', id='crverdesc', rows='1', cols='50', style='width : 25em')))
        __M_writer('\n                <div>')
        __M_writer(escape(input_submit(value='Create')))
        __M_writer('</div>\n            </div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        /* setup version creation */\n        function initform_createver() {\n            function createver_onsubmit( e ) {\n                var msg = \'\'\n                if ( dijit.byId(\'createver\').validate() ) {\n                    if (! dojo.attr( dojo.byId( \'crverdesc\' ), \'value\' )) {\n                        msg = \'Provide version description !!\'\n                    }\n\n                    if ( msg ) {\n                        dojo.publish( \'flash\', [ \'error\', msg, 2000 ]);\n                    } else {\n                        submitform( form_createver, e );\n                        verlist.store.close();\n                        verlist.fetch({\n                            onComplete : verlist_oncomplete,\n                            sort : [ { attribute : \'version_name\' } ]\n                        });\n                    }\n                } else {\n                    dojo.publish( \'flash\', [ \'error\', "Invalid form fields", 2000 ]);\n                }\n                dojo.stopEvent(e);\n            }\n            new zeta.Form({ onsubmit: createver_onsubmit, formid : \'createver\' });\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_closerev(context, u, p, r, action):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_radio(**kwargs):
            return render_input_radio(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form class="dispnone" id="closerev" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='review_id', value=str(r.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='command', value='')))
        __M_writer('\n')
        if r.closed:
            __M_writer('        Open  : ')
            __M_writer(escape(input_radio(name='radiocommand', value='open')))
            __M_writer('\n        Close : ')
            __M_writer(escape(input_radio(name='radiocommand', value='close', checked='checked')))
            __M_writer('\n')
        else:
            __M_writer('        Open  : ')
            __M_writer(escape(input_radio(name='radiocommand', value='open', checked='checked')))
            __M_writer('\n        Close : ')
            __M_writer(escape(input_radio(name='radiocommand', value='close')))
            __M_writer('\n')
        __M_writer('    </form>\n\n    <script type="text/javascript">\n        function onchange_command( value, e ) {\n            var i_command = dojo.query( \'input[name=command]\', form_closerev )[0];\n            dojo.attr( i_command,\'value\', value );\n            submitform( form_closerev, e );\n            dojo.stopEvent( e );\n        }\n        function initform_closerev() {\n            new zeta.Form({ formid: \'closerev\' });\n            var radios = dojo.query( \'input[name=radiocommand]\' );\n            dojo.connect( radios[0], \'onchange\', dojo.partial( onchange_command, \'open\' ));\n            dojo.connect( radios[1], \'onchange\', dojo.partial( onchange_command, \'close\' ));\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_configwiki(context, u, action, w='', typename='', summary=''):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form id=\'configwiki\' action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='wiki_id', value=str(w and w.id or ''))))
        __M_writer('\n    <div class="w100 form">\n        ')
        __M_writer(escape(input_text(name='wiki_typename', id='wiki_typename', value=typename)))
        __M_writer('\n        ')
        __M_writer(escape(input_text(name='summary', id='summary', value=summary)))
        __M_writer('\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        function initform_configwiki() {\n            new zeta.Form({ normalsub: true, formid: \'configwiki\' });\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_del_userrelations(context, u, reltypes, action):
    context.caller_stack._push_frame()
    try:
        elements = _mako_get_namespace(context, 'elements')

        def multiselect(**kwargs):
            return render_multiselect(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def select(**kwargs):
            return render_select(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id=\'deluserrels\' action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 7em;">\n                ')
        __M_writer(escape(elements.iconize('Relation :', 'relation')))
        __M_writer('</div>\n            <div class="fselect"  style="width : 20em;" required="true">\n                ')
        __M_writer(escape(select(name='userrel_type', id='userrel_type', options=reltypes, style='width : 10em')))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 7em;">\n                ')
        __M_writer(escape(elements.iconize('Users :', 'users')))
        __M_writer('</div>\n            <div class="fselect" style="width : 20em;" required="true">\n                ')
        __M_writer(escape(multiselect(name='user_relation_id', id='user_relation_id', options=[], size='4', style='width : 10em')))
        __M_writer('</div>\n            <div class="fsubmit ml10">')
        __M_writer(escape(input_submit(value='Delete')))
        __M_writer('</div>\n        </div>\n    </div>\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_votetck(context, u, p, t, action, upvotes, downvotes, currvote):
    context.caller_stack._push_frame()
    try:
        vote = context.get('vote', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form id=\'votetck\' class="dispnone" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='ticket_id', value=str(t.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='votedas', value=vote and vote.votedas or '')))
        __M_writer('\n    </form>\n\n    <script type="text/javascript">\n        /* Setup ticket voting form */\n        function initform_votetck() {\n            var n_span = dojo.query( "span[name=tckvote]" )[0];\n            if( n_span ) {\n                new zeta.Voting({\n                    upvotes: ')
        __M_writer(escape(upvotes))
        __M_writer(',\n                    downvotes: ')
        __M_writer(escape(downvotes))
        __M_writer(",\n                    currvote: '")
        __M_writer(escape(currvote))
        __M_writer("',\n                    formid: 'votetck'\n                }, n_span );\n            }\n        }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_input_file(context, **kwargs):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n    ')
        restrict_kwargs(kwargs, inputfile_attrs)
        attrs = make_attrs(kwargs)
        __M_writer('\n    <input type="file" ')
        __M_writer(attrs)
        __M_writer('></input>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_wikidiff(context, u, w, action, wikicontents):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_radio(**kwargs):
            return render_input_radio(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        wikicontents = wikicontents[:]
        wikicontents.reverse()
        __M_writer('\n\n    <form id="wikidiff" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='wiki_id', value=str(w.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_submit(value='View changes')))
        __M_writer('\n    <table class="zwhistory">\n        <thead><tr>\n        <th class="zwhcmp" colspan="2">O/N</th>\n        <th class="zwhver"> Version </th>\n        <th class="zwhdesc"> Description </th>\n        </tr></thead>\n')
        for wcnt in wikicontents:
            __M_writer('        <tr>\n        <td class="zwhcmp">')
            __M_writer(escape(input_radio(name='oldver', value=str(wcnt.id))))
            __M_writer('</td>\n        <td class="zwhcmp">')
            __M_writer(escape(input_radio(name='newver', value=str(wcnt.id))))
            __M_writer('</td>\n        <td class="zwhver"> ')
            __M_writer(escape(wcnt.id))
            __M_writer(' </td>\n        <td class="zwhdesc">\n            Authored by <a href="')
            __M_writer(escape(h.url_foruser(wcnt.author)))
            __M_writer('">')
            __M_writer(escape(wcnt.author))
            __M_writer('</a>,\n            on ')
            __M_writer(escape(h.utc_2_usertz(wcnt.created_on, u.timezone).strftime('%b %d, %Y, %r')))
            __M_writer('\n        </td>\n        </tr>\n')

        __M_writer('    </table>\n    </form>\n\n    <script type="text/javascript">\n        function initform_wikidiff() {\n            new zeta.Form({ formid: \'wikidiff\' });\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_createmount(context, u, vcslist, contents, action):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def select(**kwargs):
            return render_select(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id="createmount" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    <div class="form">\n        <div class="disptrow">\n            <div class="ftbox" required="true">\n                 <em>name</em>')
        __M_writer(escape(input_text(name='name', id='name')))
        __M_writer('\n            </div>\n            <div class="fselect" required="true">\n                ')
        __M_writer(escape(select(name='content', id='content', options=contents)))
        __M_writer('\n            </div>\n            <div class="fselect" required="true">\n                ')
        __M_writer(escape(select(name='vcs_id', id='vcs_id', options=vcslist)))
        __M_writer('\n            </div>\n            <div class="ftbox" required="true">\n                <em>relative-path</em>')
        __M_writer(escape(input_text(name='repospath', id='repospath')))
        __M_writer('\n            </div>\n            <div class="pl20 fsubmit">')
        __M_writer(escape(input_submit(value='Create')))
        __M_writer('</div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        function initform_createmount() {\n            new zeta.Form({ formid: \'createmount\' });\n            dijit.byId( \'name\' ).focus();\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_replyrcmt(context, u, p, r, action):
    context.caller_stack._push_frame()
    try:

        def textarea(**kwargs):
            return render_textarea(context, **kwargs)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id=\'replyrcmt\' action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='review_id', value=str(r.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='commentby', value=u.username)))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='replytocomment_id', value='')))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="ftarea" required="true">\n                ')
        __M_writer(escape(elements.captiontextarea('Use wiki markup to compose review comment.')))
        __M_writer('\n                ')
        __M_writer(escape(textarea(name='text', tatype='simpletextarea', id='rprcmt_text', cols='90', rows='1', style='width : 100%')))
        __M_writer('\n                ')
        __M_writer(escape(input_submit(value='Reply')))
        __M_writer('\n            </div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        // Setup review comment reply form\n        function initform_replyrcmt() {\n            function replyrcmt_onsubmit( e ) {\n                var i_r2cmt = dojo.query( \'input[name=replytocomment_id]\', form_replyrcmt )[0];\n                submitform( form_replyrcmt, e );\n                dojo.publish( \'flash\', [ \'message\', "Refreshing ..." ] );\n                dojo.stopEvent(e);\n                dojo.publish( \'refreshrcomments\', [ \'replyrcmt\', i_r2cmt.value ] );\n            }\n            new zeta.Form({ onsubmit: replyrcmt_onsubmit, formid: \'replyrcmt\' });\n        }\n        dojo.addOnLoad( initform_replyrcmt );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_revwmoderator(context, u, p, r, action, projusers):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def select(**kwargs):
            return render_select(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        projusers = [
         [
          '', '--Select-Moderator--']] + projusers
        default = r.moderator and r.moderator.username or '--Select-Moderator--'
        if not r.moderator:
            default = '--Select-Moderator--'
        elif r.moderator.username not in projusers:
            default = '--Select-Moderator--'
        else:
            default = r.moderator.username
        __M_writer('\n    <form class="dispnone" id="revwmoderator" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='review_id', value=str(r.id))))
        __M_writer('\n    ')
        __M_writer(escape(select(name='moderator', options=projusers, opt_selected=default)))
        __M_writer('\n    </form>\n\n    <script type="text/javascript">\n        function initform_revwmoderator() {\n            new zeta.Form({ formid: \'revwmoderator\' });\n            var n_select = dojo.query( \'select[name=moderator]\', form_revwmoderator )[0];\n            // Submit the form on selecting the moderator\n            dojo.connect( n_select, \'onchange\',\n                          function( e ) {\n                              submitform( form_revwmoderator, e );\n                              dojo.stopEvent( e );\n                          }\n            );\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_replywcmt(context, u, w, action, wcmt=None):
    context.caller_stack._push_frame()
    try:
        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def textarea(**kwargs):
            return render_textarea(context, **kwargs)

        elements = _mako_get_namespace(context, 'elements')

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id=\'replywcmt\' action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='wiki_id', value=str(w.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='commentby', value=u.username)))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='version_id', value=str(w.latest_version))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='replytocomment_id', value=wcmt and str(wcmt.id) or '')))
        __M_writer('\n    <div class="w100 form">\n        <div class="w80">\n            ')
        __M_writer(escape(elements.captiontextarea('Use wiki markup to compose wiki comment.')))
        __M_writer('\n            ')
        __M_writer(escape(textarea(name='text', id='rpwcmt_text')))
        __M_writer('\n        </div>\n        <div>')
        __M_writer(escape(input_submit(value='Reply')))
        __M_writer('</div>\n    </div>\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_replytcmt(context, u, p, t, action, tcmt=None):
    context.caller_stack._push_frame()
    try:

        def textarea(**kwargs):
            return render_textarea(context, **kwargs)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id=\'replytcmt\' action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='ticket_id', value=str(t.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='commentby', value=u.username)))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='replytocomment_id', value=tcmt and str(tcmt.id) or '')))
        __M_writer('\n    <div class="w100 form">\n        <div class="w80">\n            ')
        __M_writer(escape(elements.captiontextarea('Use wiki markup to compose ticket comment.')))
        __M_writer('\n            ')
        __M_writer(escape(textarea(name='text', id='rptcmt_text')))
        __M_writer('\n        </div>\n        <div>')
        __M_writer(escape(input_submit(value='Reply')))
        __M_writer('</div>\n    </div>\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_resetpass(context, action):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)

        def input_password(**kwargs):
            return render_input_password(context, **kwargs)

        def input_reset(**kwargs):
            return render_input_reset(context, **kwargs)

        def fieldhelp(help='', fhstyle=''):
            return render_fieldhelp(context, help, fhstyle)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        pw_help = 'Should be a minimum of 4 character password.'
        __M_writer('\n\n    <form id="resetpass" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 15em;">Enter new password :</div>\n            <div class="fpass" required="true" regExp="')
        __M_writer(escape(h.RE_PASSWD))
        __M_writer('">\n                ')
        __M_writer(escape(input_password(name='password', id='password')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(pw_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 15em;">Confirm password :</div>\n            <div class="fpass" required="true">\n                ')
        __M_writer(escape(input_password(name='confpass', id='confpass')))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(pw_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 15em;"></div>\n            <div class="fsubmit">\n                ')
        __M_writer(escape(input_submit(value='Submit')))
        __M_writer('\n                ')
        __M_writer(escape(input_reset(value='Reset')))
        __M_writer('\n            </div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        function initform_resetpass() {\n            function resetpass_onsubmit( e ) {\n                var password = dijit.byId( \'password\' ).value;\n                var confpass = dijit.byId( \'confpass\' ).value;\n                var msg  = null;\n                if ( password == \'\' ) {\n                    msg = "Enter password";\n                } else if ( password != confpass ) {\n                    msg = "Re-type the exact password";\n                }\n                if( msg ) {\n                    dojo.publish( \'flash\', [ \'error\', msg, 2000 ] );\n                    dijit.byId( \'password\' ).value = \'\';\n                    dijit.byId( \'confpass\' ).value = \'\';\n                    dojo.stopEvent( e );\n                }\n            }\n            new zeta.Form({ onsubmit : resetpass_onsubmit, formid : \'resetpass\' });\n        } \n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_changetckst(context, u, p, t, statusname, due_date, action, tck_statusnames):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def select(**kwargs):
            return render_select(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        neutral_style = 'float : none; text-align : center; margin : 0px;'
        __M_writer('\n    <form id="createtstat" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='ticket_id', value=str(t.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='owner', value=str(u.id))))
        __M_writer('\n    <div style="display : table;">\n    <div style="display : table-row;">\n        <div class="p5" style="display : table-cell;">\n            <div class="dispinln">status :</div>\n        </div>\n        <div class="p5" style="display : table-cell;">\n            <div class="dispinln">\n                ')
        __M_writer(escape(select(name='tck_statusname', id='tck_statusname', options=tck_statusnames, opt_selected=statusname)))
        __M_writer('\n            </div>\n        </div>\n        <div class="p5" style="display : table-cell;">\n            <div class="dispinln" style="width : 12em;">due date :</div>\n        </div>\n        <div class="p5" style="display : table-cell;">\n            <div class="fdtbox dispinln" style="')
        __M_writer(escape(neutral_style))
        __M_writer('">\n                ')
        __M_writer(escape(input_text(name='due_date', value=due_date, id='tsduedate')))
        __M_writer('\n            </div>\n        </div>\n        <div class="p5" style="display : table-cell;">\n            <div class="dispinln">')
        __M_writer(escape(input_submit(value='Change')))
        __M_writer('</div>\n        </div>\n    </div>\n    </div>\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_input_image(context, **kwargs):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n    ')
        restrict_kwargs(kwargs, inputimage_attrs)
        attrs = make_attrs(kwargs)
        __M_writer('\n    <input type="image" ')
        __M_writer(attrs)
        __M_writer('></input>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_add_userrelations(context, u, reltypes, action):
    context.caller_stack._push_frame()
    try:
        elements = _mako_get_namespace(context, 'elements')

        def multiselect(**kwargs):
            return render_multiselect(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def select(**kwargs):
            return render_select(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id=\'adduserrels\' action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='userfrom', value=u.username)))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 7em;">\n                ')
        __M_writer(escape(elements.iconize('Relation :', 'relation')))
        __M_writer('</div>\n            <div class="fselect"  style="width : 20em;" required="true">\n                ')
        __M_writer(escape(select(name='userrel_type', id='userrel_type', options=reltypes, style='width : 10em')))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 7em;">\n                ')
        __M_writer(escape(elements.iconize('Users :', 'users')))
        __M_writer('</div>\n            <div class="fselect" style="width : 20em;" required="true">\n                ')
        __M_writer(escape(multiselect(name='userto', id='userto', options=[], size='4', style='width : 10em')))
        __M_writer('</div>\n            <div class="fsubmit ml10">')
        __M_writer(escape(input_submit(value='Add')))
        __M_writer('</div>\n        </div>\n    </div>\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_select_revwaction(context, actionnames):
    context.caller_stack._push_frame()
    try:

        def select(**kwargs):
            return render_select(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        actionnames = [
         [
          '', '--Select-Action--']] + actionnames
        __M_writer('\n    ')
        __M_writer(escape(select(name='reviewaction', options=actionnames)))
        __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_accountinfo(context, u, action):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)

        def fieldhelp(help='', fhstyle=''):
            return render_fieldhelp(context, help, fhstyle)

        def input_reset(**kwargs):
            return render_input_reset(context, **kwargs)

        str = context.get('str', UNDEFINED)
        x = context.get('x', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def input_text(**kwargs):
            return render_input_text(context, **kwargs)

        def select(**kwargs):
            return render_select(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    ')
        uinfo = u.userinfo
        fliparg = lambda x: x and x or ''
        em_help = 'Your communication email id.'
        up_help = 'Comma separated list of user panes'
        __M_writer('\n\n    <form id="accountinfo" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='username', id='username', value=u.username)))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 10em;">Email-id :</div>\n            <div class="ftbox" required="true" regExp="')
        __M_writer(escape(h.RE_EMAIL))
        __M_writer('">\n                ')
        __M_writer(escape(input_text(name='emailid', id='emailid', value=u.emailid)))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(em_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10em;">Timezone :</div>\n            <div class="fselect">\n                ')
        __M_writer(escape(select(name='timezone', id='timezone', options=h.all_timezones, opt_selected=u.timezone)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10em;">First Name :</div>\n            <div class="ftbox">\n                ')
        __M_writer(escape(input_text(name='firstname', id='firstname', value=fliparg(uinfo.firstname))))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10em;">Middle Name :</div>\n            <div class="ftbox">\n                ')
        __M_writer(escape(input_text(name='middlename', id='middlename', value=fliparg(uinfo.middlename))))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10em;">Last Name :</div>\n            <div class="ftbox">\n                ')
        __M_writer(escape(input_text(name='lastname', id='lastname', value=fliparg(uinfo.lastname))))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10em;">Address line 1 :</div>\n            <div class="ftbox">\n                ')
        __M_writer(escape(input_text(name='addressline1', id='addressline1', value=fliparg(uinfo.addressline1))))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10em;">Address line 2 :</div>\n            <div class="ftbox">\n                ')
        __M_writer(escape(input_text(name='addressline2', id='addressline2', value=fliparg(uinfo.addressline2))))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10em;">City :</div>\n            <div class="ftbox">\n                ')
        __M_writer(escape(input_text(name='city', id='city', value=fliparg(uinfo.city))))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10em;">Pincode :</div>\n            <div class="ftbox">\n                ')
        __M_writer(escape(input_text(name='pincode', id='pincode', value=fliparg(uinfo.pincode))))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10em;">State :</div>\n            <div class="ftbox">\n                ')
        __M_writer(escape(input_text(name='state', id='state', value=fliparg(uinfo.state))))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10em;">Country :</div>\n            <div class="ftbox">\n                ')
        __M_writer(escape(input_text(name='country', id='country', value=fliparg(uinfo.country))))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10em;">Userpanes :</div>\n            <div class="ftbox">\n                ')
        __M_writer(escape(input_text(name='userpanes', id='myuserpanes', value=fliparg(uinfo.userpanes))))
        __M_writer('\n                <br></br>\n                ')
        __M_writer(escape(fieldhelp(up_help)))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 10em;"></div>\n            <div class="fsubmit">\n                ')
        __M_writer(escape(input_submit(value='Submit')))
        __M_writer('\n                ')
        __M_writer(escape(input_reset(value='Reset')))
        __M_writer('\n            </div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        function initform_accountinfo() {\n            new zeta.Form({ normalsub: true, formid : \'accountinfo\' });\n        } \n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_processrcmt(context, u, p, r, action):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form id=\'processrcmt\' action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='review_id', value=str(r.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='review_comment_id', value='')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='approve', value='empty')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='reviewnature', value='empty')))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='reviewaction', value='empty')))
        __M_writer('\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_input_reset(context, **kwargs):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n    ')
        restrict_kwargs(kwargs, inputbutton_attrs)
        attrs = make_attrs(kwargs)
        __M_writer('\n    <input type="reset" ')
        __M_writer(attrs)
        __M_writer('></input>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_deletevcs(context, u, p, action, v=None):
    context.caller_stack._push_frame()
    try:

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        t = context.get('t', UNDEFINED)
        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <form id="deletevcs" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='project_id', value=str(p.id))))
        __M_writer('\n    ')
        __M_writer(escape(input_hidden(name='vcs_id', value=t and str(t.id) or '')))
        __M_writer('\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_form_add_userpermissions(context, u, usernames, action, defuser, x_pgroups):
    context.caller_stack._push_frame()
    try:
        elements = _mako_get_namespace(context, 'elements')

        def multiselect(**kwargs):
            return render_multiselect(context, **kwargs)

        str = context.get('str', UNDEFINED)

        def input_hidden(**kwargs):
            return render_input_hidden(context, **kwargs)

        def select(**kwargs):
            return render_select(context, **kwargs)

        def input_submit(**kwargs):
            return render_input_submit(context, **kwargs)

        __M_writer = context.writer()
        __M_writer('\n    <form id="adduserperms" action="')
        __M_writer(escape(action))
        __M_writer('" method="post">\n    ')
        __M_writer(escape(input_hidden(name='user_id', value=str(u.id))))
        __M_writer('\n    <div class="w100 form">\n        <div class="field">\n            <div class="label" style="width : 7em;">\n                ')
        __M_writer(escape(elements.iconize('User :', 'user')))
        __M_writer('</div>\n            <div class="fselect vtop"  required="true">\n                ')
        __M_writer(escape(select(name='username', id='addtouser', options=usernames, opt_selected=defuser, style='width : 12em')))
        __M_writer('\n            </div>\n        </div>\n        <div class="field">\n            <div class="label" style="width : 7em;">Permissions :</div>\n            <div class="fselect vtop"  required="true">\n                ')
        __M_writer(escape(multiselect(name='perm_group', id='add_perm_group', options=x_pgroups, size='7', style='width : 15em')))
        __M_writer('</div>\n            <div class="fsubmit" style="margin-left : 50px">')
        __M_writer(escape(input_submit(value='Add')))
        __M_writer('</div>\n        </div>\n    </div>\n    </form>\n\n    <script type="text/javascript">\n        /* Initialise adduserperms form */\n        function initform_adduserperms( e ) {\n            seluser_addpg  = dojo.query( \'form#adduserperms select#addtouser\' )[0];\n            selpg_touser   = dojo.query( \'form#adduserperms select#add_perm_group\' )[0];\n            new ZSelect( seluser_addpg, null, function( e ) { refresh_userperms() } );\n            new ZSelect( selpg_touser, \'adduserpg\', null );\n\n            function adduserperms_onsubmit( e ) {\n                submitform( form_adduserperms, e )\n                dojo.publish( \'flash\', [ \'message\', "Refreshing ..." ] );\n                userperms.store.close();\n                userperms.fetch({\n                    onComplete : userperms_oncomplete,\n                    sort       : [{ attribute : \'username\' }]\n                });\n                dojo.stopEvent( e );\n            }\n            new zeta.Form({ onsubmit : adduserperms_onsubmit, formid : \'adduserperms\' });\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()