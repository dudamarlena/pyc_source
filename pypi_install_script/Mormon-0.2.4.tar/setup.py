#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='Mormon',
    packages=find_packages(),
    version='0.2.4',
    author='Travis Beauvais',
    author_email='tbeauvais@gmail.com',
    url='https://github.com/MrTravisB/mormon',
    keywords='mongo mongodb orm',
    install_requires=[
        'inflection>=0.2.0',
        'pymongo>=2.5.2',
    ],
    description='An object relational mapping library for MongoDB'
)
