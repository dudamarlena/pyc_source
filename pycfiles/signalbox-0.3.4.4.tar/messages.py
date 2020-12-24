# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/templatetags/signalbox_tags/messages.py
# Compiled at: 2014-08-27 19:26:12
from django import template
register = template.Library()

class MessagesNode(template.Node):
    """Outputs grouped Django Messages Framework messages in separate
        lists sorted by level. """

    def __init__(self, messages):
        self.messages = messages

    def render(self, context):
        try:
            messages = context[self.messages]
            grouped = {}
            for m in messages:
                if (
                 m.level, m.tags) in grouped:
                    grouped[(m.level, m.tags)].append(m.message)
                else:
                    grouped[(m.level, m.tags)] = [
                     m.message]

            out_str = ''
            d = {}
            for level, tag in sorted(grouped.iterkeys()):
                d[tag] = grouped[(level, tag)]

            context['sorted_messages'] = d
            return ''
            for level, tag in sorted(grouped.iterkeys()):
                out_str += '<div class="messages %s">\n<ul class="messages-list-%s">' % (tag, tag)
                for m in grouped[(level, tag)]:
                    out_str += '<li>%s</li>' % m

                out_str += '</ul>\n</div>\n'

            return out_str
        except KeyError:
            return ''


@register.tag(name='render_messages')
def render_messages(parser, token):
    parts = token.split_contents()
    if len(parts) != 2:
        raise template.TemplateSyntaxError('%r tag requires a single argument' % token.contents.split()[0])
    return MessagesNode(parts[1])