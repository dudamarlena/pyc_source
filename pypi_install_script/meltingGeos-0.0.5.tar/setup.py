#!/usr/bin/env python
import io
from setuptools import setup, find_packages

version = "0.0.5"

setup(
    name="meltingGeos",
    version=version,
    url='https://github.com/arrebole/meltingGeos',
    description='Find standard city info names by obfuscated names;',
    include_package_data=True,
    packages=find_packages(),
    keywords="meltingGeos",
)