# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\odddML\setup.py
# Compiled at: 2019-12-20 05:11:22
# Size of source mod 2**32: 1324 bytes
from distutils.core import setup
from pkg_resources import DistributionNotFound, get_distribution
from setuptools import setup

def get_dist(pkgname):
    try:
        return get_distribution(pkgname)
    except DistributionNotFound:
        return


install_deps = []
if get_dist('tensorflow') is None:
    if get_dist('tensorflow_gpu') is None:
        install_deps.append('tensorflow')
install_deps.extend(['numpy', 'opencv-contrib-python', 'h5py', 'matplotlib'])
setup(name='odddML',
  packages=[
 'odddML', 'odddML.resnet'],
  version='v0.1.1-alpha',
  license='MIT',
  description='Easy ML for Devs, out of the box ML tools from ODDD Technologies',
  author='Nick Koutroumpinis, ODDD Technologies',
  author_email='nick@odddtech.com',
  url='https://github.com/ODDDTechnologies/BinianML',
  download_url='https://github.com/ODDDTechnologies/odddML/archive/v0.1.1-alpha.tar.gz',
  keywords=[
 'Easy', 'Deep Learning', 'Machine Learning'],
  install_requires=install_deps,
  classifiers=[
 'Development Status :: 3 - Alpha',
 'Intended Audience :: Developers',
 'Topic :: Software Development :: Build Tools',
 'License :: OSI Approved :: MIT License',
 'Programming Language :: Python :: 3.7'])