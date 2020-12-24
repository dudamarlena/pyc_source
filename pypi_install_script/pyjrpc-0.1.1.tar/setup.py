#! /usr/bin/env python
from setuptools import setup

with open('README.rst') as readme:
    LONG_DESC = readme.read()

setup(
    name="pyjrpc",
    version='0.1.1',

    description="Simple, minimal jsonrpc library",
    long_description=LONG_DESC,
    license="MIT",

    author="Damien de Lemeny",
    author_email="ddelemeny@gmail.com",
    url='https://github.com/ddelemeny/pyjrpc',

    packages=["pyjrpc"],
    include_package_data=True,

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

    test_suite='nose.collector',
    tests_require=['nose'],
)
