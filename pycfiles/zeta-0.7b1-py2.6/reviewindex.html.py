# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/projects/reviewindex.html.py
# Compiled at: 2010-07-12 02:04:05
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278914645.296834
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/projects/reviewindex.html'
_template_uri = '/derived/projects/reviewindex.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['bd_body', 'hd_script', 'revwlist', 'hd_links', 'bd_script']
page_tooltips = [
 [
  'Help',
  'Review - document, code and wiki pages. Every review created, has\n<em>author</em>, <em>moderator</em> and <em>participants</em>.\n<br/>\nSimilar to ticket list, review list uses a grid supporting\n<b>inline editing</b>.\n'],
 [
  'Author',
  '<em>Author</em> can add comments and also reponsible for taking actions\non all review comments.'],
 [
  'Moderator',
  '<em>Moderator</em> can add comments and is responsible\nfor approving actions taken by author on review comments. Once all the\ncomments are approve, moderator can close the review.'],
 [
  'Participant',
  '<em>Participants</em> can give review comments and reply to other comments.\n'],
 [
  'Review-set',
  'Collection of reviews. Especially useful to create review entries for every\nmodified / added file in repository changeset\n'],
 [
  'Attachments',
  'Add <b>summary</b> and <b>tags</b> to project attachments.'],
 [
  'Timeline',
  'Timeline of all updates done to Review(s).']]

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

        def revwlist():
            return render_revwlist(context)

        h = context.get('h', UNDEFINED)
        forms = _mako_get_namespace(context, 'forms')
        __M_writer = context.writer()
        __M_writer('\n    ')
        searchbox = capture(forms.form_searchbox, c.authuser, 'searchreview', 'Search-review', h.suburl_search, c.searchfaces)
        sel_revw = capture(forms.form_selectrevw, c.authuser, c.revwlist, c.review and c.review.resource_url or '')
        sel_rset = capture(forms.form_selectrset, c.authuser, c.rsetlist, c.reviewset and c.reviewset.name or '')
        if c.revweditable:
            newrevw = '<span class="ml10 fwnormal fntsmall">                         <a href="%s" title="Create a new review">                         Create</a></span>' % h.url_revwcreate
        else:
            newrevw = ''
        revwsets = '<span class="ml10 fwnormal fntsmall">                     <a href="%s" title="List of reviews sets">                     Reviewsets</a></span>' % h.url_reviewsets
        attachs = '<span class="ml10 fwnormal fntsmall">' + '<a href="%s" title="List of files attached to reviews">                    Attachments</a></span>' % h.url_revwattachs
        charts = capture(elements.iconlink, h.url_revwcharts, 'barchart', title='Review analytics')
        tline = capture(elements.iconlink, h.url_revwtimeline, 'timeline', title='Timeline of reviews')
        __M_writer('\n    ')
        __M_writer(escape(elements.mainnav()))
        __M_writer('\n    ')
        __M_writer(escape(elements.contextnav([searchbox, sel_revw, sel_rset, newrevw,
         revwsets, attachs], rspans=[
         charts, tline], tooltips=page_tooltips)))
        __M_writer('\n\n    <div id="bdy" class="w100">\n')
        if c.authusername == 'anonymous' or not c.userpanes:
            __M_writer('        <div class="fullpanel1">\n')
        else:
            __M_writer('        <div class="panel1">\n')
        __M_writer('            <div>\n                ')
        __M_writer(escape(revwlist()))
        __M_writer('\n            </div>\n        </div> \n')
        if c.authusername != 'anonymous' and c.userpanes:
            __M_writer('        <div class="panel2">')
            __M_writer(escape(elements.user_panes(c.userpanes)))
            __M_writer('</div>\n')
        __M_writer('    </div>\n')
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


