# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "broad_pgm_translator"
VERSION = "0.1"

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
    description="Broad probabilistic graphical models translator",
    author_email="translator@broadinstitute.org",
    url="https://github.com/mjstealey/broad-pgm-translator",
    maintainer="Michael J. Stealey",
    maintainer_email="stealey@renci.org",
    keywords=["pgm", "Broad probabilistic graphical models translator"],
    install_requires=REQUIRES,
    packages=find_packages(),
    download_url='https://github.com/mjstealey/broad_pgm_translator/archive/0.1.tar.gz',
    include_package_data=True,
    long_description="""\
    Broad probabilistic graphical models translator
    """
)

