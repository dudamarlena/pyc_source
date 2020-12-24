# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/lib/renderers.py
# Compiled at: 2011-12-25 05:31:43
from django import template
from django.template.loader import *

class HalTemplate(object):

    def __init__(self, text):
        self.text = text

    def render(self, context):
        raise NotImplementedError('This class needs to be inherited')


class Django(HalTemplate):

    def __init__(self, text):
        HalTemplate.__init__(self, text)
        self.template = template.Template(text)

    def render(self, dict):
        return self.template.render(template.Context(dict))