# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\extra\lark.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 8677 bytes
"""
----------------
hypothesis[lark]
----------------

This extra can be used to generate strings matching any context-free grammar,
using the `Lark parser library <https://github.com/lark-parser/lark>`_.

It currently only supports Lark's native EBNF syntax, but we plan to extend
this to support other common syntaxes such as ANTLR and :rfc:`5234` ABNF.
Lark already `supports loading grammars
<https://github.com/lark-parser/lark#how-to-use-nearley-grammars-in-lark>`_
from `nearley.js <https://nearley.js.org/>`_, so you may not have to write
your own at all.

Note that as Lark is at version 0.x, this module *may* break API compatibility
in minor releases if supporting the latest version of Lark would otherwise be
infeasible.  We may also be quite aggressive in bumping the minimum version of
Lark, unless someone volunteers to either fund or do the maintainence.
"""
from inspect import getfullargspec
from typing import Dict
import attr, lark
from lark.grammar import NonTerminal, Terminal
import hypothesis.strategies._internal.core as st
from hypothesis.errors import InvalidArgument
from hypothesis.internal.conjecture.utils import calc_label_from_name
from hypothesis.internal.validation import check_type
from hypothesis.strategies._internal import SearchStrategy
__all__ = [
 'from_lark']

@attr.s()
class DrawState:
    __doc__ = 'Tracks state of a single draw from a lark grammar.\n\n    Currently just wraps a list of tokens that will be emitted at the\n    end, but as we support more sophisticated parsers this will need\n    to track more state for e.g. indentation level.\n    '
    result = attr.ib(default=(attr.Factory(list)))


def get_terminal_names(terminals, rules, ignore_names):
    """Get names of all terminals in the grammar.

    The arguments are the results of calling ``Lark.grammar.compile()``,
    so you would think that the ``terminals`` and ``ignore_names`` would
    have it all... but they omit terminals created with ``@declare``,
    which appear only in the expansion(s) of nonterminals.
    """
    names = {t.name for t in terminals} | set(ignore_names)
    for rule in rules:
        names |= {t.name for t in rule.expansion if isinstance(t, Terminal) if isinstance(t, Terminal)}
    else:
        return names


