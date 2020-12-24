# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/license/license.html.py
# Compiled at: 2010-07-12 02:00:43
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278914443.451383
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/license/license.html'
_template_uri = '/derived/license/license.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['licprojects', 'hd_script', 'bd_body', 'licdetail', 'bd_script']
page_tooltips = [
 [
  'Help',
  'License can be associated with a project (via project\'s admin page).\nIn the page bar, along with the license name, (license-id) will be displayed\nin paranthesis. Use this \'id\' when referring to license via\n<a href="/help/zwiki/zetalink>zetalinks</a>\n'],
 [
  'Attachments',
  'Upload attachments by clicking on the iconized title. Clicking them\nonce again will hide it. Delete attachments by clicking on the cross-wire.\nUpload any number of attachment files.\n<br</br>\nEvery attached file, will have its "id" in paranthesis. Use the \'id\' when\nrefering to the attachment.\n'],
 [
  'Tags',
  'Tag license by clicking on the iconized title. Delete\ntags by clicking on the cross-wire. Tag names should be 2 or more characters.\n'],
 [
  'Timeline',
  'Timeline gives a log of all updates done to license.']]

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
        __M_writer('\n\n\n\n\n')
        __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_licprojects(context, projectnames):
    context.caller_stack._push_frame()
    try:
        p = context.get('p', UNDEFINED)
        href = context.get('href', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n<div class="br4 ml10 mt5" style="border : 1px dotted gray;">\n    <div class="p3 fntbold bggray1">\n        Projects\n    </div>\n    <div class="p3">\n')
        if projectnames:
            __M_writer('            ')
            __M_writer((', ').join([ '<a href="%s">%s</a>' % (href, p) for (p, href) in projectnames
                                   ]))
            __M_writer('\n')
        else:
            __M_writer('            <span>-</span>\n')
        __M_writer('    </div>\n</div>\n')
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
        __M_writer('\n\n    <script type="text/javascript">\n\n        ')
        license_id = c.license and c.license.id or ''
        __M_writer('\n\n        function setup_license() {\n            var div_view = dojo.query( "div[name=viewlic]" )[0];\n\n            // Setup the license goto list\n            select_goto( dojo.query( \'#viewlicense\' )[0] );\n            if( div_view ) {\n                var n1 = dojo.query( \'div[name=attachblk]\', div_view )[0];\n                var n2 = dojo.query( \'div[name=tagblk]\', div_view )[0];\n                // Attachments\n                new zeta.Attachments(\n                    { user: [ \'')
        __M_writer(escape(str(c.authuser.id)))
        __M_writer("', '")
        __M_writer(escape(c.authuser.username))
        __M_writer("' ],\n                      id: 'licattachblk',\n                      addform: [ 'addlicattachs', '")
        __M_writer(h.suburl_addlicattachs)
        __M_writer("' ],\n                      delform: [ 'dellicattachs', '")
        __M_writer(h.suburl_dellicattachs)
        __M_writer("' ],\n                      attachon: [ '")
        __M_writer(escape(str(license_id)))
        __M_writer("', 'license_id' ],\n                      editable: ")
        __M_writer(escape([0, 1][(c.att_editable == True)]))
        __M_writer(",\n                      url: '")
        __M_writer(h.url_licattachments)
        __M_writer("',\n                      attachs: ")
        __M_writer(h.json.dumps(c.attachs))
        __M_writer(',\n                      clsdisplayitem: "dispblk"\n                    }, n1\n                )\n                // Tags\n                new zeta.Tags(\n                    { user: [ \'')
        __M_writer(escape(str(c.authuser.id)))
        __M_writer("', '")
        __M_writer(escape(c.authuser.username))
        __M_writer("' ],\n                      id: 'lictagblk',\n                      addform: [ 'addlictags', '")
        __M_writer(h.suburl_addlictags)
        __M_writer("' ],\n                      delform: [ 'dellictags', '")
        __M_writer(h.suburl_dellictags)
        __M_writer("' ],\n                      tagon: [ '")
        __M_writer(escape(str(license_id)))
        __M_writer("', 'license_id' ],\n                      editable: ")
        __M_writer(escape([0, 1][(c.tag_editable == True)]))
        __M_writer(",\n                      url: '")
        __M_writer(h.url_lictags)
        __M_writer("',\n                      tags: ")
        __M_writer(h.json.dumps(c.tags))
        __M_writer('\n                    }, n2\n                )\n            }\n        }\n    </script>\n')
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

        def licdetail(license):
            return render_licdetail(context, license)

        def licprojects(projectnames):
            return render_licprojects(context, projectnames)

        __M_writer = context.writer()
        __M_writer('\n    ')
        if c.license:
            pagebartext = '%s (%s)' % (c.license.licensename, c.license.id)
        else:
            pagebartext = 'License:'
        searchbox = capture(forms.form_searchbox, c.authuser, 'searchlic', 'Search-license', h.suburl_search, c.searchfaces)
        vbar = '<span class="fntsmall fwnormal">|</span>'
        attachs = '<span class="ml10 fwnormal fntsmall">' + '<a href="%s">Attachments</a></span>' % h.url_licattachs
        if c.license and c.liceditable:
            editlic = '<span name="editlic" ' + 'class="fgblue ml10 fwnormal fntsmall pointer">edit</span>'
            creatlic = '<span name="crlic" class="ml10 fwnormal fntsmall">' + '<a title="Create a new license" href="%s">create</a></span>' % h.url_crlic
            rmlic = '<span name="rmlic" class="ml10 fwnormal fntsmall">' + '<a title="Remove this license" href="%s">remove</a></span>' % h.suburl_rmlicid
            pbar_spans = [editlic, rmlic, vbar, creatlic, vbar, attachs]
        else:
            pbar_spans = [
             attachs]
        charts = capture(elements.iconlink, h.url_licensecharts, 'barchart', title='Analytics on license')
        tline = capture(elements.iconlink, h.url_lictimeline, 'timeline', title='License Timeline')
        __M_writer('\n    ')
        __M_writer(escape(elements.pagebar(pagebartext, pbar_spans + [
         capture(forms.form_licenselist, c.licenselist, c.license and c.license.licensename),
         searchbox], rspans=[
         charts, tline], tooltips=page_tooltips)))
        __M_writer('\n    <div id="bdy" class="w100">\n')
        if c.userpanes:
            __M_writer('    <div id="licensepage" class="panel1">\n')
        else:
            __M_writer('    <div id="licensepage" class="fullpanel1">\n')
        __M_writer('\n')
        if c.license:
            __M_writer('            <div name="viewlic" class="mr10">\n                <div class="floatr" style="width : 250px;">\n                    ')
            __M_writer(escape(licdetail(c.license)))
            __M_writer('\n                    ')
            __M_writer(escape(licprojects(c.licprojects)))
            __M_writer('\n                    <div>\n                        <div name="attachblk"></div>\n                    </div>\n                    <div class="bclear">\n                        <div name="tagblk"></div>\n                    </div>\n                    <div class="ml10 fntbold bclear">\n                        <a href="')
            __M_writer(escape(h.url_tagcloud))
            __M_writer('">Visit tag cloud ...</a>\n                    </div>\n                </div>\n')
            __M_writer('                <div class="ml10" style="margin-right: 250px;">\n                    <div class="fnt110 fntbold"\n                         style="padding: 10px 0 10px 0;">\n                        ')
            __M_writer(escape(c.license.licensename))
            __M_writer('\n                    </div>\n                    <div class="dispnone" name="text">')
            __M_writer(escape(c.license.text))
            __M_writer('</div>\n                </div>\n            </div>\n            <div name="editlic" class="ml20 dispnone">\n                ')
            __M_writer(escape(forms.form_updatelicense_h(c.authuser, c.license, h.suburl_uplic)))
            __M_writer('\n            </div>\n')
        else:
            __M_writer('            <div id="licensetable">\n                ')
            __M_writer(escape(elements.lictable1(c.licensetable, c.liceditable)))
            __M_writer('\n                <div name="rmlic" class="dispnone">\n                    ')
            __M_writer(escape(forms.form_removelic_h(c.authuser, h.suburl_rmlic)))
            __M_writer('\n                </div>\n            </div>\n')
        __M_writer('    </div>\n')
        if c.userpanes:
            __M_writer('    <div class="panel2">')
            __M_writer(escape(elements.user_panes(c.userpanes)))
            __M_writer('</div>\n')
        __M_writer('    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_licdetail(context, license):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer('\n<div class="br4 ml10" style="border : 1px dotted gray;">\n    <div class="p3 fntbold">\n        ')
        __M_writer(escape(license.summary))
        __M_writer('\n    </div>\n    <div class="p3" title="license source">\n        ')
        __M_writer(escape(license.source))
        __M_writer('\n    </div>\n</div>\n')
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
        __M_writer('\n\n    <script type="text/javascript">\n        dojo.addOnLoad( setup_license );\n\n        dojo.addOnLoad( setup_userpanes );\n        dojo.addOnLoad( adjust_upheight );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()