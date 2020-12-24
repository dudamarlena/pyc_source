# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\dropbox\dropbox\projects\python\do-pack\do\assist_skeleton.py
# Compiled at: 2018-02-28 18:47:52
# Size of source mod 2**32: 3013 bytes
"""
Create de skeleton of the python project and
Redirect the files and folders to the proper function.

Also write the AUTHORS.rst, LICENSE and setup.py with
the users inputs.
"""
import os, sys, json, click

def make_skeleton(project_name, authors, choosen_license, setup):
    """
    Create de skeleton of the python project and
    Redirect the files and folders to the proper function.
    """
    for folder in load_template().keys():
        makedir(folder, project_name)
        for files in load_template()[folder]:
            makefile(files, project_name, authors, choosen_license, setup)


def load_template():
    """
    Load the template for the python package
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
    Make the folders tree.
    """
    if directory == 'base' or directory == 'bin':
        directory = project_name
    try:
        os.makedirs(directory)
        os.chdir(directory)
    except FileExistsError:
        click.echo('Folder {} alredy exists. Aborted!'.format(directory))
        sys.exit(1)


def makefile(file, project_name, authors, choosen_license, setup):
    """
    Make the files for the project and write the content
    of AUTHORS.rst, LICENSE and setup.py in assistant mode
    """
    if file == 'project.py':
        file = project_name + '.py'
    else:
        if file == 'test_project.py':
            file = 'test_' + project_name + '.py'
    template_files = {'LICENSE':lambda : writefile(file, choosen_license), 
     'AUTHORS.rst':lambda : writefile(file, authors), 
     'setup.py':lambda : writefile(file, setup)}
    template_files.get(file, lambda : writefile(file))()


def writefile(file, content=''):
    """
    Function that write the files and go back one folder
    for the sake of the stucture.
    """
    if file == '..':
        os.chdir('..')
    else:
        try:
            with open(file, 'w') as (f):
                f.write(content)
        except Exception as e:
            click.echo('Error wrinting {}. Aborted!'.format(file))
            sys.exit(1)


if __name__ == '__main__':
    pass