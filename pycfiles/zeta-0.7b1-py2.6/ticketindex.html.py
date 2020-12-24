# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/projects/ticketindex.html.py
# Compiled at: 2010-07-10 01:43:10
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278740590.496638
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/projects/ticketindex.html'
_template_uri = '/derived/projects/ticketindex.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['hd_script', 'ticketindex', 'bd_body', 'hd_links', 'bd_script']
page_tooltips = [
 [
  'Ticket-list',
  "List of all tickets tracked under this project, organised in grid-style,\nenabling users to edit ticket attributes in-line. To know how, just\ndouble click on any of the grid's cell (that are not highlighted gray) and\nedit it. It is also possible to navigate from one cell to another using\n'up', 'down', 'left', 'right' arrows, to edit just press enter and edit. To save\nthe edited content, just press 'enter' or click outside the cell.\n<br/>\nThe header row in the grid can be used for two purpose. One, to sort the list\nby desired column (by left clicking), two, to add/remove columns (by right\nclicking). \n"],
 [
  'Standard-filters',
  'Standard ticket filters are named filter rules, based on complex regular\nexpressions defined at the backend. First among the list of standard filters\nwill be interpreted as default filter. These filters are available for all\nregistered users. Contact site-administrator to define a new type of standard\nfilter.\n'],
 [
  'Custom-filters',
  'Listed tickets can further be filtered using its attribute values, like,\ntype, severity, status, owner, component, milestone and version. When multiple\nvalues are selected, filter rules will be ANDed.\n'],
 [
  'Saved-filters',
  'Custom filters can be saved under the user who is defining the\nfilter.\n'],
 [
  'Ticket',
  "Track issues, bugs, features, tasks etc ... using tickets.\nThe three main attributes of a ticket are <b>type, status, severity</b>.\nType should give an idea about why? and what? of a ticket. Status\ntracks ticket workflow. Severity tells how severe the ticket is to the\nproject (synonymous to priority).\n<br/>\nUsers can move tickets from one status to another, also setting\nits due-date. <b>User who is changing the ticket status will become the new\nowner of the ticket</b>.\n<br/>\nIf, in case a ticket expects a response from a user other than the ticket's\nowner, it can be indicated so using 'promptuser' attribute.\n<br/>\nUse ticket id, where ever the ticket needs to be referenced.\n"],
 [
  'Attachments',
  'Add <b>summary</b> and <b>tags</b> to ticket attachments.'],
 [
  'Timeline',
  'Timeline of ticket(s) activity']]

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


