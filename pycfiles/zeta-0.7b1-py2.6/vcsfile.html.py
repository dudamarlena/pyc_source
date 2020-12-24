# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/projects/vcsfile.html.py
# Compiled at: 2010-07-12 03:53:31
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278921211.182503
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/projects/vcsfile.html'
_template_uri = '/derived/projects/vcsfile.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['showfilerev', 'showfile', 'hd_links', 'showfileerror', 'hd_script', 'bd_body', 'hd_styles', 'bd_script']
page_tooltips = [
 [
  'Help',
  '\nFiles in repository are viewable with syntax highlighting, annotation and\nchangesets.\n'],
 [
  'Repository-list',
  'Integrate one or more repositories with projects by providing its\n<em>type</em> (like svn ...) and <em>root-url</em>. Make sure that\n<em>root-url</em> points to the same machine, or to a machine on the local network.\n<br/>\nRepositories integrated with this project are listed in grid-style. Edit them\ninline.\n'],
 [
  'Browsing',
  '\nBrowsing the repository is provided in explorer style. By default the latest\nversion of the repository is shown in the explorer widget. To explore a different\nrevision use <b>< revno</b> and <b>revno ></b> links.\n'],
 [
  'Revisions',
  'Details about each repository revision listed in reverse chronological order.\n']]
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
        __M_writer('\n\n')
        __M_writer('\n')
        __M_writer('\n')
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
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showfilerev(context, log):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n')
        logdet = log[3].strftime('%b %d, %Y,')
        __M_writer('\n<pre class="pb5" style="border-bottom: 1px dotted #f2f2f2;" title="')
        __M_writer(escape(log[0]))
        __M_writer('">\n<a href="')
        __M_writer(escape(log[4]))
        __M_writer('">')
        __M_writer(escape(log[1]))
        __M_writer('</a> ')
        __M_writer('<span class="fggray">')
        __M_writer(escape(logdet))
        __M_writer('</span> ')
        __M_writer('<span class="fggreen">')
        __M_writer(escape(log[2]))
        __M_writer('</span>\n</pre>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showfile(context, lines):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        set = context.get('set', UNDEFINED)
        zip = context.get('zip', UNDEFINED)
        int = context.get('int', UNDEFINED)
        h = context.get('h', UNDEFINED)
        float = context.get('float', UNDEFINED)

        def showfilerev(log):
            return render_showfilerev(context, log)

        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        bgcolor = [
         '#FFFFFF', '#F2F2F2']
        fileauthors = set([ l[3] for l in lines ])
        rf_date = c.vrep.finfo['l_date']
        rl_date = c.vrep.linfo['l_date']
        rep_lifespan = rf_date and rl_date and (rl_date - rf_date).days or 0
        f_date = c.filelogs and c.filelogs[(-1)][3] or ''
        l_date = c.filelogs and c.filelogs[0][3] or ''
        updt_days = f_date and l_date and (l_date - f_date).days or 0
        before_days = rf_date and f_date and (f_date - rf_date).days or 0
        after_days = l_date and rl_date and (rl_date - l_date).days or 0
        w_before = int(before_days / float(rep_lifespan) * 100)
        w_update = int(updt_days / float(rep_lifespan) * 100)
        w_after = int(after_days / float(rep_lifespan) * 100)
        lifespan_title = ''
        if f_date and l_date:
            lifespan_title = f_date.strftime('%a, %b %d %Y') + ' TO ' + l_date.strftime('%a, %b %d %Y')
        repospath = c.fileinfo.get('repos_path', '')
        filepath = repospath.replace('/', ' /')
        __M_writer('\n    <style type="text/css">\n        ')
        __M_writer(escape(HtmlFormatter().get_style_defs('.highlight')))
        __M_writer('\n')
        __M_writer('        .highlighttable td.linenos { padding : 3px }\n        .highlighttable td.code { padding : 3px }\n    </style>\n    <div class="m10">\n        <div class="ml10 posr floatr">\n            <div class="disptable w100" \n                 style="height: 1em; width: 200px; border: 1px dotted gray;">\n            <div class="disptrow w100">\n                <div class="disptcell" style="width: ')
        __M_writer(escape(w_before))
        __M_writer('%;"></div>\n                <div class="disptcell calign fggray bgred1" \n                     style="border-left: 1px solid red; width: ')
        __M_writer(escape(w_update))
        __M_writer('%"\n                     title="')
        __M_writer(escape(lifespan_title))
        __M_writer('">\n                    ')
        __M_writer(escape(updt_days))
        __M_writer('\n                </div>\n                <div class="disptcell bgyellow" style="width: ')
        __M_writer(escape(w_after))
        __M_writer('%;"></div>\n            </div>\n            </div>\n        </div>\n        <div class="posr floatr fggreen">LifeSpan : </div>\n        <a class="mr10 floatr" title="Create review entry for this file"\n           href="')
        __M_writer(escape(h.url_reviewvfile))
        __M_writer('">Review</a>\n        <div class="pb5" style="border-bottom : 1px solid gray">\n            <span class="fntbold">')
        __M_writer(escape(filepath))
        __M_writer(' </span>\n            <span class="fntbold fggray"> ( r')
        __M_writer(escape(c.vfile.revno))
        __M_writer(' ) </span>\n            <span class="ml10 fggreen">')
        __M_writer(escape(c.fileinfo.get('size', 0)))
        __M_writer(' </span>\n                  <span>bytes, <span>\n            <span class="ml10 fggreen">')
        __M_writer(escape(len(lines)))
        __M_writer(' </span><span>lines, <span>\n            <a class="ml10 fgIred" href="')
        __M_writer(h.url_filedownl)
        __M_writer('">download-file</a>\n        </div>\n        <div class="disptable w100">\n        <div class="disptrow w100">\n            <div name="filehistory" class="disptcell w25 pr5">\n\n                <div class="m5 br4" style="border : 1px dotted gray">\n                    <div class="fntbold p5 bggray1">Authors </div>\n')
        for a in fileauthors:
            __M_writer('                    <div class="p3 fggreen"> ')
            __M_writer(escape(a))
            __M_writer(' </div>\n')

        __M_writer('                </div>\n\n                <div class="m5 br4" style="border : 1px dotted gray">\n                    <div class="fntbold p5 bggray1">\n                        File-History\n                    </div>\n                    <div class="p3">\n')
        for log in c.filelogs:
            __M_writer('                        ')
            __M_writer(escape(showfilerev(log)))
            __M_writer('\n')

        __M_writer('                    </div>\n                </div>\n            </div>\n            <div name="filecont" class="disptcell ml20 w75">\n                ')
        import re
        cont = ('\n').join([ l[1] for l in lines ])
        conthtml = h.syntaxhl(cont, lexbyfile=repospath)
        htmllines = re.search('<pre>((.|[\\r\\n])*)</pre>', conthtml).groups()[0].splitlines()
        annotats = [ 'revision%s, %s, %s' % (l[2], l[3], l[4].strftime('%b-%d-%Y')) for l in lines
                   ]
        zipped = zip(htmllines, annotats)
        lineno = 1
        __M_writer('\n                <div class="highlight disptable">\n')
        for (l, title) in zipped:
            __M_writer('                    <div class="disptrow">\n                        <div class="pl5 pr5 ralign disptcell bgaliceblue"\n                             style="border-right: 1px solid gray;\n                                    border-bottom: 1px solid gray;">\n                            ')
            __M_writer(escape(lineno))
            __M_writer('</div>\n                        <div class="pl5 pr5 disptcell" title="')
            __M_writer(escape(title))
            __M_writer('">\n                            <pre>')
            __M_writer(l)
            __M_writer('</pre>\n                        </div>\n                    </div>\n                    ')
            lineno += 1
            __M_writer('\n')

        __M_writer('                </div>\n            </div>\n        </div>\n        </div>\n    </div>\n')
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


def render_showfileerror(context, error):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n    <h3 class="m10">')
        __M_writer(escape(error))
        __M_writer('</h3>\n')
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
        h = context.get('h', UNDEFINED)

        def showfile(lines):
            return render_showfile(context, lines)

        forms = _mako_get_namespace(context, 'forms')
        str = context.get('str', UNDEFINED)

        def showfileerror(error):
            return render_showfileerror(context, error)

        __M_writer = context.writer()
        __M_writer('\n    ')
        title = '<a class="fntbold ml10">%s</a>' % c.vcs.name
        sel_vcs = capture(forms.form_selectvcs, c.authuser, c.vcslist, c.vcs and c.vcs.name or '')
        sel_frev = capture(forms.form_selectfilerevision, c.authuser, c.sel_frevs, str(c.revno))
        vcsbrowse = '<a class="ml10" title="Browse latest version"                      href="%s">Browser</a>' % h.url_vcsbrowse
        revlist = '<a class="ml10" title="List of repository revisions"                      href="%s">Revisions</a>' % h.url_revlist
        if c.vcseditable:
            newvcs = '<span class="ml10 fwnormal fntsmall">' + '<a href="%s" title="Integrate a new repository">                       Integrate</a></span>' % h.url_vcscreate
        else:
            newvcs = ''
        tline = capture(elements.iconlink, h.url_vcstimeline, 'timeline', title='Timeline of vcs-integration')
        __M_writer('\n    ')
        __M_writer(escape(elements.mainnav()))
        __M_writer('\n    ')
        __M_writer(escape(elements.contextnav([title, sel_vcs, sel_frev, vcsbrowse, revlist,
         newvcs], rspans=[
         tline], tooltips=page_tooltips)))
        __M_writer('\n    <div id="bdy" class="w100">\n')
        if c.authusername == 'anonymous' or not c.userpanes:
            __M_writer('        <div class="fullpanel1">\n')
        else:
            __M_writer('        <div class="panel1">\n')
        __M_writer('            <div>\n')
        if c.fileerror:
            __M_writer('                    ')
            __M_writer(escape(showfileerror(c.fileerror)))
            __M_writer('\n')
        else:
            __M_writer('                    ')
            __M_writer(escape(showfile(c.filelines)))
            __M_writer('\n')
        __M_writer('            </div>\n        </div> \n')
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
        __M_writer('\n\n    <script type="text/javascript">\n        dojo.addOnLoad( function () {\n            /* Setup the vcs goto list */\n            select_goto( dojo.query( \'#selectvcs\' )[0] );\n            /* Setup the file revision goto list */\n            select_goto( dojo.query( \'#selectfrev\' )[0] );\n\n        });\n        dojo.addOnLoad( setup_userpanes );\n        dojo.addOnLoad( adjust_upheight );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()