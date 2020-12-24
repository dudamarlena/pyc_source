#!/usr/bin/env python

from setuptools import find_packages, setup

__version__ = '0.1.0'

setup(
    name='skript',
    version=__version__,
    license='MIT',
    description='',
    author='Noel Martignoni',
    author_email='noel@martignoni.fr',
    url='https://gitlab.com/xneomac/skript',
    scripts=['scripts/skript'],
    install_requires=[
        'mistune',
        'soundfile',
        'gtts',
        'pydub',
        'termcolor',
    ],
    packages=find_packages(exclude=['tests*']),
)
