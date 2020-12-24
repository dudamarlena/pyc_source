#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 3 14:14:06 2019
Setup script for ProTiler
@author: Wei He
@email: whe3@mdanderson.org
"""

from setuptools import setup
import re
from os import path


def main():
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
         long_description = f.read()
    version = re.search('^__version__\s*=\s*"(.*)"',open('bin/protiler').read(), re.M).group(1)
    setup(name='protiler',
          version='1.0.2',
          author='Wei He',
          author_email='whe3@mdanderson.org',
          description="Call HS regions from CRISPR tiling screen data and predict HS region from common protein features",
          long_description=long_description,
          long_description_content_type='text/markdown',
          packages=['ProTiler'],
          package_dir={'ProTiler':'ProTiler'},
          package_data={'ProTiler':['StaticFiles/*']},
          url='https://github.com/MDhewei/ProTiler-1.0.0',
          scripts=['bin/protiler'],
          install_requires=[
                  'numpy',
                  'pandas',
                  'matplotlib',
                  'sklearn',
                  'argparse',
                  'seaborn'],
          zip_safe = True
        )
if __name__ == '__main__':
    main()