class LarkStrategy(SearchStrategy):
    __doc__ = 'Low-level strategy implementation wrapping a Lark grammar.\n\n    See ``from_lark`` for details.\n    '

    def __init__(self, grammar, start, explicit):
        if not isinstance(grammar, lark.lark.Lark):
            raise AssertionError
        else:
            if start is None:
                start = grammar.options.start
            if not isinstance(start, list):
                start = [
                 start]
            self.grammar = grammar
            if 'start' in getfullargspec(grammar.grammar.compile).args:
                terminals, rules, ignore_names = grammar.grammar.compile(start)
            else:
                terminals, rules, ignore_names = grammar.grammar.compile()
        self.names_to_symbols = {}
        for r in rules:
            t = r.origin
            self.names_to_symbols[t.name] = t
        else:
            for t in terminals:
                self.names_to_symbols[t.name] = Terminal(t.name)
            else:
                self.start = st.sampled_from([self.names_to_symbols[s] for s in start])
                self.ignored_symbols = tuple((self.names_to_symbols[n] for n in ignore_names))
                self.terminal_strategies = {st.from_regex((t.pattern.to_regexp()), fullmatch=True):t.name for t in terminals}
                unknown_explicit = set(explicit) - get_terminal_names(terminals, rules, ignore_names)
                if unknown_explicit:
                    raise InvalidArgument('The following arguments were passed as explicit_strategies, but there is no such terminal production in this grammar: %r' % (
                     sorted(unknown_explicit),))
                self.terminal_strategies.update(explicit)
                nonterminals = {}
                for rule in rules:
                    nonterminals.setdefault(rule.origin.name, []).append(tuple(rule.expansion))
                else:
                    for v in nonterminals.values():
                        v.sort(key=len)
                    else:
                        self.nonterminal_strategies = {st.sampled_from(v):k for k, v in nonterminals.items()}
                        self._LarkStrategy__rule_labels = {}

    def do_draw(self, data):
        state = DrawState()
        start = data.draw(self.start)
        self.draw_symbol(data, start, state)
        return ''.join(state.result)

    def rule_label--- This code section failed: ---

 L. 150         0  SETUP_FINALLY        14  'to 14'

 L. 151         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _LarkStrategy__rule_labels
                6  LOAD_FAST                'name'
                8  BINARY_SUBSCR    
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 152        14  DUP_TOP          
               16  LOAD_GLOBAL              KeyError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    56  'to 56'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 153        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _LarkStrategy__rule_labels
               32  LOAD_METHOD              setdefault

 L. 154        34  LOAD_FAST                'name'

 L. 154        36  LOAD_GLOBAL              calc_label_from_name
               38  LOAD_STR                 'LARK:%s'
               40  LOAD_FAST                'name'
               42  BUILD_TUPLE_1         1 
               44  BINARY_MODULO    
               46  CALL_FUNCTION_1       1  ''

 L. 153        48  CALL_METHOD_2         2  ''
               50  ROT_FOUR         
               52  POP_EXCEPT       
               54  RETURN_VALUE     
             56_0  COME_FROM            20  '20'
               56  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 24

    def draw_symbol(self, data, symbol, draw_state):
        if isinstance(symbol, Terminal):
            try:
                strategy = self.terminal_strategies[symbol.name]
            except KeyError:
                raise InvalidArgument('Undefined terminal %r. Generation does not currently support use of %%declare unless you pass `explicit`, a dict of names-to-strategies, such as `{%r: st.just("")}`' % (
                 symbol.name, symbol.name))
            else:
                draw_state.result.append(data.draw(strategy))
        else:
            assert isinstance(symbol, NonTerminal)
            data.start_example(self.rule_label(symbol.name))
            expansion = data.draw(self.nonterminal_strategies[symbol.name])
            for e in expansion:
                self.draw_symbol(data, e, draw_state)
                self.gen_ignore(data, draw_state)
            else:
                data.stop_example()

    def gen_ignore(self, data, draw_state):
        if self.ignored_symbols:
            if data.draw_bits(2) == 3:
                emit = data.draw(st.sampled_from(self.ignored_symbols))
                self.draw_symbol(data, emit, draw_state)

    def calc_has_reusable_values(self, recur):
        return True


def check_explicit(name):

    def inner(value):
        check_type(str, value, 'value drawn from ' + name)
        return value

    return inner


@st.cacheable
@st.defines_strategy_with_reusable_values
def from_lark(grammar: lark.lark.Lark, start: str=None, explicit: Dict[(str, st.SearchStrategy[str])]=None) -> st.SearchStrategy[str]:
    """A strategy for strings accepted by the given context-free grammar.

    ``grammar`` must be a ``Lark`` object, which wraps an EBNF specification.
    The Lark EBNF grammar reference can be found
    `here <https://lark-parser.readthedocs.io/en/latest/grammar/>`_.

    ``from_lark`` will automatically generate strings matching the
    nonterminal ``start`` symbol in the grammar, which was supplied as an
    argument to the Lark class.  To generate strings matching a different
    symbol, including terminals, you can override this by passing the
    ``start`` argument to ``from_lark``.  Note that Lark may remove unreachable
    productions when the grammar is compiled, so you should probably pass the
    same value for ``start`` to both.

    Currently ``from_lark`` does not support grammars that need custom lexing.
    Any lexers will be ignored, and any undefined terminals from the use of
    ``%declare`` will result in generation errors.  To define strategies for
    such terminals, pass a dictionary mapping their name to a corresponding
    strategy as the ``explicit`` argument.

    The :pypi:`hypothesmith` project includes a strategy for Python source,
    based on a grammar and careful post-processing.
    """
    check_type(lark.lark.Lark, grammar, 'grammar')
    if explicit is None:
        explicit = {}
    else:
        check_type(dict, explicit, 'explicit')
        explicit = {v.map(check_explicit('explicit[%r]=%r' % (k, v))):k for k, v in explicit.items()}
    return LarkStrategy(grammar, start, explicit)