# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/tag/tagcloud.html.py
# Compiled at: 2010-07-12 03:18:31
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278919111.061525
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/tag/tagcloud.html'
_template_uri = '/derived/tag/tagcloud.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['hd_script', 'bd_script', 'bd_body']
page_tooltips = [
 [
  'TagCloud',
  'List of all tags, font size corresponding the to number of tagged items']]

def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]


def _mako_generate_namespaces(context):
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
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
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


def render_bd_script(context):
    context.caller_stack._push_frame()
    try:
        parent = context.get('parent', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        __M_writer(escape(parent.bd_script()))
        __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bd_body(context):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')
        sorted = context.get('sorted', UNDEFINED)
        capture = context.get('capture', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        pagebartext = 'Tag Cloud'
        tline = capture(elements.iconlink, h.url_tagtimeline, 'timeline', title='Timeline')
        pbar_spans = ['&ensp;&ensp;&ensp;']
        rspans = [tline]
        __M_writer('\n    ')
        __M_writer(escape(elements.pagebar(pagebartext, spans=pbar_spans, rspans=rspans, tooltips=page_tooltips)))
        __M_writer('\n    <div id="bdy" class="w100">\n')
        if c.userpanes:
            __M_writer('    <div class="panel1">\n')
        else:
            __M_writer('    <div class="fullpanel1">\n')
        __M_writer('        <div id="tagcloud" class="ml20 mr20">\n            <h3>Special tags</h3>\n            <div class="ml10">\n')
        for tagname in c.specialtags:
            __M_writer('                ')
            weight = c.tagpercentile.pop(tagname)
            __M_writer('\n                <span class="mr10 vmiddle"\n                      style="font-size : ')
            __M_writer(escape(90 + weight[1]))
            __M_writer('%">\n                      <a href="')
            __M_writer(escape(h.url_fortag(tagname)))
            __M_writer('">')
            __M_writer(escape(tagname))
            __M_writer('</a>\n                </span>\n')

        __M_writer('            </div>\n            <h3>Normal tags</h3>\n            <div class="ml10">\n                ')
        tagnames = sorted(c.tagpercentile.keys())
        __M_writer('\n')
        for tagname in tagnames:
            __M_writer('                <span class="mr10 vmiddle"\n                      style="font-size : ')
            __M_writer(escape(90 + c.tagpercentile[tagname][1]))
            __M_writer('%">\n                      <a href="')
            __M_writer(escape(h.url_fortag(tagname)))
            __M_writer('">')
            __M_writer(escape(tagname))
            __M_writer('</a>\n                </span>\n')

        __M_writer('            </div>\n        </div>\n    </div>\n')
        if c.userpanes:
            __M_writer('    <div class="panel2">')
            __M_writer(escape(elements.user_panes(c.userpanes)))
            __M_writer('</div>\n')
        __M_writer('    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()