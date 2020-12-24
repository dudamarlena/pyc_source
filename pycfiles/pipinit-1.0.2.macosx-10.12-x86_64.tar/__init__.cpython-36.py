# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yuan/p/pipinit/.venv/lib/python3.6/site-packages/__init__.py
# Compiled at: 2017-11-09 21:37:48
# Size of source mod 2**32: 1291 bytes
from os import path, getcwd
import click

def inputWithDefault(prompt, default=''):
    inputGot = input(prompt)
    if inputGot == '':
        inputGot = default
    return inputGot


@click.command()
def cli():
    if path.isfile(getcwd() + '/setup.py'):
        print('setup.py exists, will not overwrite')
        return
    dirName = getcwd().split('/')[(-1)]
    name = inputWithDefault('Name of the project({}): '.format(dirName), dirName)
    version = inputWithDefault('Current version(1.0.0): ', '1.0.0')
    description = inputWithDefault('Short description: ')
    url = inputWithDefault('URL: ')
    author = inputWithDefault('Author: ')
    author_email = inputWithDefault('Author email: ')
    license = inputWithDefault('License(MIT): ', 'MIT')
    python_requires = inputWithDefault('Python requires(>=3): ', '>=3')
    text = "from setuptools import setup, find_packages\nsetup(\n    name='{}',\n    version='{}',\n    description='{}',\n    url='{}',\n    author='{}',\n    author_email='{}',\n    license='{}',\n    packages=find_packages(),\n    python_requires='{}'\n    )".format(name, version, description, url, author, author_email, license, python_requires)
    with open('setup.py', 'w') as (f):
        f.write(text)