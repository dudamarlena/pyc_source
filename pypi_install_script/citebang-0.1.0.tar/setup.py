#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains setup script for installing this package.

from setuptools import setup


def read_file(filename):
    """ Returns content of file as a string.
    """
    with open(filename) as f:
        return f.read()


def parse_requirements_txt(filename):
    """ Used to parse requirements.txt files.
    """
    lines = (line.strip() for line in open(filename))
    return [line for line in lines if line and not line.startswith("#")]


setup(

    #
    # PACKAGE INFORMATION
    #

    name="citebang",
    version="0.1.0",

    description="open-source tool used for academic literature searches",
    long_description=read_file("README.rst"),
    long_description_content_type='text/x-rst',

    url="https://bitbucket.org/averr/citebang/",
    license="MIT",

    python_requires=">=3",
    packages=["citebang"],
    install_requires=parse_requirements_txt("requirements.txt"),

    author="Alan Verresen",
    author_email="",

    entry_points={
        'console_scripts': [
            'citebang=citebang.__main__:main',
        ],
    },

    #
    # PYPI METADATA
    #

    keywords=" ".join([
        "science",
        "research",
        "academics",
        "citation",
        "citations",
        "literature",
        "search",
    ]),

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
    ],

    project_urls={
        'Source': "https://bitbucket.org/averr/citebang/",
        'Tracker': "https://bitbucket.org/averr/citebang/issues",
    },

)
