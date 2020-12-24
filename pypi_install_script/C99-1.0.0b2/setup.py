# Copyright (c) 2018-2019 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/zlib/

from __future__ import absolute_import

import sys
from os import path
from setuptools import setup

PY2 = sys.version_info[0] <= 2

top_dir = path.dirname(path.abspath(__file__))
with open(path.join(top_dir, "src", "C99", "__about__.py")) as f:
    class about: exec(f.read(), None)

headers = []
ext_modules = []

if PY2 and sys.platform == "win32":
    headers += [path.join(top_dir, "src", "C99", "stdint.h"),
                path.join(top_dir, "src", "C99", "inttypes.h")]

setup(
    name             = about.__title__,
    version          = about.__version__,
    description      = about.__summary__,
    url              = about.__uri__,
    download_url     = about.__uri__,

    author           = about.__author__,
    author_email     = about.__email__,
    maintainer       = about.__maintainer__,
    maintainer_email = about.__email__,
    license          = about.__license__,

    headers     = headers,
    ext_modules = ext_modules,
)
