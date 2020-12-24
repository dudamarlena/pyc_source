# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/infomap/interfaces/python/setup.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 1367 bytes
"""
setup.py file for compiling Infomap module
"""
from distutils.core import setup, Extension
from distutils.file_util import copy_file
import sysconfig, fnmatch, os, re
cppSources = []
for root, dirnames, filenames in os.walk('.'):
    if root == 'src':
        cppSources.append(os.path.join(root, 'Infomap.cpp'))
    else:
        for filename in fnmatch.filter(filenames, '*.cpp'):
            cppSources.append(os.path.join(root, filename))

infomapVersion = ''
with open(os.path.join('src', 'io', 'version.cpp')) as (f):
    for line in f:
        m = re.match('.+INFOMAP_VERSION = \\"(.+)\\"', line)
        if m:
            infomapVersion = m.groups()[0]

infomap_module = Extension('_infomap', sources=cppSources,
  extra_compile_args=[
 '-DAS_LIB', '-Wno-deprecated-declarations'])
setup(name='infomap', version=infomapVersion,
  author='Team at mapequation.org',
  description='Infomap clustering algorithm',
  url='www.mapequation.org',
  ext_modules=[
 infomap_module],
  py_modules=[
 'infomap'])
ext_suffix = sysconfig.get_config_var('EXT_SUFFIX')
if ext_suffix is None:
    ext_suffix = sysconfig.get_config_var('SO')
if ext_suffix is not None:
    copy_file('_infomap{}'.format(ext_suffix), '_infomap.so')