#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2017-2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the pyutmpx Python 3.x module, which is MIT-licensed.
#******************************************************************************
""" Setup script for the utmpx module. """

import os as _os, os.path as _path
import subprocess as _subprocess
from setuptools import setup as _setup, Extension as _Extension

version = "0.2.2"

# ---
# Find the sources.
# ---

srcdir = "src"

src = _os.listdir(srcdir)
src = filter(lambda x: x.split('.')[-1] in ("c",), src)
src = list(map(lambda x: _path.join(srcdir, x), src))

# ---
# Run the setup script.
# ---

# Actually, most of the project's data is read from the `setup.cfg` file.

_setup(version = version,
	ext_modules=[_Extension("pyutmpx", src,
		include_dirs = [], library_dirs = [], libraries = [],
		define_macros = [('PYUTMPX_VERSION', f'"{version}"')])])

# End of file.
