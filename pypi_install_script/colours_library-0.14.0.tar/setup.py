from setuptools import setup
import os
import sys
from colours_library import __version__ 

setup(name='colours_library',
  version=__version__,
  description='Colours library package',
  url='https://gitlab.bitcomp.intra/eryk_malczyk/colours_library.git',
  author='ErykM',
  author_email='eryk.malczyk@bitcomp.fi',
  license='some_license',
  packages=['colours_library'],
  install_requires=[
    'webcolors==1.3',
    'Pillow',
  ],
  setup_requires=[
    'pytest-runner',
  ],
  tests_require=['pytest',],
  include_package_data=True,
  zip_safe=False)