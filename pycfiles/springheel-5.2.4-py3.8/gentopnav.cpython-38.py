# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/springheel/gentopnav.py
# Compiled at: 2019-12-16 03:04:33
# Size of source mod 2**32: 2130 bytes


def genTopNav(characters_page, extras_page, store_page, translated_strings):
    """
    Generate the navigation at the top of each page.

    Parameters
    ----------
    characters_page : bool
        Whether or not to link to the characters page.
    extras_page : bool
        Whether or not to link to an extras page.
    store_page : str
        If not None, a URL to an external store page.
    translated_strings : dict
        The translation file contents for this site.
    Returns
    -------
    elements : str
        An HTML unordered list of navigation links.
    """
    home_s = translated_strings['home_s']
    char_s = translated_strings['char_s']
    archive_s = translated_strings['archive_s']
    extra_s = translated_strings['extra_s']
    store_s = translated_strings['store_s']
    d = [
     {'s':home_s, 
      'u':'index.html'}, {'s':archive_s,  'u':'archive.html'}]
    if characters_page == True:
        d.append({'s':char_s,  'u':'characters.html'})
    if extras_page == True:
        d.append({'s':extra_s,  'u':'extras.html'})
    if store_page:
        d.append({'s':store_s,  'u':store_page})
    elements = ['<ul>']
    for pair in d:
        line = '<li><a href="{u}">{s}</a></li>'.format(u=(pair['u']), s=(pair['s']))
        elements.append(line)
    else:
        elements.append('</ul>')
        return elements