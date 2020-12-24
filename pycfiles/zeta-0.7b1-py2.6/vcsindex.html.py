# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/projects/vcsindex.html.py
# Compiled at: 2010-07-12 03:41:02
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278920462.393942
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/projects/vcsindex.html'
_template_uri = '/derived/projects/vcsindex.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['hd_links', 'hd_script', 'bd_body', 'hd_styles', 'bd_script', 'vcslist']
page_tooltips = [
 [
  'Help',
  'Integrate one or more repositories with projects by providing its\n<em>type</em> (like svn ...) and <em>root-url</em>. Make sure that\n<em>root-url</em> points to the same machine, or to a machine on the local network.\n<br/>\nRepositories integrated with this project are listed in grid-style. Edit them\ninline.\n'],
 [
  'Browsing',
  '\nBrowsing the repository is provided in explorer style. By default the latest\nversion of the repository is shown in the explorer widget. To explore a different\nrevision use <b>< revno</b> and <b>revno ></b> links.\n'],
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
        __M_writer('\n    <link href="/zdojo/zdojoGrid.css" rel="stylesheet" type="text/css"></link>\n    <link href="/zdojo/zdojowikiGrid.css" rel="stylesheet" type="text/css"></link>\n')
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
        __M_writer('\n\n    <script type="text/javascript">\n    /********** Setup VCS Grid **************/\n    ')
        vcseditable = c.vcseditable and 'true' or 'false'
        editcolor = c.vcseditable and 'color : black;' or 'color : grey;'
        __M_writer('\n    vcs_typenames = ')
        __M_writer(h.json.dumps(c.vcs_typenames))
        __M_writer('\n\n    // Grid Columns\n    colnames    = { Id      : null,\n                    Name    : null,\n                    Type    : null,\n                    Rooturl : null,\n                  };\n    // Format ids.\n    function get_vcsids( rowindex, item ) {\n        if( ! grid_vindex ) { return; }\n        if( ! item ) { return; }\n        return [ vcslist.store.getValue( item, \'href\' ),\n                 vcslist.store.getValue( item, \'id\' ) ]\n    }\n    function format_vcsids( item, rowindex ) {\n        if( ! grid_vindex ) { return; }\n        if( ! item ) { return; }\n        return create_anchor( item[0], item[1] );\n    }\n\n    // GRID Title customization menu\n    function refresh_csmenu() {\n        // Refresh column labels\n        for( name in colnames ) {\n            var mitem = colnames[name];\n            var check = \'<input type="checkbox" checked="checked"></input> &ensp;\';\n            mitem.colhide ?\n                mitem.attr( \'label\', \'&ensp;&ensp;&ensp;\' + mitem.orglabel )\n                : mitem.attr( \'label\', check + mitem.orglabel )\n        }\n    }\n    function on_selectcolumns( name ) {\n        // Toggle the hidden attribute and refresh\n        var visibile = colnames[name].colhide;\n        colnames[name].colhide = colnames[name].colhide ? false : true;\n        refresh_csmenu();\n        // Refresh column hidden status in the layout\n        var cells = grid_vindex.layout.cells;\n        for( i=0 ; i < cells.length; i++ ) {\n            if ( name == cells[i].name ) {\n                grid_vindex.layout.setColumnVisibility( i, visibile );\n            }\n        }\n    }\n\n    function setup_csmenu() {\n        // Create Menu on the last column\n        var csmenu   = new dijit.Menu();\n        var mi_title = new dijit.MenuItem({ \n                            label : \'Columns\',\n                            iconClass:"dispnone",\n                            class: "calign"\n                       });\n\n        dojo.style( mi_title.domNode, { fontWeight: \'bold\', color: \'black\' });\n        dojo.style( csmenu.domNode, { fontSize: \'small\', color: \'blue\' });\n\n        csmenu.addChild( mi_title );\n        csmenu.addChild( new dijit.MenuSeparator() );\n\n        // Create menu items\n        for( name in colnames ) {\n            colnames[name] = new dijit.MenuItem({\n                                    label   : name,\n                                    iconClass: "dispnone",\n                                    onClick : dojo.hitch( null,\n                                                          on_selectcolumns,\n                                                          name\n                                                        )\n                             })\n            colnames[name].colhide  = false;\n            colnames[name].orglabel = name;\n            csmenu.addChild( colnames[name] );\n        }\n        dojo.setObject( \'csmenu\', csmenu )\n    }\n\n    /* Data store Write handlers */\n    function vl_onset( item, attr_name, oldval, newval ) {\n        if( item ) {\n            var id          = vcslist.store.getValue( item, \'id\' );\n            var name        = vcslist.store.getValue( item, \'name\' );\n            var rooturl     = vcslist.store.getValue( item, \'rooturl\' );\n            var vcs_typename= vcslist.store.getValue( item, \'vcs_typename\' );\n\n            dojo.query( \'input[name=vcs_id]\', form_configvcs \n                      )[0].value = id;\n            dojo.query( \'input[name=name]\', form_configvcs \n                      )[0].value = name;\n            dojo.query( \'input[name=rooturl]\', form_configvcs \n                      )[0].value = rooturl;\n            dojo.query( \'input[name=vcs_typename]\', form_configvcs \n                      )[0].value = vcs_typename;\n            submitform( form_configvcs );\n        }\n    }\n\n    function setup_vcslist( div_prjvcslist ) {\n        make_ifws_vcslist( \'')
        __M_writer(h.url_vcslist)
        __M_writer('\', vl_onset );\n\n        var glayout_vindex = [\n                { // View is an array of cells\n                    cells: [\n                      { name : \'Id\',\n                        field: \'id\',\n                        width: \'4em\',\n                        hidden: false,\n                        get  : get_vcsids,\n                        formatter : format_vcsids,\n                        styles : "text-align : left;"\n                      },\n                      { name : \'Name\',\n                        field: \'name\',\n                        width: \'auto\',\n                        hidden: false,\n                        styles: \'')
        __M_writer(escape(editcolor))
        __M_writer("',\n                        editable: ")
        __M_writer(escape(vcseditable))
        __M_writer("\n                      },\n                      { name : 'Type',\n                        field: 'vcs_typename',\n                        width: '7em',\n                        hidden: false,\n                        editable: ")
        __M_writer(escape(vcseditable))
        __M_writer(",\n                        styles: '")
        __M_writer(escape(editcolor))
        __M_writer("',\n                        type: dojox.grid.cells.Select,\n                        options : ")
        __M_writer(h.json.dumps(c.vcs_typenames))
        __M_writer("\n                      },\n                      { name : 'Root-url',\n                        field: 'rooturl',\n                        width: 'auto',\n                        hidden: false,\n                        styles: '")
        __M_writer(escape(editcolor))
        __M_writer("',\n                        editable: ")
        __M_writer(escape(vcseditable))
        __M_writer(',\n                      },\n                    ]\n                },\n            ];\n\n        /* Grid with Layout */\n        dojo.setObject(\n            \'grid_vindex\',\n            new dojox.grid.DataGrid({\n                            store: vcslist.store,\n                            clientSort: true,\n                            columnReordering: true,\n                            structure: glayout_vindex,\n                            headerMenu: csmenu\n             }, document.createElement( \'div\' ))\n        );\n\n        /* Append the new grid */\n        div_prjvcslist.appendChild( grid_vindex.domNode );\n\n        /* Call startup, in order to render the grid: */\n        grid_vindex.startup();\n        refresh_csmenu();\n\n        /* Grid editing */\n        new zeta.Form({ normalsub: true, formid: \'configvcs\' });\n\n        /* grid resizing */\n        grid_vindex.connect( window, \'onresize\',\n                             function( e ) { this.resize() } );\n        dojo.subscribe( \'resize_upane\', grid_vindex,\n                        function( collapsed ) { this.resize() } );\n    }\n\n    function setup_vcs() {\n        var div_prjvcslist = dojo.byId("prjvcslist");\n        /* Setup the vcs goto list */\n        select_goto( dojo.query( \'#selectvcs\' )[0] );\n        // VCS list\n        setup_csmenu();\n        setup_vcslist( div_prjvcslist );\n    }\n\n    </script>\n')
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

        def vcslist():
            return render_vcslist(context)

        __M_writer = context.writer()
        __M_writer('\n    ')
        title = 'Vcs list'
        sel_vcs = capture(forms.form_selectvcs, c.authuser, c.vcslist, c.vcs and c.vcs.name or '')
        if c.vcseditable:
            newvcs = '<span class="ml10 fwnormal fntsmall">' + '<a href="%s" title="Integrate a new repository">                      Integrate</a></span>' % h.url_vcscreate
        else:
            newvcs = ''
        tline = capture(elements.iconlink, h.url_vcstimeline, 'timeline', title='Timeline of vcs-integration')
        __M_writer('\n    ')
        __M_writer(escape(elements.mainnav()))
        __M_writer('\n    ')
        __M_writer(escape(elements.contextnav([title, sel_vcs, newvcs], rspans=[
         tline], tooltips=page_tooltips)))
        __M_writer('\n    <div id="bdy" class="w100">\n')
        if c.authusername == 'anonymous' or not c.userpanes:
            __M_writer('        <div class="fullpanel1">\n')
        else:
            __M_writer('        <div class="panel1">\n')
        __M_writer('            <div>\n                ')
        __M_writer(escape(vcslist()))
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
        __M_writer('\n\n    <script type="text/javascript">\n        dojo.addOnLoad( setup_vcs );\n        dojo.addOnLoad( setup_userpanes );\n        dojo.addOnLoad( adjust_upheight );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_vcslist(context):
    context.caller_stack._push_frame()
    try:
        forms = _mako_get_namespace(context, 'forms')
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <div id="prjvcslist" class="mt10 ml10 mr10 br5"\n         style="height: 600px; border: 4px solid #B3CFB3;">\n    </div>\n    <div class="dispnone">\n        ')
        __M_writer(escape(forms.form_configvcs(c.authuser, c.project, h.suburl_configvcs)))
        __M_writer('\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()