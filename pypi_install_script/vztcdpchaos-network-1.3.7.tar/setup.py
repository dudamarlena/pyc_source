#!/usr/bin/env python
"""chaostoolkit-toxiproxy extension builder and installer"""

import os
import sys
import io

import setuptools


name = 'vztcdpchaos-network'
desc = 'Extension for managing toxiproxy from an experiment'



classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: Freely Distributable',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: Implementation',
    'Programming Language :: Python :: Implementation :: CPython'
]
author = "CDP"
author_email = 'sucpandu@gmail.com'
url = 'http://chaostoolkit.org'
license = 'Apache License Version 2.0'
packages = [
   'cdpchaostoxi',
   'cdpchaostoxi.proxy',
   'cdpchaostoxi.toxic'
 ]


setup_params = dict(
    name=name,
    version='1.3.7',
    description=desc,

    author=author,
    author_email=author_email,
    url=url,
    license=license,
    packages=packages,
    include_package_data=True,

    python_requires='>=3.5.*'
)


def main():
    """Package installation entry point."""
    setuptools.setup(**setup_params)


if __name__ == '__main__':
    main()
