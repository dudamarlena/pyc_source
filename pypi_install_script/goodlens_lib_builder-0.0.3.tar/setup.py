# coding: utf-8

"""
    goodlens_lib_builder

    Utility package for goodlens builder

"""


import sys
from setuptools import setup, find_packages

NAME = "goodlens_lib_builder"
VERSION = "0.0.3"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = []

setup(
    name=NAME,
    version=VERSION,
    description="",
    author_email="swcbok@gmail.com",
    url="",
    keywords=["GoodLens", "goodlens_builder"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    """
)
