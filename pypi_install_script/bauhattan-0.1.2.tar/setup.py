#!/usr/bin/env python

from setuptools import setup

setup(
    name='bauhattan',
    version='0.1.2',
    packages=[
        'bauhattan',
        'bauhattan.connectors',
        ],
    license='MIT License',
    long_description=open('README.txt').read(),
    author='izrik',
    author_email='izrik@yahoo.com',
    url='https://github.com/izrik/bauhattan',
    description='Automated CI/CD Tool',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
    install_requires=[
        'requests',
    ],
)
