# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/search/searchpage.html.py
# Compiled at: 2010-07-12 02:04:10
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278914650.89545
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/search/searchpage.html'
_template_uri = '/derived/search/searchpage.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['searchitem', 'searchitems', 'hd_script', 'bd_script', 'bd_body']
page_tooltips = [
 [
  'Help',
  'Faceted search allows you to search for resources based its classification.\nUser <b>Filter By</b> checklist to select classification.\n']]

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
        __M_writer('\n\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n\n')
        __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_searchitem(context, match, terms):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <div class="mb5">\n        <a href="')
        __M_writer(escape(match['url']))
        __M_writer('">')
        __M_writer(escape(match['text']))
        __M_writer('</a>\n        <span class="fggreen fntbold fnt83">match : ')
        __M_writer(escape(match['percent']))
        __M_writer('%</span>\n    </div>\n    <div class="ml10 fnt95">')
        __M_writer(h.localizeterms(match['data'], terms))
        __M_writer('</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_searchitems(context, matches, terms):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)

        def searchitem(match, terms):
            return render_searchitem(context, match, terms)

        __M_writer = context.writer()
        __M_writer('\n    <div class="mb10">\n        <span class="fgcrimson">About ')
        __M_writer(escape(c.total))
        __M_writer(' matches</span>\n        <div class="posr floatr">\n            <a class="ml5" href="')
        __M_writer(escape(h.suburl_search))
        __M_writer('">&#171;</a>\n            <a class="ml5" href="')
        __M_writer(escape(h.suburl_searchprev))
        __M_writer('">&#8249; Prev</a>\n            <a class="ml5 mr10" href="')
        __M_writer(escape(h.suburl_searchnext))
        __M_writer('">Next &#8250;</a>\n        </div>\n    </div>\n')
        for m in matches:
            __M_writer('        <div class="mb20">\n            ')
            __M_writer(escape(searchitem(m, terms)))
            __M_writer('\n        </div>\n')

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
        __M_writer('\n\n    <script type="text/javascript">\n        dojo.addOnLoad( initform_searchadv );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bd_body(context):
    context.caller_stack._push_frame()
    try:
        forms = _mako_get_namespace(context, 'forms')
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')

        def searchitems(matches, terms):
            return render_searchitems(context, matches, terms)

        __M_writer = context.writer()
        __M_writer('\n    ')
        underproject = c.project and ', under project %s' % c.project or ''
        pagebartext = 'Search %s%s' % (c.sitename, underproject)
        __M_writer('\n    ')
        __M_writer(escape(elements.pagebar(pagebartext, tooltips=page_tooltips)))
        __M_writer('\n    <div id="bdy">\n    <div class="mt20 w100">\n        <div class="m10 bggray1 p5 br10">\n            ')
        __M_writer(escape(forms.form_search(c.querystring, c.authuser, h.suburl_search, c.allfaces, c.faces)))
        __M_writer('\n        </div>\n        <div class="m10">\n            ')
        __M_writer(escape(searchitems(c.matches, c.terms)))
        __M_writer('\n        </div>\n    </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()