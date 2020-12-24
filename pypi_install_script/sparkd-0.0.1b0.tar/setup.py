# -*- coding: utf-8 -*-

"""
setup.py
"""

from setuptools import setup
from setuptools import find_packages


with open('README.md', 'r') as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name='sparkd',
    version='0.0.1b',
    author='Ivan Lopez',
    author_email='ivan@askai.net',
    description='Spark Networks DevOps coding challenge',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/askainet/spark-networks-code-challenge',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    extras_require={
        'dev': [
            'pylint',
            'sphinx',
            'twine',
        ]
    },
    python_requires='>=3.4, <4',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: POSIX'
    ],
    entry_points={
        'console_scripts': [
            'sparkd = sparkd.main:main',
        ],
    },
    test_suite='tests'
)
