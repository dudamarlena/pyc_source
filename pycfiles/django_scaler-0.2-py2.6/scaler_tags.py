# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/scaler/templatetags/scaler_tags.py
# Compiled at: 2012-05-30 07:38:44
import time
from django import template
register = template.Library()

@register.tag
def delay(parser, token):
    (tag_name, value) = token.split_contents()
    return DelayNode()


class DelayNode(template.Node):

    def render(self, context):
        value = float(context['request'].GET.get('delay', 0))
        if value:
            time.sleep(value)
            return 'Delayed by %s seconds' % value
        return ''