# Copyright (C) 2017 chainside srl
#
# This file is part of the btcpy package.
#
# It is subject to the license terms in the LICENSE.md file found in the top-level
# directory of this distribution.
#
# No part of btcpy, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE.md file.


import sys
from distutils.core import setup
from setuptools import find_packages

BTCPYVERSION = '0.6.2'

requirements = ['ecdsa==0.13']

if sys.version_info.minor < 4:
    requirements.append('enum34')

setup(name='peerassets-btcpy',
      version=BTCPYVERSION,
      packages=find_packages(),
      install_requires=requirements,
      extras_require={'develop': ['python-bitcoinlib==0.7.0']},
      description='A Python3 SegWit-compliant library which provides tools to handle Bitcoin data structures in a simple fashion.',
      author='chainside srl & PeerAssets development team',
      url='https://github.com/PeerAssets/btcpy',
      download_url='https://github.com/PeerAssets/btcpy/archive/0.6.2.pa.tar.gz',
      python_requires='>=3',
      keywords=['bitcoin', 'blockchain', 'peercoin', 'peerassets'])
