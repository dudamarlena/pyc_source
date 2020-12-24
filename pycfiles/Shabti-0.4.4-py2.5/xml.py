# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/shabti/templates/moinmoin/data/moin/data/plugin/parser/xml.py
# Compiled at: 2010-04-25 12:11:22
"""
        MoinMoin - XML Source Parser

    @copyright: 2005 by Davin Dubeau <davin.dubeau@gmail.com>
    @license: GNU GPL, see COPYING for details.

"""
from MoinMoin.util.ParserBase import ParserBase
Dependencies = []

class Parser(ParserBase):
    parsername = 'ColorizedXML'
    extensions = ['.xml']
    Dependencies = []

    def setupRules(self):
        ParserBase.setupRules(self)
        self.addRulePair('Comment', '<!--', '-->')
        self.addRule('Number', '[0-9]+')
        self.addRule('SPChar', '[=<>/"]')
        self.addRule('ResWord', '(?!<)[\\w\\s]*(?![\\w="])?(?![\\w\\s\\.<])+(?!>)*')