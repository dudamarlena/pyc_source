#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='triton',
    version='3.4.1',
    description='Extended tryton daemon helpful for debugging',
    long_description=open('README.rst').read(),
    author="Prakash Pandey",
    author_email="prakashpp.pandey@gmail.com",
    url="https://github.com/prakashpp/triton",
    package_dir={'triton': '.'},
    packages=[
        'triton',
    ],
    scripts=[
        'bin/trytond',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Office/Business',
    ],
    license='BSD',
    install_requires=[
        "trytond>=3.4,<3.5",
        "psycopg2",
        "sqlparse",
    ],
    zip_safe=False,
)