def render_hd_script(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        parent = context.get('parent', UNDEFINED)
        h = context.get('h', UNDEFINED)
        m = context.get('m', UNDEFINED)
        dict = context.get('dict', UNDEFINED)
        str = context.get('str', UNDEFINED)
        v = context.get('v', UNDEFINED)
        cp = context.get('cp', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        __M_writer(escape(parent.hd_script()))
        __M_writer('\n\n    <script type="text/javascript">\n    /********** Setup Ticket Grid **************/\n    ')
        ticket_id = c.ticket and c.ticket.id or ''
        tckeditable = c.tckeditable and 'true' or 'false'
        editcolor = c.tckeditable and 'color : black;' or 'color : grey;'
        ticketresolv = dict([ (str(st), '') for st in c.tstat_resolv ])
        __M_writer('\n\n    // Add empty component, milestone, version for select options\n    components  = ')
        __M_writer(h.json.dumps(dict(c.pcomponents + [('', '')])))
        __M_writer('\n    milestones  = ')
        __M_writer(h.json.dumps(dict(c.pmilestones + [('', '')])))
        __M_writer('\n    versions    = ')
        __M_writer(h.json.dumps(dict(c.pversions + [('', '')])))
        __M_writer('\n\n    tck_typenames    = ')
        __M_writer(h.json.dumps(c.tck_typenames))
        __M_writer('\n    tck_severitynames= ')
        __M_writer(h.json.dumps(c.tck_severitynames))
        __M_writer('\n    projusers        = ')
        __M_writer(h.json.dumps(c.projusers))
        __M_writer('\n\n    tckccodes   = ')
        __M_writer(c.tckccodes)
        __M_writer('\n    ticketresolv= ')
        __M_writer(escape(ticketresolv))
        __M_writer("\n    currdate    = new Date();\n\n    // Grid - Row styling using ticket color-coding\n    function compute_rowcolor( item ) {\n        var tckdetail = {\n            tck_statusname   : ticketlist.store.getValue( item, 'tck_statusname'),\n            tck_severityname : ticketlist.store.getValue( item, 'tck_severityname'),\n            tck_typename     : ticketlist.store.getValue( item, 'tck_typename'),\n        };\n        var bgcolor = tckcolorcode( tckdetail, tckccodes );\n        return bgcolor;\n    }\n\n    // GRID\n    colnames    = { Id        : null,\n                    Summary   : null,\n                    Type      : null,\n                    Severity  : null,\n                    Status    : null,\n                    Duedate   : null,\n                    Owner     : null,\n                    Prompting : null,\n                    Component : null,\n                    Milestone : null,\n                    UpVotes   : null,\n                    DownVotes : null,\n                    Version   : null,\n                    Olderby   : null\n                  };\n    // GRID Cell formatters\n    function get_ticketids( rowindex, item ) {\n        if( ! grid_tindex ) { return; }\n        if( ! item ) { return; }\n        return [ ticketlist.store.getValue( item, 'ticketurl' ),\n                 ticketlist.store.getValue( item, 'id' ) ]\n    }\n    function format_ticketids( item, rowindex ) {\n        if( ! grid_tindex ) { return; }\n        if( ! item ) { return; }\n        return create_anchor( item[0], item[1] );\n    }\n    function get_duedate( idx, item ) { \n        if( ! grid_tindex ) { return; }\n        if( ! item ) { return; }\n        var dd = ticketlist.store.getValues( item, 'due_date' );\n        dd = dd ? new Date( dd[0], dd[1]-1, dd[2] ) : null;\n        return [ ticketlist.store.getValue( item, 'tck_statusname'), dd, idx ]\n    }\n    function format_date(args){\n        // While re-sorting the grid via user events, this function is called\n        // with empty arguments\n        if ( args ) {\n            var tckstat    = args[0];\n            var inDatum    = args[1];\n            var inRowindex = args[2];\n            var text = String(inDatum) == 'Invalid Date' ? \n                       '-'\n                       : dojo.date.locale.format(new Date(inDatum), this.constraint )\n            if( tckstat in ticketresolv ) {\n                strike = 'text-decoration: line-through;'\n                color  = 'gray;'\n            } else {\n                color  = 'color: ' + ")
        __M_writer('                         (new Date(inDatum) - currdate < 0 ? \'red;\' : \'gray;\')\n                strike = \'\'\n            }\n            this.customStyles.push( color + strike )\n            return text\n        }\n    }\n    function format_cctype( val, idx ) {\n        var item = this.grid.getItem( idx );\n        bgcolor  = compute_rowcolor( item )\n        this.view.getRowNode(idx).style.backgroundColor = bgcolor;\n        return val\n    }\n    function format_ccseverity( val, idx ) {\n        var item = this.grid.getItem( idx );\n        bgcolor  = compute_rowcolor( item )\n        this.view.getRowNode(idx).style.backgroundColor = bgcolor;\n        return val\n    }\n\n\n    function onStyleRow( inRow ) {\n        var item = grid_tindex.getItem( inRow.index );\n        if( item ) {        // dojo.data store item\n            bgcolor      = item.bgcolor ? item.bgcolor : compute_rowcolor( item )\n            item.bgcolor = bgcolor;\n            inRow.customStyles = \'background-color : \' + bgcolor + \';\';\n        }\n    }\n\n    // Data store Write handlers\n    function tl_onset( item, attr_name, oldval, newval ) {\n        var formnode     = null;\n        var id           = ticketlist.store.getValue( item, \'id\' );\n        var typename     = ticketlist.store.getValue( item, \'tck_typename\' );\n        var severityname = ticketlist.store.getValue( item, \'tck_severityname\' );\n        var promptuser   = ticketlist.store.getValue( item, \'promptuser\' );\n        var compname     = ticketlist.store.getValue( item, \'componentname\' );\n        var mstnname     = ticketlist.store.getValue( item, \'milestone_name\' );\n        var vername      = ticketlist.store.getValue( item, \'version_name\' );\n        var summary      = ticketlist.store.getValue( item, \'summary\' );\n\n        if ( attr_name == \'tck_typename\' ) {\n            formnode = form_tcktype;\n            dojo.query( \'input[name=tck_typename]\', form_tcktype\n                      )[0].value = typename;\n        } else if ( attr_name == \'tck_severityname\' ) {\n            formnode = form_tckseverity;\n            dojo.query( \'input[name=tck_severityname]\', form_tckseverity\n                      )[0].value = severityname;\n        } else if ( attr_name == \'promptuser\' ) {\n            formnode = form_tckpromptuser;\n            dojo.query( \'input[name=promptuser]\', form_tckpromptuser\n                      )[0].value = promptuser;\n        } else if ( attr_name == \'componentname\' ) {\n            formnode = form_tckcomponent;\n            dojo.query( \'input[name=component_id]\', form_tckcomponent\n                      )[0].value = components[compname];\n        } else if ( attr_name == \'milestone_name\' ) {\n            formnode = form_tckmilestone;\n            dojo.query( \'input[name=milestone_id]\', form_tckmilestone\n                      )[0].value = milestones[mstnname];\n        } else if ( attr_name == \'version_name\' ) {\n            formnode = form_tckversion;\n            dojo.query( \'input[name=version_id]\', form_tckversion\n                      )[0].value = versions[vername];\n        } else if ( attr_name == \'summary\' ) {\n            formnode = form_tcksummary;\n            dojo.query( \'input[name=summary]\', form_tcksummary\n                      )[0].value = summary;\n        }\n        if( formnode ) {\n            dojo.query( \'input[name=ticket_id]\', formnode )[0].value = id;\n            submitform( formnode );\n        }\n        // Recompute the background\n        // item.bgcolor = compute_rowcolor( item )\n    }\n\n    // GRID Title customization menu\n    function refresh_csmenu() {\n        // Refresh column labels\n        for( name in colnames ) {\n            var mitem = colnames[name];\n            var check = \'<input type="checkbox" checked="checked"></input> &ensp;\';\n            mitem.colhide ?\n                mitem.attr( \'label\', \'&ensp;&ensp;&ensp;&ensp;\' + mitem.orglabel )\n                : mitem.attr( \'label\', check + mitem.orglabel )\n        }\n    }\n    function on_selectcolumns( name ) {\n        // Toggle the hidden attribute and refresh\n        var visibile = colnames[name].colhide;\n        colnames[name].colhide = colnames[name].colhide ? false : true;\n        refresh_csmenu();\n        // Refresh column hidden status in the layout\n        var cells = grid_tindex.layout.cells;\n        for( i=0 ; i < cells.length; i++ ) {\n            if ( name == cells[i].name ) {\n                grid_tindex.layout.setColumnVisibility( i, visibile );\n            }\n        }\n    }\n    function setup_csmenu() {\n        // Create Menu on the last column\n        var csmenu   = new dijit.Menu();\n        var mi_title = new dijit.MenuItem({ \n                            label : \'Columns\',\n                            iconClass:"dispnone",\n                            class: "calign"\n                       });\n\n        dojo.style( mi_title.domNode, { fontWeight: \'bold\', color: \'black\' });\n        dojo.style( csmenu.domNode, { fontSize: \'small\', color: \'blue\' });\n\n        csmenu.addChild( mi_title );\n        csmenu.addChild( new dijit.MenuSeparator() );\n\n        // Create menu items\n        for( name in colnames ) {\n            colnames[name] = new dijit.MenuItem({\n                                    label: name,\n                                    iconClass: "dispnone",\n                                    onClick : dojo.hitch( null,\n                                                          on_selectcolumns,\n                                                          name\n                                                        )\n                             })\n            colnames[name].colhide  = false;\n            colnames[name].orglabel = name;\n            csmenu.addChild( colnames[name] );\n        }\n        colnames.Prompting.colhide = true;\n        colnames.Component.colhide = true;\n        colnames.Version.colhide = true;\n        colnames.Olderby.colhide = true;\n        colnames.DownVotes.colhide = true;\n        dojo.setObject( \'csmenu\', csmenu )\n    }\n\n    function setup_tcklist() {\n        var div_prjtcklist = dojo.byId("prjtcklist");\n\n        /* Setup the wiki goto list */\n        select_goto( dojo.byId( \'selectticket\' ) );\n        select_goto( dojo.byId( \'selsavfilter\' ) );\n\n        // GRID Layout\n        var glayout_tindex = [\n                { // View is an array of cells\n                    cells: [\n                      { name : \'Id\',\n                        field: \'id\',\n                        width: \'4em\',\n                        hidden: false,\n                        get  : get_ticketids,\n                        formatter : format_ticketids,\n                        styles : "text-align : left;"\n                      },\n                      { name : \'Summary\',\n                        field: \'summary\',\n                        width: \'30em\',\n                        hidden: false,\n                        styles: \'')
        __M_writer(escape(editcolor))
        __M_writer("',\n                        editable: ")
        __M_writer(escape(tckeditable))
        __M_writer("\n                      },\n                      { name : 'Type',\n                        field: 'tck_typename',\n                        width: '7em',\n                        hidden: false,\n                        editable: ")
        __M_writer(escape(tckeditable))
        __M_writer(",\n                        styles: '")
        __M_writer(escape(editcolor))
        __M_writer("',\n                        type: dojox.grid.cells.Select,\n                        formatter: format_cctype,\n                        options : ")
        __M_writer(h.json.dumps(c.tck_typenames))
        __M_writer("\n                      },\n                      { name : 'Severity',\n                        field: 'tck_severityname',\n                        width: '7em',\n                        hidden: false,\n                        editable: ")
        __M_writer(escape(tckeditable))
        __M_writer(",\n                        styles: '")
        __M_writer(escape(editcolor))
        __M_writer("',\n                        type: dojox.grid.cells.Select,\n                        formatter: format_ccseverity,\n                        options : ")
        __M_writer(h.json.dumps(c.tck_severitynames))
        __M_writer("\n                      },\n                      { name : 'Status',\n                        field: 'tck_statusname',\n                        width: '7em',\n                        hidden: false,\n                        editable: false,\n                        styles: 'color : gray;',\n                        type: dojox.grid.cells.Select,\n                        options : ")
        __M_writer(h.json.dumps(c.tck_statusnames))
        __M_writer('\n                      },\n                      { name : \'Duedate\',\n                        field: \'due_date\',\n                        width: \'7em\',\n                        hidden: false,\n                        type: dojox.grid.cells.DateTextBox,\n                        editable: false,\n                        editorProps: {},\n                        get  : get_duedate,\n                        formatter: format_date,\n                        constraint: { datePattern: \'dd/MM/yyyy\',\n                                      formatLength: \'short\',\n                                      selector: "date" }\n                      },\n                      { name : \'Owner\',\n                        field: \'owner\',\n                        width: \'7em\',\n                        hidden: false,\n                        styles: \'color : gray;\'\n                      },\n                      { name : \'Prompting\',\n                        field: \'promptuser\',\n                        width: \'7em\',\n                        hidden: true,\n                        editable: ')
        __M_writer(escape(tckeditable))
        __M_writer(",\n                        styles: '")
        __M_writer(escape(editcolor))
        __M_writer("',\n                        type: dojox.grid.cells.Select,\n                        options : ")
        __M_writer(h.json.dumps(c.projusers))
        __M_writer("\n                      },\n                      { name : 'Component',\n                        field: 'componentname',\n                        width: '7em',\n                        hidden: true,\n                        editable: ")
        __M_writer(escape(tckeditable))
        __M_writer(",\n                        styles: '")
        __M_writer(escape(editcolor))
        __M_writer("',\n                        type: dojox.grid.cells.Select,\n                        options : ")
        __M_writer(h.json.dumps([ cp[0] for cp in c.pcomponents ]))
        __M_writer("\n                      },\n                      { name : 'Milestone',\n                        field: 'milestone_name',\n                        width: '9em',\n                        hidden: false,\n                        editable: ")
        __M_writer(escape(tckeditable))
        __M_writer(",\n                        styles: '")
        __M_writer(escape(editcolor))
        __M_writer("',\n                        type: dojox.grid.cells.Select,\n                        options : ")
        __M_writer(h.json.dumps([ m[0] for m in c.pmilestones ]))
        __M_writer("\n                      },\n                      { name : 'UpVotes',\n                        field: 'upvotes',\n                        width: '6em',\n                        hidden: false,\n                        styles: 'text-align: center; color : green;'\n                      },\n                      { name : 'DownVotes',\n                        field: 'downvotes',\n                        width: '7em',\n                        hidden: true,\n                        styles: 'text-align: center; color : red;'\n                      },\n                      { name : 'Version',\n                        field: 'version_name',\n                        width: '7em',\n                        hidden: true,\n                        editable: ")
        __M_writer(escape(tckeditable))
        __M_writer(",\n                        styles: '")
        __M_writer(escape(editcolor))
        __M_writer("',\n                        type: dojox.grid.cells.Select,\n                        options : ")
        __M_writer(h.json.dumps([ v[0] for v in c.pversions ]))
        __M_writer("\n                      },\n                      { name : 'Olderby',\n                        field: 'age',\n                        width: '7em',\n                        hidden: true,\n                        styles: 'color : gray;'\n                      }\n                    ]\n                },\n            ];\n\n        setup_csmenu();\n\n        make_ifws_ticketlist( '")
        __M_writer(h.url_ticketlist)
        __M_writer('\', tl_onset );\n\n        /* Grid with Layout */\n        dojo.setObject(\n            \'grid_tindex\',\n            new dojox.grid.DataGrid({\n                    store: ticketlist.store,\n                    clientSort: true,\n                    columnReordering: true,\n                    structure: glayout_tindex,\n                    headerMenu: csmenu,\n                    columnReordering: true\n             }, document.createElement( \'div\' ))\n        );\n\n        /* Append the new grid */\n        div_prjtcklist.appendChild( grid_tindex.domNode );\n\n        /* Call startup, in order to render the grid: */\n        grid_tindex.startup();\n        refresh_csmenu();\n\n        /* Grid editing */\n        new zeta.Form({ normalsub: true, formid: \'tcktype\' });\n        new zeta.Form({ normalsub: true, formid: \'tckseverity\' });\n        new zeta.Form({ normalsub: true, formid: \'tcksummary\' });\n        new zeta.Form({ normalsub: true, formid: \'tckpromptuser\' });\n        new zeta.Form({ normalsub: true, formid: \'tckcomponent\' });\n        new zeta.Form({ normalsub: true, formid: \'tckmilestone\' });\n        new zeta.Form({ normalsub: true, formid: \'tckversion\' });\n\n        /* grid resizing */\n        grid_tindex.connect( window, \'onresize\',\n                             function( e ) { this.resize() } );\n        dojo.subscribe( \'resize_upane\', grid_tindex,\n                        function( collapsed ) { this.resize() } );\n\n        /* Timeout to update ticket count */\n        function tm_onesecrecur() {\n            doticketcount() ? "Done" : setTimeout( tm_onesecrecur, 1000 );\n        }\n        setTimeout( tm_onesecrecur, 1000 )\n    }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_ticketindex(context, typenames, severitynames, statusnames, users, components, milestones, versions):
    context.caller_stack._push_frame()
    try:
        forms = _mako_get_namespace(context, 'forms')
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <div class="disptable w100">\n    <div class="disptrow">\n        <div class="disptcell">\n            <div id="prjtcklist" class="posr ml5 mr5 br5"\n                 style="height: 600px; border: 4px solid #B3CFB3;">\n            </div>\n        </div>\n        <div class="disptcell vtop" \n             style="width: 12em; border-left : 1px solid gray;">\n             <div class="pl5 pb10 fggray fntbold">\n                 <span>Tickets : </span>\n                 <span id="tckcount" class="fgblack">')
        __M_writer(escape(len(c.projtckids)))
        __M_writer('</span>\n             </div>\n            <div class="pl5 fggray fntbold">Standard Filters</div>\n            <div class="disptable">\n')
        for (filtername, _l) in c.tckfilters:
            __M_writer('            <div class="disptrow">\n                <div id="')
            __M_writer(escape(filtername))
            __M_writer('" \n                     class="disptcell pl10 standrdfilter">\n                     <div class="hoverhighlight br4 fgblue pointer p3"\n                          title="In-browser filtering">\n                         ')
            __M_writer(escape(filtername))
            __M_writer('\n                     </div>\n                </div>\n                <div class="disptcell pl10">\n                    ')
            href = h.url_fortcklist(c.projectname, stdfilter=filtername)
            __M_writer('\n                    ')
            __M_writer(escape(elements.iconlink(href, 'servergo', title='Filter from server')))
            __M_writer('\n                </div>\n            </div>\n')

        __M_writer('            </div>\n            <div class="pl5 pb5 pt10 fggray fntbold">Custom Filters</div>\n            <div id="filter_prjtcklist" class="pl10">\n                ')
        filt = h.json.loads(c.savfilterval[1] or '{}')
        __M_writer('\n                <div forcol="status" class="pt3">\n                    ')
        __M_writer(escape(forms.select(name='tck_statusname', options=[
         'by-status'] + statusnames, opt_selected=filt.get('tck_statusname', 'by-status'))))
        __M_writer('\n                </div>\n                <div forcol="type" class="pt3">\n                    ')
        __M_writer(escape(forms.select(name='tck_typename', options=[
         'by-type'] + typenames, opt_selected=filt.get('tck_typename', 'by-type'))))
        __M_writer('\n                </div>\n                <div forcol="severity" class="pt3">\n                    ')
        __M_writer(escape(forms.select(name='tck_severityname', options=[
         'by-severity'] + severitynames, opt_selected=filt.get('tck_severityname', 'by-severity'))))
        __M_writer('\n                </div>\n                <div forcol="owner" class="pt3">\n                    ')
        __M_writer(escape(forms.select(name='owner', options=[
         'by-owner'] + users, opt_selected=filt.get('owner', 'by-owner'))))
        __M_writer('\n                </div>\n                <div forcol="component" class="pt3">\n                    ')
        __M_writer(escape(forms.select(name='componentname', options=[
         'by-component'] + components, opt_selected=filt.get('componentname', 'by-component'))))
        __M_writer('\n                </div>\n                <div forcol="milestone" class="pt3">\n                    ')
        __M_writer(escape(forms.select(name='milestone_name', options=[
         'by-milestone'] + milestones, opt_selected=filt.get('milestone_name', 'by-milestone'))))
        __M_writer('\n                </div>\n                <div forcol="version" class="pt3">\n                    ')
        __M_writer(escape(forms.select(name='version_name', options=[
         'by-version'] + versions, opt_selected=filt.get('version_name', 'by-version'))))
        __M_writer('\n                </div>\n                ')
        __M_writer(escape(forms.form_addtckfilter(c.authuser, h.suburl_addtckfilter)))
        __M_writer('\n            </div>\n            <div class="bclear pl5 pb5 pt10 fggray fntbold">Saved Filters</div>\n            <div class="pl10">\n                ')
        __M_writer(escape(forms.form_selectsavfilter(c.authuser, c.savfilterlist, c.savfiltername and c.savfiltername or '')))
        __M_writer('\n')
        if c.savfilter:
            __M_writer('                    ')
            __M_writer(escape(forms.form_deltckfilter(c.authuser, c.savfilter, h.suburl_deltckfilter)))
            __M_writer('\n')
        __M_writer('            </div>\n        </div>\n    </div>\n    </div>\n    <div class="dispnone">\n        ')
        __M_writer(escape(forms.form_tcksummary(c.authuser, c.project, h.suburl_configtck)))
        __M_writer('\n        ')
        __M_writer(escape(forms.form_tcktype(c.authuser, c.project, h.suburl_configtck)))
        __M_writer('\n        ')
        __M_writer(escape(forms.form_tckseverity(c.authuser, c.project, h.suburl_configtck)))
        __M_writer('\n        ')
        __M_writer(escape(forms.form_tckpromptuser(c.authuser, c.project, h.suburl_configtck)))
        __M_writer('\n        ')
        __M_writer(escape(forms.form_tckcomponent(c.authuser, c.project, h.suburl_configtck)))
        __M_writer('\n        ')
        __M_writer(escape(forms.form_tckmilestone(c.authuser, c.project, h.suburl_configtck)))
        __M_writer('\n        ')
        __M_writer(escape(forms.form_tckversion(c.authuser, c.project, h.suburl_configtck)))
        __M_writer('\n    </div>\n    <script type="text/javascript">\n        var resolved   = false;\n        var unresolved = false;\n\n        function doticketcount() {\n            var n = dojo.byId( \'tckcount\' );\n            n.innerHTML = grid_tindex.rowCount;\n            return grid_tindex.rowCount;\n        }\n\n        function customquery() {\n            var n_selects = dojo.query( \'#filter_prjtcklist select\' );\n            var query     = {}\n            var re        = /by-/\n            for( i = 0; i < n_selects.length; i++ ) {\n                var n = n_selects[i];\n                var v = n.value;\n                if( re.test( v ) ) {\n                    continue;\n                }\n                query[dojo.attr(n, \'name\')] = n.value;\n            }\n            return query\n        }\n        function filter_onchange( e ) {\n            grid_tindex.filter( customquery(), true );\n            doticketcount();\n        }\n        function standrd_filter( filtername, e ) {\n            var q = {}\n            q[filtername] = true\n            grid_tindex.filter(q, true );\n            doticketcount();\n        }\n        function setup_tckfilters() {\n            // Connect custom filters\n            dojo.forEach(\n                dojo.query( \'#filter_prjtcklist select\' ),\n                function( n ) { dojo.connect( n, \'onchange\', filter_onchange ); }\n            );\n            // Connect standard filters\n            dojo.forEach(\n                dojo.query( \'.standrdfilter\' ),\n                function( n ) {\n                    var filtername = dojo.attr( n, \'id\' );\n                    dojo.connect(\n                        n, \'onclick\', dojo.partial( standrd_filter, filtername )\n                    );\n                }\n            );\n        }\n    </script>\n')
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

        def ticketindex(typenames, severitynames, statusnames, users, components, milestones, versions):
            return render_ticketindex(context, typenames, severitynames, statusnames, users, components, milestones, versions)

        forms = _mako_get_namespace(context, 'forms')
        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        searchbox = capture(forms.form_searchbox, c.authuser, 'searchticket', 'Search-ticket', h.suburl_search, c.searchfaces)
        sel_tck = capture(forms.form_selectticket, c.authuser, c.seltickets, c.ticket and str(c.ticket.id) or '')
        if c.tckeditable:
            newtck = '<span class="ml10 fwnormal fntsmall">                        <a href="%s" title="Create a new ticket">                        Create</a></span>' % h.url_ticketcreate
        else:
            newtck = '<span></span>'
        attachs = '<span class="ml10 fwnormal fntsmall">' + '<a href="%s" title="List of files attached to tickets">                    Attachments</a></span>' % h.url_tckattachs
        charts = capture(elements.iconlink, h.url_ticketcharts, 'barchart', title='Ticket analytics')
        tline = capture(elements.iconlink, h.url_tcktimeline, 'timeline', title='Timeline of tickets')
        __M_writer('\n    ')
        __M_writer(escape(elements.mainnav()))
        __M_writer('\n    ')
        __M_writer(escape(elements.contextnav([searchbox, sel_tck, newtck, attachs], rspans=[
         charts, tline], tooltips=page_tooltips)))
        __M_writer('\n    <div id="bdy" class="w100">\n')
        if c.authusername == 'anonymous' or not c.userpanes:
            __M_writer('        <div class="fullpanel1">\n')
        else:
            __M_writer('        <div class="panel1">\n')
        __M_writer('            <div>\n                ')
        __M_writer(escape(ticketindex(c.tck_typenames, c.tck_severitynames, c.tck_statusnames, c.projusers, c.pcompnames, c.mstnnames, c.vernames)))
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
        __M_writer('\n\n    <script type="text/javascript">\n        dojo.addOnLoad( setup_tcklist );\n        dojo.addOnLoad( setup_tckfilters );\n        dojoaddOnLoad( \'initform_addtckfilter\' );\n        dojoaddOnLoad( \'initform_deltckfilter\' );\n\n        dojo.addOnLoad( setup_userpanes );\n        dojo.addOnLoad( adjust_upheight );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()