# Copyright (c) Microsoft Corporation
# This source code is licensed under the MIT license

from os import path
from setuptools import setup, find_packages

with open(
    path.join(path.abspath(path.dirname(__file__)), "README.md"),
    encoding="utf-8",
) as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    install_requires = f.read().splitlines()

setup(
    name="mssibyl",
    version="0.1.1.dev0",
    license="MIT",
    description="Time Series Forecasting Tool for Machine Learning Researchers with Nerual Process",
    packages=find_packages(),
    author="More Zhou",
    author_email="jinyzho@microsoft.com",
    keywords=["time series forecasting", "deep learning", "pytorch"],
    install_requires=["numpy", "pytorch-lightning", "pandas"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
