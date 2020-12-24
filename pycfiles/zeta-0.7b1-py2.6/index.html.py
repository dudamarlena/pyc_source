# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/projects/index.html.py
# Compiled at: 2010-07-12 02:00:52
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278914452.200107
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/projects/index.html'
_template_uri = '/derived/projects/index.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['hd_script', 'bd_script', 'bd_body', 'highlightprojects']
page_tooltips = [
 [
  'Help',
  'List of projects hosted under this site. To quickly go to a project that\nyou belong to, use <em>projects</em> drop down menu in meta-nav.\nAccess to each of these projects are controlled by project\'s administrator.\n<br/>Use <span class="fgblue bggray1">...</span> to expand text.\n']]

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
        parent = context.get('parent', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        __M_writer(escape(parent.hd_script()))
        __M_writer('\n\n    <script type="text/javascript">\n    function projdescriptions() {\n        dojo.forEach(\n            dojo.query( \'div.shrinkview\' ),\n            function( n ) {\n                new zeta.ShrinkNode({\n                        hexp: \'100%\',\n                        hshrink: \'6em\',\n                        def: \'shrink\'\n                    }, n );\n            }\n        );\n    }\n    </script>\n')
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
        __M_writer('\n\n    <script type="text/javascript">\n        dojo.addOnLoad( projdescriptions );\n        dojo.addOnLoad( setup_userpanes );\n        dojo.addOnLoad( adjust_upheight );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bd_body(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')

        def highlightprojects(projects):
            return render_highlightprojects(context, projects)

        __M_writer = context.writer()
        __M_writer('\n    ')
        pagebartext = 'Project list'
        __M_writer('\n    ')
        __M_writer(escape(elements.pagebar(pagebartext, tooltips=page_tooltips)))
        __M_writer('\n    <div id="bdy" class="w100">\n')
        if c.authusername == 'anonymous' or not c.userpanes:
            __M_writer('        <div class="fullpanel1">')
            __M_writer(escape(highlightprojects(c.projects)))
            __M_writer('</div>\n')
        else:
            __M_writer('        <div class="panel1">')
            __M_writer(escape(highlightprojects(c.projects)))
            __M_writer('</div>\n        <div class="panel2">')
            __M_writer(escape(elements.user_panes(c.userpanes)))
            __M_writer('</div>\n')
        __M_writer('    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_highlightprojects(context, projects):
    context.caller_stack._push_frame()
    try:
        sorted = context.get('sorted', UNDEFINED)
        h = context.get('h', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <ol class="mt10 mr20 pl10">\n')
        for p in sorted(projects, key=lambda p: p.projectname):
            __M_writer('        ')
            desc = p.project_info.descriptionhtml
            __M_writer('\n        <li class="lstnone">\n            <div class="fntbold mt20">\n                <a href="')
            __M_writer(escape(h.url_projects[p.id]))
            __M_writer('">')
            __M_writer(escape(p.projectname))
            __M_writer('</a>\n                <span>- (')
            __M_writer(escape(p.summary))
            __M_writer(')</span>\n                <span class="fggray fntnormal ml20">\n                    Administered by\n                    <a href="')
            __M_writer(escape(h.url_foruser(p.admin.username)))
            __M_writer('">')
            __M_writer(escape(p.admin.username))
            __M_writer(' </a>\n                </span>\n            </div>\n            <div class="shrinkview mt5">\n                ')
            __M_writer(desc)
            __M_writer('\n            </div>\n        </li>\n')

        __M_writer('    </ol>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()