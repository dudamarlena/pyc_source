# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/projects/projmilestone.html.py
# Compiled at: 2010-07-12 03:28:28
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278919708.813853
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/projects/projmilestone.html'
_template_uri = '/derived/projects/projmilestone.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['hd_script', 'bd_script', 'bd_body', 'milestone']
page_tooltips = [
 [
  'Help',
  'Learn about individual milestone and its analytics'],
 [
  'Project homepage',
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
    ns = runtime.Namespace('charts', context._clean_inheritance_tokens(), templateuri='/component/charts.html', callables=None, calling_uri=_template_uri, module=None)
    context.namespaces[(__name__, 'charts')] = ns
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
        parent = context.get('parent', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        __M_writer(escape(parent.hd_script()))
        __M_writer('\n\n    <script type="text/javascript">\n    var zcharts = {};\n    function setup_charts() {\n        var chart13_data  = ')
        __M_writer(h.json.dumps(c.chart13_data))
        __M_writer("\n        var idx = 'chart13_' + chart13_data[0]\n        zcharts[idx] = chart13_milestone_tickets( chart13_data, idx );\n\n        // Connect hover handler to show tooltip\n        dojo.query( '.compbar' ).forEach(\n            function( n ) {\n                var n_ttip = dojo.query( '.tooltip', n )[0]\n                dojo.connect(\n                    n, 'onmouseenter',\n                    dojo.partial(\n                        function(ntip, e) {\n                            dojo.toggleClass( ntip, 'dispnone', false );\n                        }, n_ttip\n                    )\n\n                );\n                dojo.connect(\n                    n, 'onmouseleave',\n                    dojo.partial(\n                        function( ntip, e) {\n                            dojo.toggleClass( ntip, 'dispnone', true );\n                        }, n_ttip\n                    )\n\n                );\n            }\n        );\n    }\n    </script>\n")
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
        __M_writer('\n\n    <script type="text/javascript">\n        dojo.addOnLoad( setup_charts );\n        dojoaddOnLoad( \'initform_projfav\' );\n        dojo.addOnLoad( setup_userpanes );\n        dojo.addOnLoad( adjust_upheight );\n    </script>\n')
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

        def milestone(m):
            return render_milestone(context, m)

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
        __M_writer('\n    ')
        __M_writer(escape(elements.mainnav()))
        __M_writer('\n    ')
        __M_writer(escape(elements.contextnav([fav, searchbox, roadmap, mountpt, attachs, downlds], rspans=[
         charts, tline], tooltips=page_tooltips)))
        __M_writer('\n    <div id="bdy" class="w100">\n')
        if c.authusername == 'anonymous' or not c.userpanes:
            __M_writer('        <div class="fullpanel1">\n')
        else:
            __M_writer('        <div class="panel1">\n')
        if c.authorized:
            __M_writer('                ')
            __M_writer(escape(forms.form_projfav(c.authuser, c.project, h.suburl_projfav, c.project in c.authuser.favoriteprojects and 'delfavuser' or 'addfavuser')))
            __M_writer('\n')
        __M_writer('            <div class="ml20">\n                ')
        __M_writer(escape(milestone(c.milestone)))
        __M_writer('\n            </div>\n        </div>\n')
        if c.authusername != 'anonymous' and c.userpanes:
            __M_writer('        <div class="panel2">')
            __M_writer(escape(elements.user_panes(c.userpanes)))
            __M_writer('</div>\n')
        __M_writer('    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_milestone(context, m):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        charts = _mako_get_namespace(context, 'charts')
        __M_writer = context.writer()
        __M_writer('\n    ')
        status = m.completed and 'Complete' or m.cancelled and 'Cancelled' or 'Open'
        __M_writer('\n    <h3>')
        __M_writer(escape(m.milestone_name))
        __M_writer(' (')
        __M_writer(escape(m.id))
        __M_writer(')</h3>\n    <div class="disptable">\n    <div class="disptrow">\n        <div class="disptcell p3 ralign fggray fntbold">Status :</div>\n        <div class="disptcell p3 fntbold">')
        __M_writer(escape(status))
        __M_writer('</div>\n    </div>\n    <div class="disptrow">\n        <div class="disptcell p3 ralign fggray fntbold">Created On :</div>\n        <div class="disptcell p3 fntbold">\n            ')
        __M_writer(escape(m.created_on and m.created_on.strftime('%a, %b %d, %Y')))
        __M_writer('\n        </div>\n    </div>\n    <div class="disptrow">\n        <div class="disptcell p3 ralign fggray fntbold">Due On :</div>\n        <div class="disptcell p3 fntbold">\n            ')
        __M_writer(escape(m.due_date and m.due_date.strftime('%a, %b %d, %Y')))
        __M_writer('\n        </div>\n    </div>\n    </div>\n    <h4>Description</h4>\n    <div class="ml10">')
        __M_writer(m.descriptionhtml)
        __M_writer('</div>\n')
        if m.closing_remarkhtml:
            __M_writer('        <h4>Closing Remark</h4>\n        <div class="ml10">')
            __M_writer(m.closing_remarkhtml)
            __M_writer('</div>\n')
        __M_writer('\n    <div class="ml50 bgwhite">\n        ')
        __M_writer(escape(charts.chart13(m.id, *c.mstnresolved)))
        __M_writer('\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()