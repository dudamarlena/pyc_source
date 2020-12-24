#!/usr/bin/env python3

import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aquila",
    packages=["aquila"],
    version="0.4",
    license="GPL3",
    description="ASCII Screen Splash for SHYCD software.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Carlos A. Planchón",
    author_email="bubbledoloresuruguay2@gmail.com",
    url="https://github.com/carlosplanchon/aquila",
    download_url="https://github.com/carlosplanchon/"
        "aquila/archive/v0.4.tar.gz",
    keywords=["ascii", "screen", "splash"],
    install_requires=[
        "colored",
        "pendulum"
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