def render_revwlist(context):
    context.caller_stack._push_frame()
    try:
        forms = _mako_get_namespace(context, 'forms')
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <div id="prjrevwlist" class="mt10 ml10 mr10 br5"\n         style="height: 600px; border: 4px solid #B3CFB3;">\n    </div>\n    <div class="dispnone">\n        ')
        __M_writer(escape(forms.form_configrev(c.authuser, c.project, h.suburl_configrev)))
        __M_writer('\n    </div>\n    <script type="text/javascript">\n    ')
        editcolor = c.revweditable and 'color : black;' or 'color : grey;'
        revweditable = c.revweditable and 'true' or 'false'
        __M_writer('\n    // Grid Columns\n    colnames    = { Id           : null,\n                    ReviewSet    : null,\n                    ResourceUrl  : null,\n                    Version      : null,\n                    Author       : null,\n                    Moderator    : null,\n                    Comments     : null,\n                    Olderby      : null\n                  };\n\n    // Format ids.\n    function get_revwids( rowindex, item ) {\n        if( ! grid_rindex ) { return; }\n        if( ! item ) { return; }\n        return [ revwlist.store.getValue( item, \'href\' ),\n                 revwlist.store.getValue( item, \'id\' ) ]\n    }\n    function format_revwids( item, rowindex ) {\n        if( ! grid_rindex ) { return; }\n        if( ! item ) { return; }\n        return create_anchor( item[0], item[1] );\n    }\n    // Format review set ids\n    function get_rsetids( rowindex, item ) {\n        if( ! grid_rindex ) { return; }\n        if( ! item ) { return; }\n        return [ revwlist.store.getValue( item, \'rshref\' ),\n                 revwlist.store.getValue( item, \'reviewset\' ) ]\n    }\n    function format_rsetids( item, rowindex ) {\n        if( ! grid_rindex ) { return; }\n        if( ! item ) { return; }\n        return create_anchor( item[0], item[1] );\n    }\n\n    // GRID Title customization menu\n    function refresh_csmenu() {\n        // Refresh column labels\n        for( name in colnames ) {\n            var mitem = colnames[name];\n            var check = \'<input type="checkbox" checked="checked"></input> &ensp;\';\n            mitem.colhide ?\n                mitem.attr( \'label\', \'&ensp;&ensp;&ensp;\' + mitem.orglabel )\n                : mitem.attr( \'label\', check + mitem.orglabel )\n        }\n    }\n    function on_selectcolumns( name ) {\n        // Toggle the hidden attribute and refresh\n        var visibile = colnames[name].colhide;\n        colnames[name].colhide = colnames[name].colhide ? false : true;\n        refresh_csmenu();\n        // Refresh column hidden status in the layout\n        var cells = grid_rindex.layout.cells;\n        for( i=0 ; i < cells.length; i++ ) {\n            if ( name == cells[i].name ) {\n                grid_rindex.layout.setColumnVisibility( i, visibile );\n            }\n        }\n    }\n    function setup_csmenu() {\n        // Create Menu on the last column\n        var csmenu   = new dijit.Menu();\n        var mi_title = new dijit.MenuItem({ \n                            label : \'Columns\',\n                            iconClass:"dispnone",\n                            class: "calign"\n                       });\n\n        dojo.style( mi_title.domNode, { fontWeight: \'bold\', color: \'black\' });\n        dojo.style( csmenu.domNode, { fontSize: \'small\', color: \'blue\' });\n\n        csmenu.addChild( mi_title );\n        csmenu.addChild( new dijit.MenuSeparator() );\n\n        // Create menu items\n        for( name in colnames ) {\n            colnames[name] = new dijit.MenuItem({\n                                    label   : name,\n                                    iconClass: "dispnone",\n                                    onClick : dojo.hitch( null,\n                                                          on_selectcolumns,\n                                                          name\n                                                        )\n                             })\n            colnames[name].colhide  = false;\n            colnames[name].orglabel = name;\n            csmenu.addChild( colnames[name] );\n        }\n        dojo.setObject( \'csmenu\', csmenu )\n    }\n\n    /* Data store Write handlers */\n    function revwl_onset( item, attr_name, oldval, newval ) {\n        if( item ) {\n            var id        = revwlist.store.getValue( item, \'id\' );\n            var rurl      = revwlist.store.getValue( item, \'resource_url\' );\n            var version   = revwlist.store.getValue( item, \'version\' );\n            var author    = revwlist.store.getValue( item, \'author\' );\n            var moderator = revwlist.store.getValue( item, \'moderator\' );\n\n            dojo.query( \'input[name=review_id]\', form_configrev\n                      )[0].value = id;\n            dojo.query( \'input[name=resource_url]\', form_configrev\n                      )[0].value = rurl;\n            dojo.query( \'input[name=version]\', form_configrev\n                      )[0].value = version;\n            dojo.query( \'input[name=author]\', form_configrev\n                      )[0].value = author;\n            dojo.query( \'input[name=moderator]\', form_configrev\n                      )[0].value = moderator;\n            submitform( form_configrev );\n        }\n    }\n    function setup_revwlist() {\n        var div_prjrevwlist = dojo.byId( \'prjrevwlist\' );\n        make_ifws_revwlist( \'')
        __M_writer(h.url_revwlist)
        __M_writer('\', revwl_onset );\n\n        var glayout_rindex = [\n                { // View is an array of cells\n                    cells: [\n                      { name : \'Id\',\n                        field: \'id\',\n                        width: \'4em\',\n                        hidden: false,\n                        get  : get_revwids,\n                        formatter : format_revwids,\n                        styles : "text-align : left;"\n                      },\n                      { name : \'ReviewSet\',\n                        field: \'reviewset\',\n                        width: \'8em\',\n                        hidden: false,\n                        get  : get_rsetids,\n                        formatter : format_rsetids,\n                      },\n                      { name : \'ResourceUrl\',\n                        field: \'resource_url\',\n                        width: \'auto\',\n                        hidden: false,\n                        styles: \'')
        __M_writer(escape(editcolor))
        __M_writer("',\n                        editable: ")
        __M_writer(escape(revweditable))
        __M_writer("\n                      },\n                      { name : 'Version',\n                        field: 'version',\n                        width: '4em',\n                        hidden: false,\n                        styles: '")
        __M_writer(escape(editcolor))
        __M_writer("',\n                        editable: ")
        __M_writer(escape(revweditable))
        __M_writer("\n                      },\n                      { name : 'Author',\n                        field: 'author',\n                        width: '9em',\n                        hidden: false,\n                        styles: '")
        __M_writer(escape(editcolor))
        __M_writer("',\n                        editable: ")
        __M_writer(escape(revweditable))
        __M_writer(',\n                        type: dojox.grid.cells.Select,\n                        options : ')
        __M_writer(h.json.dumps(c.projusers))
        __M_writer("\n                      },\n                      { name : 'Moderator',\n                        field: 'moderator',\n                        width: '9em',\n                        hidden: false,\n                        styles: '")
        __M_writer(escape(editcolor))
        __M_writer("',\n                        editable: ")
        __M_writer(escape(revweditable))
        __M_writer(',\n                        type: dojox.grid.cells.Select,\n                        options : ')
        __M_writer(h.json.dumps(c.projusers))
        __M_writer("\n                      },\n                      { name : 'Comments',\n                        field: 'comments',\n                        width: '6em',\n                        hidden: false,\n                        editable: false,\n                        styles: 'color : gray;'\n                      },\n                      { name : 'Olderby',\n                        field: 'olderby',\n                        width: '7em',\n                        hidden: false,\n                        editable: false,\n                        styles: 'color : gray;'\n                      }\n                    ]\n                },\n            ];\n\n        setup_csmenu();\n\n        /* Grid with Layout */\n        dojo.setObject( 'grid_rindex',\n                        new dojox.grid.DataGrid({\n                                        store: revwlist.store,\n                                        clientSort: true,\n                                        columnReordering: true,\n                                        structure: glayout_rindex,\n                                        headerMenu: csmenu\n                         }, document.createElement( 'div' ))\n        );\n\n        /* Append the new grid */\n        div_prjrevwlist.appendChild( grid_rindex.domNode );\n\n        /* Call startup, in order to render the grid: */\n        grid_rindex.startup();\n        refresh_csmenu();\n\n        /* Grid editing */\n        new zeta.Form({ normalsub: true, formid: 'configrev' });\n\n        /* grid resizing */\n        grid_rindex.connect( window, 'onresize',\n                             function( e ) { this.resize() } );\n        dojo.subscribe( 'resize_upane', grid_rindex,\n                        function( collapsed ) { this.resize() } );\n    }\n    </script>\n")
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
        __M_writer('\n\n    <script type="text/javascript">\n        dojo.addOnLoad( function() {\n            var n_selrevw = dojo.query( \'#selectrevw\' )[0];\n            var n_selrset = dojo.query( \'#selectrset\' )[0];\n            n_selrevw ? select_goto( n_selrevw ) : null;\n            n_selrset ? select_goto( n_selrset ) : null;\n        });\n        dojo.addOnLoad( setup_revwlist )\n\n        dojo.addOnLoad( setup_userpanes );\n        dojo.addOnLoad( adjust_upheight );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()