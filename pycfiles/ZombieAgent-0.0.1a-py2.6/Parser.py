# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/ZombieAgent/Plugin/Parser.py
# Compiled at: 2012-01-04 17:03:27


def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"


def parse_cli_params(params):
    params_out = {}
    for pair in params:
        pair = _escape_split('=', pair)
        key = pair[0]
        value = True
        if len(pair) == 2:
            value = pair[1]
        params_out[key] = value

    return params_out


def _escape_split(sep, argstr):
    r"""
        Allows for escaping of the separator: e.g. task:arg='foo\, bar'
        
        It should be noted that the way bash et. al. do command line parsing, those
        single quotes are required.
        """
    escaped_sep = '\\%s' % sep
    if escaped_sep not in argstr:
        return argstr.split(sep)
    (before, _, after) = argstr.partition(escaped_sep)
    startlist = before.split(sep)
    unfinished = startlist[(-1)]
    startlist = startlist[:-1]
    endlist = _escape_split(sep, after)
    unfinished += sep + endlist[0]
    return startlist + [unfinished] + endlist[1:]