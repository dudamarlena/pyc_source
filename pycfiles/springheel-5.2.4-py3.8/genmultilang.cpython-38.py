# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/springheel/genmultilang.py
# Compiled at: 2019-12-16 01:32:30
# Size of source mod 2**32: 1888 bytes


def genMultiLang(multilang, language_names):
    """
    Generate links to the site in other languages.

    Parameters
    ----------
    multilang : str
        Language code=URL pairs, separated by commas.
    language_names : dict
        Language code-language name mappings from strings.json.
    Returns
    -------
    olangs : str
        Formatted list of language links, separated by pipes.
    """
    other_langs = []
    multilang_kvs = [item.split('=') for item in multilang.split(',')]
    for pair in multilang_kvs:
        d = {'langcode':pair[0], 
         'path':pair[1]}
        other_langs.append(d)
    else:
        olang_links = []
        for langsite in other_langs:
            if langsite['langcode'] in language_names:
                langsite['name'] = language_names[langsite['langcode']]
            else:
                langsite['name'] = langsite['langcode']
            langsite['element'] = '<a href="{path}">{name}</a>'.format(path=(langsite['path']), name=(langsite['name']))
            olang_links.append(langsite['element'])
            olangs = ' | '.join(olang_links)
        else:
            return olangs