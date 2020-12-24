# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/complete.py
# Compiled at: 2015-05-27 10:28:33
"""CommandProcessor completion routines"""
import pyficache, re
from trepan.lib import complete as Mcomplete

def complete_token_filtered(aliases, prefix, expanded):
    """Find all starting matches in dictionary *aliases* that start
    with *prefix*, but filter out any matches already in
    *expanded*."""
    complete_ary = list(aliases.keys())
    results = [cmd for cmd in complete_ary if cmd.startswith(prefix)] and not (cmd in aliases and expanded not in aliases[cmd])
    return sorted(results, key=lambda pair: pair[0])


def completer(self, str, state, last_token=''):
    next_blank_pos, token = Mcomplete.next_token(str, 0)
    if len(token) == 0 and not 0 == len(last_token):
        return ['', None]
    match_pairs = Mcomplete.complete_token_with_next(self.commands, token)
    match_hash = {}
    for pair in match_pairs:
        match_hash[pair[0]] = pair[1]

    alias_pairs = Mcomplete.complete_token_filtered_with_next(self.aliases, token, match_hash, list(self.commands.keys()))
    match_pairs += alias_pairs
    macro_pairs = Mcomplete.complete_token_filtered_with_next(self.macros, token, match_hash, self.commands.keys())
    match_pairs += macro_pairs
    if len(str) == next_blank_pos:
        if len(match_pairs) == 1 and match_pairs[0][0] == token:
            match_pairs[0][0] += ' '
        return sorted([pair[0] for pair in match_pairs]) + [None]
    else:
        for pair in alias_pairs:
            match_hash[pair[0]] = pair[1]

        if len(match_pairs) > 1:
            return [
             None]
        if str[(-1)] == ' ' and str.rstrip().endswith(token):
            token = ''
        return next_complete(str, next_blank_pos, match_pairs[0][1], token) + [None]


def next_complete(str, next_blank_pos, cmd, last_token):
    next_blank_pos, token = Mcomplete.next_token(str, next_blank_pos)
    if hasattr(cmd, 'complete_token_with_next'):
        match_pairs = cmd.complete_token_with_next(token)
        if len(match_pairs) == 0:
            return [None]
        else:
            if next_blank_pos == len(str) and 1 == len(match_pairs) and match_pairs[0][0] == token:
                match_pairs[0][0] += ' '
            if next_blank_pos >= len(str):
                return sorted([pair[0] for pair in match_pairs])
            if len(match_pairs) == 1:
                return next_complete(str, next_blank_pos, match_pairs[0][1], token)
            return sorted([pair[0] for pair in match_pairs])
    elif hasattr(cmd, 'complete'):
        matches = cmd.complete(token)
        if 0 == len(matches):
            return [None]
        return matches
    return [
     None]


def complete_bpnumber(self, prefix):
    return Mcomplete.complete_brkpts(self.core.bpmgr, prefix)


def complete_break_linenumber(self, prefix):
    canonic_name = self.proc.curframe.f_code.co_filename
    completions = pyficache.trace_line_numbers(canonic_name)
    return Mcomplete.complete_token([str(i) for i in completions], prefix)


def complete_identifier(cmd, prefix):
    """Complete an arbitrary expression."""
    if not cmd.proc.curframe:
        return [
         None]
    else:
        ns = cmd.proc.curframe.f_globals.copy()
        ns.update(cmd.proc.curframe.f_locals)
        if '.' in prefix:
            dotted = prefix.split('.')
            try:
                obj = ns[dotted[0]]
                for part in dotted[1:-1]:
                    obj = getattr(obj, part)

            except (KeyError, AttributeError):
                return []

            pre_prefix = '.'.join(dotted[:-1]) + '.'
            return [pre_prefix + n for n in dir(obj) if n.startswith(dotted[(-1)])]
        else:
            return Mcomplete.complete_token(ns.keys(), prefix)
        return


def complete_id_and_builtins(cmd, prefix):
    if not cmd.proc.curframe:
        return [
         None]
    else:
        items = list(cmd.proc.curframe.f_builtins.keys()) + complete_identifier(cmd, prefix)
        return Mcomplete.complete_token(items, prefix)


if __name__ == '__main__':
    import inspect
    from trepan.processor import cmdproc as Mcmdproc
    from trepan.processor.command import mock as Mmock
    from trepan.processor.command import base_cmd as mBaseCmd
    d = Mmock.MockDebugger()
    cmdproc = Mcmdproc.CommandProcessor(d.core)
    cmdproc.curframe = inspect.currentframe()
    cmd = mBaseCmd.DebuggerCommand(cmdproc)
    print(complete_identifier(cmd, ''))
    print(complete_identifier(cmd, 'M'))
    print(complete_id_and_builtins(cmd, 'M'))