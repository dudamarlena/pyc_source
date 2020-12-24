from setuptools import setup
import setuptools
from distutils.core import Extension
import os

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name='MARC_prototype',
    license='GPL',
    version='0.3',
    author_email="grokwithahul@gmail.com",
    description="NYAS COVID-19 Challenge",
    long_description=open("README.md").read(),
    packages=setuptools.find_packages(),
    project_urls={
        "Source": "https://github.com/Redstomite/MARC-prototype",
    },
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
    ],
    author='Rahul Prabhu',
)
