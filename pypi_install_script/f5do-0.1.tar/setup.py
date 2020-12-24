#!/usr/bin/env python
from setuptools import setup, find_packages

import os
import sys
if sys.version_info[0] < 3:
    with open('README.rst') as f:
        long_description = f.read()
else:
    with open('README.rst', encoding='utf-8') as f:
        long_description = f.read()

setup(
        name="f5do",
        version="0.1",
        packages=find_packages(),
        install_requires=['iCR>=2.4'],
        long_description=long_description,
        author="Pete White",
        author_email="pwhite@f5.com",
        description="This is a Python module to easily use the F5 Declarative Onboarding interface",
        license="PSF",
        url="https://pypi.python.org/pypi?:action=display&name=f5do&version=0.1",
        include_package_data = True
)
