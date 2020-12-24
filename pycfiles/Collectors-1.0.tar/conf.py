# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/stefan/Workspace/Collectors/docs/conf.py
# Compiled at: 2010-03-26 11:18:39
import sys, os
sys.path.append(os.path.abspath('..'))
extensions = [
 'sphinx.ext.autodoc', 'sphinx.ext.intersphinx']
templates_path = [
 '_templates']
source_suffix = '.txt'
master_doc = 'index'
project = 'Collectors'
copyright = '2010, Stefan Scherfke and Ontje Lünsdorf'
version = '0.2'
release = '0.2'
exclude_trees = [
 '_build']
pygments_style = 'sphinx'
html_theme = 'default'
html_static_path = [
 '_static']
htmlhelp_basename = 'Collectorsdoc'
latex_documents = [
 ('index', 'Collectors.tex', 'Collectors Documentation', 'Stefan Scherfke and Ontje Lünsdorf',
 'manual')]
intersphinx_mapping = {'http://docs.python.org/': None, 
   'http://simpy.sourceforge.net/SimPyDocs/': None}