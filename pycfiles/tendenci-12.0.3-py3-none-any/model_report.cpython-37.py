# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/libs/model_report/templatetags/model_report.py
# Compiled at: 2020-02-11 12:52:19
# Size of source mod 2**32: 1064 bytes
from django import template
from django.template.loader import render_to_string
register = template.Library()

class ModelReportInlineNode(template.Node):

    def __init__(self, inline, row):
        self.inline = template.Variable(inline)
        self.row = template.Variable(row)

    def render(self, context):
        inline = self.inline.resolve(context)
        row = self.row.resolve(context)
        request = context.get('request')
        if row.is_value():
            inline_context = inline.get_render_context(request, by_row=row)
            if len(inline_context['report_rows']) > 0:
                return render_to_string(template_name='model_report/includes/report_inline.html', context=inline_context)
        return ''


@register.tag()
def model_report_render_inline(parser, token):
    try:
        tag_name, inline, row = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%r tag requires arguments' % token.contents.split()[0])

    return ModelReportInlineNode(inline, row)