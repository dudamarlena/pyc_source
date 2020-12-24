# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/projects/wikiattachs.html.py
# Compiled at: 2010-07-12 03:59:45
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278921585.185707
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/projects/wikiattachs.html'
_template_uri = '/derived/projects/wikiattachs.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['hd_script', 'bd_script', 'bd_body']
page_tooltips = [
 [
  'Help',
  "List of attachments to project's wiki pages."],
 [
  'Wiki list',
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
        __M_writer('\n')
        __M_writer('\n')
        __M_writer('\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n\n')
        __M_writer('\n\n\n')
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


def render_bd_script(context):
    context.caller_stack._push_frame()
    try:
        parent = context.get('parent', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        __M_writer(escape(parent.bd_script()))
        __M_writer('\n\n    <script type="text/javascript">\n    dojo.addOnLoad( function () {\n        /* Setup the wiki goto list */\n        select_goto( dojo.query( \'#selectwikipage\' )[0] );\n    });\n    dojo.addOnLoad( setup_userpanes );\n    dojo.addOnLoad( adjust_upheight );\n    </script>\n')
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
        sel_wp = capture(forms.form_selectwikipage, c.authuser, c.wikipagenames, c.wikipagename or '')
        searchbox = capture(forms.form_searchbox, c.authuser, 'searchwiki', 'Search-wiki', h.suburl_search, c.searchfaces)
        addattachs = '<span class="ml10 fwnormal fntsmall">' + '<a href="%s" title="Add attachment to site">                       Add</a></span>' % h.url_addattachment
        charts = capture(elements.iconlink, h.url_wikicharts, 'barchart', title='Wiki charts')
        tline = capture(elements.iconlink, h.url_wikitimeline, 'timeline', title='Timeline for all wiki pages')
        __M_writer('\n    ')
        __M_writer(escape(elements.mainnav()))
        __M_writer('\n    ')
        __M_writer(escape(elements.contextnav([searchbox, sel_wp, addattachs], rspans=[
         charts, tline], tooltips=page_tooltips)))
        __M_writer('\n    <div id="bdy" class="w100">\n')
        if c.authusername == 'anonymous' or not c.userpanes:
            __M_writer('        <div class="fullpanel1">\n')
        else:
            __M_writer('        <div class="panel1">\n')
        __M_writer('            <div class="m10">\n                ')
        __M_writer(escape(elements.attachments(c.authuser, c.attachments, c.editable)))
        __M_writer('\n                ')
        __M_writer(escape(forms.form_attachssummary(c.authuser, h.suburl_attachssummary)))
        __M_writer('\n                ')
        __M_writer(escape(forms.form_attachstags(c.authuser, h.suburl_attachstags)))
        __M_writer('\n            </div>\n        </div>\n')
        if c.authusername != 'anonymous' and c.userpanes:
            __M_writer('        <div class="panel2">')
            __M_writer(escape(elements.user_panes(c.userpanes)))
            __M_writer('</div>\n')
        __M_writer('    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()