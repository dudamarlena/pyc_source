# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/indra/ipc/russ.py
# Compiled at: 2008-07-28 17:15:44
"""@file russ.py
@brief Recursive URL Substitution Syntax helpers
@author Phoenix

Many details on how this should work is available on the wiki:
https://wiki.secondlife.com/wiki/Recursive_URL_Substitution_Syntax

Adding features to this should be reflected in that page in the
implementations section.

$LicenseInfo:firstyear=2007&license=mit$

Copyright (c) 2007-2008, Linden Research, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
$/LicenseInfo$
"""
import urllib
from indra.ipc import llsdhttp

class UnbalancedBraces(Exception):
    __module__ = __name__


class UnknownDirective(Exception):
    __module__ = __name__


class BadDirective(Exception):
    __module__ = __name__


def format_value_for_path(value):
    if type(value) in [list, tuple]:
        return ('/').join([ urllib.quote(str(item)) for item in value ])
    else:
        return urllib.quote(str(value))


def format(format_str, context):
    """@brief Format format string according to rules for RUSS.
@see https://osiris.lindenlab.com/mediawiki/index.php/Recursive_URL_Substitution_Syntax
@param format_str The input string to format.
@param context A map used for string substitutions.
@return Returns the formatted string. If no match, the braces remain intact.
"""
    while True:
        all_matches = _find_sub_matches(format_str)
        if not all_matches:
            break
        substitutions = 0
        while True:
            matches = all_matches.pop()
            matches.reverse()
            for pos in matches:
                end = format_str.index('}', pos)
                if format_str[(pos + 1)] == '$':
                    value = context[format_str[pos + 2:end]]
                    if value is not None:
                        value = format_value_for_path(value)
                elif format_str[(pos + 1)] == '%':
                    value = _build_query_string(context.get(format_str[pos + 2:end]))
                elif format_str[pos + 1:pos + 5] == 'http' or format_str[pos + 1:pos + 5] == 'file':
                    value = _fetch_url_directive(format_str[pos + 1:end])
                else:
                    raise UnknownDirective, format_str[pos:end + 1]
                if value is not None:
                    format_str = format_str[:pos] + str(value) + format_str[end + 1:]
                    substitutions += 1

            if substitutions:
                break
            if not all_matches:
                break

        if not substitutions:
            break

    return format_str


def _find_sub_matches(format_str):
    """@brief Find all of the substitution matches.
@param format_str the RUSS conformant format string.    
@return Returns an array of depths of arrays of positional matches in input.
"""
    depth = 0
    matches = []
    for pos in range(len(format_str)):
        if format_str[pos] == '{':
            depth += 1
            if not len(matches) == depth:
                matches.append([])
            matches[(depth - 1)].append(pos)
            continue
        if format_str[pos] == '}':
            depth -= 1
            continue

    if not depth == 0:
        raise UnbalancedBraces, format_str
    return matches


def _build_query_string(query_dict):
    """    @breif given a dict, return a query string. utility wrapper for urllib.
    @param query_dict input query dict
    @returns Returns an urlencoded query string including leading '?'.
    """
    if query_dict:
        keys = query_dict.keys()
        keys.sort()

        def stringize(value):
            if type(value) in (str, unicode):
                return value
            else:
                return str(value)

        query_list = [ urllib.quote(str(key)) + '=' + urllib.quote(stringize(query_dict[key])) for key in keys ]
        return '?' + ('&').join(query_list)
    else:
        return ''


def _fetch_url_directive(directive):
    """*FIX: This only supports GET"""
    commands = directive.split('|')
    resource = llsdhttp.get(commands[0])
    if len(commands) == 3:
        resource = _walk_resource(resource, commands[2])
    return resource


def _walk_resource(resource, path):
    path = path.split('/')
    for child in path:
        if not child:
            continue
        resource = resource[child]

    return resource