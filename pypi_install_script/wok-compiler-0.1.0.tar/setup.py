#!/usr/bin/env python3
import os
from setuptools import setup, find_packages
from pathlib import Path

# Read README
with open(Path(__file__).parent / "README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="wok-compiler",
    version="0.1.0",
    author="Tijl Van den Brugghen",
    author_email="me@tijlvdb.me",
    url="https://gitlab.com/tijlvdb/wok",
    description="Advanced yet human-readable markup language",
    long_description_content_type="text/markdown",
    long_description=long_description,
    license="MIT",
    packages=find_packages(),
    install_requires=["markdown==3.1"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
    ],
    entry_points={"console_scripts": ["wok = wok.cli:run"]},
)
