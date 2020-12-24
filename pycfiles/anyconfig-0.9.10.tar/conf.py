# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ssato/repos/public/github.com/ssato/python-anyconfig.git/docs/conf.py
# Compiled at: 2015-07-12 01:03:14
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
extensions = [
 'sphinx.ext.autodoc']
source_suffix = '.rst'
master_doc = 'index'
project = 'python-anyconfig'
copyright = '2015, Satoru SATOH <ssato@redhat.com>'
version = '0.0.10'
release = version
exclude_patterns = []
html_theme = 'default'
autodoc_member_order = 'bysource'