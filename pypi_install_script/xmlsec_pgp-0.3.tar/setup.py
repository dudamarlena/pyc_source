#!/usr/bin/env python3

from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    author_email="luke@lukeross.name",
    author="Luke Ross",
    description="xmlenc and xmldsig XML encryption and signing using PGP keys",
    install_requires=["cryptography", "lxml", "pgpy", "xmlsec"],
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    name="xmlsec_pgp",
    packages=["xmlsec_pgp"],
    url="http://lukeross.name/projects/xmlsec_pgp",
    version="0.3",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Topic :: Text Processing :: Markup :: XML"
    ]
)
