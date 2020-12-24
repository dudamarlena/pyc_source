# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/oort/test/test_misc.py
# Compiled at: 2007-09-29 15:43:43
from oort.util._genshifilters import language_filtered_xml
XML = '\n<span>XML.</span>\n'
XML_EN = '\n<span xml:lang="en">Testing.</span>\n'
XML_SV = '\n<span xml:lang="sv">Testar.</span>\n'
FULL_XML = '\n<div xml:lang="en">Testing.</div>\n<div xml:lang="sv">Testar.</div>\n'
WRAPPED = '<rdf-wrapper>\n    <p><em>XML</em>.</p>\n</rdf-wrapper>'
WRAPPED_EN = '<rdf-wrapper xml:lang="en">\n    <p>Some content.</p>\n    <p>Some <em>more</em> content.</p>\n</rdf-wrapper>'
WRAPPED_SV = '<rdf-wrapper xml:lang="sv">\n    <p>Lite inneåll.</p>\n    <p>Lite <em>mer</em> innehåll.</p>\n</rdf-wrapper>'

def test_language_filtered_xml():
    for lang in ('en', 'sv'):
        print '====================', lang
        for xml in (XML, XML_EN, XML_SV, FULL_XML, WRAPPED, WRAPPED_EN, WRAPPED_SV):
            stream = language_filtered_xml(xml, lang)
            print stream.render()

    stream = language_filtered_xml([XML_EN, XML_SV], 'en')