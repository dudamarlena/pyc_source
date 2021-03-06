# coding: utf-8

"""
    Stroy API

    This api serves as and entry point for managing stories on the presaltytics api  # noqa: E501

    OpenAPI spec version: 3.0.2
    Generated by: https://openapi-generator.tech
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "presalytics_story"
VERSION = "0.1.63"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "urllib3 >= 1.15", 
    "six >= 1.10", 
    "certifi", 
    "python-dateutil"
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=NAME,
    version=VERSION,
    description="Story API",
    author_email="kevin@presalytics.io",
    url="http://github.com/presalytics/story-python-client",
    keywords=["presalytics", "Story API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description_content_type="text/markdown",
    long_description=long_description
)
