#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from setuptools import setup, find_packages

setup(
    name="coinsuper_api_rest_sdk",
    version="0.0.3",
    keywords=["pip", "coinsuper", "exchange", "api", "sdk"],
    description="Coinsuper API REST SDK",
    long_description="SDK for Coinsuper API REST endpoints",
    license="Coinsuper",

    url="https://github.com/coinsuperapi/coinsuper-api-rest-python-sdk",
    author="coinsuperapi",
    author_email="",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[]
)
