# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ventriloquist/page.py
# Compiled at: 2010-02-27 17:31:39
import copy
from webob import Response

class Page(object):
    """
    The basic page object in puppetcms.
    """

    def __init__(self, template, context):
        self.template = template
        self.context = context

    def __call__(self, request):
        context = copy.copy(self.context)
        context['request'] = request
        return Response(self.template.render(context))