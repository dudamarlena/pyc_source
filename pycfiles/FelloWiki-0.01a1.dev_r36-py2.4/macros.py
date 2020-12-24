# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fellowiki/controllers/wikiparser/macros.py
# Compiled at: 2006-11-21 20:30:39
"""fellowiki wiki parser: macro support

TODO
    
"""
import re
from parser import Token, XMLElement, BetweenParagraphsXHTML, PROC
from util import remove_backslashes_and_whitespace
SPLIT = 'split'
ESCAPE = 'escape'
DEFERRED = 'deferred'
BLOCK_LEVEL = 'block level'
MACRO = 'macro'

class MacroToken(Token):
    __module__ = __name__

    def render(self, new_token):
        if not self.block_level:
            new_token.prepend(self.xhtml)

    def evaluate(self, result, tokens, state, procs):
        Token.evaluate(self, result, tokens, state, procs)
        self.proc = None
        self.proc_not_deferred = None
        self.parameter = []
        self.xhtml = XMLElement('span')
        self.xhtml.append(self.text)
        self.block_level = False
        match_obj = re.match('\\{\\{(([^\\\\\\}\\|]|\\\\.|\\}(?=[^\\}]))*)\\|(([^\\\\\\}]|\\\\.|\\}(?=[^\\}]))*)\\}\\}', self.text)
        if match_obj:
            (command, _, parms, _) = match_obj.groups()
        else:
            command = self.text[2:-2]
            parms = None
        command = '%s%s' % (MACRO, remove_backslashes_and_whitespace(command))
        try:
            this_proc = procs[command]
        except KeyError:
            self.xhtml.attributes['class'] = 'macro_unresolved'
            return

        self.proc = command
        if parms is not None:
            if this_proc.get(SPLIT):
                if this_proc.get(ESCAPE):
                    self.parameter = [ remove_backslashes_and_whitespace(par[0]) for par in re.findall('(([^\\\\,]|\\\\.)+)(?=|,)', parms) ]
                else:
                    self.parameter = [ par[0] for par in re.findall('(([^\\\\,]|\\\\.)+)(?=|,)', parms) ]
            elif this_proc.get(ESCAPE):
                self.parameter = [
                 remove_backslashes_and_whitespace(parms)]
            else:
                self.parameter = [
                 parms]
        if not this_proc.get(DEFERRED):
            self.proc_not_deferred = this_proc[PROC]
        self.xhtml.translations.append((self.proc, self.proc_not_deferred, self.parameter))
        self.xhtml.attributes['class'] = 'macro_resolved'
        if this_proc.get(BLOCK_LEVEL):
            self.block_level = True
            self.xhtml.tag = 'p'
            self.tokens.insert(0, BetweenParagraphsXHTML(self.token, self.xhtml))
        return


def extend_wiki_parser(wiki_parser):
    wiki_parser.regexes[MACRO] = (
     10, '\\{\\{([^\\\\\\}\\n]|\\\\.|\\}(?=[^\\}]))*\\}\\}', MacroToken, dict(preference=20))