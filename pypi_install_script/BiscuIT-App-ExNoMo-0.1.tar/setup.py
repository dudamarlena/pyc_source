#!/usr/bin/env python3

from setuptools import setup

setup(
    name='BiscuIT-App-ExNoMo',
    version='0.1',
    url='https://edugit.org/Teckids/BiscuIT/BiscuIT-App-ExNoMo',
    author="Teckids e.V.",
    author_email="verein@teckids.org",
    packages=[
              'biscuit.apps.exnomo'
             ],
    namespace_packages=[
                        'biscuit',
                        'biscuit.apps'
                       ],
    include_package_data=True,
    install_requires=[
                      'BiscuIT-ng',
                      'openpyxl',
                     ],
    classifiers=[
                 "Development Status :: 3 - Alpha",
                 "Environment :: Web Environment",
                 "Intended Audience :: Education",
                 "License :: OSI Approved :: MIT License",
                 "Programming Language :: Python :: 3",
                 "Topic :: Education",
                ],
)
