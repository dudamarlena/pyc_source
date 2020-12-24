# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/doapfiend/__init__.py
# Compiled at: 2008-06-10 01:25:29
"""
doapfiend
=========

U{http://trac.doapspace.org/doapfiend}

Description
-----------
doapfiend is a command-line client and library for querying, creating and
displaying DOAP (Description of a Project) RDF profiles.

doapfiend uses RDFAlchemy and rdflib to parse and serialize DOAP.

Plugins
-------
Plugins can be written for editing DOAP, scraping websites and creating DOAP,
searching for DOAP in SPARQL endpoints, displaying DOAP in various formats such
as HTML etc.

"""
import logging
log = logging.getLogger()
log.setLevel(logging.ERROR)
__docformat__ = 'epytext'
__version__ = '0.3.3'
__author__ = 'Rob Cakebread <rob@doapspace.org>'
__copyright__ = '(C) 2007-2008 Rob Cakebread'
__license__ = 'BSD-2'