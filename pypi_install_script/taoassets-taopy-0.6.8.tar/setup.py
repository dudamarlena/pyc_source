# Copyright (C) 2017 chainside srl
# Copyright (C) 2018 Bryce Weiner
#
# This file is part of the taopy package.
#
# It is subject to the license terms in the LICENSE.md file found in the top-level
# directory of this distribution.
#
# No part of taopy, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE.md file.


import sys
from distutils.core import setup
from setuptools import find_packages

TAOPYVERSION = '0.6.8'

requirements = ['ecdsa==0.13']

if sys.version_info.minor < 4:
    requirements.append('enum34')

setup(name='taoassets-taopy',
      version=TAOPYVERSION,
      packages=find_packages(),
      install_requires=requirements,
      extras_require={'develop': ['python-bitcoinlib==0.7.0']},
      description='A Python3 SegWit-compliant library which provides tools to handle Tao data structures in a simple fashion.',
      author='chainside srl, PeerAssets & TaoAssets development team',
      url='https://github.com/taoblockchain/taopy',
      python_requires='>=3',
      keywords=['tao', 'blockchain', 'bitcoin', 'peercoin', 'taoassets'])
