#!/usr/bin/env python
from setuptools import setup

setup(
    name='cd-python-plugin',
    version='0.0.0',
    description='Cloud Defense Python scanner plugin',
    packages=["src"],
    python_requires='>=3.5, <4',
    install_requires=['requests'],
    entry_points={  # Optional
        'console_scripts': [
            'scan=scanner:main',
        ],
    },
)