# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /MyWork/Projects/PyCK/pyck/mako_utils/cache/multi_selector.mako.py
# Compiled at: 2015-07-09 23:12:14
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1436497934.838919
_enable_loop = True
_template_filename = '/MyWork/Projects/PyCK/pyck/mako_utils/templates/multi_selector.mako'
_template_uri = 'multi_selector.mako'
_source_encoding = 'utf8'
_exports = ['show_items']

def render_body(context, **pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)

        def show_items(records, fname=None, ignore_prefix=None, indent='', parent_key=None):
            return render_show_items(context._locals(__M_locals), records, fname, ignore_prefix, indent, parent_key)

        items = context.get('items', UNDEFINED)
        field_name = context.get('field_name', UNDEFINED)
        ignore_prefix = context.get('ignore_prefix', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n\n<script type="application/x-javascript">\n    //dojo.query(\'#main2 > input[type=checkbox]:checked\')\n    \n    function toggle_selection(chkbox, target_container){\n        require([ "dijit/registry", "dojo/query"], function(registry, query){  \n            query(target_container + " input").forEach(function(node, index, arr){\n              registry.byId(node.id).set("checked", registry.byId(chkbox).checked);\n            });\n          });\n    }\n</script>\n\n')
        __M_writer(unicode(show_items(items, field_name, ignore_prefix, '')))
        __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()

    return


def render_show_items(context, records, fname=None, ignore_prefix=None, indent='', parent_key=None):
    __M_caller = context.caller_stack._push_frame()
    try:

        def show_items(records, fname=None, ignore_prefix=None, indent='', parent_key=None):
            return render_show_items(context, records, fname, ignore_prefix, indent, parent_key)

        isinstance = context.get('isinstance', UNDEFINED)
        dict = context.get('dict', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        extra_css_class = ''
        table_id = ''
        if parent_key:
            extra_css_class = 'collapse in'
            table_id = ('id="{}_subitems"').format(parent_key)
        __M_writer('\n    \n    <table class="table table-condensed table-hover table-striped ')
        __M_writer(unicode(extra_css_class))
        __M_writer('" ')
        __M_writer(unicode(table_id))
        __M_writer('>\n')
        for k, v in records.items():
            __M_writer('        ')
            if ignore_prefix is not None and k.startswith(ignore_prefix):
                continue
            __M_writer('\n        \n')
            if not isinstance(v, dict):
                __M_writer('            <tr>\n                <td colspan="2">\n')
                if indent:
                    __M_writer('                    ')
                    __M_writer(unicode(indent))
                    __M_writer('\n')
                __M_writer('                    <input type="checkbox" data-dojo-type="dijit/form/CheckBox" name="')
                __M_writer(unicode(fname))
                __M_writer('" id="" value="')
                __M_writer(unicode(k))
                __M_writer('" />\n                    ')
                __M_writer(unicode(v))
                __M_writer('\n                </td>\n            </tr>\n')
            else:
                __M_writer('            <tr>\n                <td style="width: 4%;">\n                    <input data-dojo-type="dijit/form/CheckBox" id="')
                __M_writer(unicode(k))
                __M_writer('_parent" type="checkbox" onclick="toggle_selection(\'')
                __M_writer(unicode(k))
                __M_writer("_parent', '#")
                __M_writer(unicode(k))
                __M_writer('_subitems\');" />\n                </td>\n                <td data-toggle="collapse" data-target="#')
                __M_writer(unicode(k))
                __M_writer('_subitems">\n                    <b>')
                __M_writer(unicode(k))
                __M_writer('</b>\n                    <span class="glyphicon glyphicon-chevron-down"></span>\n                </td>\n            </tr>\n            <tr>\n                <td colspan="2">\n                    ')
                __M_writer(unicode(show_items(records=v, fname=fname, ignore_prefix=ignore_prefix, parent_key=k, indent=indent + '&nbsp;' * 4)))
                __M_writer('\n                </td>\n            </tr>\n')

        __M_writer('    </table>\n    \n    \n')
        return ''
    finally:
        context.caller_stack._pop_frame()

    return