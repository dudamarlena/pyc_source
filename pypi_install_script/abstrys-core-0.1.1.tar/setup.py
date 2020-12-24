#!/usr/bin/env python3
# ~~ coding=utf-8 ~~
import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="abstrys-core",
    version="0.1.1",
    author = "Eron Hennessey",
    author_email = "eron@abstrys.com",
    description = "Core modules for Abstrys command-line applications",
    long_description=read('README.rst'),
    long_description_content_type='text/x-rst',
    license = "BSD",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    keywords = "python module",
    url = "https://github.com/Abstrys/abstrys-core/",
    packages=['abstrys'],
    namespace_packages=["abstrys"],
)
