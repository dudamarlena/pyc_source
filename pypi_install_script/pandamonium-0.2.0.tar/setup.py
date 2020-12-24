#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from pip.req import parse_requirements

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = parse_requirements('./requirements.txt', session=False)
test_requirements = parse_requirements('./requirements_test.txt', session=False)

setup(
    name='pandamonium',
    version='0.2.0',
    description="Package for generating random pandas DataFrames",
    long_description=readme,
    author="Keiron James Pizzey",
    author_email='kjpizzey@gmail.com',
    url='https://github.com/Ffisegydd/pandamonium',
    packages=[
        'pandamonium',
    ],
    package_dir={'pandamonium':
                 'pandamonium'},
    include_package_data=True,
    install_requires=[str(req.req) for req in requirements
    ],
    license="MIT license",
    zip_safe=False,
    keywords='pandamonium',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=[str(req.req) for req in test_requirements]
)
