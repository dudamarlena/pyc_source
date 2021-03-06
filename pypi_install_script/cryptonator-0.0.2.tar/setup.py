#!/usr/bin/env/ python
# encoding: utf-8

"""Setuptools configuration file."""

import setuptools

__author__ = 'aldur'


def readme():
    """Try converting the README to an RST document. Return it as is on failure."""
    try:
        import pypandoc
        readme_content = pypandoc.convert('README.md', 'rst')
    except(IOError, ImportError):
        print("Warning: no pypandoc module found.")
        try:
            readme_content = open('README.md').read()
        except IOError:
            readme_content = ''
    return readme_content


setuptools.setup(
    name='cryptonator',
    version='0.0.2',
    description='A simple wrapper for the cryptonator exchange rate API.',
    long_description=readme(),
    url='https://github.com/aldur/cryptonator',

    author='Adriano Di Luzio',
    author_email='adrianodl@hotmail.it',

    py_modules=['cryptonator'],
    install_requires=['requests', ],

    keywords=["cryptonator", ],
    license='MIT',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Development Status :: 6 - Mature",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial",
    ],

    zip_safe=False,
    include_package_data=True,
)
