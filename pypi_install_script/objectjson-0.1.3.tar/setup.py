# -*- coding: utf-8 -*-
#!/usr/bin/python

import objectjson
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

with open('README.rst', 'r') as f:
    readme = f.read()
with open('HISTORY.rst', 'r') as f:
    history = f.read()

setup(
    name='objectjson',

    description='A python tool to create Python objects from large, complicated JSON objects. Dictionaries are great and all, but large nested ones can get tedious.',
    long_description=readme + '\n\n' + history,

    url='https://github.com/abmohan/objectjson',
    download_url='https://github.com/abmohan/objectjson/tarball/master',

    version=objectjson.__version__,
    license=objectjson.__license__,

    author=objectjson.__author__,
    author_email='abmohan@gmail.com',

    packages=['objectjson'],

    classifiers=[],

    keywords = "json",

)
