# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/webob_view/__init__.py
# Compiled at: 2009-11-21 14:58:57
from paste.script import templates
var = templates.var

class WebobViewTemplate(templates.Template):
    _template_dir = 'template'
    summary = 'a simple view with webob'
    vars = [
     var('description', 'One-line description of the package'),
     var('author', 'Author name'),
     var('author_email', 'Author email'),
     var('url', 'URL of homepage'),
     var('port', 'port to serve paste')]