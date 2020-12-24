# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/springheel/genchars.py
# Compiled at: 2019-12-16 01:38:16
# Size of source mod 2**32: 3630 bytes
import os
sep = '\n'

def parseChars(charfile):
    """
    Format the contents of a character file.

    Parameters
    ----------
    charfile : str
        The contents of a character file.
    Returns
    -------
    cl : list
        A list of character file elements formatted as key:value pairs.
    """
    l = []
    divider = '---' + sep
    sectioned = charfile.split(divider)
    for i in sectioned:
        s_text = i.split(sep)[:-1]
        l.append(s_text)
    else:
        raw_page_m = l[0]
        category = raw_page_m[0].split('category: ', 1)[1]
        lang = raw_page_m[1].split('lang: ')[1]
        cl = [
         category, lang]
        characters = l[1:]
        for char in characters:
            if char != []:
                d = {}
                char_attrs = []
                for item in char:
                    attr, val = item.split(': ', 1)
                    tup = (attr, val)
                    char_attrs.append(tup)
                else:
                    cl.append(char_attrs)

            return cl


def genCharsPage(chars_list):
    """
    Create a characters page from a list of character elements.

    Parameters
    ----------
    chars_list : list
        A list of character file elements formatted as key:value pairs.
    Returns
    -------
    characters : str
        The contents of the generated HTML characters page.
    """
    chars = []
    for item in chars_list:
        char_elements = [
         '<div class="char">']
        if type(item) == list:
            title = '<h2>{name}</h2>'.format(name=(item[0][1]))
            char_elements.append(title)
            if item[2][1] != 'None':
                img = '<img src="{img}" alt="" />'.format(img=(item[2][1]))
                char_elements.append(img)
            if len(item) > 3:
                dls = []
                char_elements.append("<dl class='chartraits'>")
                for key in item:
                    if not key[0] == 'name':
                        if not key[0] == 'img':
                            if key[0] == 'desc':
                                pass
                            else:
                                line = '<dt>{attr}</dt>{sep}<dd>{val}</dd>'.format(attr=(key[0]),
                                  val=(key[1]),
                                  sep=sep)
                                dls.append(line)
                    else:
                        dl = sep.join(dls)
                        char_elements.append(dl)
                        char_elements.append('</dl>')

            char_elements.append('<div class="chartext">')
            desc = '<p>{desc}</p>'.format(desc=(item[1][1]))
            char_elements.append(desc)
            char_elements.append('</div>')
            char_elements.append('</div>')
            char_fin = sep.join(char_elements)
            chars.append(char_fin)
        characters = sep.join(chars)
        return characters