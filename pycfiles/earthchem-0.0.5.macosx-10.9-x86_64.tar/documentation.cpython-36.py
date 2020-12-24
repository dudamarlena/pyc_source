# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jess/.local/conda/lib/python3.6/site-packages/earthchem/documentation.py
# Compiled at: 2018-06-02 08:11:53
# Size of source mod 2**32: 1873 bytes
""" file:   documentation.py (earthchem)
    author: Jess Robertson, CSIRO Minerals
    date:   May 2018

    description: Scraping the Earthchem site for documentation etc
"""
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import pkg_resources, re, textwrap

def strip_whitespace(string):
    """ Strip newline, tab and multple whitespace from a string
    """
    return re.sub(' +', ' ', string.replace('\n', ' ').replace('\t', ' ').strip())


REST_DOCO_URL = 'http://ecp.iedadata.org/rest_search_documentation/'
if not requests.get(REST_DOCO_URL).ok:
    CACHED_DOCO_FILE = pkg_resources.resource_stream('earthchem.resources', 'earthchem_rest_search_documentation.html')
    REST_DOCO_URL = 'file://' + str(CACHED_DOCO_FILE)
IGNORE_VALUES = (
 re.compile('Example.*'),
 re.compile('level[0-9]'))

def get_documentation():
    """ Get query items and documentaton by scraping the EarthChem rest
        documentation
    """
    response = requests.get(REST_DOCO_URL)
    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')
    else:
        raise IOError("Can't find Earthchem REST documentation")
    docs = OrderedDict()
    for item in soup.select('.itemtitle'):
        itemname = strip_whitespace(item.contents[0])
        if any(map(lambda regex: regex.match(itemname), IGNORE_VALUES)):
            continue
        itemdoc = strip_whitespace(item.contents[1].contents[0])
        docs[itemname] = itemdoc

    return docs