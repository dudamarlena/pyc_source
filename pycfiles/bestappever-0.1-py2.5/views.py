# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/bestappever/views.py
# Compiled at: 2008-08-25 05:58:58
from repoze.bfg.template import render_template_to_response

def my_view(context, request):
    return render_template_to_response('templates/mytemplate.pt', project='bestappever', abspath=context.absolute_path(), name=context.__name__)