"""
DS-OOP-Review has two modules that I am using to learn this week
"""
import setuptools
import unittest

REQUIRED = [
    "numpy",
    "pandas"
    
]

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()
    setuptools.setup(
    name="DS-OOP-Review",
    version = "0.1.2",
    author = "Zebfred",
    description = "two modules",
    long_description = LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/Zebfred/DS-OOP-Review",
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    install_requires = REQUIRED,
    classifiers=["Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ]
    )