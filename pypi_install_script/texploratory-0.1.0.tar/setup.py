# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='texploratory',
    version='0.1.0',
    description='Exploratory Data Analysis tools for text data',
    long_description=readme,
    author='Miori Igarashi',
    author_email='miorgash@gmail.com',
    install_requires=['numpy'],
    url='https://github.com/miorgash/texploratory',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

