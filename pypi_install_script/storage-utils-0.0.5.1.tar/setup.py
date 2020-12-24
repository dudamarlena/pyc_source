#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
import setuptools

version_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "storage_utils", "__version__.py"))
with open(version_file, mode="rt") as f:
    exec(f.read())
# noinspection PyUnresolvedReferences
VERSION = __version__

extras_require = {
    "s3": ["s3fs"],
    "hdfs": ["pyarrow"]
}
extras_require["complete"] = {v for req in extras_require.values() for v in req}

setuptools.setup(

    name="storage-utils",
    version=VERSION,
    description="Blob storage utilities",
    long_description="Blob storage utilities",
    url="https://volantisiq.com",
    license="MIT",

    author="Akrom Khasani",
    author_email="akrom@volantis.io",

    packages=setuptools.find_packages(exclude=("tests*",)),
    python_requires=">=3.7",
    install_requires=[],
    extras_require=extras_require,
    platforms=[
        "any"
    ],

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython"
    ]

)
