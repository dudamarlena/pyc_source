# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/land/copernicus/content/content/marshaller.py
# Compiled at: 2018-01-16 07:51:31
""" Custom overrides for eea.rdfmarshaller
"""
from eea.rdfmarshaller.archetypes.fields import ShortenHTMLField2Surf

class LandItemDescription(ShortenHTMLField2Surf):
    sentences = 1
    alternate_field = 'dataResourceAbstract'