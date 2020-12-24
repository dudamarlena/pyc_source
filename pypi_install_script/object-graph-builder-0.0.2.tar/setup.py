import os
from codecs import open

from setuptools import setup, find_packages

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
VERSION = __import__('object_graph').__version__

with open(os.path.join(BASE_DIR, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='object-graph-builder',
    version=VERSION,
    description='Provides an interface to build the dependency injection container.',
    long_description=long_description,
    url='https://github.com/eshta/object-graph-builder',
    project_urls={
        'Bug Reports': 'https://github.com/eshta/object-graph-builder/issues',
        'Source': 'https://github.com/eshta/object-graph-builder',
    },
    author='Omar Shaban',
    author_email='o.shaban.000@gmail.com',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=['decorator', 'pinject'],
    include_package_data=True,
    keywords='Dependency injection, dependency-injection, dependency-injection-container,'
             ' dependency-injection-framework, design-patterns, factory, ioc, ioc-container, python, pinject, '
             'singleton',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries  '
    ],
)
