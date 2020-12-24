#!/usr/bin/env python3

from setuptools import setup
from mario_battle.version import (
    BINARY_NAME,
    DESCRIPTION,
    HOME_URL,
    PYPI_NAME,
    VERSION,)


# Parse readme to include in PyPI page
with open('README.md') as f:
    long_description = f.read()

def capitalize(s):
    """Capitalize the first letter of a string.

    Unlike the capitalize string method, this leaves the other
    characters untouched.
    """
    return s[:1].upper() + s[1:]

setup(
    name=PYPI_NAME,
    version=VERSION,
    description=capitalize(DESCRIPTION),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=HOME_URL,
    author='Branko Bajcetic, Matt Wiens',
    author_email='bajcetic.branko@gmail.com, mwiens91@gmail.com',
    license='BSD 3-clause "New" or "Revised License"',
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=['mario_battle'],
    entry_points={
        'console_scripts': [BINARY_NAME + ' = mario_battle.main:main'],
    },
    python_requires='>=3.5',
    install_requires=[
        'colorama',
    ],
)
