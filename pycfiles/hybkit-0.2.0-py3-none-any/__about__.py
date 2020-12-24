# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ds/hybkit/hybkit/__about__.py
# Compiled at: 2020-03-10 16:45:31
"""
Package details for the hybkit project.
"""
import os, sys
if sys.version_info.major >= 3 and sys.version_info.minor >= 7:
    from importlib import resources as importlib_resources
else:
    import importlib_resources
project_name = 'hybkit'
description = 'Toolkit for analysis of .hyb format genomic '
description += 'sequence data from ribonomics experiments.'
project_url = 'https://github.com/RenneLab/hybkit'
keywords = 'genetics genomics ribonomics bioinformatics hyb CLASH qCLASH miRNA '
keywords += 'RNA DNA vienna viennad unafold'
version = '0.1.3'
name_and_version = project_name + '-' + version
module_dir = importlib_resources.files('hybkit')
prefix_data_dir = os.path.join(sys.prefix, name_and_version)
try:
    local_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
except NameError:
    local_data_dir = 'using_with_exec'

if os.path.isdir(os.path.join(prefix_data_dir, 'databases')):
    hybkit_data_dir = prefix_data_dir
elif os.path.isdir(os.path.join(local_data_dir, 'databases')):
    hybkit_data_dir = local_data_dir
else:
    print 'WARNING: hybkit_data_dir variable cannot be set.'
    hybkit_data_dir = ''
databases_dir = os.path.join(hybkit_data_dir, 'databases')
reference_data_dir = os.path.join(hybkit_data_dir, 'reference_data')
docs_dir = os.path.join(hybkit_data_dir, 'docs')
scripts_extra_dir = os.path.join(hybkit_data_dir, 'scripts_extra')
default_string_match_params = os.path.join(module_dir, 'string_match_params.csv')
classifiers = [
 'Development Status :: 4 - Beta',
 'Natural Language :: English',
 'Intended Audience :: Science/Research',
 'Intended Audience :: Developers',
 'Topic :: Scientific/Engineering',
 'Topic :: Scientific/Engineering :: Bio-Informatics',
 'Topic :: Software Development :: Libraries :: Python Modules',
 'Operating System :: OS Independent',
 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
 'Programming Language :: Python :: 3',
 'Programming Language :: Python :: 3.6',
 'Programming Language :: Python :: 3.7',
 'Programming Language :: Python :: 3.8']
info_urls = {'Renne Lab Github': 'https://github.com/RenneLab', 
   'Renne Lab Mainpage': 'https://www.rennelab.com/', 
   'Hyb Format Specification': 'https://www.sciencedirect.com/science/article/pii/S1046202313004180'}
__author__ = 'Daniel Stribling'
__contact__ = 'ds@ufl.edu'
__credits__ = ['Daniel B. Stribling', 'Rolf Renne']
__date__ = '2020/03/10'
__deprecated__ = False
__email__ = 'ds@ufl.edu'
__license__ = 'GPLv3'
__maintainer__ = 'Renne Group, University of Florida'
__status__ = 'Development'
__version__ = version
spec_version = __version__