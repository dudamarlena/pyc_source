# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/w20e/pycms/sitemaker/pycmsprojecttemplate.py
# Compiled at: 2012-01-06 04:14:07
from paste.script.templates import Template, var
vars = [
 var('version', 'Version (like 0.1)'),
 var('description', 'One-line description of the package'),
 var('keywords', 'Space-separated keywords/tags'),
 var('author', 'Author name'),
 var('author_email', 'Author email'),
 var('url', 'URL of homepage'),
 var('license_name', 'License name'),
 var('zip_safe', 'True/False: if the package can be distributed as a .zip file', default=False)]

class PyCMSProjectTemplate(Template):
    _template_dir = './skel'
    summary = 'PyCMS project template'
    vars = vars