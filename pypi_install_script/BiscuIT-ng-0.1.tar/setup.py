#!/usr/bin/env python3

from setuptools import setup

setup(
    name='BiscuIT-ng',
    version='0.1',
    url='https://edugit.org/Teckids/BiscuIT/BiscuIT-ng',
    author="Teckids e.V.",
    author_email="verein@teckids.org",
    packages=[
              'biscuit.core'
             ],
    namespace_packages=[
                        'biscuit',
                       ],
    include_package_data=True,
    install_requires=[
                      'Django >= 2.0',
                      'django-bootstrap3',
                      'django-easy-audit',
                      'django-local-settings',
                      'django-simple-menu',
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
