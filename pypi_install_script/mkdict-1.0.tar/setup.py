import setuptools
import sys
import os

version = '1.0'

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mkdict",
    version=version,
    author="Anton Dries",
    author_email="anton.dries@gmail.com",
    description="A multi-key dictionary with wildcard lookup.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    python_requires='>=3.5'
)
