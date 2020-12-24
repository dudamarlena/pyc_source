# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerard/1r_MASTER/2n_TRIMESTRE/SBI/PROJECT/YouSet_v1.0/setup.py
# Compiled at: 2020-03-29 12:57:54
# Size of source mod 2**32: 577 bytes
from distutils.core import setup
setup(name='YouSet',
  packages=[
 'YouSet', 'YouSet.modules'],
  version='2.0',
  license='MIT',
  description='Superimposition macrocomplex builder',
  long_description=(open('README.md').read()),
  long_description_content_type='text/markdown',
  author='Paula Lopez, Gerard Serrano, Laura Vila',
  url='https://github.com/gsergom/YouSet',
  download_url='https://github.com/gsergom/YouSet/releases/tag/2.0',
  keywords=[
 'macrocomplex', 'builder', 'bioinformatics'],
  install_requires=[
 'biopython'])