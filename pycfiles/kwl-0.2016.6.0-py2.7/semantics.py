# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/text2kwl/semantics.py
# Compiled at: 2016-03-08 17:29:32


class Semantics:

    def _default(self, ast):
        if ast:
            return ast
        return ''

    def adjective(self, ast):
        return self.entry(ast)

    def conjugated_verb(self, ast):
        return ('').join(ast)

    def conjunction(self, ast):
        return (' ').join(ast)

    def determiner(self, ast):
        return self.entry(ast)

    def entry(self, ast):
        if 't' in ast['v'] and 'v' in ast['v']:
            return '%s(%s)' % (ast['t'], self.entry(ast['v']))
        else:
            return ast['t'] + ':' + ast['v']

    def noun(self, ast):
        return self.entry(ast)

    def plural(self, ast):
        return '%s(%s)' % (ast['t'], ast['v'])

    def preposition_p(self, ast):
        ast[0] = ast[0]['v']
        return '%s(%s)' % tuple(ast)

    def pronoun(self, ast):
        return self.entry(ast)

    def subject_verb_object(self, ast):
        return '%s %s %s' % (ast['subject'], ast['verb'], ast['object'])

    def title(self, ast):
        return '%s(%s)' % (ast['t'], ast['v'].lower())

    def tuple(self, ast):
        if 'raw(' in ast[0] and 'raw(' in ast[1]:
            return ast[0].replace(')', '') + ast[1].replace('raw(', ' ')
        else:
            return ('_').join([ast[0], ast[1]])

    def triple(self, ast):
        return '%s(%s_%s)' % (ast[0], ast[1], ast[2])

    def verb_object(self, ast):
        return '%s %s' % (ast['verb'], ast['object'])

    def verb(self, ast):
        return self.entry(ast)

    def sentence(self, ast):
        if type([]) == type(ast):
            return (' ').join(ast)
        else:
            return ast