# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\dropbox\dropbox\projects\python\do-pack\do\skeleton.py
# Compiled at: 2018-03-04 17:12:09
# Size of source mod 2**32: 2805 bytes
"""
Create a default folder and a file structure for a
python package based on the name of the project.
"""
import os, sys, json, click

def make_skeleton(project_name, template=False):
    """
    Create a default structure for a python project.
    """
    if template:
        loaded_template = load_template(template)
    else:
        loaded_template = load_template()
    for folder in loaded_template.keys():
        makedir(folder, project_name)
        for files in loaded_template[folder]:
            makefile(files, project_name)


def load_template(template=False):
    """
    Load the default or custom template for the python package.
    """
    if template:
        full_template = template + '.json'
        if os.path.exists(os.path.join(os.getcwd(), full_template)):
            path = os.path.join(os.getcwd(), full_template)
        else:
            path = os.path.join(os.path.dirname(__file__), 'templates', full_template)
    else:
        path = os.path.join(os.path.dirname(__file__), 'templates', 'default_structure.json')
    try:
        with open(path, 'r') as (template):
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


def makefile(file, project_name):
    """
    Write the files for the project_name
    """
    if file == 'project.py':
        file = '{}'.format(project_name + '.py')
    elif file == 'test_project.py':
        file = '{}'.format('test_' + project_name + '.py')
    else:
        if file == '<--':
            os.chdir('..')
        else:
            try:
                with open(file, 'w') as (f):
                    f.write('')
            except Exception as e:
                click.echo('Error wrinting {}. Aborted!'.format(file))
                sys.exit(1)


if __name__ == '__main__':
    pass