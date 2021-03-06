# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scopedconfig/parser.py
# Compiled at: 2019-03-17 14:14:39
from scopedconfig import error
SYMBOL_OPTION = ':'
SYMBOL_SECTION_BEGIN = '{'
SYMBOL_SECTION_END = '}'
SYMBOL_WORD = ''
FSM_START = 0
FSM_STOP = 1
FSM_SECTION_BEGIN = 2
FSM_SECTION_END = 3
FSM_CHILD_BEGIN = 4
FSM_CHILD_END = 5
FSM_SECTION_NAME = 6
FSM_OPTION_NAME = 7
FSM_OPTION_VALUE = 8
FSM_SYMBOL_OPTION = 9

class ScopedParser(object):
    """Parse scoped configuration into AST-like structure

    Config file syntax is as follows:
   
       <object-name>
       {
           [attribute-name: [attribute-value]
           ...
       }
    """

    def __init__(self, lexer, caster=None):
        self._lexer = lexer
        self._caster = caster

    def load_section(self, tokens):
        obj = {'_name': '', 
           '_children': []}
        state = FSM_START
        for (token, symbol) in tokens:
            if state == FSM_START:
                tokens.send(2)
                if symbol == SYMBOL_SECTION_END:
                    state = FSM_SECTION_END
                elif symbol == SYMBOL_OPTION:
                    state = FSM_OPTION_NAME
                else:
                    state = FSM_SECTION_NAME
            elif state == FSM_SECTION_NAME:
                tokens.send(2)
                state = FSM_SECTION_BEGIN
            elif state == FSM_SECTION_BEGIN:
                (token, symbol) = next(tokens)
                tokens.send(3)
                if symbol != SYMBOL_SECTION_BEGIN:
                    raise error.ScopedConfigError('%s missing object beginning sign: %s' % (
                     self, token))
                state = FSM_CHILD_BEGIN
            elif state == FSM_CHILD_BEGIN:
                next(tokens)
                child_object = self.load_section(tokens)
                child_object['_name'] = token
                obj['_children'].append(child_object)
                state = FSM_CHILD_END
            elif state == FSM_CHILD_END:
                if symbol != SYMBOL_SECTION_END:
                    raise error.ScopedConfigError('%s missing object closure sign: %s' % (self, token))
                state = FSM_START
            elif state == FSM_SECTION_END:
                tokens.send(2)
                if symbol != SYMBOL_SECTION_END:
                    raise error.ScopedConfigError('%s missing object closure sign: %s' % (self, token))
                state = FSM_STOP
            elif state == FSM_OPTION_NAME:
                if token in obj:
                    raise error.ScopedConfigError('%s multiple option occurrence: %s' % (self, token))
                obj[token] = []
                tokens.send(2)
                state = FSM_OPTION_VALUE
            elif state == FSM_OPTION_VALUE:
                option = token
                while True:
                    try:
                        (token, symbol) = next(tokens)
                    except StopIteration:
                        state = FSM_STOP
                        break

                    if symbol != SYMBOL_WORD:
                        tokens.send(2)
                        if symbol == SYMBOL_SECTION_BEGIN:
                            tokens.send(2)
                            del obj[option][-1]
                        state = FSM_START
                        break
                    if self._caster:
                        token = self._caster(token)
                    obj[option].append(token)

            elif state == FSM_STOP:
                break
            else:
                raise error.ScopedConfigError('%s unknown FSM state: %s' % (self, state))

        return obj

    def parse(self):
        try:
            return self.load_section(iter(self._lexer))
        except error.EofError:
            raise error.ScopedConfigError('%s premature EOF while reading config file' % self)