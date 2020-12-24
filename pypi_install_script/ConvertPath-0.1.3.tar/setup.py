# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name="ConvertPath",
    version="0.1.3",
    packages=find_packages(),

    install_requires=['pathlib'],

    # metadata to display on PyPI
    author="Shinya Akagi",
    description="Simple Path Convertor",
    long_description=readme,
    url="https://github.com/ShinyaAkagiI/convertpath", 
    license="PSF",
)
