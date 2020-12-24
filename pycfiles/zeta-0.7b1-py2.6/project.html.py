# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/projects/project.html.py
# Compiled at: 2010-07-10 01:32:36
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278739956.113704
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/projects/project.html'
_template_uri = '/derived/projects/project.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['hd_script', 'bd_script', 'bd_body', 'show_homepage']
page_tooltips = [
 [
  'Help',
  "Home page can be constructed using wiki markup. To change home page\ncontent edit project's <b>'homepage'</b> wiki document.\n"],
 [
  'Roadmap',
  'Use the Roadmap page to view project\'s progress and achievements.\nMilestones are grouped into catagories <em>closed</em> and <em>opened</em>,\nand chronologically sorted.<br/>\n<b>Background color coding</b> : \n<span class="bgblue1">open milestones</span>\n<span class="bggrn2">closed milestones</span>\n<span class="bggray1">cancelled milestones</span>\n<br/><br/>\nMilestone-id is displayed along with the milestone name in paranthesis, use\nthis where ever the milestone needs to be referenced.\n<b>Report Card</b> gives a visual segmentation of milestone tickets in terms\nof \'ticket-types\', \'ticket-status\', \'ticket-severity\'.\n'],
 [
  'Mountpoints',
  "Repository directories can be mounted on-to site's url path, so that\ncontents of its directory, including its sub-directory can be viewed as html\npages"],
 [
  'Favorites',
  "Registered users can pick project(s) as their favorite, provided the user\nhas 'PROJECT_VIEW' permission"],
 [
  'Downloads',
  'Downloable files for this project.'],
 [
  'Attachments',
  'Add <b>summary</b> and <b>tags</b> to project attachments.'],
 [
  'Tags',
  'Tag a project by clicking on the iconized title. Delete\ntags by clicking on the cross-wire. Tag names should be 2 or more characters.\n'],
 [
  'Timeline',
  'Timeline for project, shows all updates done in the context of a project\nexcept project-administrative logs, which is available under admin/timeline.']]

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
        __M_writer('\n\n\n')
        __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_hd_script(context):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        str = context.get('str', UNDEFINED)
        parent = context.get('parent', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        __M_writer(escape(parent.hd_script()))
        __M_writer('\n\n    <script type="text/javascript">\n    ')
        project_id = c.project and c.project.id or ''
        __M_writer("\n    function setup_project() {\n\n        /* Tags */\n        new zeta.Tags(\n            { user: [ '")
        __M_writer(escape(str(c.authuser.id)))
        __M_writer("', '")
        __M_writer(escape(c.authuser.username))
        __M_writer("' ],\n              id: 'prjtagblk',\n              addform: [ 'addprjtags', '")
        __M_writer(h.suburl_addprjtags)
        __M_writer("' ],\n              delform: [ 'delprjtags', '")
        __M_writer(h.suburl_delprjtags)
        __M_writer("' ],\n              tagon: [ '")
        __M_writer(escape(str(project_id)))
        __M_writer("', 'project_id' ],\n              editable: ")
        __M_writer(escape([0, 1][(c.tag_editable == True)]))
        __M_writer(",\n              url: '")
        __M_writer(h.url_prjtags)
        __M_writer("',\n              tags: ")
        __M_writer(h.json.dumps(c.tags))
        __M_writer('\n            }, dojo.query( "div[name=ptagblk]" )[0]\n        )\n    }\n    </script>\n')
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
        __M_writer('\n\n    <script type="text/javascript">\n        dojo.addOnLoad( setup_project );\n        dojoaddOnLoad( \'initform_projfav\' );\n\n        dojo.addOnLoad( setup_userpanes );\n        dojo.addOnLoad( adjust_upheight );\n    </script>\n')
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

        def show_homepage():
            return render_show_homepage(context)

        __M_writer = context.writer()
        __M_writer('\n    ')
        fav = capture(elements.favoriteicon, 'favproj')
        searchbox = capture(forms.form_searchbox, c.authuser, 'searchproject', 'Search-project', h.suburl_search, c.searchfaces)
        attachs = '<span class="ml10 fwnormal fntsmall">' + '<a href="%s" title="Project attachmens">                     Attachments</a></span>' % h.url_projattachs
        downlds = '<span class="ml10 fwnormal fntsmall">' + '<a href="%s" title="Project downloads">                     Downloads</a></span>' % h.url_projdownloads
        roadmap = '<span class="ml10 fwnormal fntsmall">' + '<a href="%s" title="Past, current and future milestones">                    Roadmap</a></span>' % h.url_projroadmap
        mountpt = '<span class="ml10 fwnormal fntsmall">' + '<a href="%s" title="Mounted repository directories">                     Mountpoints</a></span>' % h.url_projmounts
        charts = capture(elements.iconlink, h.url_projectcharts, 'barchart', title='Project analytics')
        tline = capture(elements.iconlink, h.url_projtimeline, 'timeline', title='Project timeline')
        refr = capture(elements.iconlink, h.url_translatefp, 'refresh', classes='mr5', title='Bring this wiki-html upto-date')
        __M_writer('\n    ')
        __M_writer(escape(elements.mainnav()))
        __M_writer('\n    ')
        __M_writer(escape(elements.contextnav([fav, searchbox, roadmap, mountpt, attachs, downlds], rspans=[
         refr, charts, tline], tooltips=page_tooltips)))
        __M_writer('\n    <div id="bdy" class="w100">\n')
        if c.authusername == 'anonymous' or not c.userpanes:
            __M_writer('        <div class="fullpanel1">\n')
        else:
            __M_writer('        <div class="panel1">\n')
        if c.authorized:
            __M_writer('                ')
            __M_writer(escape(forms.form_projfav(c.authuser, c.project, h.suburl_projfav, c.isfavorite and 'delfavuser' or 'addfavuser')))
            __M_writer('\n')
        __M_writer('            <div>\n                ')
        __M_writer(escape(show_homepage()))
        __M_writer('            \n            </div>\n        </div>\n')
        if c.authusername != 'anonymous' and c.userpanes:
            __M_writer('        <div class="panel2">')
            __M_writer(escape(elements.user_panes(c.userpanes)))
            __M_writer('</div>\n')
        __M_writer('    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_show_homepage(context):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <div class="zhomepage mr10">\n        <div class="floatr" style="width: 250px;">\n            <div class="br4 ml10 fntbold p3" style="border : 1px dotted gray;">\n                ')
        __M_writer(escape(c.project.summary))
        __M_writer('\n            </div>\n            <div class="br4 ml10 mt5" style="border : 1px dotted gray;">\n                <div class="p3 fntbold bggray1">\n                    Project Details\n                </div>\n                <div class="p3">\n')
        if c.project.license:
            __M_writer('                    <div class="p3" title="project license"\n                         >')
            __M_writer(escape(c.project.license.licensename))
            __M_writer('</div>\n')
        __M_writer('\n')
        if c.project.admin_email:
            __M_writer('                    <div class="p3" title="project administrator">\n                        <div>\n                            <a href="')
            __M_writer(escape(h.url_foruser(c.project.admin.username)))
            __M_writer('"\n                                >')
            __M_writer(escape(c.project.admin.username))
            __M_writer('</a>\n                        </div>\n                        <div>')
            __M_writer(escape(c.project.admin_email))
            __M_writer('</div>\n                    </div>\n')
        __M_writer('\n')
        if c.project.mailinglists:
            __M_writer('                    <div class="p3" title="project mailinglist">\n')
            for m in c.project.mailinglists:
                __M_writer('                        <div>')
                __M_writer(escape(m.mailing_list))
                __M_writer('</div>\n')

            __M_writer('                    </div>\n')
        __M_writer('\n')
        if c.project.ircchannels:
            __M_writer('                    <div class="p3" title="project irc channels">\n')
            for r in c.project.ircchannels:
                __M_writer('                        <div>')
                __M_writer(escape(r.ircchannel))
                __M_writer('</div>\n')

            __M_writer('                    </div>\n')
        __M_writer('                </div>\n            </div>\n\n')
        for (team, users) in c.projectteams.iteritems():
            __M_writer('            <div class="br4 ml10 mt5" style="border : 1px dotted gray;">\n                <div class="p3 fntbold bggray1">')
            __M_writer(escape(team))
            __M_writer('</div>\n                <div class="p3"\n')
            for u in users:
                __M_writer('                    <a href="')
                __M_writer(escape(h.url_foruser(u)))
                __M_writer('">')
                __M_writer(escape(u))
                __M_writer('</a>,\n')

            __M_writer('                </div>\n            </div>\n')

        __M_writer('\n            <div class="">\n                <div name="ptagblk"></div>\n            </div>\n\n            <div class="ml10 fntbold bclear">\n                <a href="')
        __M_writer(escape(h.url_tagcloud))
        __M_writer('">Visit tag cloud ...</a>\n            </div>\n        </div>\n        <div class="pl10" style="margin-right: 250px;">\n')
        if c.fphtml:
            __M_writer('                ')
            __M_writer(c.fphtml)
            __M_writer('\n')
        __M_writer('        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()