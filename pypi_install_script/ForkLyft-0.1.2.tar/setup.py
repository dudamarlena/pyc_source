"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='ForkLyft',
    version='0.1.2',
    description='Automates AWS Multi-Account and enforces naming '
                'conventions for an organization.',
    url='https://github.com/DjangoFett/ForkLyft',
    author='Jake Myshrall',
    author_email='jmyshrall@cvent.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'Topic :: Other/Nonlisted Topic',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'forklyft=forklyft.cli:main',
        ],
    },
    # projvect_urls={  # Optional
    #     'Bug Reports': 'https://github.com/pypa/sampleproject/issues',
    #     'Funding': 'https://donate.pypi.org',
    #     'Say Thanks!': 'http://saythanks.io/to/example',
    #     'Source': 'https://github.com/pypa/sampleproject/',
    # },
)
