#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = ['numpy', 'scikit-learn']

setup_requirements = ['pytest-runner', 'numpy', 'scikit-learn']

test_requirements = ['pytest']

setup(
    author="Ekaba Bisong",
    author_email='dvdbisong@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        # Indicate who your project is intended for
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    description="Data structures that re-organize based on queries received from a non-stationary environment",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,  # + '\n\n' + history,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='learning automata, reinforcement learning, adaptive data structures',
    name='adaptive-data-structures',
    packages=find_packages(include=['src']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/dvdbisong/Adaptive-Data-Structures-SLLs-on-SLLs',
    version='0.3.1',
    zip_safe=False,
)
