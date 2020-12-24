# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/stacktraces/functions.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import re
from sentry.stacktraces.platform import get_behavior_family_for_platform
from sentry.utils.safe import setdefault_path
_windecl_hash = re.compile('^@?(.*?)@[0-9]+$')
_rust_hash = re.compile('::h[a-z0-9]{16}$')
_cpp_trailer_re = re.compile('(\\bconst\\b|&)$')
_lambda_re = re.compile('(?x)\n    # gcc\n    (?:\n        \\{\n            lambda\\(.*?\\)\\#\\d+\n        \\}\n    ) |\n    # msvc\n    (?:\n        \\blambda_[a-f0-9]{32}\\b\n    ) |\n    # clang\n    (?:\n        \\$_\\d+\\b\n    )\n')
PAIRS = {'(': ')', '{': '}', '[': ']', '<': '>'}

def replace_enclosed_string(s, start, end, replacement=None):
    if start not in s:
        return s
    else:
        depth = 0
        rv = []
        pair_start = None
        for idx, char in enumerate(s):
            if char == start:
                if depth == 0:
                    pair_start = idx
                depth += 1
            elif char == end:
                depth -= 1
                if depth == 0:
                    if replacement is not None:
                        if callable(replacement):
                            rv.append(replacement(s[pair_start + 1:idx], pair_start))
                        else:
                            rv.append(replacement)
            elif depth == 0:
                rv.append(char)

        return ('').join(rv)


def split_func_tokens(s):
    buf = []
    rv = []
    stack = []
    end = 0
    for idx, char in enumerate(s):
        if char in PAIRS:
            stack.append(PAIRS[char])
        elif stack and char == stack[(-1)]:
            stack.pop()
            if not stack:
                buf.append(s[end:idx + 1])
                end = idx + 1
        elif not stack:
            if char.isspace():
                if buf:
                    rv.append(buf)
                buf = []
            else:
                buf.append(s[end:idx + 1])
            end = idx + 1

    if buf:
        rv.append(buf)
    return [ ('').join(x) for x in rv ]


def trim_function_name(function, platform, normalize_lambdas=True):
    """Given a function value from the frame's function attribute this returns
    a trimmed version that can be stored in `function_name`.  This is only used
    if the client did not supply a value itself already.
    """
    if get_behavior_family_for_platform(platform) != 'native':
        return function
    else:
        if function in ('<redacted>', '<unknown>'):
            return function
        original_function = function
        function = function.strip()
        if function.startswith(('[', '+[', '-[')):
            return function
        while True:
            match = _cpp_trailer_re.search(function)
            if match is None:
                break
            function = function[:match.start()].rstrip()

        function = function.replace('operator<<', 'operator⟨⟨').replace('operator<', 'operator⟨').replace('operator()', 'operator◯').replace(' -> ', ' ⟿ ')
        if normalize_lambdas:
            function = _lambda_re.sub('lambda', function)

        def process_args(value, start):
            value = value.strip()
            if value in ('anonymous namespace', 'operator'):
                return '(%s)' % value
            return ''

        function = replace_enclosed_string(function, '(', ')', process_args)

        def process_generics(value, start):
            if start == 0:
                return '<%s>' % replace_enclosed_string(value, '<', '>', process_generics)
            return '<T>'

        function = replace_enclosed_string(function, '<', '>', process_generics)
        tokens = split_func_tokens(function)
        try:
            func_token = tokens[(tokens.index('⟿') - 1)]
        except ValueError:
            if tokens:
                func_token = tokens[(-1)]
            else:
                func_token = None

        if func_token:
            function = func_token.replace('⟨', '<').replace('◯', '()').replace(' ⟿ ', ' -> ')
        else:
            function = original_function
        function = _rust_hash.sub('', function)
        return _windecl_hash.sub('\\1', function)


def get_function_name_for_frame(frame, platform=None):
    """Given a frame object or dictionary this returns the actual function
    name trimmed.
    """
    if hasattr(frame, 'get_raw_data'):
        frame = frame.get_raw_data()
    if frame.get('raw_function'):
        return frame.get('function')
    rv = frame.get('function')
    if rv:
        return trim_function_name(rv, frame.get('platform') or platform)


def set_in_app(frame, value):
    orig_in_app = frame.get('in_app')
    if orig_in_app == value:
        return
    else:
        orig_in_app = int(orig_in_app) if orig_in_app is not None else -1
        setdefault_path(frame, 'data', 'orig_in_app', value=orig_in_app)
        frame['in_app'] = value
        return