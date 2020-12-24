#!/usr/bin/env python

#
# [setup.py]
#
# The installer for the git_downloader language.
# Copyright (C) 2019, Liam Schumm.
#

from setuptools import setup, find_packages

setup(
    name="git_downloader",
    version="1.0.2",
    description="Downloads all the respositories from a GitHub and/or GitLab user's account.",
    long_description=open("README.rst").read(),
    author="Liam Schumm",
    author_email="liamschumm@icloud.com",
    python_requires=">=3",
    url="https://gitlab.com/lschumm/git_downloader",
    packages=find_packages(exclude=('tests',)),
    entry_points={
        'console_scripts': ['git_downloader=git_downloader:main'],
    },
    requirements=["PyGithub", "python-gitlab"],
    include_package_data=True,
    license='GPL',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
    ]
)
