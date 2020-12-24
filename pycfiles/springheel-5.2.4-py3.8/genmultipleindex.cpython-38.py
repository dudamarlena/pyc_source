# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/springheel/genmultipleindex.py
# Compiled at: 2019-12-29 18:53:39
# Size of source mod 2**32: 2921 bytes
import os
from slugify import slugify, slugify_url
sep = '\n'

def genMultipleIndex(comics, characters_page, translated_strings):
    """
    Generate an index page for a site with multiple comics.

    Parameters
    ----------
    comics : list
        A list of the Comics on the site.
    characters_page : bool
        Whether or not to add character-page links.
    translated_strings : dict
        The translation file contents for this site.
    """
    elements = []
    dopen = '<div class="intro">'
    dclose = '</div>'
    golatest_s = translated_strings['golatest_s']
    gofirst_s = translated_strings['gofirst_s']
    if characters_page == True:
        character_s = translated_strings['char_s']
    ltemplate = ['<h2>{category}</h2>', '<img src="{header}" alt="{category}" />',
     '<p class="author">by {author}</p>', '<p class="desc">{desc} (<span class="status">{status}</span>)</p>',
     '<p>{golatest} | {gofirst}</p>']
    maintemplate = sep.join(ltemplate)
    for i in comics:
        golatest = [
         '<a href="', i.lbp_link, '">', golatest_s, '</a>']
        golatest = ''.join(golatest)
        gofirst = ['<a href="', i.fbp_link, '">', gofirst_s, '</a>']
        gofirst = ''.join(gofirst)
        elements.append(dopen)
        div = maintemplate.format(header=(i.header), category=(i.category_escaped),
          author=(i.author),
          desc=(i.desc),
          status=(i.statuss),
          golatest=golatest,
          gofirst=gofirst)
        elements.append(div)
        if characters_page == True:
            if i.chars_file != 'None':
                if i.chars_file != 'False':
                    cat_slug = slugify_url(i.category)
                    characters_link = ''.join([cat_slug, '-', 'characters.html'])
                    char_line = '<p><a href="{characters_link}">{character_s}</a></p>'.format(characters_link=characters_link, character_s=character_s)
                    elements.append(char_line)
        elements.append(dclose)
    else:
        return elements