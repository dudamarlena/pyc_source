#!/usr/bin/env python3
import sys
from setuptools import setup, find_packages
from pathlib import Path

long_description = (Path(__file__).parent / "README.md").read_text()

setup(
    name="j2scr",
    version="1.0.1",
    license="MIT",
    author="Jonas Lundholm Bertelsen",
    packages=find_packages(),
    install_requires=["jinja2"],
    description="Convenience wrapper around Jinja for scripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonaslb/j2scr",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
