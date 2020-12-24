# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simplesitetemplate/__init__.py
# Compiled at: 2008-11-08 17:25:08
from paste.script.templates import BasicPackage, var

class SimpleSitePackage(BasicPackage):
    _template_dir = 'template'
    summary = 'A Pylons template to create a simple, user-editable website'
    egg_plugins = ['PasteScript', 'Pylons']
    vars = [
     var('sqlalchemy_url', 'The SQLAlchemy URL to the database to use', default='sqlite:///%(here)s/develpment.db')]