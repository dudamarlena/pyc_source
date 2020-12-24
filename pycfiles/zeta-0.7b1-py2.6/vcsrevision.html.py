# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/projects/vcsrevision.html.py
# Compiled at: 2010-07-12 03:53:33
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278921213.601395
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/projects/vcsrevision.html'
_template_uri = '/derived/projects/vcsrevision.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['showrevision', 'changedfile', 'hd_links', 'hd_script', 'bd_body', 'hd_styles', 'bd_script']
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
import xml.etree.cElementTree as et
from pygments.formatters import HtmlFormatter

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
        __M_writer('\n\n')
        __M_writer('\n\n\n')
        __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showrevision(context):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)

        def changedfile(cf):
            return render_changedfile(context, cf)

        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        if c.revno_p:
            prevrev = [
             '&#8249; r' + str(c.revno_p) or '', h.url_revprev]
        if c.revno_n:
            nextrev = [
             'r' + str(c.revno_n) + ' &#8250;' or '', h.url_revnext]
        __M_writer('\n    <div class="disptable w100">\n    <div class="disptrow w100">\n        <div class="disptcell w100">\n            <div class="ml10 pb5" style="border-bottom : 1px solid gray">\n                <div class="ml10 posr floatr">\n')
        if c.revno_p:
            __M_writer('                        <a href="')
            __M_writer(escape(prevrev[1]))
            __M_writer('" class="pl10">')
            __M_writer(prevrev[0])
            __M_writer('</a>\n')
        __M_writer('                    <span class="fntbold pl10">r')
        __M_writer(escape(c.revno))
        __M_writer('</span>\n')
        if c.revno_n:
            __M_writer('                        <a href="')
            __M_writer(escape(nextrev[1]))
            __M_writer('" class="pl10">')
            __M_writer(nextrev[0])
            __M_writer('</a>\n')
        __M_writer('                </div>\n                <a class="ml10 floatr"\n                   title="Review all modified / added files in this changeset"\n                   href="')
        __M_writer(escape(h.url_reviewrev))
        __M_writer('">Review</a>\n                <span class="fntbold">Revision: </span>\n                <span class="fntbold fggreen">r')
        __M_writer(escape(c.revision[1]))
        __M_writer(' </span>\n                <span class="pl10">by <span>\n                <span class="fggreen">')
        __M_writer(escape(c.revision[2]))
        __M_writer(', </span>\n                <span class="pl10">on <span>\n                <span class="fggreen">\n                    ')
        __M_writer(escape(c.revision[3].strftime('%a, %b %d, %Y')))
        __M_writer('\n                </span>\n            </div>\n            <div class="pl10">\n                <br></br>\n                <div class="fnt100 fntbold">Log Message</div>\n                <br></br>\n                <pre class="wsprewrap" style="margin-left:1em;">')
        __M_writer(escape(c.revision[0]))
        __M_writer('</pre>\n                <br></br>\n                <div class="fnt100 fntbold floatl">Affected Files</div>\n                <div class="ml10 fntsmall floatl">\n                <a class="fgIred" title="download it as patchfile"\n                   href="')
        __M_writer(escape(c.revision[4]))
        __M_writer('">download-diff</a>\n                </div>\n                <br></br>\n                <table id="affectedfiles" class="ml20">\n')
        for cf in c.changedfiles:
            __M_writer('                    ')
            __M_writer(escape(changedfile(cf)))
            __M_writer('\n')

        __M_writer('                </table>\n            </div>\n        </div>\n    </div>\n    </div>\n    <script type="text/javascript">\n        function setup_diff() {\n            var n_tbl = dojo.byId( "affectedfiles" );\n            if( n_tbl ) {\n                var n_trs = dojo.query( "tr.cfrows", n_tbl );\n                for( i = 0; i < n_trs.length; i+=2 ) {\n                    var n_span = dojo.query( "span[name=diff]", n_trs[i] )[0];\n                    if( n_span ) {\n                        toggler( n_span, n_trs[i+1], "close", "diff", true )\n                    }\n                }\n            }\n        };\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_changedfile(context, cf):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        cf_ddurl = ''
        if cf['mime_type'] == 'text/directory':
            cf_url = '<span class="fggray">dir: ' + cf['repos_path'] + '</span>'
        else:
            cf_url = '<a href="%s">file:%s</a>' % (
             cf['fileurl'], cf['repos_path'])
        cfdiff = cf['diff'].strip()
        cfdiff = cf['diff'].strip('\r\n\t')
        if cfdiff:
            cfdiff = h.syntaxhl(cfdiff, lexname='diff', linenos=True)
            cfdiff = '<code class="wsprewrap">%s</code>' % cfdiff
        else:
            cfdiff = '<em> Empty difference</em>'
        __M_writer('\n    <tr class="cfrows">\n')
        if cf['changetype'] == 'modified':
            __M_writer('        <td class="pt10" style="width: 10em">\n            Modified\n            ( <span name="diff" class="fgblue pointer"> diff </span> )\n        </td>\n        <td class="pt10 pl10">\n            <span>')
            __M_writer(cf_url)
            __M_writer('</span>\n            <a class="ml10 fgIred" href="')
            __M_writer(cf['diffdownlurl'])
            __M_writer('">download-diff</a>\n        </td>\n')
        elif cf['changetype'] == 'added':
            __M_writer('        <td class="pt10 fggreen">Added</td>\n        <td class="pl10 pt10 ">')
            __M_writer(cf_url)
            __M_writer('</td>\n')
        elif cf['changetype'] == 'deleted':
            __M_writer('        <td class="fgred">Deleted</td>\n        <td class="pl10 pt10 fggray">')
            __M_writer(escape(cf['repos_path']))
            __M_writer('</td>\n')
        elif cf['changetype'] == 'normal':
            __M_writer('        <td class="fggray">Normal</td>\n        <td class="pl10 pt10">')
            __M_writer(cf_url)
            __M_writer('</td>\n')
        __M_writer('    </tr>\n    <tr class="cfrows dispnone ml50 pt10 pl10">\n        <td class="pl20 pt10 pb10" colspan="3">\n            <div class="pl5" style="border-left: 2px solid gray;">\n            ')
        __M_writer(cfdiff)
        __M_writer('\n            </div>\n        </td>\n    </tr>\n')
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


def render_bd_body(context):
    context.caller_stack._push_frame()
    try:
        capture = context.get('capture', UNDEFINED)
        c = context.get('c', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')

        def showrevision():
            return render_showrevision(context)

        h = context.get('h', UNDEFINED)
        forms = _mako_get_namespace(context, 'forms')
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
        __M_writer('            <div class="mr10">\n                ')
        __M_writer(escape(showrevision()))
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
        __M_writer('\n    <style type="text/css">\n        ')
        __M_writer(escape(HtmlFormatter().get_style_defs('.highlight')))
        __M_writer('\n')
        __M_writer('        .highlighttable td.linenos { padding : 3px }\n        .highlighttable td.code { padding : 3px }\n    </style>\n')
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
        __M_writer('\n\n    <script type="text/javascript">\n        dojo.addOnLoad( function() {\n            /* Setup the vcs goto list */\n            select_goto( dojo.query( \'#selectvcs\' )[0] );\n        });\n        dojo.addOnLoad( setup_diff );\n\n        dojo.addOnLoad( setup_userpanes );\n        dojo.addOnLoad( adjust_upheight );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()