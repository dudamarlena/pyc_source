# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/aneumeier/web/env/lib/python2.7/site-packages/flattr/templatetags/flattr.py
# Compiled at: 2013-06-20 10:34:28
"""
templatetags/flattr.py 

See also:
[[http://developers.flattr.net/button/]]

"""
from django import template
register = template.Library()

class FlattrScriptNode(template.Node):
    """
    FlattrScriptNode renders the actual javascript
    """
    script = '<script type="text/javascript">\n    /* <![CDATA[ */\n    (function() {\n    var s = document.createElement(\'script\');\n    var t = document.getElementsByTagName(\'script\')[0];\n\n    s.type = \'text/javascript\';\n    s.async = true;\n    s.src = \'//api.flattr.com/js/0.6/load.js?mode=auto\';\n\n    t.parentNode.insertBefore(s, t);\n    })();\n    /* ]]> */\n    </script>\n    '

    def __init__(self, *args, **kwargs):
        """
        Arguments:
        mode - auto | manual(default)
        https - 1 | 0 (defaults to the schema of load.js)
        popout - 1 | 0 (show popout when hovering mouse over button)
        uid - username
        button - compact | default
        language - can be set to any of the available languages
        category - Can be set to any of the available categories
        html5-key-prefix - a string that must start with 'data-'
        """
        if 'mode' in kwargs:
            self.args['mode'] = kwargs['mode']
        if 'https' in kwargs:
            self.args['https'] = kwargs['https']
        if 'popout' in kwargs:
            self.args['popout'] = kwargs['popout']
        if 'uid' in kwargs:
            self.args['uid'] = kwargs['uid']
        if 'language' in kwargs:
            self.args['language'] = kwargs['language']
        if 'category' in kwargs:
            self.args['category'] = kwargs['category']
        if 'html5-key-prefix' in kwargs:
            self.args['html5-key-prefix'] = kwargs['html5-key-prefix']

    def render(self, context):
        return self.script


@register.tag
def flattr_script(parser, token):
    return FlattrScriptNode()


class FlattrButtonNode(template.Node):

    def __init__(self, *args, **kwargs):
        pass

    def render(self, context):
        pass


@register.tag
def flattr_button(parser, token):
    return FlattrButtonNode()