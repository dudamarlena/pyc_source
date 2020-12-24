# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/templatetemplate/__init__.py
# Compiled at: 2009-07-23 16:33:15
from paste.script import templates
var = templates.var

class PasteScriptTemplateTemplate(templates.Template):
    _template_dir = 'template'
    summary = 'a template for creating PasteScript templates'
    vars = [
     var('description', 'One-line description of the package'),
     var('author', 'Author name'),
     var('author_email', 'Author email'),
     var('url', 'URL of homepage')]