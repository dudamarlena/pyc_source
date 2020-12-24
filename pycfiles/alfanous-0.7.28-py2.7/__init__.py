# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/alfanous/__init__.py
# Compiled at: 2015-06-30 17:24:37
""" hint: 

    Use `alfanous.search` for searching in Quran verses and translations.
    Use `alfanous.get_info` for getting meta info.
    Use `alfanous.do` method for search, suggestion and get most useful info.
    """
from alfanous.Outputs import Raw as _search_engine
from alfanous.Data import Paths as PATHS
DEFAULTS, DOMAINS, HELPMESSAGES = _search_engine.DEFAULTS, _search_engine.DOMAINS, _search_engine.HELPMESSAGES
FLAGS = DEFAULTS['flags'].keys()
from alfanous.Outputs import Fields as _fields
FIELDS_ARABIC = _fields.keys()
FIELDS_ENGLISH = _fields.values()
_R = _search_engine()

def do(flags):
    ur"""
    Perform the action defined in `flags` and return results as `dict`.
    
    flags is a dict with values for those keys:
    - "action": action to be performed, could be "search" or "suggest" or "show". default is "search"
    - "query": query for action to be pefromed
    - "unit": search unit, could be "aya" or "translation". default is "aya"
    Check alfanous.FLAGS for the list of all flags, alfanous.HELPMESSAGES for their discriptions, alfanous.DOMAINS for their possible values and alfanous.DEFAULTS for their default values.
    
        >>> results = do({"query":u"الحمد لله"})
        >>> results["error"]
        {'msg': 'success', 'code': 0}
        >>> results["search"]["ayas"][1]["identifier"]
        {'sura_id': 1, 'gid': 2, 'sura_arabic_name': u'\u0627\u0644\u0641\u0627\u062a\u062d\u0629', 'sura_name': u'Al-Fat
ihah', 'aya_id': 2}

    """
    return _R.do(flags)


def search(query, unit='aya', page=1, sortedby='relevance', fuzzy=False, view='normal', highlight='bold', flags={}):
    u""" Search for query in Quran
    
    @param query: search query, examples: الحمد, qwl, gid:1.
    @param unit: search unit, possible values = ['aya', 'word', 'translation']
    @param page: page to be retrieved, possible values = 1..INF
    @param sortedby: order of results, possible values = ['relevance', 'mushaf', 'tanzil', 'subject', 'ayalength']
    @param fuzzy: use fuzzy search, possible values = [True, False]
    @param view: information to be retrieved, possible values = ['minimal', 'normal', 'full', 'statistic', 'linguistic', 'recitation','costum']
    @param highlight: type of highlight, possible values = ['css', 'html', 'genshi', 'bold', 'bbcode']
    @param flags: extra flags as a dict , check alfanous.FLAGS and alfanous.DOMAINS.
    
    
    Example:
    -------
        >>> search("qawol",page=2, fuzzy = True)

    """
    all_flags = flags
    all_flags.update({'action': 'search', 'unit': unit, 
       'query': query, 
       'page': page, 
       'sortedby': sortedby, 
       'fuzzy': fuzzy, 
       'view': view, 
       'highlight': highlight})
    return do(all_flags)


def get_info(query='all'):
    """
    Show useful meta info.
    
    @param query: info to be retrieved, possible_values = ['chapters', 'defaults', 'domains', 'errors', 'fields', 'fields_reverse', 'flags', 'help_messages', 'hints', 'information', 'recitations', 'roots', 'surates', 'translations']
    """
    return do({'action': 'show', 'query': query})