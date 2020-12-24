# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /MyWork/Projects/PyCK/pyck/forms/cache/form_as_p.mako.py
# Compiled at: 2016-05-04 17:04:33
# Size of source mod 2**32: 3651 bytes
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1462395873.3746402
_enable_loop = True
_template_filename = '/MyWork/Projects/PyCK/pyck/forms/templates/form_as_p.mako'
_template_uri = 'form_as_p.mako'
_source_encoding = 'utf-8'
_exports = []

def render_body(context, **pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        form = context.get('form', UNDEFINED)
        labels_position = context.get('labels_position', UNDEFINED)
        errors_position = context.get('errors_position', UNDEFINED)
        __M_writer = context.writer()
        if form._use_csrf_protection:
            __M_writer('<input type="hidden" name="csrf_token" value="')
            __M_writer(str(form._csrf_token))
            __M_writer('" />\n')
        if '_csrf' in form.errors:
            __M_writer('<div class="errors">')
            __M_writer(str(form.errors['_csrf'][0]))
            __M_writer('</div><br />\n')
        for field in form:
            field_errors = ''
            if field.errors:
                field_errors = '<span class="errors">'
                for e in field.errors:
                    field_errors += e + ', '

                field_errors = field_errors[:-2] + '</span>'
            __M_locals_builtin_stored = __M_locals_builtin()
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['field_errors', 'e'] if __M_key in __M_locals_builtin_stored]))
            __M_writer('\n<p>\n')
            if 'top' == labels_position:
                __M_writer(str(field.label))
                __M_writer('<br /> ')
            if field_errors and 'top' == errors_position:
                __M_writer(str(field_errors))
                __M_writer('<br /> ')
            if 'left' == labels_position:
                __M_writer(str(field.label))
                __M_writer(' ')
            if field_errors and 'left' == errors_position:
                __M_writer(str(field_errors))
                __M_writer(' ')
            __M_writer(str(field(class_='form-control')))
            __M_writer(' ')
            if 'bottom' == labels_position:
                __M_writer('<br />')
                __M_writer(str(field.label))
                __M_writer(' ')
            if field_errors and 'bottom' == errors_position:
                __M_writer('<br />')
                __M_writer(str(field_errors))
                __M_writer(' ')
            if 'right' == labels_position:
                __M_writer(str(field.label))
                __M_writer(' ')
            if field_errors and 'right' == errors_position:
                __M_writer(str(field_errors))
                __M_writer(' ')
            __M_writer('</p>\n')

        return ''
    finally:
        context.caller_stack._pop_frame()