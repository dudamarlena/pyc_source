# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/component/charts.html.py
# Compiled at: 2010-07-12 03:18:17
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278919097.579029
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/component/charts.html'
_template_uri = '/component/charts.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['chart21', 'chart20', 'chart23', 'chart22', 'chart25', 'chart24', 'chart27', 'chart26', 'chart18', 'chart19', 'chart14', 'chart15', 'chart16', 'chart17', 'chart10', 'chart11', 'chart12', 'chart13', 'chart8', 'chart9', 'chart6', 'chart7', 'chart4', 'chart5', 'chart2', 'chart3', 'chart1', 'selectcharts']
sel_charts = {'chart1': 'tagged-resource-pie', 
   'chart2': 'uploaders', 
   'chart3': 'files-downloaded', 
   'chart4': 'tagged-files', 
   'chart5': 'uploaded-timeline', 
   'chart6': 'license-projects', 
   'chart7': 'tagged-license', 
   'chart8': 'user activity', 
   'chart9': 'user-site-permissions', 
   'chart10': 'project-administrators', 
   'chart11': 'component-owners', 
   'chart12': 'project-activities', 
   'chart13': 'milestone-tickets', 
   'chart14': 'project-activity', 
   'chart15': 'roadmap', 
   'chart16': 'wiki-edits', 
   'chart17': 'wiki-votes', 
   'chart18': 'wiki-authors', 
   'chart19': 'wiki-commenters', 
   'chart20': 'wiki-tags', 
   'chart21': 'project-tickets', 
   'chart22': 'ticket-owners', 
   'chart23': 'ticket-components', 
   'chart24': 'ticket-milestones', 
   'chart25': 'ticket-versions', 
   'chart26': 'ticket-commenters', 
   'chart27': 'reviewers'}

def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]


def _mako_generate_namespaces(context):
    ns = runtime.Namespace('forms', context._clean_inheritance_tokens(), templateuri='/component/forms.html', callables=None, calling_uri=_template_uri, module=None)
    context.namespaces[(__name__, 'forms')] = ns
    return


