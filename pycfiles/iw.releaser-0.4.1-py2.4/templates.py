# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/releaser/templates.py
# Compiled at: 2008-04-29 08:14:25
""" Template definitions
"""
from paste.script import templates
from zopeskel.base import var

class IWPloneProject(templates.Template):
    """ Generates a Plone 3 project tree 
    """
    __module__ = __name__
    _template_dir = 'templates/iw_plone_project'
    summary = 'A Plone 3 project tree for Ingeniweb projects'
    use_cheetah = True
    vars = [
     var('project_name', 'Project Name'), var('project_repo', 'Project Subversion root'), var('zope_user', 'Zope root admin user', default='admin'), var('zope_password', 'Zope root admin password'), var('http_port', 'HTTP port', default=8080), var('debug_mode', 'Should debug mode be "on" or "off"?', default='off'), var('verbose_security', 'Should verbose security be "on" or "off"?', default='off')]