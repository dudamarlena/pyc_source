# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/darkfy/lib/wrappers/torsearch.py
# Compiled at: 2014-12-25 06:48:18
from darkengine import DarkEngine

class Torsearch(DarkEngine):
    """ 
                <Torsearch> class.
        """

    def __init__(self):
        """ 
                        Constructor without parameters.
                        Most of the times, this will be the ONLY method needed to be overwritten.
                """
        self.name = 'i3visio.torsearch'
        self.url = 'https://torsearch.es/en/search?q=' + '<THE_WORD>'
        self.delimiters = {}
        self.delimiters['start'] = "<div class='page-listing col-sm-12'>"
        self.delimiters['end'] = "<div class='row'>"
        self.fields = {}
        self.fields['i3visio.text'] = {'start': "<div class='description'>", 'end': '</div>'}
        self.fields['i3visio.title'] = {'start': "<div class='title'>", 'end': '</a>'}
        self.fields['i3visio.url'] = {'start': "<span class='path'>", 'end': '</span>'}