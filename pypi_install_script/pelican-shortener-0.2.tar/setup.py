#!/usr/bin/python3

"""setup.py for pelican-shortener."""

from setuptools import find_packages
from setuptools import setup

setup(
    name="pelican-shortener",
    version="0.2",
    description="Plugin for pelican to shorten URLs",
    author="Felipe S. S. Schneider",
    author_email="schneider.felipe@posgrad.ufsc.br",
    url="https://github.com/schneiderfelipe/pelican-shortener",
    license="MIT",
    packages=find_packages(),
    install_requires=["pelican>=4.0.0", "pyshorteners>=1.0.0"],
    classifiers=(
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Framework :: Pelican",
        "Framework :: Pelican :: Plugins",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ),
)
