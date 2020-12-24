# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/extdirect/django/templatetags/direct_providers.py
# Compiled at: 2010-02-06 11:40:48
import os
from django import template
from extdirect.router import DirectProviderDefinition
from extdirect.django import registry
register = template.Library()

def do_direct_providers(parser, token):
    tokens = token.split_contents()
    return ScriptNode()


class ScriptNode(template.Node):

    def render(self, context):
        js = []
        for (klass, name, ns) in registry.classes():
            js.append(DirectProviderDefinition(klass, '/extdirect/%s/' % name, ns).render())

        return ('\n').join(js)


register.tag('direct_providers', do_direct_providers)