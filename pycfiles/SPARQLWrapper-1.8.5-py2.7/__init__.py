# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/SPARQLWrapper/__init__.py
# Compiled at: 2019-12-22 05:59:06
"""

**SPARQLWrapper** is a simple Python wrapper around a `SPARQL <https://www.w3.org/TR/sparql11-overview/>`_ service to
remotelly execute your queries. It helps in creating the query
invokation and, possibly, convert the result into a more manageable
format.

"""
__version__ = '1.8.5'
__authors__ = 'Ivan Herman, Sergio Fernández, Carlos Tejo Alonso, Alexey Zakhlestin'
__license__ = 'W3C® SOFTWARE NOTICE AND LICENSE, http://www.w3.org/Consortium/Legal/copyright-software'
__url__ = 'http://rdflib.github.io/sparqlwrapper'
__contact__ = 'rdflib-dev@googlegroups.com'
__date__ = '2019-04-18'
__agent__ = 'sparqlwrapper %s (rdflib.github.io/sparqlwrapper)' % __version__
from Wrapper import SPARQLWrapper
from Wrapper import XML, JSON, TURTLE, N3, JSONLD, RDF, RDFXML, CSV, TSV
from Wrapper import GET, POST
from Wrapper import SELECT, CONSTRUCT, ASK, DESCRIBE, INSERT, DELETE
from Wrapper import URLENCODED, POSTDIRECTLY
from Wrapper import BASIC, DIGEST
from SmartWrapper import SPARQLWrapper2