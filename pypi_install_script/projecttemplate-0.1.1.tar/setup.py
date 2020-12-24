#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    README = readme_file.read()

with open("HISTORY.rst") as history_file:
    HISTORY = history_file.read()

REQUIREMENTS = ["appdirs", "pandas"]

SETUP_REQUIREMENTS = []

TEST_REQUIREMENTS = ["pytest"]

DESCRIPTION = (
    "A template utility for data-science projects using Python that "
    "provides a skeletal project. http://projecttemplate.net"
)

setup(
    author="Hugo van den Berg",
    author_email="hugo@tbdwebdesign.nl",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description=DESCRIPTION,
    install_requires=REQUIREMENTS,
    license="GNU General Public License v3",
    long_description=README + "\n\n" + HISTORY,
    include_package_data=True,
    keywords="projecttemplate_python",
    name="projecttemplate",
    packages=find_packages(include=["projecttemplate"]),
    setup_requires=SETUP_REQUIREMENTS,
    test_suite="tests",
    tests_require=TEST_REQUIREMENTS,
    url="https://github.com/Hugovdberg/projecttemplate_python",
    version="0.1.1",
    zip_safe=False,
)
