#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''The setup script.'''

from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='whatifmachine',
    version='0.1.0',
    description='',
    long_description=readme(),
    author='Mark Bell',
    author_email='mcbell@illinois.edu',
    url='https://github.com/MarkCBell/whatifmachine',
    packages=find_packages(),
    entry_points='''
    [gui_scripts]
    whatifmachine=whatifmachine.__main__:main
    ''',
    include_package_data=True,
    install_requires=['attr'],
    license='MIT License',
    zip_safe=False,
    keywords='profiling',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Mathematics',
        ],
)

