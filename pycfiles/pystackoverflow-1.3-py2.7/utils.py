# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/stackoverflow/utils.py
# Compiled at: 2014-02-22 10:22:35
import re, htmlentitydefs, ConfigParser
from html2text import HTML2Text

def html2md(text, width=0):
    h = HTML2Text()
    h.body_width = width
    return h.handle(text)


def unescape(text):
    """
    Removes HTML or XML character references and entities from a text string.

    @param text The HTML (or XML) source text.
    @return The plain text, as a Unicode string, if necessary.
    """

    def fixup(m):
        text = m.group(0)
        if text[:2] == '&#':
            try:
                if text[:3] == '&#x':
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))

            except ValueError:
                pass

        else:
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass

        return text

    return re.sub('&#?\\w+;', fixup, text)


class DictConfig(ConfigParser.ConfigParser):
    """
    http://stackoverflow.com/questions/3220670/read-all-the-contents-in-ini-file-into-dictionary-with-python
    """

    def __init__(self, cf):
        ConfigParser.ConfigParser.__init__(self)
        self._path = cf
        self.load()

    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)

        return d

    def from_dict(self, d):
        for k in d:
            self._sections[k] = d[k]

    def load(self):
        self.read(self._path)

    def save(self):
        with open(self._path, 'w') as (cf):
            self.write(cf)


def authenticate(f):

    def wrapper(so, *args, **kwargs):
        so.authenticate()
        f(so, *args, **kwargs)

    return wrapper