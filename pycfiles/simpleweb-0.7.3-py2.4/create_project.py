# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simpleweb/admin/plugins/create_project.py
# Compiled at: 2007-01-10 11:14:11
import sys, os, string
from simpleweb.admin.plugins import templates
import simpleweb.utils

def create_project(cmdline, args):
    """Usage: simpleweb-admin create-project <project-name> [summary] [description string]

Creates a new simpleweb project Project-Name. The new project
will have the neccessary files and filesystem structure that
a simpleweb project requires.
        """
    if len(args) < 1 or len(args) > 3:
        simpleweb.utils.msg_err("Try 'simpleweb-admin help create-project' for help")
        sys.exit()
    summary = ''
    description = ''
    try:
        projectname = args[0]
        summary = args[1]
        description = args[2]
    except IndexError:
        pass

    create_folder_toplevel(projectname, summary, description)
    create_file(projectname, 'main.py', templates.main_py, 493)
    create_file(projectname, 'config.py', templates.config_py)
    create_file(projectname, 'urls.py', templates.urls_py)
    create_file(projectname, 'models.py', templates.models_py)
    create_folder(projectname, 'static', subfolders=['css', 'img', 'js'])
    create_file(projectname, 'static/css/main.css', templates.main_css)
    create_folder(projectname, 'templates')
    create_file(projectname, 'templates/index.html', templates.index_html)
    create_file(projectname, 'templates/master.html', templates.master_html)
    create_folder(projectname, 'tests')
    controllers_project = '%s/%s' % (projectname, 'controllers')
    create_folder_toplevel(controllers_project, 'The controllers package for %s' % projectname, 'This package contains standalone controllers for the project %s' % projectname)
    create_file(projectname, 'controllers/index.py', templates.index_py)


def create_folder_toplevel(projectname, summary='', description=''):
    try:
        os.mkdir(projectname)
        f = open('%s/__init__.py' % projectname, 'w')
        f.write('"""\n%s\n\n%s\n"""' % (summary, description))
        f.close()
    except Exception, e:
        simpleweb.utils.msg_warn('Error creating toplevel: %s' % e)


def create_folder(projectname, foldername, subfolders=[]):
    try:
        fname = '%s/%s' % (projectname, foldername)
        os.mkdir(fname)
        for f in subfolders:
            create_folder(fname, f)

    except Exception, e:
        simpleweb.utils.msg_warn('Error creating folder: %s' % e)


def create_file(projectname, filename, template_string, perms=420):
    try:
        fname = '%s/%s' % (projectname, filename)
        f = open(fname, 'w')
        content = string.Template(template_string)
        f.write(content.substitute(projectname=projectname))
        f.close()
        os.chmod(fname, perms)
    except Exception, e:
        simpleweb.utils.msg_warn('Error creating file: %s' % e)