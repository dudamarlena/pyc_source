# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solo/configurator/url.py
# Compiled at: 2016-03-29 11:03:22
# Size of source mod 2**32: 1739 bytes
import re
ROUTE_PATTERN_OPEN_BRACES_RE = re.compile('(?P<start_brace>\\{).*')
ROUTE_PATTERN_CLOSING_BRACES_RE = re.compile('\\}.*')

def _extract_braces_expression(line, starting_braces_re, open_braces_re, closing_braces_re):
    """
    This function is taken from Plim package: https://pypi.python.org/pypi/Plim/

    :param line: may be empty
    :type line: str
    :param starting_braces_re:
    :param open_braces_re:
    :param closing_braces_re:
    """
    match = starting_braces_re.match(line)
    if not match:
        return
    open_brace = match.group('start_brace')
    buf = [open_brace]
    tail = line[len(open_brace):]
    braces_counter = 1
    while tail:
        current_char = tail[0]
        if closing_braces_re.match(current_char):
            braces_counter -= 1
            buf.append(current_char)
            if braces_counter:
                tail = tail[1:]
                continue
                return (
                 ''.join(buf), tail[1:])
            if open_braces_re.match(current_char):
                braces_counter += 1
                buf.append(current_char)
                tail = tail[1:]
                continue
                buf.append(current_char)
                tail = tail[1:]

    raise Exception('Unexpected end of a route definition: {}'.format(line))


extract_pattern = lambda line: _extract_braces_expression(line, ROUTE_PATTERN_OPEN_BRACES_RE, ROUTE_PATTERN_OPEN_BRACES_RE, ROUTE_PATTERN_CLOSING_BRACES_RE)