# MIT License

# Copyright (c) 2018 AnonymousDapper

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from setuptools import setup, Extension
import re

with open("README.md", "r", encoding="utf-8") as f:
    long_readme = f.read()

version = None
# Version fetch regex comes from Discord.py, Copyright Rapptz
with open("ct_crypto/__init__.py", "r", encoding="utf-8") as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if version is None:
    raise RuntimeError("version is not set, contact AnonymousDapper")

setup(
    name="ct_crypto",
    author="AnonymousDapper",
    author_email="dapper@a-sketchy.site",
    url="https://gitlab.a-sketchy.site/AnonymousDapper/ct_crypto",
    version=version,
    packages=["ct_crypto"],
    license="MIT",
    description="Fast module for PyChickenTicket crypto work",
    long_description=long_readme,
    long_description_content_type="text/markdown",
    ext_modules=[
        Extension("ct_crypto._crypto_backend", ["ct_crypto/ct_crypto.c"], libraries=["sodium"])
    ],
    classifiers=[
    "Development Status :: 4 - Beta",
    "Natural Language :: English",
    "License :: OSI Approved :: MIT License",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: C",
    "Topic :: Security :: Cryptography",

    ]
)