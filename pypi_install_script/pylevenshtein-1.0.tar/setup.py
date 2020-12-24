from setuptools import setup, find_packages
import os
from distutils.core import Extension

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name='pylevenshtein',
    version='1.0',
    license='GPL',
    author='Rahul Prabhu',
    author_email='grokwithahul@gmail.com',
    description='Levenshtein project for python',
    long_description=open("README.md").read(),
    project_urls={
        "Source": "https://github.com/Redstomite/py-levenshtein",
        "Say Thanks!": "https://saythanks.io/to/grokwithrahul%40gmail.com",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
