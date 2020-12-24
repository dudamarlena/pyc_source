# encoding: utf-8
from setuptools import setup, find_packages
pkg = "pyamdcovc"
ver = '0.1.0'

with open(pkg+'/version.py', 'wt') as h:
    h.write('__version__ = "{}"\n'.format(ver))

setup(
    name             = pkg,
    version          = ver,
    description      = (
        "Control AMD GPUs using AMDCOVC utility"),
    author           = "Eduard Christian Dumitrescu",
    author_email     = "eduard.c.dumitrescu@gmail.com",
    license          = "LGPLv3",
    url              = "https://hydra.ecd.space/eduard/pyamdcovc/",
    packages         = find_packages(),
    install_requires = [],
    # optional dependencies: argh, scipy
    classifiers      = [
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries",
    ],
)

