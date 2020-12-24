#!/usr/bin/env python

import setuptools
from Cython.Build import cythonize


setuptools.setup(
    name="nopy",
    version="0.0.3",
    setup_requires=["cffi>=1.0.0", "cython"],
    install_requires=["wasmer"],
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    ext_modules=cythonize("src/nopy/fib_pyx.pyx"),
    cffi_modules=["src/fib_c_build.py:ffi"],
    include_package_data=True,
)
