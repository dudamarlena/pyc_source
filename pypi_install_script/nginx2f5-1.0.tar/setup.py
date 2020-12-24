#!/usr/bin/env python
from setuptools import setup, find_packages
setup(
        name="nginx2f5",
        version="1.0",
        packages=find_packages(),
        install_requires=['re'],
        author="Pete White",
        author_email="pwhite@f5.com",
        description="This is a Python script to convert nginx configuration to F5 syntax",
        license="PSF",
        url="https://pypi.python.org/pypi?:action=display&name=nginx2f5&version=1.0",
)
