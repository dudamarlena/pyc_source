#! /usr/bin/env python
import os
from setuptools import setup
from finitelycomputable_microsites_setup import version, base_setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='finitelycomputable-morepath-mount',
    version=version,
    py_modules=['finitelycomputable.morepath_mount'],
    entry_points={
        'console_scripts': [
            'finitelycomputable-morepath-mount = finitelycomputable.morepath_mount:run']
        },
    description='The Morepath-based wsgi app using Morepath.mount to combine the microsites of finitelycomputable.net',
    long_description=README,
    long_description_content_type="text/x-rst",
    scripts=['finitelycomputable_microsites_setup.py'],
    install_requires=['morepath~=0.18'],
    extras_require={
        'helloworld': ['finitelycomputable-helloworld-morepath~=' + version],
        'bjoern': ['bjoern<4'],
        'cheroot': ['cheroot<9'],
        'cherrypy': ['cherrypy<19'],
        'gunicorn': ['gunicorn<20'],
        'waitress': ['waitress<1.4'],
        },
    url='https://www.finitelycomputable.net/',
    **base_setup
)
