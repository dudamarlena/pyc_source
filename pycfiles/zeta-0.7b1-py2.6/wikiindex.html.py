# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/projects/wikiindex.html.py
# Compiled at: 2010-07-10 01:32:39
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278739959.881973
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/projects/wikiindex.html'
_template_uri = '/derived/projects/wikiindex.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['wikiindex', 'hd_script', 'bd_body', 'hd_links', 'bd_script']
page_tooltips = [
 [
  'Help',
  "List of all wiki pages associated with the project, in a grid-style,\nallowing user to <em>edit attributes in-line</em>. To know how,\njust double click on any of the grid cell (that are not in gray)\nand edit it. It is also possible to navigate from one cell to another using\n'up', 'down', 'left', 'right' arrows, to edit just press enter and edit. To save\nedited content, just press 'enter' or click outside the cell.\n<br/>\nThe header row in the grid can be used for two purpose. One, to <em>sort the list\nby desired column</em> (by left clicking), two, to\n<em>add/remove columns</em> (by right clicking). \n"],
 [
  'Wikipage',
  'Each wiki page is rendered with html translated wiki document and gives simple\nstatistical details for the page. Download a wiki page as text, pdf, html or\nps file.\n'],
 [
  'Timeline',
  'Timeline of updates done to all wiki pages in this project']]

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
        __M_writer('\n\n\n')
        __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_wikiindex(context):
    context.caller_stack._push_frame()
    try:
        forms = _mako_get_namespace(context, 'forms')
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <div id="prjwikilist" class="mt10 ml10 mr10 br5"\n         style="height: 600px; border: 4px solid #B3CFB3;">\n    </div>\n    <div class="dispnone">\n        ')
        __M_writer(escape(forms.form_configwiki(c.authuser, h.suburl_configwiki)))
        __M_writer('\n    </div>\n')
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
        __M_writer('\n\n    <script type="text/javascript">\n    /********** Setup Wiki Grid **************/\n    ')
        wiki_id = c.wiki and c.wiki.id or ''
        wikieditable = c.wikieditable and 'true' or 'false'
        editcolor = c.wikieditable and 'color : black;' or 'color : grey;'
        __M_writer('\n    // Grid columns\n    colnames    = { WikiPage : null,\n                    Type     : null,\n                    Summary  : null,\n                    LastModified : null,\n                    Author   : null,\n                    UpVotes  : null,\n                    DownVotes: null,\n                    Version  : null\n                  };\n    // Grid callbacks\n    function get_wikipagename( rowindex, item ) {\n        if( (! grid_windex) || (! item) ) { return; }\n        return [ wikilist.store.getValue( item, \'wikiurl\' ),\n                 wikilist.store.getValue( item, \'pagename\' ) ]\n    }\n    function format_wikipagename( item, rowindex ) {\n        if( (! grid_windex) || (! item) ) { return; }\n        return create_anchor( item[0], item[1] );\n    }\n    // Grid Data store Write handlers\n    function wl_onset( item, attr_name, oldval, newval ) {\n        if( item ) {\n            var id            = wikilist.store.getValue( item, \'id\' );\n            var wiki_typename = wikilist.store.getValue( item, \'wiki_typename\' );\n            var summary       = wikilist.store.getValue( item, \'summary\' );\n            dojo.query( \'input[name=wiki_id]\', form_configwiki\n                      )[0].value = item.id;\n            dojo.query( \'input[name=wiki_typename]\', form_configwiki\n                      )[0].value = item.wiki_typename;\n            dojo.query( \'input[name=summary]\', form_configwiki\n                      )[0].value = item.summary;\n            submitform( form_configwiki );\n        }\n    }\n\n    // GRID Title customization menu\n    function refresh_csmenu() {\n        // Refresh column labels\n        for( name in colnames ) {\n            var mitem = colnames[name];\n            var check = \'<input type="checkbox" checked="checked"></input> &ensp;\';\n            mitem.colhide ?\n                mitem.attr( \'label\', \'&ensp;&ensp;&ensp;&ensp;\' + mitem.orglabel )\n                : mitem.attr( \'label\', check + mitem.orglabel )\n        }\n    }\n    function on_selectcolumns( name ) {\n        // Toggle the hidden attribute and refresh\n        var visibile = colnames[name].colhide;\n        colnames[name].colhide = colnames[name].colhide ? false : true;\n        refresh_csmenu();\n        // Refresh column hidden status in the layout\n        var cells = grid_windex.layout.cells;\n        for( i=0 ; i < cells.length; i++ ) {\n            if ( name == cells[i].name ) {\n                grid_windex.layout.setColumnVisibility( i, visibile );\n            }\n        }\n    }\n    function setup_csmenu() {\n        // Create Menu on the last column\n        var csmenu   = new dijit.Menu();\n        var mi_title = new dijit.MenuItem({\n                            label : \'Columns\',\n                            iconClass:"dispnone",\n                            class : "calign"\n                       });\n\n        dojo.style( mi_title.domNode, { fontWeight: \'bold\', color: \'black\' });\n        dojo.style( csmenu.domNode, { fontSize: \'small\', color: \'blue\' });\n\n        csmenu.addChild( mi_title );\n        csmenu.addChild( new dijit.MenuSeparator() );\n\n        // Create menu items\n        for( name in colnames ) {\n            colnames[name] = new dijit.MenuItem({\n                                    label   : name,\n                                    iconClass: "dispnone",\n                                    onClick : dojo.hitch( null,\n                                                          on_selectcolumns,\n                                                          name\n                                                        )\n                             })\n            colnames[name].colhide  = false;\n            colnames[name].orglabel = name;\n            csmenu.addChild( colnames[name] );\n        }\n        colnames.Version.colhide = true;\n        dojo.setObject( \'csmenu\', csmenu )\n    }\n\n    function setup_wikilist() {\n        var div_prjwikilist = dojo.byId("prjwikilist");\n\n        /* Setup the wiki goto list */\n        select_goto( dojo.query( \'#selectwikipage\' )[0] );\n\n        // Grid Layout\n        var glayout_windex = [\n                { // View is an array of cells\n                    cells: [\n                      { name : \'WikiPage\',\n                        field: \'wikiurl\',\n                        width: \'15em\',\n                        hidden: false,\n                        get  : get_wikipagename,\n                        formatter : format_wikipagename,\n                        styles : "text-align : left;"\n                      },\n                      { name : \'Type\',\n                        field: \'wiki_typename\',\n                        width: \'7em\',\n                        hidden: false,\n                        editable: ')
        __M_writer(escape(wikieditable))
        __M_writer(",\n                        styles: '")
        __M_writer(escape(editcolor))
        __M_writer("',\n                        type: dojox.grid.cells.Select,\n                        options : ")
        __M_writer(h.json.dumps(c.wikitypenames))
        __M_writer("\n                      },\n                      { name : 'Summary',\n                        field: 'summary',\n                        width: 'auto',\n                        hidden: false,\n                        styles: '")
        __M_writer(escape(editcolor))
        __M_writer("',\n                        editable: ")
        __M_writer(escape(wikieditable))
        __M_writer("\n                      },\n                      { name : 'LastModified',\n                        field: 'last_modified',\n                        width: '13em',\n                        hidden: false,\n                        styles: 'color : gray;'\n                      },\n                      { name : 'Author',\n                        field: 'author',\n                        width: '8em',\n                        hidden: false,\n                        styles: 'color : gray;'\n                      },\n                      { name : 'UpVotes',\n                        field: 'upvotes',\n                        width: '6em',\n                        hidden: false,\n                        styles: 'text-align: center; color : green;'\n                      },\n                      { name : 'DownVotes',\n                        field: 'downvotes',\n                        width: '7em',\n                        hidden: false,\n                        styles: 'text-align: center; color : red;'\n                      },\n                      { name : 'Version',\n                        field: 'latest_version',\n                        width: '6em',\n                        hidden : true,\n                        styles: 'color : gray;'\n                      },\n                    ]\n                },\n            ];\n\n        setup_csmenu();\n\n        make_ifws_wikilist( '")
        __M_writer(h.url_wikilist)
        __M_writer("', wl_onset );\n\n        /* Grid with Layout */\n        dojo.setObject(\n            'grid_windex',\n            new dojox.grid.DataGrid({\n                            store: wikilist.store,\n                            clientSort: true,\n                            columnReordering: true,\n                            structure: glayout_windex,\n                            headerMenu: csmenu\n             }, document.createElement( 'div' ))\n        );\n\n        /* Append the new grid */\n        div_prjwikilist.appendChild(grid_windex.domNode);\n\n        /* Call startup, in order to render the grid: */\n        grid_windex.startup();\n        refresh_csmenu();\n\n        /* grid resizing */\n        grid_windex.connect( window, 'onresize',\n                             function( e ) { this.resize() } );\n        dojo.subscribe( 'resize_upane', grid_windex,\n                        function( collapsed ) { this.resize() } );\n    }\n\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bd_body(context):
    context.caller_stack._push_frame()
    try:
        capture = context.get('capture', UNDEFINED)
        c = context.get('c', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')

        def wikiindex():
            return render_wikiindex(context)

        h = context.get('h', UNDEFINED)
        forms = _mako_get_namespace(context, 'forms')
        __M_writer = context.writer()
        __M_writer('\n    ')
        sel_wp = capture(forms.form_selectwikipage, c.authuser, c.wikipagenames, c.wikipagename or '')
        searchbox = capture(forms.form_searchbox, c.authuser, 'searchwiki', 'Search-wiki', h.suburl_search, c.searchfaces)
        attachs = '<span class="ml10 fwnormal fntsmall">' + '<a href="%s" title="Attachments to wiki pages">                    Attachments</a></span>' % h.url_wikiattachs
        tindex = '<span class="ml10 fwnormal fntsmall">' + '<a href="%s" title="Index of wiki pages">                    Titleindex</a></span>' % h.url_wikititleindex
        charts = capture(elements.iconlink, h.url_wikicharts, 'barchart', title='Wiki charts')
        tline = capture(elements.iconlink, h.url_wikitimeline, 'timeline', title='Timeline for all wiki pages')
        __M_writer('\n    ')
        __M_writer(escape(elements.mainnav()))
        __M_writer('\n    ')
        __M_writer(escape(elements.contextnav([searchbox, sel_wp, tindex, attachs], rspans=[
         charts, tline], tooltips=page_tooltips)))
        __M_writer('\n    <div id="bdy" class="w100">\n')
        if c.authusername == 'anonymous' or not c.userpanes:
            __M_writer('        <div class="fullpanel1">\n')
        else:
            __M_writer('        <div class="panel1">\n')
        __M_writer('            <div>\n                ')
        __M_writer(escape(wikiindex()))
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
        __M_writer('\n    <link href="/zdojo/zdojoGrid.css" rel="stylesheet" type="text/css"></link>\n    <link href="/zdojo/zdojowikiGrid.css" rel="stylesheet" type="text/css"></link>\n')
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
        __M_writer('\n\n    <script type="text/javascript">\n        dojo.addOnLoad( setup_wikilist );\n        dojo.addOnLoad( initform_configwiki );\n\n        dojo.addOnLoad( setup_userpanes );\n        dojo.addOnLoad( adjust_upheight );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()