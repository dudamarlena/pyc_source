# Copyright (c) 2020 smarsu. All Rights Reserved.

"""Setup SMNet as a package.
Upload SMNet to pypi, then you can install smnet via:
    pip install smnet
Script for uploading:
```sh
(export use_cuda=true)
python setup.py sdist
twine upload dist/*
rm -r dist
rm -r smnet.egg-info
```
"""

import os
from setuptools import find_packages, setup


def config_setup(name):
  packages = find_packages()

  setup(
    name = name,
    version = '0.0.2',
    packages = packages,
    install_requires = [
        'numpy',
        'glog',
    ],
    author = 'smarsu',
    author_email = 'smarsu@foxmail.com',
    url = 'https://github.com/smarsu/compare',
    zip_safe = False,
  )

print('---------------- Setup compare ----------------')
config_setup('evaluation')
