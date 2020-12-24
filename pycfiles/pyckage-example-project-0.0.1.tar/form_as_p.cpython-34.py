# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /MyWork/Projects/PyCK/pyck/forms/cache/form_as_p.mako.py
# Compiled at: 2014-12-11 07:31:49
# Size of source mod 2**32: 3587 bytes
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1407862340.456977
_enable_loop = True
_template_filename = '/MyWork/Projects/PyCK/pyck/forms/templates/form_as_p.mako'
_template_uri = 'form_as_p.mako'
_source_encoding = 'utf-8'
_exports = []

def render_body(context, **pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        errors_position = context.get('errors_position', UNDEFINED)
        labels_position = context.get('labels_position', UNDEFINED)
        form = context.get('form', UNDEFINED)
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
            __M_writer(str(field))
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