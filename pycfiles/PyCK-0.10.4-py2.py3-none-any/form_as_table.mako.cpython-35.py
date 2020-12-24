# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /MyWork/Projects/PyCK/pyck/forms/cache/form_as_table.mako.py
# Compiled at: 2016-03-27 07:23:14
# Size of source mod 2**32: 8283 bytes
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1459077794.0478497
_enable_loop = True
_template_filename = '/MyWork/Projects/PyCK/pyck/forms/templates/form_as_table.mako'
_template_uri = 'form_as_table.mako'
_source_encoding = 'utf8'
_exports = []

def render_body(context, **pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        form = context.get('form', UNDEFINED)
        labels_position = context.get('labels_position', UNDEFINED)
        errors_position = context.get('errors_position', UNDEFINED)
        str = context.get('str', UNDEFINED)
        include_table_tag = context.get('include_table_tag', UNDEFINED)
        __M_writer = context.writer()
        num_cols = 2
        num_rows = 2
        if labels_position in ('left', 'right') and errors_position in ('left', 'right'):
            num_cols = 3
            num_rows = 1
        else:
            if labels_position in ('top', 'bottom') and errors_position in ('top',
                                                                            'bottom'):
                num_cols = 1
                num_rows = 3
            __M_locals_builtin_stored = __M_locals_builtin()
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['num_rows', 'num_cols'] if __M_key in __M_locals_builtin_stored]))
            __M_writer('\n')
            if include_table_tag:
                __M_writer('<table class="table table-striped table-hover">\n')
            if form._use_csrf_protection:
                __M_writer('    <input type="hidden" name="csrf_token" value="')
                __M_writer(str(form._csrf_token))
                __M_writer('" />\n')
            if '_csrf' in form.errors:
                __M_writer('    <tr><td class="errors" colspan="')
                __M_writer(str(num_cols))
                __M_writer('">')
                __M_writer(str(form.errors['_csrf'][0]))
                __M_writer('</td></tr>\n')
            for field in form:
                __M_writer('    ')
                field_label = '<td>' + str(field.label) + '</td>'
                field_content = '<td>' + str(field(class_='form-control')) + '</td>'
                field_errors = '<td></td>'
                if field.errors:
                    field_errors = '<td class="errors">'
                    for e in field.errors:
                        field_errors += e + ', '

                    field_errors = field_errors[:-2] + '</td>'
                __M_locals_builtin_stored = __M_locals_builtin()
                __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['field_content', 'field_label', 'e', 'field_errors'] if __M_key in __M_locals_builtin_stored]))
                __M_writer('\n')
                if 1 == num_rows:
                    __M_writer('    <tr>\n')
                    if 'left' == labels_position:
                        __M_writer('        ')
                        __M_writer(str(field_label))
                        __M_writer('\n')
                    if 'left' == errors_position:
                        __M_writer('        ')
                        __M_writer(str(field_errors))
                        __M_writer('\n')
                    __M_writer('        ')
                    __M_writer(str(field_content))
                    __M_writer('\n')
                    if 'right' == labels_position:
                        __M_writer('        ')
                        __M_writer(str(field_label))
                        __M_writer('\n')
                    if 'right' == errors_position:
                        __M_writer('        ')
                        __M_writer(str(field_errors))
                        __M_writer('\n')
                    __M_writer('    </tr>\n')
                else:
                    if 3 == num_rows:
                        __M_writer('    <tr>\n    <td>\n        <table>\n')
                        if 'top' == labels_position:
                            __M_writer('        <tr>')
                            __M_writer(str(field_label))
                            __M_writer('</tr>\n')
                        if 'top' == errors_position:
                            __M_writer('        <tr>')
                            __M_writer(str(field_errors))
                            __M_writer('</tr>\n')
                        __M_writer('        <tr>')
                        __M_writer(str(field_content))
                        __M_writer('</tr>\n')
                        if 'bottom' == labels_position:
                            __M_writer('        <tr>')
                            __M_writer(str(field_label))
                            __M_writer('</tr>\n')
                        if 'bottom' == errors_position:
                            __M_writer('        <tr>')
                            __M_writer(str(field_errors))
                            __M_writer('</tr>\n')
                        __M_writer('        </table>\n    </td>\n    </tr>\n')
                    else:
                        __M_writer('    <tr>\n    <td>\n        <table>\n')
                        if 'top' == labels_position:
                            __M_writer('        <tr>')
                            __M_writer(str(field_label))
                            __M_writer('</tr> \n        <tr> ')
                        elif 'left' == labels_position:
                            __M_writer('        <tr>')
                            __M_writer(str(field_label))
                            __M_writer(' ')
                        __M_writer('        ')
                        if 'top' == errors_position:
                            __M_writer('        <tr>')
                            __M_writer(str(field_errors))
                            __M_writer('</tr> \n        <tr> ')
                        elif 'left' == errors_position:
                            __M_writer('        <tr>')
                            __M_writer(str(field_errors))
                            __M_writer(' ')
                        __M_writer('        ')
                        __M_writer('        ')
                        __M_writer(str(field_content))
                        __M_writer('\n        ')
                        if 'bottom' == labels_position:
                            __M_writer('        </tr>\n        <tr>')
                            __M_writer(str(field_label))
                            __M_writer('</tr>\n')
                        elif 'right' == labels_position:
                            __M_writer('        ')
                            __M_writer(str(field_label))
                            __M_writer('</tr>\n')
                        __M_writer('        ')
                if 'bottom' == errors_position:
                    __M_writer('        </tr>\n        <tr>')
                    __M_writer(str(field_errors))
                    __M_writer('</tr>\n')
                else:
                    if 'right' == errors_position:
                        __M_writer('        ')
                        __M_writer(str(field_errors))
                        __M_writer('</tr>\n')
                    __M_writer('        </table>\n    </td>\n    </tr>\n')
                __M_writer('    \n')

            if include_table_tag:
                __M_writer('</table>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()