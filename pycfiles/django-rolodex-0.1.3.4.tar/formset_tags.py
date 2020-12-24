# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jon/DMN/Scripts/on_the_record/dmn-labs/rolodex/templatetags/formset_tags.py
# Compiled at: 2014-11-23 19:59:36
"""
django-formset-js: https://bitbucket.org/ionata/django-formset-js/

Copyright (c) 2013, Ionata Web Solutions
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice, this
list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
from django.template import Library, Node
register = Library()

class EscapeScriptNode(Node):
    TAG_NAME = 'escapescript'

    def __init__(self, nodelist):
        super(EscapeScriptNode, self).__init__()
        self.nodelist = nodelist

    def render(self, context):
        out = self.nodelist.render(context)
        escaped_out = out.replace('</script>', '<\\/script>')
        return escaped_out


@register.tag(EscapeScriptNode.TAG_NAME)
def media(parser, token):
    nodelist = parser.parse(('end' + EscapeScriptNode.TAG_NAME,))
    parser.delete_first_token()
    return EscapeScriptNode(nodelist)