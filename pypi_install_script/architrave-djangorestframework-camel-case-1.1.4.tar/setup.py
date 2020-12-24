#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

readme = open("README.rst").read()
history = open("HISTORY.rst").read().replace(".. :changelog:", "")
import architrave_djangorestframework_camel_case

setup(
    name="architrave-djangorestframework-camel-case",
    version=architrave_djangorestframework_camel_case.__version__,
    description="Camel case JSON support for Django REST framework.",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/x-rst",
    author="Jeremy Mayeres",
    author_email="jeremy@jerr.dev",
    url="https://github.com/architrave-de/djangorestframework-camel-case",
    packages=["architrave_djangorestframework_camel_case"],
    package_dir={
        "architrave_djangorestframework_camel_case": "architrave_djangorestframework_camel_case"
    },
    include_package_data=True,
    python_requires=">=3.5",
    install_requires=[],
    license="BSD",
    zip_safe=False,
    keywords="djangorestframework_camel_case",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    test_suite="tests",
)
