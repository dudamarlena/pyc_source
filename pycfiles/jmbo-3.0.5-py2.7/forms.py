# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo/forms.py
# Compiled at: 2016-03-08 06:26:22


def as_div(form):
    """This formatter arranges label, widget, help text and error messages by
    using divs.  Apply to custom form classes, or use to monkey patch form
    classes not under our direct control."""
    form.required_css_class = 'required'
    return form._html_output(normal_row='<div class="field"><div %(html_class_attr)s>%(label)s %(errors)s <div class="helptext">%(help_text)s</div> %(field)s</div></div>', error_row='%s', row_ender='</div>', help_text_html='%s', errors_on_separate_row=False)