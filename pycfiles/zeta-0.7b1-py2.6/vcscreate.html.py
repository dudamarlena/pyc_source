# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/projects/vcscreate.html.py
# Compiled at: 2010-07-12 03:41:03
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278920463.924311
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/projects/vcscreate.html'
_template_uri = '/derived/projects/vcscreate.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['hd_links', 'hd_script', 'bd_body', 'hd_styles', 'create_vcs', 'bd_script']
page_tooltips = [
 [
  'Help',
  'Integrate one or more repositories with projects by providing its\n<em>type</em> (like svn ...) and <em>root-url</em>. Make sure that\n<em>root-url</em> points to the same machine, or to a machine on the local network.\n']]

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


def render_bd_body(context):
    context.caller_stack._push_frame()
    try:
        forms = _mako_get_namespace(context, 'forms')
        capture = context.get('capture', UNDEFINED)
        c = context.get('c', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')

        def create_vcs():
            return render_create_vcs(context)

        __M_writer = context.writer()
        __M_writer('\n    ')
        sel_vcs = capture(forms.form_selectvcs, c.authuser, c.vcslist, c.vcs and c.vcs.name or '')
        __M_writer('\n    ')
        __M_writer(escape(elements.mainnav()))
        __M_writer('\n    ')
        __M_writer(escape(elements.contextnav([sel_vcs], tooltips=page_tooltips)))
        __M_writer('\n    <div id="bdy" class="w100">\n')
        if c.authusername == 'anonymous' or not c.userpanes:
            __M_writer('        <div class="fullpanel1">\n')
        else:
            __M_writer('        <div class="panel1">\n')
        __M_writer('            <div>\n                ')
        __M_writer(escape(create_vcs()))
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


def render_create_vcs(context):
    context.caller_stack._push_frame()
    try:
        forms = _mako_get_namespace(context, 'forms')
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')
        __M_writer = context.writer()
        __M_writer('\n    <div name="zvcscreate" class="disptable mr5">\n    <div class="disptrow">\n        <div class="disptcell">\n            ')
        __M_writer(escape(forms.form_createvcs(c.authuser, c.project, h.suburl_createvcs, c.vcs_typenames)))
        __M_writer('\n        </div>\n        <div class="disptcell">\n        <div class="ml10" style="width : 30em;">\n            ')
        __M_writer(escape(elements.helpboard('\n                Note that this process does not create a repository, instead\n                it just integrates with an already created repository,\n                and specified by <b>`url`</b>, which typically looks like,\n                <div class="ml10">\n                <em>file:///path/to/repository/root</em>\n                    for a repository hosted on a local machine,\n                </div>\n                <div class="ml10">\n                <em>http://ip-address:port/path/to/hosted/root</em>\n                    for a repository hosted via http.\n                </div>\n                Visit <a href="/help/vcs">vcs-doc</a> to know more\n                <br></br>\n                <br></br>\n                And it is better to have the url pointing to a repository\n                resource in the local machine, are atleast in your subnet.\n                ')))
        __M_writer('\n        </div>\n        </div>\n    </div>\n    </div>\n')
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
        __M_writer('\n\n    <script type="text/javascript">\n        dojo.addOnLoad( function () {\n            /* Setup the vcs goto list */\n            select_goto( dojo.query( \'#selectvcs\' )[0] );\n        });\n        dojo.addOnLoad( initform_createvcs );\n\n        dojo.addOnLoad( setup_userpanes );\n        dojo.addOnLoad( adjust_upheight );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()