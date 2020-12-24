#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError as ex:
    print('[python-bibtexparser] setuptools not found. Falling back to distutils.core')
    from distutils.core import setup
from libcitebib import __version__ as version

setup(
    name         = 'CiteBib',
    version      = version,
    url          = "https://github.com/sciunto-org/python-bibtexparser",
    author       = "Francois Boulogne",
    license      = "GPLv3+",
    author_email = "fboulogne@sciunt.org",
    description  = "Generate a nice Bibtex or Latex bibliography according to the document content",
    packages     = ['libcitebib'],
    scripts      = ['citebib', 'citekey'],
)
