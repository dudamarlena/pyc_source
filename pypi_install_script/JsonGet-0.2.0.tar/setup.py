# -*- coding:UTF-8 -*-
#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="JsonGet",
    version="0.2.0",
    author="Dennis Wang",
    author_email="dennis.wang@detvista.com",
    license="Apache License",
    url="https://github.com/cortexiphan1/JsonGet",
    packages=["JsonGet"],
    install_requires=["simplejson"],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6"
    ],
)
