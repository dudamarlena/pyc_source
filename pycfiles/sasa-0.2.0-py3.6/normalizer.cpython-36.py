# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/sasa/normalizer.py
# Compiled at: 2019-04-09 16:17:45
# Size of source mod 2**32: 1546 bytes
import re
__author__ = 'Dogan Can, Abe Kazemzadeh, Hao Wang'
__copyright__ = 'Copyright 2013, University of Southern California'
__credits__ = []
__license__ = 'http://www.apache.org/licenses/LICENSE-2.0'
__version__ = '1.0'
__maintainer__ = 'Last modified by Abe Kazemzadeh'
__email__ = "See the authors' website"

class N0(object):

    def normalize(self, tokens):
        return [token.lower() for token in tokens]


class N1(object):

    def __init__(self):
        self.url = re.compile('^\\b[^\\s]*[a-z]\\.[a-z]{2,3}[^\\s]*$')
        self.emopos = re.compile("^[<>]?[:;=8][\\-o\\*\\']?[\\)\\]dDpP\\}]|[\\)\\]dDpP\\}][\\-o\\*\\']?[:;=8][<>]?$")
        self.emoneg = re.compile("^[<>]?[:;=8][\\-o\\*\\']?[\\(\\[/\\{\\\\]|[\\(\\[/\\{\\\\][\\-o\\*\\']?[:;=8][<>]?$")
        self.emo = re.compile("^[<>]?[:;=8][\\-o\\*\\']?[\\)\\]\\(\\[dDpP/\\:\\}\\{@\\|\\\\]|[\\)\\]\\(\\[dDpP/\\:\\}\\{@\\|\\\\][\\-o\\*\\']?[:;=8][<>]?$")
        self.repeat = re.compile('^(?P<first_char>\\W)(?P=first_char){1,}$')
        self.lowercase = re.compile('^.*[a-z].*$')

    def normalize(self, tokens):
        norms = []
        for token in tokens:
            token = self.url.sub('URL', token)
            token = self.emopos.sub('EMOTICON+', token)
            token = self.emoneg.sub('EMOTICON-', token)
            token = self.emo.sub('EMOTICON', token)
            token = self.repeat.sub(lambda m: m.group(0)[0] + '_REPEAT', token)
            token = self.lowercase.sub(lambda m: m.group(0).lower(), token)
            norms += [token]

        return norms