#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import os.path
from setuptools import find_packages, setup

with open(
    os.path.join(os.path.dirname(__file__), "README.md"),
    encoding="utf-8"
) as f:
    long_description = f.read()

setup(
    name="changelogmd",
    version="0.2.0",
    description="Python module and CLI tool for CHANGELOG.md manipulation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gronke/py-changelogmd",
    author="Stefan Grönke",
    author_email="stefan@gronke.net",
    python_requires=">=3.6",
    tests_require=["pytest-runner", "pytest"],
    entry_points=dict(
        console_scripts=["changelogmd=changelogmd.__main__:main"]
    ),
    packages=find_packages(exclude=('tests',))
)
