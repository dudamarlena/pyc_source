# coding: utf-8

"""
    Ruler API

    Ruler API is a flexible API for rules. Originally designed for FIRST Robotics Competition, it is flexible in nature to allow for any program to use it.  # noqa: E501

    OpenAPI spec version: 1.0.0
    Generated by: https://openapi-generator.tech
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "frcrules"
VERSION = "1.0.1"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]

setup(
    name=NAME,
    version=VERSION,
    description="Ruler API",
    author_email="",
    url="",
    keywords=["OpenAPI", "OpenAPI-Generator", "Ruler API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    Ruler API is a flexible API for rules. Originally designed for FIRST Robotics Competition, it is flexible in nature to allow for any program to use it.  # noqa: E501
    """
)
