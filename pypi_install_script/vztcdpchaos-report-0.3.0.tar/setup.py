#!/usr/bin/env python
"""chaostoolkit reporting library builder and installer"""

import sys
import io

import setuptools

name = 'vztcdpchaos-report'
desc = 'CDP chaos reporting lib'


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
author = 'vztcdpchaos'
author_email = 'sucpandu@gmail.com'

license = 'Apache License Version 2.0'
packages = [
    'cdpchaosreport',
    'cdpchaosreport.template',

]

setup_params = dict(
    name=name,
    version='0.3.0',
    description=desc,



    author=author,
    author_email=author_email,

    license=license,
    packages=packages,
    include_package_data=True,
    install_requires=[
    'chaostoolkit-lib',
    'click',
    'dateparser',
    'logzero',
    'jinja2',
    'matplotlib',
    'maya',
    'natural',
    'pygal',
    'pypandoc',
    'pandoc',
    'semver'
            ],

    python_requires='>=3.5.*',
    entry_points="""
        [cdpchaostoolkit.cli_plugins]

    """,
)


def main():
    """Package installation entry point."""
    setuptools.setup(**setup_params)


if __name__ == '__main__':
    main()
