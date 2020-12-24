#!/usr/bin/env python3
import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="snipco",
    version="0.2.1",
    author="Eron Hennessey",
    author_email="eron@abstrys.com",
    description="A command-line clipboard utility and snippet catalog",
    long_description=read('README.rst'),
    long_description_content_type='text/x-rst',
    license="BSD",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    keywords="clipboard snip",
    url = "https://github.com/Abstrys/snipco/",
    packages=find_packages(),
    namespace_packages=["abstrys"],
    include_package_data=True,
    entry_points={
        'console_scripts' : ['snipco = abstrys.snipco:main'],
        },
    install_requires = ['abstrys-core']
)

