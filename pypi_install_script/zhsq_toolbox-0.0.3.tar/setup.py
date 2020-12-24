#!/usr/bin/env python
import os
import sys
from pathlib import Path

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

package_dir = "toolbox"
packages = [package_dir]
requires = ["maya", "pycryptodomex"]
readme = Path("README.md").read_text()

about = {
}

_filepath = Path(here) / "toolbox/.version.py"
for line in _filepath.read_text().splitlines():
    if "=" in line:
        k, v = line.split("=")
        about[k.strip()] = v.strip(' "')

# 'setup.py publish' shortcut.吃
if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel")
    print("You probably want to also tag the version now:")
    print("  git tag -a {0} -m 'version {0}'".format(about["__version__"]))
    print("  git push --tags")
    sys.exit()

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    license=about["__license__"],
    packages=packages,
    include_package_data=True,
    install_requires=requires,
    python_requires=">=3.6",
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
