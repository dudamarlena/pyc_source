# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/projects/ticketcreate.html.py
# Compiled at: 2010-07-12 03:29:23
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278919763.719762
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/projects/ticketcreate.html'
_template_uri = '/derived/projects/ticketcreate.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['bd_body', 'hd_script', 'create_ticket', 'hd_links', 'bd_script']
page_tooltips = [
 [
  'Help',
  "Track issues, bugs, features, tasks etc ... using tickets.\nThe three main attributes of a ticket are <b>type, status, severity</b>.\nType should give an idea about why? and what? of a ticket. Status\ntracks ticket workflow. Severity tells how severe the ticket is to the\nproject (synonymous to priority).\n<br/>\nUsers can move tickets from one status to another, also setting\nits due-date. <b>User who is changing the ticket status will become the new\nowner of the ticket</b>.\n<br/>\nIf, in case a ticket expects a response from a user other than the ticket's\nowner, it can be indicated so using 'promptuser' attribute.\n<br/>\nUse ticket id, where ever the ticket needs to be referenced.\n"]]

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
        h = context.get('h', UNDEFINED)
        forms = _mako_get_namespace(context, 'forms')
        str = context.get('str', UNDEFINED)

        def create_ticket():
            return render_create_ticket(context)

        __M_writer = context.writer()
        __M_writer('\n    ')
        searchbox = capture(forms.form_searchbox, c.authuser, 'searchticket', 'Search-ticket', h.suburl_search, c.searchfaces)
        sel_tck = capture(forms.form_selectticket, c.authuser, c.seltickets, c.ticket and str(c.ticket.id) or '')
        if c.tckeditable:
            newtck = '<span class="ml10 fwnormal fntsmall">' + '<a href="' + h.url_ticketcreate + '">Create</a>' + '</span>'
        else:
            newtck = '<span></span>'
        if c.ticket:
            fav = capture(elements.favoriteicon, 'favtck')
        else:
            fav = '<span></span>'
        charts = capture(elements.iconlink, h.url_ticketcharts, 'barchart', title='Ticket analytics')
        tline = capture(elements.iconlink, h.url_tcktimeline, 'timeline', title='Timeline of tickets')
        __M_writer('\n    ')
        __M_writer(escape(elements.mainnav()))
        __M_writer('\n    ')
        __M_writer(escape(elements.contextnav([fav, searchbox, sel_tck], rspans=[
         charts, tline], tooltips=page_tooltips)))
        __M_writer('\n    <div id="bdy" class="w100">\n')
        if c.authusername == 'anonymous' or not c.userpanes:
            __M_writer('        <div class="fullpanel1">\n')
        else:
            __M_writer('        <div class="panel1">\n')
        __M_writer('            <div>\n                ')
        __M_writer(escape(create_ticket()))
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


def render_create_ticket(context):
    context.caller_stack._push_frame()
    try:
        forms = _mako_get_namespace(context, 'forms')
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <div class="zticketcreate mr5">\n        ')
        __M_writer(escape(forms.form_createticket(c.authuser, c.project, h.suburl_createtck, c.tck_typenames, c.tck_severitynames, c.projusers, c.pcomponents, c.pmilestones, c.pversions)))
        __M_writer('\n    </div>\n')
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
        __M_writer('\n\n    <script type="text/javascript">\n        dojo.addOnLoad( function () {\n            /* Setup the wiki goto list */\n            select_goto( dojo.query( \'#selectticket\' )[0] );\n        });\n        dojo.addOnLoad( initform_createtck );\n\n        dojo.addOnLoad( setup_userpanes );\n        dojo.addOnLoad( adjust_upheight );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()