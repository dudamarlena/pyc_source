# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\geoffrey\workspace\python-plex\build\lib\plex\lexicons.py
# Compiled at: 2018-02-04 13:34:24
# Size of source mod 2**32: 7110 bytes
import types
from plex import actions
from plex import dfa as DFA
from plex import errors
from plex import machines
from plex import regexps
DUMP_NFA = 1
DUMP_DFA = 2

class State:
    __doc__ = '\n    This class is used as part of a Plex.Lexicon specification to\n    introduce a user-defined state.\n\n    Constructor:\n\n        State(name, token_specifications)\n    '
    name = None
    tokens = None

    def __init__(self, name, tokens):
        self.name = name
        self.tokens = tokens


class Lexicon:
    __doc__ = "\n    Lexicon(specification) builds a lexical analyser from the given\n    |specification|. The specification consists of a list of\n    specification items. Each specification item may be either:\n\n        1) A token definition, which is a tuple:\n\n                (pattern, action)\n\n            The |pattern| is a regular axpression built using the\n            constructors defined in the Plex module.\n\n            The |action| is the action to be performed when this pattern\n            is recognised (see below).\n\n        2) A state definition:\n\n                State(name, tokens)\n\n            where |name| is a character string naming the state,\n            and |tokens| is a list of token definitions as\n            above. The meaning and usage of states is described\n            below.\n\n    Actions\n    -------\n\n    The |action| in a token specication may be one of three things:\n\n        1) A function, which is called as follows:\n\n            function(scanner, text)\n\n        where |scanner| is the relevant Scanner instance, and |text|\n        is the matched text. If the function returns anything\n        other than None, that value is returned as the value of the\n        token. If it returns None, scanning continues as if the IGNORE\n        action were specified (see below).\n\n        2) One of the following special actions:\n\n            IGNORE means that the recognised characters will be treated as\n                   white space and ignored. Scanning will continue until\n                   the next non-ignored token is recognised before returning.\n\n            TEXT   causes the scanned text itself to be returned as the\n                   value of the token.\n\n        3) Any other value, which is returned as the value of the token.\n\n    States\n    ------\n\n    At any given time, the scanner is in one of a number of states.\n    Associated with each state is a set of possible tokens. When scanning,\n    only tokens associated with the current state are recognised.\n\n    There is a default state, whose name is the empty string. Token\n    definitions which are not inside any State definition belong to\n    the default state.\n\n    The initial state of the scanner is the default state. The state can\n    be changed in one of two ways:\n\n        1) Using Begin(state_name) as the action of a token.\n\n        2) Calling the begin(state_name) method of the Scanner.\n\n    To change back to the default state, use '' as the state name.\n    "
    machine = None
    tables = None

    def __init__(self, specifications, debug=None, debug_flags=7, timings=None):
        if type(specifications) != list:
            raise errors.InvalidScanner('Scanner definition is not a list')
        else:
            if timings:
                from plex.timing import time
                total_time = 0.0
                time1 = time()
            else:
                nfa = machines.Machine()
                default_initial_state = nfa.new_initial_state('')
                token_number = 1
                for spec in specifications:
                    if isinstance(spec, State):
                        user_initial_state = nfa.new_initial_state(spec.name)
                        for token in spec.tokens:
                            self.add_token_to_machine(nfa, user_initial_state, token, token_number)
                            token_number = token_number + 1

                    else:
                        if isinstance(spec, tuple):
                            self.add_token_to_machine(nfa, default_initial_state, spec, token_number)
                            token_number = token_number + 1
                        else:
                            raise errors.InvalidToken(token_number, 'Expected a token definition (tuple) or State instance')

                if timings:
                    time2 = time()
                    total_time = total_time + (time2 - time1)
                    time3 = time()
                if debug and debug_flags & 1:
                    debug.write('\n============= NFA ===========\n')
                    nfa.dump(debug)
                dfa = DFA.nfa_to_dfa(nfa, debug=(debug_flags & 3 == 3 and debug))
                if timings:
                    time4 = time()
                    total_time = total_time + (time4 - time3)
                if debug:
                    if debug_flags & 2:
                        debug.write('\n============= DFA ===========\n')
                        dfa.dump(debug)
            if timings:
                timings.write('Constructing NFA : %5.2f\n' % (time2 - time1))
                timings.write('Converting to DFA: %5.2f\n' % (time4 - time3))
                timings.write('TOTAL            : %5.2f\n' % total_time)
        self.machine = dfa

    def add_token_to_machine(self, machine, initial_state, token_spec, token_number):
        try:
            re, action_spec = self.parse_token_definition(token_spec)
            if isinstance(action_spec, actions.Action):
                action = action_spec
            else:
                if callable(action_spec):
                    action = actions.Call(action_spec)
                else:
                    action = actions.Return(action_spec)
            final_state = machine.new_state()
            re.build_machine(machine, initial_state, final_state, match_bol=1,
              nocase=0)
            final_state.set_action(action, priority=(-token_number))
        except errors.PlexError as e:
            raise e.__class__('Token number %d: %s' % (token_number, e))

    def parse_token_definition(self, token_spec):
        if not isinstance(token_spec, tuple):
            raise errors.InvalidToken('Token definition is not a tuple')
        else:
            if len(token_spec) != 2:
                raise errors.InvalidToken('Wrong number of items in token definition')
            pattern, action = token_spec
            raise isinstance(pattern, regexps.RE) or errors.InvalidToken('Pattern is not an RE instance')
        return (pattern, action)

    def get_initial_state(self, name):
        return self.machine.get_initial_state(name)