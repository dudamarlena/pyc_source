# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/tag/tag.html.py
# Compiled at: 2010-07-12 03:18:28
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278919108.845135
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/tag/tag.html'
_template_uri = '/derived/tag/tag.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['showtag', 'hd_script', 'bd_script', 'bd_body']
page_tooltips = []

def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]


def _mako_generate_namespaces(context):
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
        __M_writer('\n\n')
        __M_writer('\n')
        __M_writer('\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showtag(context, tag):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        bb_style = 'border-bottom : 2px solid darkkhaki;'
        __M_writer('\n\n    <div id="tagdetail" class="ml20 mr20">\n    <h3>Items tagged as \n        <span class="fggray">')
        __M_writer(escape(tag.tagname))
        __M_writer('</span>\n    </h3>\n\n')
        if tag.attachments:
            __M_writer('    <h3 class="pl3 fgmpurple" style="')
            __M_writer(escape(bb_style))
            __M_writer('">Attachments</h3>\n    <div class="ml10">\n        ')
            cont = [ '<span class="ml5"> <a href="%s">%s(%s)</a></span>' % (h.url_forattach(a.id), a.filename, a.id) for a in tag.attachments
                   ]
            cont = (', ').join(cont)
            __M_writer('\n        ')
            __M_writer(cont)
            __M_writer('\n    </div>\n')
        __M_writer('\n')
        if tag.licenses:
            __M_writer('    <h3 class="pl3 fgmpurple" style="')
            __M_writer(escape(bb_style))
            __M_writer('">License</h3>\n    <div class="ml10">\n        ')
            cont = [ '<span class="ml5"> <a title="%s" href="%s">%s</a></span>' % (l.summary, h.url_forlicense(l.id), l.licensename) for l in tag.licenses
                   ]
            cont = (', ').join(cont)
            __M_writer('\n        ')
            __M_writer(cont)
            __M_writer('\n    </div>\n')
        __M_writer('\n')
        if tag.projects:
            __M_writer('    <h3 class="pl3 fgmpurple" style="')
            __M_writer(escape(bb_style))
            __M_writer('">Projects</h3>\n    <div class="ml10">\n        ')
            cont = [ '<span class="ml5"> <a title="%s" href="%s">%s</a></span>' % (p.summary, h.url_forproject(p.projectname), p.projectname) for p in tag.projects
                   ]
            cont = (', ').join(cont)
            __M_writer('\n        ')
            __M_writer(cont)
            __M_writer('\n    </div>\n')
        __M_writer('\n')
        if tag.tickets:
            __M_writer('    <h3 class="pl3 fgmpurple" style="')
            __M_writer(escape(bb_style))
            __M_writer('">Tickets</h3>\n    <div class="ml10">\n        ')
            cont = [ '<span class="ml5"> <a title="%s" href="%s">%s</a></span>' % (t.summary, h.url_forticket(t.project.projectname, t.id), t.id) for t in tag.tickets
                   ]
            cont = (', ').join(cont)
            __M_writer('\n        ')
            __M_writer(cont)
            __M_writer('\n    </div>\n')
        __M_writer('\n')
        if tag.reviews:
            __M_writer('    <h3 class="pl3 fgmpurple" style="')
            __M_writer(escape(bb_style))
            __M_writer('">Reviews</h3>\n    <div class="ml10">\n        ')
            cont = [ '<span class="ml5"> <a href="%s">%s</a></span>' % (h.url_forreview(r.project.projectname, r.id), r.id) for r in tag.reviews
                   ]
            cont = (', ').join(cont)
            __M_writer('\n        ')
            __M_writer(cont)
            __M_writer('\n    </div>\n')
        __M_writer('\n')
        if tag.wikipages:
            __M_writer('    <h3 class="pl3 fgmpurple" style="')
            __M_writer(escape(bb_style))
            __M_writer('">Wiki</h3>\n    <div class="ml10">\n        ')
            cont = [ '<span class="ml5"> <a href="%s">%s</a></span>' % (w.wikiurl, w.wikiurl) for w in tag.wikipages
                   ]
            cont = (', ').join(cont)
            __M_writer('\n        ')
            __M_writer(cont)
            __M_writer('\n    </div>\n')
        __M_writer('\n    </div>\n')
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
        __M_writer('\n\n    <script type="text/javascript">\n        dojo.addOnLoad( setup_chart1 );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bd_body(context):
    context.caller_stack._push_frame()
    try:
        capture = context.get('capture', UNDEFINED)
        c = context.get('c', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')

        def showtag(tag):
            return render_showtag(context, tag)

        h = context.get('h', UNDEFINED)
        charts = _mako_get_namespace(context, 'charts')
        __M_writer = context.writer()
        __M_writer('\n    ')
        pagebartext = 'Tag: %s' % c.tag.tagname
        tagcloud = '<div class="floatl mt4 ml10 fwnormal fntsmall">' + '<a href="%s">TagCloud</a></div>' % h.url_tagcloud
        tline = capture(elements.iconlink, h.url_tagtimeline, 'timeline', title='Timeline')
        pbar_spans = [
         tagcloud]
        rspans = [tline]
        __M_writer('\n    ')
        __M_writer(escape(elements.pagebar(pagebartext, spans=pbar_spans, rspans=rspans)))
        __M_writer('\n    <div id="bdy" class="w100">\n')
        if c.userpanes:
            __M_writer('    <div class="panel1">\n')
        else:
            __M_writer('    <div class="fullpanel1">\n')
        __M_writer('        ')
        __M_writer(escape(charts.chart1(c.chart1_data, c.chart1_rtags)))
        __M_writer('\n        ')
        __M_writer(escape(showtag(c.tag)))
        __M_writer('\n    </div>\n')
        if c.userpanes:
            __M_writer('    <div class="panel2">')
            __M_writer(escape(elements.user_panes(c.userpanes)))
            __M_writer('</div>\n')
        __M_writer('    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()