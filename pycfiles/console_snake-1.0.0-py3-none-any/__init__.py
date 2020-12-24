# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/console_script/__init__.py
# Compiled at: 2009-12-22 14:47:46
from paste.script import templates
var = templates.var

class console_script(templates.Template):
    _template_dir = 'template'
    summary = 'pastescript template for creating command line applications'
    vars = [
     var('description', 'One-line description of the package'),
     var('author', 'Author name'),
     var('author_email', 'Author email'),
     var('url', 'URL of homepage')]