def render_body(context, **pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer('\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n')
        __M_writer('\n\n')
        __M_writer('\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n')
        __M_writer('\n\n')
        __M_writer('\n\n\n')
        __M_writer('\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n')
        __M_writer('\n\n')
        __M_writer('\n')
        __M_writer('\n\n')
        __M_writer('\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_chart21(context, chart21_data):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <div name="chart21" class="dispnone ml10 mt10 mr10 bgwhite">\n        <div id="chart21" class="chart" style="width: 100%; height: 600px;">\n        </div>\n    </div>\n\n    <script type="text/javascript">\n    function setup_chart21() {\n        var chart21_data  = ')
        __M_writer(h.json.dumps(chart21_data))
        __M_writer("\n        zcharts['chart21'] = {\n            init: dojo.partial( chart21_projtickets, chart21_data, 'chart21' ),\n            cntnr: dojo.query( '[name=chart21]' )[0]\n        }\n    }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_chart20(context, chart20_data, tagnames):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        tag = context.get('tag', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        chartwidth = h.computechartwidth(len(chart20_data), 50, 100)
        __M_writer('\n    <div name="chart20" class="dispnone ml10 mt10 mr10 bgwhite">\n        <div class="floatl" style="width: 75%; overflow: auto;">\n            <div id="chart20" class="chart" style="width: ')
        __M_writer(escape(chartwidth))
        __M_writer('%; height: 600px;">\n            </div>\n        </div>\n        <div class="vtop p10 floatl" style="width: 22%;">\n            <div class="br5 p5 ml20" style="border: 2px solid LightSteelBlue">\n                <div class="fntbold">Tagnames : </div>\n                ')
        __M_writer((', ').join([ '<a href="%s">%s</a>' % (h.url_fortag(tag), tag) for tag in tagnames
                               ]))
        __M_writer('\n            </div>\n        </div>\n    </div>\n\n    <script type="text/javascript">\n    function setup_chart20() {\n        var chart20_data  = ')
        __M_writer(h.json.dumps(chart20_data))
        __M_writer("\n        zcharts['chart20'] = {\n            init: dojo.partial( chart20_wiki_vs_tags, chart20_data, 'chart20' ),\n            cntnr: dojo.query( '[name=chart20]' )[0]\n        }\n    }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_chart23(context, chart23_data):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        chartheight = 320 * len(chart23_data) + 100
        __M_writer('\n    <div name="chart23" class="dispnone ml10 mt10 mr10 bgwhite">\n        <div id="chart23" class="chart" style="width: 100%; height: ')
        __M_writer(escape(chartheight))
        __M_writer('px;">\n        </div>\n    </div>\n\n    <script type="text/javascript">\n    function setup_chart23() {\n        var chart23_data  = ')
        __M_writer(h.json.dumps(chart23_data))
        __M_writer("\n        zcharts['chart23'] = {\n            init: dojo.partial( chart23_ticketcomponents, chart23_data, 'chart23' ),\n            cntnr: dojo.query( '[name=chart23]' )[0]\n\n        }\n    }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_chart22(context, chart22_data, users):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        chartheight = 320 * len(users) + 100
        __M_writer('\n    <div name="chart22" class="dispnone ml10 mt10 mr10 bgwhite">\n        <div class="floatl" style="width: 75%; overflow: auto;">\n            <div id="chart22" class="chart" style="width: 100%; height: ')
        __M_writer(escape(chartheight))
        __M_writer('px;">\n            </div>\n        </div>\n        <div class="floatl p10 w20">\n            <div class="p5 ml20 br5" style="border: 2px solid LightSteelBlue">\n')
        for u in users:
            __M_writer('                <div><a href="')
            __M_writer(escape(u[1]))
            __M_writer('">')
            __M_writer(escape(u[0]))
            __M_writer('</a></div>\n')

        __M_writer('            </div>\n        </div>\n    </div>\n\n    <script type="text/javascript">\n    function setup_chart22() {\n        var chart22_data  = ')
        __M_writer(h.json.dumps(chart22_data))
        __M_writer("\n        zcharts['chart22'] = {\n            init: dojo.partial( chart22_ticketowners, chart22_data, 'chart22' ),\n            cntnr: dojo.query( '[name=chart22]' )[0]\n\n        }\n    }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_chart25(context, chart25_data):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        chartheight = 320 * len(chart25_data) + 100
        __M_writer('\n    <div name="chart25" class="dispnone ml10 mt10 mr10 bgwhite">\n        <div id="chart25" class="chart" style="width: 100%; height: ')
        __M_writer(escape(chartheight))
        __M_writer('px;">\n        </div>\n    </div>\n\n    <script type="text/javascript">\n    function setup_chart25() {\n        var chart25_data  = ')
        __M_writer(h.json.dumps(chart25_data))
        __M_writer("\n        zcharts['chart25'] = {\n            init: dojo.partial( chart25_ticketversions, chart25_data, 'chart25' ),\n            cntnr: dojo.query( '[name=chart25]' )[0]\n\n        }\n    }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_chart24(context, chart24_data):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        chartheight = 320 * len(chart24_data) + 100
        __M_writer('\n    <div name="chart24" class="dispnone ml10 mt10 mr10 bgwhite">\n        <div id="chart24" class="chart" style="width: 100%; height: ')
        __M_writer(escape(chartheight))
        __M_writer('px;">\n        </div>\n    </div>\n\n    <script type="text/javascript">\n    function setup_chart24() {\n        var chart24_data  = ')
        __M_writer(h.json.dumps(chart24_data))
        __M_writer("\n        zcharts['chart24'] = {\n            init: dojo.partial( chart24_ticketmilestones, chart24_data, 'chart24' ),\n            cntnr: dojo.query( '[name=chart24]' )[0]\n\n        }\n    }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_chart27(context, chart27_data, users):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <div name="chart27" class="dispnone ml10 mt10 mr10 bgwhite">\n        <div class="floatl" style="width: 75%; overflow: auto;">\n            <div id="chart27" class="chart" style="width: 100%; height: 400px;">\n            </div>\n        </div>\n        <div class="floatl p10 w20">\n            <div class="p5 ml20 br5" style="border: 2px solid LightSteelBlue">\n')
        for u in users:
            __M_writer('                <div><a href="')
            __M_writer(escape(u[1]))
            __M_writer('">')
            __M_writer(escape(u[0]))
            __M_writer('</a></div>\n')

        __M_writer('            </div>\n        </div>\n    </div>\n\n    <script type="text/javascript">\n    function setup_chart27() {\n        var chart27_data  = ')
        __M_writer(h.json.dumps(chart27_data))
        __M_writer("\n        zcharts['chart27'] = {\n            init: dojo.partial( chart27_reviewusers, chart27_data, 'chart27' ),\n            cntnr: dojo.query( '[name=chart27]' )[0]\n\n        }\n    }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_chart26(context, chart26_data, users):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <div name="chart26" class="dispnone ml10 mt10 mr10 bgwhite">\n        <div class="floatl" style="width: 75%; overflow: auto;">\n            <div id="chart27" class="chart" style="width: 100%; height: 600px;">\n            </div>\n        </div>\n        <div class="floatl p10 w20">\n            <div class="p5 ml20 br5" style="border: 2px solid LightSteelBlue">\n')
        for u in users:
            __M_writer('                <div><a href="')
            __M_writer(escape(u[1]))
            __M_writer('">')
            __M_writer(escape(u[0]))
            __M_writer('</a></div>\n')

        __M_writer('            </div>\n        </div>\n    </div>\n\n    <script type="text/javascript">\n    function setup_chart26() {\n        var chart26_data  = ')
        __M_writer(h.json.dumps(chart26_data))
        __M_writer("\n        zcharts['chart26'] = {\n            init: dojo.partial( chart26_ticketcommentors, chart26_data, 'chart26' ),\n            cntnr: dojo.query( '[name=chart26]' )[0]\n\n        }\n    }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_chart18(context, chart18_data, users):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        chartwidth = h.computechartwidth(len(chart18_data), 50, 100)
        __M_writer('\n    <div name="chart18" class="dispnone ml10 mt10 mr10 bgwhite">\n        <div class="floatl" style="width: 75%; overflow: auto;">\n            <div id="chart18" class="chart" style="width: ')
        __M_writer(escape(chartwidth))
        __M_writer('%; height: 600px;">\n            </div>\n        </div>\n        <div class="floatl p10 w20">\n            <div class="p5 ml20 br5" style="border: 2px solid LightSteelBlue">\n')
        for u in users:
            __M_writer('                <div><a href="')
            __M_writer(escape(u[1]))
            __M_writer('">')
            __M_writer(escape(u[0]))
            __M_writer('</a></div>\n')

        __M_writer('            </div>\n        </div>\n    </div>\n\n    <script type="text/javascript">\n    function setup_chart18() {\n        var chart18_data  = ')
        __M_writer(h.json.dumps(chart18_data))
        __M_writer("\n        zcharts['chart18'] = {\n            init: dojo.partial( chart18_wikiauthors, chart18_data, 'chart18' ),\n            cntnr: dojo.query( '[name=chart18]' )[0]\n        }\n    }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_chart19(context, chart19_data, users):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        chartwidth = h.computechartwidth(len(chart19_data), 50, 100)
        __M_writer('\n    <div name="chart19" class="dispnone ml10 mt10 mr10 bgwhite">\n        <div class="floatl" style="width: 75%; overflow: auto;">\n            <div id="chart19" class="chart" style="width: ')
        __M_writer(escape(chartwidth))
        __M_writer('%; height: 600px;">\n            </div>\n        </div>\n        <div class="floatl p10 w20">\n            <div class="p5 ml20 br5" style="border: 2px solid LightSteelBlue">\n')
        for u in users:
            __M_writer('                <div><a href="')
            __M_writer(escape(u[1]))
            __M_writer('">')
            __M_writer(escape(u[0]))
            __M_writer('</a></div>\n')

        __M_writer('            </div>\n        </div>\n    </div>\n\n    <script type="text/javascript">\n    function setup_chart19() {\n        var chart19_data  = ')
        __M_writer(h.json.dumps(chart19_data))
        __M_writer("\n        zcharts['chart19'] = {\n            init: dojo.partial( chart19_wikicommentors, chart19_data, 'chart19' ),\n            cntnr: dojo.query( '[name=chart19]' )[0]\n\n        }\n    }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_chart14(context, chart14_data):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <div name="chart14" class="dispnone ml10 mt10 mr10 bgwhite">\n        <div id="chart14" class="chart" style="width: 100%; height: 400px;">\n        </div>\n    </div>\n\n    <script type="text/javascript">\n    function setup_chart14() {\n        var chart14_data  = ')
        __M_writer(h.json.dumps(chart14_data))
        __M_writer("\n        zcharts['chart14'] = {\n            init: dojo.partial( chart14_project_activity, chart14_data, 'chart14' ),\n            cntnr: dojo.query( '[name=chart14]' )[0]\n        }\n    }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_chart15(context, chart15_data, startdt):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        chart_height = len(chart15_data) * 50 + 50
        chart_height = 400 if chart_height < 400 else chart_height
        __M_writer('\n    <div name="chart15" class="dispnone ml10 mt10 mr10 bgwhite">\n        <div id="chart15" class="chart" style="width: 100%; height: ')
        __M_writer(escape(chart_height))
        __M_writer('px;">\n        </div>\n    </div>\n\n\n    <script type="text/javascript">\n    function setup_chart15() {\n        var chart15_data  = ')
        __M_writer(h.json.dumps(chart15_data))
        __M_writer("\n        zcharts['chart15'] = {\n            init: dojo.partial( chart15_roadmap, Date.UTC( ")
        __M_writer(escape((',').join(startdt)))
        __M_writer(" ),\n                                chart15_data, 'chart15' ),\n            cntnr: dojo.query( '[name=chart15]' )[0]\n        }\n    }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_chart16(context, chart16_data, wikis):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        chartwidth = h.computechartwidth(len(chart16_data), 40, 100)
        __M_writer('\n    <div name="chart16" class="dispnone ml10 mt10 mr10 bgwhite">\n        <div class="floatl" style="width: 75%; overflow: auto;">\n            <div id="chart16" class="chart" style="width: ')
        __M_writer(escape(chartwidth))
        __M_writer('%; height: 600px;">\n            </div>\n        </div>\n        <div class="floatl p10 w20">\n            <div class="p5 ml20 br5" style="border: 2px solid LightSteelBlue">\n')
        for w in wikis:
            __M_writer('                <div><a href="')
            __M_writer(escape(w[0]))
            __M_writer('">')
            __M_writer(escape(w[1]))
            __M_writer('</a></div>\n')

        __M_writer('            </div>\n        </div>\n    </div>\n\n    <script type="text/javascript">\n    function setup_chart16() {\n        var chart16_data = ')
        __M_writer(h.json.dumps(chart16_data))
        __M_writer("\n        zcharts['chart16'] = {\n            init: dojo.partial( chart16_wiki_cmtsvers, chart16_data, 'chart16'),\n            cntnr: dojo.query( '[name=chart16]' )[0]\n        }\n    }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_chart17(context, chart17_data):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <div name="chart17" class="dispnone ml10 mr10 mt10 bgwhite">\n        <div id="chart17" class="chart" style="width: 100%; height: 600px;">\n        </div>\n    </div>\n\n    <script type="text/javascript">\n    function setup_chart17() {\n        var chart17_data  = ')
        __M_writer(h.json.dumps(chart17_data))
        __M_writer("\n        zcharts['chart17'] = {\n            init: dojo.partial( chart17_wikivotes, chart17_data, 'chart17' ),\n            cntnr: dojo.query( '[name=chart17]' )[0]\n        }\n    }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_chart10(context, chart10_data):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <div name="chart10" class="dispnone ml10 mt10 mr10 bgwhite">\n        <div id="chart10" class="chart" style="width: 100%; height: 400px;">\n        </div>\n    </div>\n\n    <script type="text/javascript">\n    function setup_chart10() {\n        var chart10_data  = ')
        __M_writer(h.json.dumps(chart10_data))
        __M_writer("\n        zcharts['chart10'] = {\n            init: dojo.partial( chart10_project_admins, chart10_data, 'chart10' ),\n            cntnr: dojo.query( '[name=chart10]' )[0]\n        }\n    }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_chart11(context, chart11_data, components_no):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <div name="chart11" class="dispnone ml10 mt10 mr10 bgwhite">\n        <div id="chart11" class="chart" style="width: 100%; height: 400px;">\n        </div>\n    </div>\n\n    <script type="text/javascript">\n    function setup_chart11() {\n        var chart11_data  = ')
        __M_writer(h.json.dumps(chart11_data))
        __M_writer("\n        zcharts['chart11'] = {\n            init: dojo.partial( chart11_component_owners, ")
        __M_writer(escape(components_no))
        __M_writer(",\n                                chart11_data, 'chart11' ),\n            cntnr: dojo.query( '[name=chart11]' )[0]\n        }\n    }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_chart12(context, chart12_data):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <div name="chart12" class="dispnone ml10 mt10 mr10 bgwhite">\n        <div id="chart12" class="chart" style="width: 100%; height: 400px;">\n        </div>\n    </div>\n\n    <script type="text/javascript">\n    function setup_chart12() {\n        var chart12_data  = ')
        __M_writer(h.json.dumps(chart12_data))
        __M_writer("\n        zcharts['chart12'] = {\n            init: dojo.partial( chart12_userproject_activity,\n                                chart12_data, 'chart12' ),\n            cntnr: dojo.query( '[name=chart12]' )[0]\n        }\n    }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_chart13(context, id, reslved, unreslved):
    context.caller_stack._push_frame()
    try:
        int = context.get('int', UNDEFINED)
        float = context.get('float', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        total = reslved + unreslved
        res_width = total and int(reslved / float(total) * 60)
        unres_width = total and int(unreslved / float(total) * 60)
        __M_writer('\n')
        if total:
            __M_writer('        <div class="m10 br2" style="width: 90%; height: 1.2em;">\n            <div class="compbar posr floatl brtl4 brbl4"\n                 style="background-color: #9cdfb9; width: ')
            __M_writer(escape(res_width))
            __M_writer('%; height: 1.2em;\n                        border-left: 2px solid #b2ffd4; border-top: 2px solid #b2ffd4;\n                        border-bottom: 2px solid #83bc9c;">\n                <div class="tooltip dispnone posa br4 p3 bggray1"\n                     style="left: 20%; bottom: -50%; width: 7em; height: 1.2em; border: 2px solid green;\n                            opacity: 0.4; filter:alpha(opacity=40); z-index: 99">\n                    <span><b>resolved, ')
            __M_writer(escape(reslved))
            __M_writer('</b></span>\n                </div>\n            </div>\n            <div class="compbar posr floatl brtr4 brbr4"\n                 style="background-color: #df9c9c; width: ')
            __M_writer(escape(unres_width))
            __M_writer('%; height: 1.2em;\n                        border-right: 2px solid #ae7a7a; border-top: 2px solid #ffc9c9;\n                        border-bottom: 2px solid #ae7a7a;">\n                <div class="tooltip dispnone posa br4 p3 bggray1"\n                    style="left: 20%; bottom: -50%; width: 8em; height: 1.2em; border: 2px solid red;\n                           opacity: 0.4; filter:alpha(opacity=40); z-index: 99">\n                   <span><b>unresolved, ')
            __M_writer(escape(unreslved))
            __M_writer('</b></span>\n                </div>\n            </div>\n            <span class="pl10 vmiddle disptcell fntbold" style="height: 1.2em;">\n                ')
            __M_writer(escape(int(reslved / float(total) * 100)))
            __M_writer(' % complete\n            </span>\n        </div>\n')
        __M_writer('    <div name="chart13" class="ml10 mt10 mr10 bgwhite">\n        <div id="chart13_')
        __M_writer(escape(id))
        __M_writer('" class="chart" style="width: 900px; height: 210px;">\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_chart8(context, chart8_data):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        chartwidth = h.computechartwidth(len(chart8_data), 50, 100)
        __M_writer('\n    <div name="chart8" class="dispnone ml10 mt10 mr10 bgwhite"\n         style="width: 95%; overflow: auto;">\n        <div id="chart8" class="chart" style="width: ')
        __M_writer(escape(chartwidth))
        __M_writer('%; height: 400px;">\n        </div>\n    </div>\n\n    <script type="text/javascript">\n    function setup_chart8() {\n        var chart8_data  = ')
        __M_writer(h.json.dumps(chart8_data))
        __M_writer("\n        zcharts['chart8'] = {\n            init: dojo.partial( chart8_users_activity, chart8_data, 'chart8' ),\n            cntnr: dojo.query( '[name=chart8]' )[0]\n        }\n    }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_chart9(context, chart9_data):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        chartwidth = h.computechartwidth(len(chart9_data), 50, 95)
        __M_writer('\n    <div name="chart9" class="dispnone ml10 mt10 mr10 bgwhite"\n         style="width: 95%; overflow: auto;">\n         <div id="chart9" class="chart" style="width: ')
        __M_writer(escape(chartwidth))
        __M_writer('%; height: 400px;">\n        </div>\n    </div>\n\n    <script type="text/javascript">\n    function setup_chart9() {\n        var chart9_data  = ')
        __M_writer(h.json.dumps(chart9_data))
        __M_writer("\n        zcharts['chart9'] = {\n            init: dojo.partial( chart9_users_siteperm, chart9_data, 'chart9' ),\n            cntnr: dojo.query( '[name=chart9]' )[0]\n        }\n    }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_chart6(context, chart6_data):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        p = context.get('p', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <div name="chart6" class="dispnone ml10 mt10 mr10 bgwhite">\n        <div id="chart6" class="chart floatl" style="width: 65%; height: 400px;">\n        </div>\n        <div class="vtop p10 floatl" style="width: 32%;">\n            <div class="br5 p5 ml20" style="border: 2px solid LightSteelBlue">\n                <table class="w100">\n')
        for (lid, lic, projects) in chart6_data:
            __M_writer('                <tr>\n                    <td class="p3 ralign" style="border-right: 1px dotted gray;">\n                        <a href="')
            __M_writer(escape(h.url_forlicense(lid)))
            __M_writer('">')
            __M_writer(escape(lic))
            __M_writer('</a>\n                    </td>\n                    <td class="p3">\n                        ')
            __M_writer((', ').join([ '<a href="%s">%s</a>' % (h.url_forproject(p), p) for p in projects
                                   ]))
            __M_writer('\n                    </td>\n               </tr>\n')

        __M_writer('                </table>\n            </div>\n        </div>\n    </div>\n\n    <script type="text/javascript">\n    function setup_chart6() {\n        var chart6_data  = ')
        __M_writer(h.json.dumps(chart6_data))
        __M_writer("\n        zcharts['chart6'] = {\n            init: dojo.partial( chart6_license_projects, chart6_data, 'chart6'),\n            cntnr: dojo.query( '[name=chart6]' )[0]\n\n        }\n    }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_chart7(context, chart7_data, tagnames):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        tag = context.get('tag', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <div name="chart7" class="dispnone ml10 mt10 mr10 bgwhite">\n            <div id="chart7" class="chart floatl" style="width: 80%; height: 400px;">\n            </div>\n            <div class="vtop p10 floatl" style="width: 17%">\n                <div class="br5 p5 ml20" style="border: 2px solid LightSteelBlue">\n                    <div class="fntbold">Tagnames : </div>\n                    ')
        __M_writer((', ').join([ '<a href="%s">%s</a>' % (h.url_fortag(tag), tag) for tag in tagnames
                               ]))
        __M_writer('\n                </div>\n            </div>\n    </div>\n\n    <script type="text/javascript">\n    function setup_chart7() {\n        var chart7_data  = ')
        __M_writer(h.json.dumps(chart7_data))
        __M_writer("\n        zcharts['chart7'] = {\n            init: dojo.partial( chart7_license_vs_tags, chart7_data, 'chart7' ),\n            cntnr: dojo.query( '[name=chart7]' )[0]\n        }\n    }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_chart4(context, chart4_data, tagnames):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        tag = context.get('tag', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        chartwidth = h.computechartwidth(len(chart4_data), 50, 100)
        __M_writer('\n    <div name="chart4" class="dispnone ml10 mt10 mr10 bgwhite">\n        <div class="floatl" style="width: 75%; overflow: auto;">\n            <div id="chart4" class="chart" style="width: ')
        __M_writer(escape(chartwidth))
        __M_writer('%; height: 400px;">\n            </div>\n        </div>\n        <div class="vtop p10 floatl" style="width: 22%;">\n            <div class="br5 p5 ml20" style="border: 2px solid LightSteelBlue">\n                <div class="fntbold">Tagnames : </div>\n                ')
        __M_writer((', ').join([ '<a href="%s">%s</a>' % (h.url_fortag(tag), tag) for tag in tagnames
                               ]))
        __M_writer('\n            </div>\n        </div>\n    </div>\n\n    <script type="text/javascript">\n    function setup_chart4() {\n        var chart4_data  = ')
        __M_writer(h.json.dumps(chart4_data))
        __M_writer("\n        zcharts['chart4'] = {\n            init: dojo.partial( chart4_attach_vs_tags, chart4_data, 'chart4' ),\n            cntnr: dojo.query( '[name=chart4]' )[0]\n        }\n    }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_chart5(context, chart5_data, startdt):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <div name="chart5" class="dispnone ml10 mt10 mr10 bgwhite">\n        <div class="disptable w100">\n        <div class="disptrow w100">\n            <div id="chart5" class="chart disptcell" style="width: 800px; height: 400px;">\n            </div>\n        </div>\n        </div>\n    </div>\n\n    <script type="text/javascript">\n    function setup_chart5() {\n        var chart5_data  = ')
        __M_writer(h.json.dumps(chart5_data))
        __M_writer("\n        zcharts['chart5'] = {\n            init: dojo.partial( chart5_attach_vs_time, Date.UTC( ")
        __M_writer(escape((',').join(startdt)))
        __M_writer(" ),\n                                chart5_data, 'chart5' ),\n            cntnr: dojo.query( '[name=chart5]' )[0]\n\n        }\n    }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_chart2(context, chart2_data, payload, fcount):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        len = context.get('len', UNDEFINED)
        sorted = context.get('sorted', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        topupld = sorted(chart2_data, key=lambda x: x[1], reverse=True)
        toppyld = sorted(chart2_data, key=lambda x: x[2], reverse=True)
        chartwidth = h.computechartwidth(len(chart2_data), 50, 100)
        __M_writer('\n    <div name="chart2" class="dispnone ml10 mt10 mr10 bgwhite">\n        <div class="floatl" style="width: 75%; overflow: auto;">\n            <div class="bgblue1 p5 br5 calign" style="margin-left: 20%; margin-right: 20%">\n                Number of files uploaded by registered users, and its payload\n            </div>\n            <div id="chart2" class="chart" style="width: ')
        __M_writer(escape(chartwidth))
        __M_writer('%; height: 400px;">\n            </div>\n        </div>\n        <div class="floatl p10 w20">\n            <div class="p5 ml20 fntbold fgcrimson">\n                Around \n                <span class="fgblack">')
        __M_writer(escape(payload / 1048576))
        __M_writer(' MB</span>\n                in\n                <span class="fgblack">')
        __M_writer(escape(fcount))
        __M_writer(' </span> files\n            </div>\n            <div class="p5 ml20 br5" style="border: 2px solid LightSteelBlue">\n                <div class="fntbold">Top uploaders, by files </div>\n                <table>\n')
        for x in topupld[:10]:
            __M_writer('                    <tr>\n                        <td class="fggray ralign p3">\n                            <a href="')
            __M_writer(escape(h.url_foruser(x[0])))
            __M_writer('">')
            __M_writer(escape(x[0]))
            __M_writer('</a>\n                        </td>\n                        <td class="fggray p3"> ')
            __M_writer(escape(x[1]))
            __M_writer(' files</td>\n                    </tr>\n')

        __M_writer('                </table>\n            </div>\n            <div class="br5 p5 mt10 ml20"\n                 style="border: 2px solid LightSteelBlue">\n                <div class="fntbold">Top uploaders, by payload </div>\n                <table>\n')
        for x in toppyld[:10]:
            __M_writer('                    <tr>\n                        <td class="fggray ralign p3">\n                            <a href="')
            __M_writer(escape(h.url_foruser(x[0])))
            __M_writer('">')
            __M_writer(escape(x[0]))
            __M_writer('</a>\n                         </td>\n                        <td class="fggray p3"> ')
            __M_writer(escape(x[2]))
            __M_writer(' b</td>\n                    </tr>\n')

        __M_writer('                </table>\n            </div>\n        </div>\n    </div>\n\n    <script type="text/javascript">\n    function setup_chart2() {\n        var chart2_data = ')
        __M_writer(h.json.dumps(chart2_data))
        __M_writer("\n        zcharts['chart2'] = {\n            init: dojo.partial( chart2_user_vs_attach, chart2_data, 'chart2'),\n            cntnr: dojo.query( '[name=chart2]' )[0]\n        }\n    }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_chart3(context, chart3_data):
    context.caller_stack._push_frame()
    try:
        sorted = context.get('sorted', UNDEFINED)
        h = context.get('h', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        topdwnd = sorted(chart3_data, key=lambda x: x[2], reverse=True)
        __M_writer('\n    <div name="chart3" class="dispnone ml10 mr10 mt10 bgwhite">\n        <div id="chart3" class="chart floatl" style="width: 75%; height: 400px;">\n        </div>\n        <div class="vtop p10 floatl" style="width: 22%">\n            <div class="br5 p5 ml20" style="border: 2px solid LightSteelBlue">\n                <div class="fntbold">Top downloads : </div>\n')
        for x in topdwnd[:10]:
            __M_writer('                    <div class="p3">\n                        <span class="fggray">')
            __M_writer(escape(x[1]))
            __M_writer(', </span>\n                        <span class="fgblue">')
            __M_writer(escape(x[2]))
            __M_writer('</span>\n                    </div>\n')

        __M_writer('            </div>\n        </div>\n    </div>\n\n    <script type="text/javascript">\n    function setup_chart3() {\n        var chart3_data  = ')
        __M_writer(h.json.dumps(chart3_data))
        __M_writer("\n        zcharts['chart3'] = {\n            init: dojo.partial( chart3_attach_vs_download, chart3_data, 'chart3' ),\n            cntnr: dojo.query( '[name=chart3]' )[0]\n        }\n    }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_chart1(context, chart1_data, relatedtags):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <div class="floatr p5 bgwhite">\n        <div class="chartcntnr">\n            <div id="chart1" class="chart" style="width: 500px; height: 325px;">\n            </div>\n        </div>\n        <div class="br5 bgwhite p5 mt10"\n             style="width:490px; border: 2px solid LightSteelBlue">\n             <h4>Related tags :</h4>\n')
        for (tagname, weight) in relatedtags:
            __M_writer('                <span class="mr10 vmiddle" style="font-size : ')
            __M_writer(escape(70 + weight))
            __M_writer('%">\n                      <a href="')
            __M_writer(escape(h.url_fortag(tagname)))
            __M_writer('">')
            __M_writer(escape(tagname))
            __M_writer('</a>\n                </span>\n')

        __M_writer('        </div>\n    </div>\n\n    <script type="text/javascript">\n    function setup_chart1() {\n        var data = ')
        __M_writer(h.json.dumps(chart1_data))
        __M_writer("\n        chart1_tagchart( data, 'chart1' );\n    }\n    </script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_selectcharts(context, options, default):
    context.caller_stack._push_frame()
    try:
        forms = _mako_get_namespace(context, 'forms')
        __M_writer = context.writer()
        __M_writer('\n    ')
        options = [ [opt, sel_charts[opt]] for opt in options ]
        __M_writer('\n    <div class="ralign pb3 pr10" style="border-bottom: 1px solid gray">\n        <span class="fgcrimson fntbold">Select chart : </span>\n        ')
        __M_writer(escape(forms.select(id='selchart', options=options, opt_selected=default)))
        __M_writer('\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()