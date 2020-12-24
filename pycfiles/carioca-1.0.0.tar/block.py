# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/scott/.virtualenvs/carinata/lib/python2.7/site-packages/carinata/block.py
# Compiled at: 2014-08-05 19:47:36
__doc__ = 'A simple block class to wrap spec blocks'
from . import utils

class Block(object):
    """Represent a block structure by indent, name, description and code"""
    test = 'test'
    describe = 'describe'
    context = 'context'
    before = 'before'
    after = 'after'
    let = 'let'
    it = 'it'
    valid_children = {test: [
            describe], 
       describe: [
                describe, context, before, after, let, it], 
       context: [
               context, before, after, let, it], 
       before: [], after: [], let: [], it: []}

    def __init__(self, indent, name, words, lineno, rest=None):
        self.indent = len(indent)
        self.name = name
        self.words = words
        self.lineno = lineno
        self.code = []
        self.decorators = None
        self.args = '(self)'
        if rest:
            if self.name == self.let and not rest.startswith('return'):
                rest = 'return (%s)' % rest
            self.code.append((lineno, rest))
        if self.name in [self.before, self.after]:
            self.words += utils.uuid_hex()
        return

    def __eq__(self, other):
        return self.name == other.name and self.words == other.words

    def __hash__(self):
        return hash((self.name, self.words))

    def __repr__(self):
        return '<%s: %s>' % (self.name, self.words)

    def is_applicable(self, indent):
        """Determine whether this block applies at the given indent"""
        if self.name == self.test:
            return True
        if self.indent > indent:
            return False
        if self.indent == indent:
            return self.name not in [self.describe, self.context, self.it]
        return True