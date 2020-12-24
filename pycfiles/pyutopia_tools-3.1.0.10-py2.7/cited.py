# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/utopia/tools/cited.py
# Compiled at: 2017-06-20 06:17:42
import json, urllib, urllib2, utopia.citation

def resolve(**identifiers):
    query = urllib.urlencode(identifiers)
    url = ('https://utopia.cs.manchester.ac.uk/cited/resolutions?{}').format(query)
    response = urllib2.urlopen(url, timeout=8)
    citations = json.load(response)
    return citations


def submit(citations):
    citations = [ citation for citation in citations if 'error' not in citation ]
    url = 'https://utopia.cs.manchester.ac.uk/cited/resolutions'
    req = urllib2.Request(url, headers={'Content-Type': 'application/json'}, data=json.dumps(citations))
    for c in citations:
        p = c.get('provenance', {})
        if p is not None:
            for refspec in p.get('input', []):
                id, keyspec = utopia.citation.split_refspec(refspec)

    res = urllib2.urlopen(req)
    citations = json.load(res)
    return citations


def parse(citations):
    url = 'https://utopia.cs.manchester.ac.uk/cited/parse'
    req = urllib2.Request(url, headers={'Content-Type': 'application/json'}, data=json.dumps(citations))
    res = urllib2.urlopen(req)
    citations = json.load(res)
    return citations