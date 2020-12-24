# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/doc/conf.py
# Compiled at: 2019-10-04 13:17:54
# Size of source mod 2**32: 2905 bytes
import os, codecs, sys, re
sys.path.insert(0, os.path.abspath('..'))
here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    with codecs.open((os.path.join)(here, *parts), 'r') as (fp):
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search('^__version__ = [\'\\"]([^\'\\"]*)[\'\\"]', version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


project = 'GenTex'
author = 'GenTex developers'
version = find_version('..', 'gentex', '__init__.py')
release = version
extensions = [
 'sphinx.ext.autodoc',
 'numpydoc',
 'sphinx.ext.napoleon']
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
templates_path = [
 '_templates']
exclude_patterns = [
 '_build', 'Thumbs.db', '.DS_Store']
html_theme = 'sphinx_rtd_theme'
html_static_path = [
 '_static']