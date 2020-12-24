# -*- coding: utf-8 -*-
"""
PyLD
====

PyLD_ is a Python JSON-LD_ library.

.. _PyLD: http://github.com/digitalbazaar/pyld
.. _JSON-LD: http://json-ld.org/
"""

import os
import sys
import uuid

from pip.req import parse_requirements
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

install_reqs = parse_requirements(os.path.join(here, 'requirements.txt'), session=uuid.uuid1())
reqs = [str(ir.req) for ir in install_reqs]

sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

with open('README.rst') as file:
    long_description = file.read()

setup(
    name='blockcerts-pyld',
    version='0.0.2',
    description='Blockcerts fork of Digital Bazaar Python implementation of the JSON-LD API',
    author='Blockcerts',
    url='http://github.com/blockchain-certificates/pyld',
    packages=['pyld'],
    package_dir={'': 'lib'},
    install_requires=reqs
)
