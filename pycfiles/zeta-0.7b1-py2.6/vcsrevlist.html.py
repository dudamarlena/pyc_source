# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/projects/vcsrevlist.html.py
# Compiled at: 2010-07-12 03:53:39
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278921219.1493
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/projects/vcsrevlist.html'
_template_uri = '/derived/projects/vcsrevlist.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['hd_links', 'hd_script', 'showrevlist', 'bd_body', 'hd_styles', 'bd_script']
page_tooltips = [
 [
  'Help',
  'Details about each repository revision listed in reverse chronological order.\n'],
 [
  'Repository-list',
  'Integrate one or more repositories with projects by providing its\n<em>type</em> (like svn ...) and <em>root-url</em>. Make sure that\n<em>root-url</em> points to the same machine, or to a machine on the local network.\n<br/>\nRepositories integrated with this project are listed in grid-style. Edit them\ninline.\n'],
 [
  'Browsing',
  '\nBrowsing the repository is provided in explorer style. By default the latest\nversion of the repository is shown in the explorer widget. To explore a different\nrevision use <b>< revno</b> and <b>revno ></b> links.\n'],
 [
  'Files',
  '\nFiles in repository are viewable with syntax highlighting, annotation and\nchangesets.\n']]

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
        __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showrevlist(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <div class="ml10 w100">\n        <div class="calign m10 w95 p5" \n             style="overflow-x: auto; border: 1px solid #f2f2f2">\n')
        for rp in c.revpages:
            __M_writer('                <a class="ml5" href=')
            __M_writer(escape(rp[1]))
            __M_writer('>')
            __M_writer(escape(rp[0]))
            __M_writer('</a>\n')

        __M_writer('        </div>\n        <div class="m10 w95 p5">\n            <div class="disptable w100">\n                <div class="disptrow w100 bggrn2 fntbold">\n                    <div class="disptcell p5" \n                         style="width: 6em; border-left: 1px solid #d6d6d6;">\n                        Rev\n                    </div>\n                    <div class="disptcell p5"\n                         style="border-left: 1px solid #d6d6d6;">\n                         Log\n                    </div>\n                    <div class="disptcell p5" \n                         style="border-left: 1px solid #d6d6d6;">\n                        Author\n                    </div>\n                    <div class="disptcell p5" \n                         style="width: 12em; border-left: 1px solid #d6d6d6;">\n                        Date\n                    </div>\n                </div>\n')
        for log in c.revlist:
            __M_writer('                <div class="disptrow" name="revitem">\n                    <div class="disptcell calign p5" \n                         style="width: 6em; border-bottom: 1px solid #f2f2f2;">\n                        <a href="')
            __M_writer(escape(log[4]))
            __M_writer('">')
            __M_writer(escape(log[1]))
            __M_writer('</a>\n                    </div>\n                    <div class="disptcell p5" \n                         style="border-bottom: 1px solid #f2f2f2;">\n                        <div style="font-family : Courier, Courier New">\n                            ')
            __M_writer(log[0].replace('\n', '<br></br>'))
            __M_writer('\n                        </div>\n                    </div>\n                    <div class="disptcell p5" \n                         style="border-bottom: 1px solid #f2f2f2;">\n                        ')
            __M_writer(escape(log[2]))
            __M_writer('\n                    </div>\n                    <div class="disptcell p5" \n                         style="width: 12em; border-bottom: 1px solid #f2f2f2;">\n                        ')
            __M_writer(escape(log[3].strftime('%a, %b %d, %Y')))
            __M_writer('\n                    </div>\n                </div>\n')

        __M_writer('            </table>\n        </div>\n    </div>\n')
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

        def showrevlist():
            return render_showrevlist(context)

        __M_writer = context.writer()
        __M_writer('\n    ')
        title = '<a class="fntbold ml10">%s</a>' % c.vcs.name
        sel_vcs = capture(forms.form_selectvcs, c.authuser, c.vcslist, c.vcs and c.vcs.name or '')
        vcsbrowse = '<a class="ml10" title="Browse latest version"                      href="%s">Browser</a>' % h.url_vcsbrowse
        revlist = '<a class="ml10" title="List of repository revisions"                      href="%s">Revisions</a>' % h.url_revlist
        if c.vcseditable:
            newvcs = '<span class="ml10 fwnormal fntsmall">' + '<a href="%s"                           title="Integrate a new repository">Integrate</a></span>' % h.url_vcscreate
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
        __M_writer(escape(showrevlist()))
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
        __M_writer('\n\n    <script type="text/javascript">\n        dojo.addOnLoad( function () {\n            /* Setup the vcs goto list */\n            select_goto( dojo.query( \'#selectvcs\' )[0] );\n        });\n        dojo.addOnLoad( function() {\n            dojo.forEach(\n                dojo.query( "tr[name=revitem]" ),\n                function( n ) { highlightbyclass( n, \'bggray1\' ) }\n            );\n        });\n        dojo.addOnLoad( setup_userpanes );\n        dojo.addOnLoad( adjust_upheight );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()