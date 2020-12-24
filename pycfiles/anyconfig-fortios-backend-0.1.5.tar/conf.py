# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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