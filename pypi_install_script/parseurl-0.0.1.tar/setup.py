#!/usr/bin/env python

# !/usr/bin/env python3
from setuptools import setup
from vparse.version import __version__
import os, codecs, platform
 

def find_packages(*tops):
    packages = []
    for d in tops:
        for root, dirs, files in os.walk(d, followlinks=True):
            if "__init__.py" in files:
                packages.append(root)
    return packages


setup(
    name="parseurl",
    version='0.0.1',
    author="AIR",
    author_email="i@iippcc.com",
    url="https://github.com/airdge/vparse",
    license="MIT",
    description="test",
 
    # install_requires=install_reqs,
    # include_package_data=True,
    python_requires=">=3.0",
    long_description="""ttt""",
    classifiers=["License :: OSI Approved :: MIT License"],
    platforms="any", 
)
