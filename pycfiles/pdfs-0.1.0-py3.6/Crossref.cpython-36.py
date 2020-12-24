# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pdfs/Crossref.py
# Compiled at: 2017-08-14 16:20:11
# Size of source mod 2**32: 614 bytes
import requests, json
from .TermOutput import msg
from .Cache import cachedRequest

@cachedRequest('DOI')
def crossrefLookup(doi):
    url = 'https://api.crossref.org/works/' + doi
    response = None
    decoded = None
    try:
        response = requests.get(url).text
        if response == 'Resource not found.':
            return
        decoded = json.loads(response)
        if decoded['status'] != 'ok':
            raise RuntimeError('Crossref API call failed')
        return decoded['message']
    except:
        msg('doi=%s\n\nresponse=%s\n\ndecoded=%s\n\n', doi, response, decoded)
        raise