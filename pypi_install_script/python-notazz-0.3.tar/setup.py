#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='python-notazz',
    version='0.3',
    description="Notazz Python Binding",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
    author='Joao Carvalho',
    author_email='joao.carvalho@maestrus.com',
    install_requires=[
        "requests>=2.22.0",
        "urllib3>=1.25.6",
    ],
    url='https://github.com/jdcarvalho/python-notazz',
    packages=find_packages(),
)
