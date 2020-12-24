# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mardochee.macxis/Projects/Python/flask-pilot/flask_pilot/cmd.py
# Compiled at: 2015-02-15 06:47:28
"""
Flask-Pilot

Command line tool

flask-pilot -c project_name

"""
import os, argparse, pkg_resources, flask_pilot
PACKAGE = flask_pilot
CWD = os.getcwd()
PROJECTS_TEMPLATES = 'skeleton'

def get_project_dir_path(project_name):
    return '%s/%s' % (CWD, project_name)


def copy_resource(src, dest):
    """
    To copy package data to destination
    """
    dest = (dest + '/' + os.path.basename(src)).rstrip('/')
    if pkg_resources.resource_isdir(PACKAGE.__name__, src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        for res in pkg_resources.resource_listdir(__name__, src):
            copy_resource(src + '/' + res, dest)

    elif os.path.splitext(src)[1] not in ('.pyc', ):
        with open(dest, 'wb') as (f):
            f.write(pkg_resources.resource_string(__name__, src))


def create_project(project_name, template='default'):
    """
    Create the project
    """
    project_dir = get_project_dir_path(project_name)
    server_file = '%s/server_%s.py' % (CWD, project_name)
    server_tpl = pkg_resources.resource_string(__name__, '%s/server.py.tpl' % PROJECTS_TEMPLATES)
    requirements_txt = '%s/requirements.txt' % CWD
    if not os.path.isdir(project_dir):
        os.makedirs(project_dir)
    else:
        raise OSError("Project directory '%s' exists already " % project_name)
    if not os.path.isfile(server_file):
        with open(server_file, 'wb') as (f):
            f.write(server_tpl.format(project_name=project_name))
    if not os.path.isfile(requirements_txt):
        with open(requirements_txt, 'wb') as (f):
            f.write('%s==%s' % (PACKAGE.NAME, PACKAGE.__version__))
    copy_resource('%s/%s/' % (PROJECTS_TEMPLATES, template), project_dir)


def main():
    try:
        parser = argparse.ArgumentParser(description='%s %s' % (PACKAGE.NAME, PACKAGE.__version__))
        parser.add_argument('-c', '--create', help='To create a new project. [flask-pilot -c project_name]')
        arg = parser.parse_args()
        if arg.create:
            project_name = arg.create
            template = 'default'
            create_project(project_name, template)
            print "Flask-Pilot '%s' project created successfully " % project_name
            print 'Run server_%s.py to start the server' % project_name
    except Exception as ex:
        print 'ERROR: %s ' % ex.__repr__()