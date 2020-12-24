# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\dropbox\dropbox\projects\python\do-pack\do\test.py
# Compiled at: 2018-02-28 17:58:00
# Size of source mod 2**32: 1956 bytes
import os, sys, json, click

def create_empty_skeleton(project_name):
    """
    Creates an empty folder and file structure for a python project.
    """
    for folder in load_template().keys():
        makedir(folder, project_name)
        for files in load_template()[folder]:
            makefile(files, project_name)


def load_template():
    """
    Load the default template for the python package.
    """
    try:
        default_skeleton = os.path.join(os.path.dirname(__file__), 'templates', 'default_structure.json')
        with open(default_skeleton) as (template):
            return json.load(template)
    except FileNotFoundError:
        click.echo('Template file not found. Aborted!')
        sys.exit(1)


def makedir(directory, project_name):
    """
    Make the folder tree.
    """
    if directory == 'base' or directory == 'bin':
        directory = project_name
    try:
        os.makedirs(directory)
        os.chdir(directory)
    except FileExistsError:
        click.echo('Folder {} alredy exists. Aborted!'.format(directory))
        sys.exit(1)


def makefile(file, project_name, assist=False):
    """
    Write the files for the project_name
    """
    if file == 'project.py':
        file = '{}'.format(project_name + '.py')
    elif file == 'test_project.py':
        file = '{}'.format('test_' + project_name + '.py')
    else:
        if file == '..':
            os.chdir('..')
        else:
            try:
                with open(file, 'w') as (f):
                    f.write('')
            except Exception as e:
                click.echo('Error wrinting {}. Aborted!'.format(file))
                sys.exit(1)