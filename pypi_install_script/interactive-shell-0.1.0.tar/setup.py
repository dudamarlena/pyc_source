# -*- coding: utf-8 -*-
import os
from setuptools import setup

current_directory = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(current_directory, "VERSION"), "r", encoding="utf-8") as f:
    version = f.read()

with open(os.path.join(current_directory, "README.rst"), "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="interactive-shell",
    version=version,
    description="Interactive shell classes to easily integrate a terminal in application.",
    long_description=long_description,
    license="MIT License",
    author="Julien Vaslet",
    author_email="julien.vaslet@gmail.com",
    url="https://github.com/julienvaslet/interactive-shell",
    packages=["interactive_shell"],
    install_requires=[],
    scripts=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development",
        "Topic :: Terminals"
    ]
)
