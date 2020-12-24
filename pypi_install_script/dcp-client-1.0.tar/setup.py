# -*- coding: utf-8 -*-
import sys

# First, we try to use setuptools. If it's not available locally,
# we fall back on ez_setup.
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

with open("README.md") as readmeFile:
    long_description = readmeFile.read()


setup(
    name="dcp-client",
    description="Client to authorize requests against the gen3 DCP",
    packages=[
        "dcp"
    ],
    url="https://github.com/david4096/dcp",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'requests'
    ],
    license='Apache License 2.0',
    zip_safe=False,
    author="David Steinberg",
    author_email="david@resium.com",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    version="1.0"
)
