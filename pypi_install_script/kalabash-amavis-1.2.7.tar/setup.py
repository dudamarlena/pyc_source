#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import io
from os import path

try:
    from pip.req import parse_requirements
except ImportError:
    # pip >= 10
    from pip._internal.req import parse_requirements
from setuptools import find_packages, setup


def get_requirements(requirements_file):
    """Use pip to parse requirements file."""
    requirements = []
    if path.isfile(requirements_file):
        for req in parse_requirements(requirements_file, session="hack"):
            if req.match_markers():
                requirements.append(str(req.req))
    return requirements


if __name__ == "__main__":
    HERE = path.abspath(path.dirname(__file__))
    INSTALL_REQUIRES = get_requirements(path.join(HERE, "requirements.txt"))

    with io.open(path.join(HERE, "README.rst"), encoding="utf-8") as readme:
        LONG_DESCRIPTION = readme.read()

    setup(
        name="kalabash-amavis",
        description="The amavis frontend of Kalabash",
        long_description=LONG_DESCRIPTION,
	version='1.2.7',
        url="https://alphamonak.com/",
        author="Alphamonak Solutions",
        author_email="info@alphamonak.com",
        classifiers=[
            "Environment :: Web Environment",
            "Framework :: Django :: 1.11",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Topic :: Communications :: Email",
            "Topic :: Internet :: WWW/HTTP",
        ],
        keywords="email amavis spamassassin",
        packages=find_packages(exclude=["test_project"]),
        include_package_data=True,
        zip_safe=False,
        install_requires=INSTALL_REQUIRES,
    )
