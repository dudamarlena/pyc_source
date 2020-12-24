#!/usr/bin/env python3

from setuptools import setup
from yaft.version import (
    PYPI_NAME,
    DESCRIPTION,
    VERSION,
)


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
    url='https://github.com/mwiens91/yaft',
    author='Matt Wiens',
    author_email='mwiens91@gmail.com',
    license='BSD 3-clause "New" or "Revised License"',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=['yaft'],
    entry_points={
        'console_scripts': ['yaft = yaft.main:main'],
    },
    python_requires='>=3.5',
    install_requires=[
        'peewee',
        'PyYAML',
    ],
)
