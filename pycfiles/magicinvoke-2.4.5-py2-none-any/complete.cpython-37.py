# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hayden/code/invokestuf/magicinvoke/invoke/completion/complete.py
# Compiled at: 2018-09-26 18:54:26
# Size of source mod 2**32: 5065 bytes
"""
Command-line completion mechanisms, executed by the core ``--complete`` flag.
"""
import glob, os, re, shlex
from ..exceptions import Exit, ParseError
from ..parser import Parser
from ..util import debug, task_name_sort_key

def complete(names, core, initial_context, collection):
    invocation = re.sub('^({}) '.format('|'.join(names)), '', core.remainder)
    debug('Completing for invocation: {!r}'.format(invocation))
    tokens = shlex.split(invocation)
    parser = Parser(initial=initial_context, contexts=(collection.to_contexts()))
    if tokens and tokens[(-1)].startswith('-'):
        tail = tokens[(-1)]
        debug("Invocation's tail {!r} is flag-like".format(tail))
        try:
            debug('Seeking context name in tokens: {!r}'.format(tokens))
            contexts = parser.parse_argv(tokens)
        except ParseError as e:
            try:
                msg = 'Got parser error ({!r}), grabbing its last-seen context {!r}'
                debug(msg.format(e, e.context))
                contexts = [e.context]
            finally:
                e = None
                del e

        debug('Parsed invocation, contexts: {!r}'.format(contexts))
        if contexts:
            context = contexts[(-1)] or initial_context
        else:
            context = contexts[(-1)]
        debug('Selected context: {!r}'.format(context))
        debug('Looking for {!r} in {!r}'.format(tail, context.flags))
        if tail not in context.flags:
            debug('Not found, completing with flag names')
            if tail.startswith('--'):
                for name in filter(lambda x: x.startswith('--'), context.flag_names()):
                    print(name)

            else:
                if tail == '-':
                    for name in context.flag_names():
                        print(name)

                else:
                    pass
        else:
            if context.flags[tail].takes_value:
                debug('Found, and it takes a value, so no completion')
            else:
                debug('Found, takes no value, printing task names')
                print_task_names(collection)
    else:
        debug("Last token isn't flag-like, just printing task names")
        print_task_names(collection)
    raise Exit


def print_task_names(collection):
    for name in sorted((collection.task_names), key=task_name_sort_key):
        print(name)
        for alias in collection.task_names[name]:
            print(alias)


def print_completion_script(shell, names):
    completions = {os.path.splitext(os.path.basename(x))[0]:x for x in glob.glob(os.path.join(os.path.dirname(os.path.realpath(__file__)), '*.completion'))}
    try:
        path = completions[shell]
    except KeyError:
        err = 'Completion for shell "{}" not supported (options are: {}).'
        raise ParseError(err.format(shell, ', '.join(sorted(completions))))

    debug('Printing completion script from {}'.format(path))
    binary = names[0]
    with open(path, 'r') as (script):
        print(script.read().format(binary=binary, spaced_names=(' '.join(names))))