"""
appnexus-client
"""

import os
import subprocess
import sys
from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def get_version():
    if not os.path.isdir(".git"):
        sys.stderr.write("This does not appear to be a Git repository.")
        return ""
    return subprocess.check_output(["git", "describe", "--tags", "--always"],
                                   universal_newlines=True)[:-1]

setup(
    name="pypi-interface",
    version=get_version(),
    author="Alexandre Bonnetain",
    author_email="alexandrebonnetain@gmail.com",
    description="pypi-interface is meant to serve as a client for pypi use",
    url="https://github.com/shir0kamii/pypi-interface",
    download_url="https://github.com/shir0kamii/pypi-interface/tags",
    platforms="any",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
