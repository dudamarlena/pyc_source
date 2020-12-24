# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kdb/plugins/spell.py
# Compiled at: 2014-04-26 09:00:59
"""Spell Checker

This plugin provides to the user a command that
can be used to check the spelling of words and
give suggestions for incorrectly spelled words.
"""
__version__ = '0.0.1'
__author__ = 'James Mills, prologic at shortcircuit dot net dot au'
from enchant import request_dict
from circuits import Component
from ..plugin import BasePlugin
DEFAULT_LANGUAGE = 'en_US'

class Commands(Component):
    channel = 'commands'

    def spell(self, source, target, args):
        """Check the spelling of the given word.

        Syntax: SPELL <word>
        """
        if not args:
            return 'No word specified.'
        word = args
        if self.parent.dictionary.check(word):
            msg = ('{0:s} is spelled correctly.').format(word)
        else:
            suggestions = self.parent.dictionary.suggest(word)
            msg = ('{0:s} ? Try: {1:s}').format(word, (' ').join(suggestions))
        return msg


class Spell(BasePlugin):
    """Spell Checker"""

    def init(self, *args, **kwargs):
        super(Spell, self).init(*args, **kwargs)
        self.language = DEFAULT_LANGUAGE
        self.dictionary = request_dict(self.language)
        Commands().register(self)