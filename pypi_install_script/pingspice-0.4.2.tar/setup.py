#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# pingspice:
# Object-oriented circuit construction and efficient asynchronous
# simulation with Ngspice and Twisted.
#
# Copyright (C) 2017-20 by Edwin A. Suominen,
# http://edsuom.com/pingspice
#
# See edsuom.com for API documentation as well as information about
# Ed's background and other projects, software and otherwise.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language
# governing permissions and limitations under the License.
#
# I'm serious about this: There are NO GUARANTEES to this
# software. None. If you simulate a circuit and everything looks
# great, and then you build it and it blows up, I CANNOT AND WILL NOT
# BE RESPONSIBLE. Nor do I make any promises as to how closely the
# included models compare to the actual devices whose behavior they
# attempt to simulate. Nor have the manufacturers of ANY of those
# devices provided (or been asked to provide) any endorsement about
# the models. This is free software, OK? You don't even get a
# money-back guarantee, because you paid nothing to begin with.

NAME = "pingspice"


### Imports and support
from setuptools import setup

### Define requirements
required = [
    'Twisted', 'numpy', 'scipy',
    # Other EAS projects
    'yampex>=0.9.5', 'ade>=1.3.3', 'AsynQueue>=0.9.8'
]


### Define setup options
kw = {'version': '0.4.2',
      'license': 'Apache License (2.0)',
      'platforms': 'OS Independent',

      'url': "http://edsuom.com/{}.html".format(NAME),
      'author': "Edwin A. Suominen",
      'author_email': "foss@edsuom.com",
      'maintainer': 'Edwin A. Suominen',
      'maintainer_email': "foss@edsuom.com",
      
      'install_requires': required,
      'packages': [
          'pingspice', 'pingspice.test', 'pingspice.examples',
          'pingspice.lib', 'pingspice.analysis', 'pingspice.scripts',],
      'package_data': {
          'pingspice.test': ['rc.cir'],
          'pingspice.lib': ['*.lib', '*.goals'],
      },
      'entry_points': {
          'console_scripts': [
              "rc = pingspice.scripts.readcsv:main",
              "pf = pingspice.scripts.paramfind:main",
              "ps2sc = pingspice.scripts.ps2sc:main",
              'pingspice-examples = pingspice.scripts.examples:extract',
          ],
      },
      'zip_safe': False,
}

kw['keywords'] = [
    'Ngspice', 'spice', 'eda', 'Twisted', 'asynchronous',
    'simulation', 'electronic', 'netlist',
]


kw['classifiers'] = [
    'Development Status :: 4 - Beta',

    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Framework :: Twisted',

    'Topic :: Software Development :: Libraries :: Python Modules',
]


kw['description'] = " ".join("""
Object-oriented netlist construction and multiprocess SPICE simulation.
""".split("\n"))

kw['long_description'] = """
The pingspice_ package is **P**ython **in**tegrated with **Ngspice**.

It provides a fast, compact object-oriented circuit construction and
SPICE simulation framework using Twisted and Ngspice. Netlists are
produced from components and subcircuits using a powerful
context-calling setup. A single instance of Ngspice is kept running in
pipe mode for each parallel processing branch, communicated with
asynchronously via STDIO and Twisted.

.. _pingspice: http://edsuom.com/pingspice.html
"""

### Finally, run the setup
setup(name=NAME, **kw)
print("\n" + '-'*79)
print("To create a subdirectory 'pingspice-examples' of example files in")
print("the current directory, you may run the command 'pingspice-examples'.")
print("It's not required to use the pingspice package, but you might find")
print("it instructive.")


