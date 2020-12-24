# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/antonin/Programmation/OA/wikiciteparser/.virtualenv/lib/python2.7/site-packages/wikiciteparser/parser.py
# Compiled at: 2016-03-11 17:40:27
from __future__ import unicode_literals
import re, os, lupa, json, mwparserfromhell
from time import sleep
lua = lupa.LuaRuntime()
luacode = b''
luafilepath = os.path.join(os.path.dirname(__file__), b'cs1.lua')
with open(luafilepath, b'r') as (f):
    luacode = f.read()
citation_template_names = set([
 b'Citation',
 b'Cite AV media',
 b'Cite AV media notes',
 b'Cite book',
 b'Cite conference',
 b'Cite DVD notes',
 b'Cite encyclopedia',
 b'Cite episode',
 b'Cite interview',
 b'Cite journal',
 b'Cite mailing list',
 b'Cite map',
 b'Cite news',
 b'Cite newsgroup',
 b'Cite podcast',
 b'Cite press release',
 b'Cite report',
 b'Cite serial',
 b'Cite sign',
 b'Cite speech',
 b'Cite techreport',
 b'Cite thesis',
 b'Cite web',
 b'Cite arXiv'])

def lua_to_python_re(regex):
    rx = re.sub(b'%a', b'[a-zA-Z]', regex)
    rx = re.sub(b'%c', b'[\x7f\x80]', regex)
    rx = re.sub(b'%d', b'[0-9]', rx)
    rx = re.sub(b'%l', b'[a-z]', rx)
    rx = re.sub(b'%p', b'\\p{P}', rx)
    rx = re.sub(b'%s', b'\\s', rx)
    rx = re.sub(b'%u', b'[A-Z]', rx)
    rx = re.sub(b'%w', b'\\w', rx)
    rx = re.sub(b'%x', b'[0-9A-F]', rx)
    return rx


def ustring_match(string, regex):
    return re.match(lua_to_python_re(regex), string) is not None


def ustring_len(string):
    return len(string)


def uri_encode(string):
    return string


def text_split(string, pattern):
    return lua.table_from(re.split(lua_to_python_re(pattern), string))


def nowiki(string):
    try:
        wikicode = mwparserfromhell.parse(string)
        return wikicode.strip_code()
    except (ValueError, mwparserfromhell.parser.ParserError):
        return string


def is_int(val):
    """
    Is this lua object an integer?
    """
    try:
        x = int(val)
        return True
    except (ValueError, TypeError):
        return False


wrapped_type = lua.globals().type

def toPyDict(lua_val):
    """
    Converts a lua dict to a Python one
    """
    wt = wrapped_type(lua_val)
    if wt == b'string':
        return nowiki(lua_val)
    else:
        if wt == b'table':
            dct = {}
            lst = []
            for k, v in sorted(lua_val.items(), key=lambda x: x[0]):
                vp = toPyDict(v)
                if not vp:
                    continue
                if is_int(k):
                    lst.append(vp)
                dct[k] = vp

            if lst:
                return lst
            return dct
        return lua_val


def parse_citation_dict(arguments, template_name=b'citation'):
    """
    Parses the Wikipedia citation into a python dict.

    :param arguments: a dictionary with the arguments of the citation template
    :param template_name: the name of the template used (e.g. 'cite journal', 'citation', and so on)
    :returns: a dictionary used as internal representation in wikipedia for rendering and export to other formats
    """
    arguments[b'_tpl'] = template_name
    lua_table = lua.table_from(arguments)
    lua_result = lua.eval(luacode)(lua_table, ustring_match, ustring_len, uri_encode, text_split, nowiki)
    return toPyDict(lua_result)


def params_to_dict(params):
    """
    Converts the parameters of a mwparserfromhell template to a dictionary
    """
    dct = {}
    for param in params:
        dct[param.name.strip()] = param.value.strip()

    return dct


def is_citation_template_name(template_name):
    """
    Is this name the name of a citation template?
    If true, returns a normalized version of it. Otherwise, returns None
    """
    if not template_name:
        return False
    template_name = template_name.replace(b'_', b' ')
    template_name = template_name.strip()
    template_name = template_name[0].upper() + template_name[1:]
    if template_name in citation_template_names:
        return template_name


def parse_citation_template(template):
    """
    Takes a mwparserfromhell template object that represents
    a wikipedia citation, and converts it to a normalized representation
    as a dict.

    :returns: a dict representing the template, or None if the template provided
        does not represent a citation.
    """
    name = unicode(template.name)
    if not is_citation_template_name(name):
        return
    return parse_citation_dict(params_to_dict(template.params), template_name=name)