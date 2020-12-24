"""
Setup script for taskmgr
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.
version = "0.0.0-1" #NOTE: please blame pypy for the weird version numbers...

setup(
    name='taskmgr',
    version=version,
    description="taskmgr - A simple to use task manager",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/dsikes/taskmgr',
    author='Dan Sikes',
    author_email='dansikes7@gmail.com',
    keywords='task manager, automation',
    packages=find_packages(),
    install_requires=['requests'],

    project_urls={
        'Source': 'https://gitlab.com/dsikes/taskmgr',
    },
)