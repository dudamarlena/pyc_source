"""Setup script for lixi2 package project"""

import os.path
from setuptools import setup, find_packages

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="lixi-ammar",
    version="0.0.29",
    description="lixi is a python package to manipulate a valid LIXI message and schema.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://standards.lixi.org.au/lixi-tech/lixi-pypi",
    author="Ammar Khan",
    author_email="lixilab@lixi.org.au",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(exclude=['build','dist','lixi.egg-info','lixi_ammar.egg-info','tests','.git', 'docs']),
    include_package_data=True,
    install_requires=['lxml>=4.4.1','isodate>=0.6.0','boto3>=1.9.238','xmljson>=0.2.0','jsonschema>=3.0.2','s3transfer>=0.2.1','botocore>=1.12.238'] 
)
