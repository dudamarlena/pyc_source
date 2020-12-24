#!/usr/bin/env python

from distutils.core import setup

setup(
    name='serverlaze',
    version='0.0.1',
    description='Reblaze RASP',
    long_description='''Reblaze Serverlaze RASP''',
    author='Elon Salfati',
    author_email='elon@reblaze.com',
    url='http://reblaze.com',
    packages=['serverlaze'],
    package_dir={'serverlaze': 'serverlaze'},
)