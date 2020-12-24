#!/usr/bin/env python3

from setuptools import setup
from english_words.version import NAME, DESCRIPTION, VERSION


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
    name=NAME,
    version=VERSION,
    description=capitalize(DESCRIPTION),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mwiens91/english-words-py',
    author='Matt Wiens',
    author_email='mwiens91@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
    ],
    packages=['english_words'],
)
