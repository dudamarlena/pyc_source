# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/darkfy/lib/wrappers/ahmia.py
# Compiled at: 2014-12-25 06:48:18
from darkengine import DarkEngine

class Ahmia(DarkEngine):
    """ 
                <Ahmia> class.
        """

    def __init__(self):
        """ 
                        Constructor without parameters.
                        Most of the times, this will be the ONLY method needed to be overwritten.
                """
        self.name = 'i3visio.ahmia'
        self.url = 'https://ahmia.fi/search/?q=' + '<THE_WORD>'
        self.delimiters = {}
        self.delimiters['start'] = '<li class="hs_site">'
        self.delimiters['end'] = '</li>'
        self.fields = {}
        self.fields['i3visio.date'] = {'start': '<p class="urlinfo">', 'end': '</p>'}
        self.fields['i3visio.text'] = {'start': '<div class="urltext">', 'end': '</div>'}
        self.fields['i3visio.title'] = {'start': '<h3>', 'end': '</h3>'}
        self.fields['i3visio.url'] = {'start': '<p class="links">Access without Tor Browser: ', 'end': '</a>'}