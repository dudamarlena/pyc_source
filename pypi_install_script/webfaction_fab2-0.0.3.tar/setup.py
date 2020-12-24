#!/usr/bin/env python

from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

def read(fname):
    return open(path.join(here, fname)).read()

setup(
    name="webfaction_fab2",
    version="0.0.3",
    description=("Scripts to help provision, configure and deply to"
                 "webfaction using Python and Fabric 2"),
    url="https://github.com/moaxey/wf_fab2",
    packages=["wf_fab2",],
    python_requires='>3.6',
    install_requires=[
        "fabric",
        "dnspython",
        "requests",
    ],
    author="Mathew Oakes",
    author_email="open@mathewoak.es",
    license="MIT",
    long_description=read("README.rst"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
)
