# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/projects/vcsbrowse.html.py
# Compiled at: 2010-07-12 03:53:24
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278921204.230097
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/projects/vcsbrowse.html'
_template_uri = '/derived/projects/vcsbrowse.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['browse', 'hd_links', 'hd_script', 'bd_body', 'hd_styles', 'bd_script']
page_tooltips = [
 [
  'Help',
  '\nBrowsing the repository is provided in explorer style. By default the latest\nversion of the repository is shown in the explorer widget. To explore a different\nrevision use <b>< revno</b> and <b>revno ></b> links.\n'],
 [
  'Repository-list',
  'Integrate one or more repositories with projects by providing its\n<em>type</em> (like svn ...) and <em>root-url</em>. Make sure that\n<em>root-url</em> points to the same machine, or to a machine on the local network.\n<br/>\nRepositories integrated with this project are listed in grid-style. Edit them\ninline.\n'],
 [
  'Files',
  '\nFiles in repository are viewable with syntax highlighting, annotation and\nchangesets.\n'],
 [
  'Revisions',
  'Details about each repository revision listed in reverse chronological order.\n']]

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
        __M_writer('\n\n\n')
        __M_writer('\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_browse(context):
    context.caller_stack._push_frame()
    try:
        forms = _mako_get_namespace(context, 'forms')
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <div id="prjvcsbrowse" class="mt10 ml10 mr10" style="height: 500px">\n    </div>\n    ')
        __M_writer(escape(forms.form_createmount_e(c.authuser, c.vcs, c.contents, h.suburl_createmount_e)))
        __M_writer('\n    ')
        __M_writer(escape(forms.form_deletemount_e(c.authuser, h.suburl_deletemount_e)))
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
        parent = context.get('parent', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        __M_writer(escape(parent.hd_script()))
        __M_writer('\n\n    <script type="text/javascript">\n    ')
        vcseditable = c.vcseditable and 'true' or 'false'
        __M_writer('\n    function setup_vcs() {\n        var div_prjvcsbrowse = dojo.byId("prjvcsbrowse");\n\n        /* Setup the vcs goto list */\n        select_goto( dojo.query( \'#selectvcs\' )[0] );\n\n        w = new zeta.VcsExplorer({\n                vcstype: \'')
        __M_writer(escape(c.vcs.type.vcs_typename.upper()))
        __M_writer("',\n                rootpath: '")
        __M_writer(escape(c.vcs.rooturl.rstrip('/')))
        __M_writer("',\n                revno_p: [ '")
        __M_writer(escape(c.revno_p))
        __M_writer("', '")
        __M_writer(escape(h.url_browseprev))
        __M_writer("' ],\n                revno: '")
        __M_writer(escape(c.revno))
        __M_writer("',\n                revno_n: [ '")
        __M_writer(escape(c.revno_n))
        __M_writer("', '")
        __M_writer(escape(h.url_browsenext))
        __M_writer("' ],\n                rootdir: '")
        __M_writer(escape(c.rootdir))
        __M_writer("',\n                listrootdir: '")
        __M_writer(escape(h.list_rootdir))
        __M_writer("',\n                mountpoints: ")
        __M_writer(h.json.dumps(c.mountdirs))
        __M_writer(",\n                n_mountform: dojo.byId( 'createmount_e' ),\n                n_unmountform: dojo.byId( 'deletemount_e' ),\n                n_mountpopup: dojo.byId( 'mountpopup' ),\n                editable: ")
        __M_writer(escape(vcseditable))
        __M_writer('\n            }, div_prjvcsbrowse );\n    }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bd_body(context):
    context.caller_stack._push_frame()
    try:
        capture = context.get('capture', UNDEFINED)
        c = context.get('c', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')

        def browse():
            return render_browse(context)

        h = context.get('h', UNDEFINED)
        forms = _mako_get_namespace(context, 'forms')
        __M_writer = context.writer()
        __M_writer('\n    ')
        title = '<a class="fntbold ml10">%s</a>' % c.vcs.name
        sel_vcs = capture(forms.form_selectvcs, c.authuser, c.vcslist, c.vcs and c.vcs.name or '')
        vcsbrowse = '<a class="ml10" title="Browse latest version"                      href="%s">Browser</a>' % h.url_vcsbrowse
        revlist = '<a class="ml10" title="List of repository revisions"                      href="%s">Revisions</a>' % h.url_revlist
        if c.vcseditable:
            newvcs = '<span class="ml10 fwnormal fntsmall">' + '<a href="%s"                          title="Integrate a new repository">Integrate</a></span>' % h.url_vcscreate
        else:
            newvcs = ''
        tline = capture(elements.iconlink, h.url_vcstimeline, 'timeline', title='Timeline of vcs-integration')
        __M_writer('\n    ')
        __M_writer(escape(elements.mainnav()))
        __M_writer('\n    ')
        __M_writer(escape(elements.contextnav([title, sel_vcs, vcsbrowse, revlist, newvcs], rspans=[
         tline], tooltips=page_tooltips)))
        __M_writer('\n    <div id="bdy" class="w100">\n')
        if c.authusername == 'anonymous' or not c.userpanes:
            __M_writer('        <div class="fullpanel1">\n')
        else:
            __M_writer('        <div class="panel1">\n')
        __M_writer('            <div>\n                ')
        __M_writer(escape(browse()))
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
        __M_writer('\n\n    <script type="text/javascript">\n        dojo.addOnLoad( initform_createmount_e );\n        dojo.addOnLoad( initform_deletemount_e );\n        dojo.addOnLoad( setup_vcs );\n\n        dojo.addOnLoad( setup_userpanes );\n        dojo.addOnLoad( adjust_upheight );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()