# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/utopia/tools/pmc.py
# Compiled at: 2017-04-26 11:18:25
import utopia.tools.eutils
from lxml import etree

def fetch(pmcid):
    return utopia.tools.eutils.efetch(id=pmcid, db='pmc')


def search(title):
    data = []
    return data


def identify(id, id_type):
    results = utopia.tools.eutils.esearch(term=('"{0}"[{1}]').format(id, id_type.upper()), db='pmc', retmax=1)
    parser = etree.XMLParser(ns_clean=True, recover=True)
    ids = etree.fromstring(results, parser).xpath('//Id')
    if len(ids) == 1:
        pmcid = ids[0].text.upper()
        if not pmcid.startswith('PMC'):
            pmcid = ('PMC{}').format(pmcid)
        return pmcid