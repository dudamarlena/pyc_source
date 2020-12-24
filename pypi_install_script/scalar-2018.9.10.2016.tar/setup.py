#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import setuptools

def main():
    setuptools.setup(
        name                 = "scalar",
        version              = "2018.09.10.2016",
        description          = "Python Matrix library",
        long_description     = long_description(),
        url                  = "https://github.com/wdbm/scalar",
        author               = "Will Breaden Madden",
        author_email         = "wbm@protonmail.ch",
        license              = "GPLv3",
        packages             = setuptools.find_packages(),
        install_requires     = [
                               "docopt",
                               "matrix_client",
                               "megaparsex",
                               "pyprel",
                               "pyyaml",
                               "technicolor"
                               ],
        #python_requires      = ">=3",
        entry_points         = {
                               "console_scripts": [
                                   "scalar_alert  = scalar.__init__:alert",
                                   "scalar_client = scalar.client:main"
                               ]
                               },
        include_package_data = True,
        zip_safe             = False
    )

def long_description(filename = "README.md"):
    if os.path.isfile(os.path.expandvars(filename)):
      try:
          import pypandoc
          long_description = pypandoc.convert_file(filename, "rst")
      except ImportError:
          long_description = open(filename).read()
    else:
        long_description = ""
    return long_description

if __name__ == "__main__":
    main()
