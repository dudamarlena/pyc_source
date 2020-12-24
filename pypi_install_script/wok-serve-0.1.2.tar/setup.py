#!/usr/bin/env python3
import os
from setuptools import setup, find_packages
from pathlib import Path

# Read README
with open(Path(__file__).parent / "README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="wok-serve",
    version="0.1.2",
    author="Tijl Van den Brugghen",
    author_email="me@tijlvdb.me",
    url="https://gitlab.com/tijlvdb/wok-serve",
    description="Tool to serve a directory of Wok files using a Notion-like template.",
    long_description_content_type="text/markdown",
    long_description=long_description,
    license="MIT",
    packages=find_packages(),
    package_data={"wok_serve": ["static/*", "templates/*"]},
    install_requires=["bottle>=0.12,<0.13", "wok-compiler>=0.1,<0.2"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
    ],
    entry_points={"console_scripts": ["wok-serve = wok_serve.cli:run"]},
)
