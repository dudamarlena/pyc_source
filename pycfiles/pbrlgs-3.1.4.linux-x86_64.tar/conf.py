# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pbr/tests/testpackage/doc/source/conf.py
# Compiled at: 2017-12-04 07:19:32
import os, sys
sys.path.insert(0, os.path.abspath('../..'))
extensions = [
 'sphinx.ext.autodoc']
source_suffix = '.rst'
master_doc = 'index'
project = 'testpackage'
copyright = '2013, OpenStack Foundation'
add_function_parentheses = True
add_module_names = True
pygments_style = 'sphinx'
htmlhelp_basename = '%sdoc' % project
latex_documents = [
 (
  'index',
  '%s.tex' % project,
  '%s Documentation' % project,
  'OpenStack Foundation', 'manual')]