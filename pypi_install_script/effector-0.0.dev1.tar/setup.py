# coding: utf-8

import os

from setuptools import find_packages, setup, Command


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    long_description = '\n' + f.read()

install_required = []

setup(
    name='effector',
    version='0.0.dev1',
    description='Universal GUI framework based on WebAssembly',
    long_description=long_description,
    author='Rin Arakaki',
    author_email='rnarkkx@gmail.com',
    url='https://github.com/rnarkk/effector',
    packages=find_packages(exclude=('tests',)),
    install_requires=install_required,
    include_package_data=True,
    license='Apache License 2.0',
    classifiers=[
        'Programming Language :: Python'])
