#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    # Use setuptools if available, for install_requires (among other things).
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='pyptm',
    packages=['pyptm'],
    version='0.0.6',
    description='The linux performance toolkit',
    long_description=open('README.md').read(),
    author='leviathan1995',
    author_email='leviathan0992@gmail.com',
    url='https://github.com/Leviathan1995/pyptm',
    license='MIT',
    install_requires=[
        'pygrape',
        'PyYAML'
    ],
    entry_points={
        'console_scripts': [
            'pyptm = pyptm.pyptm:main'
        ]
    },
    include_package_data=True,
    data_files=[('/usr/local/', ['tools.yml'])]
)
