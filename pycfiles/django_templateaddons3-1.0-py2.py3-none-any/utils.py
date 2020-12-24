# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: templateaddons/../templateaddons/utils.py
# Compiled at: 2016-10-21 19:35:42
import re
from django import template
from django.utils.encoding import force_text
from six import iteritems, text_type

def parse_tag_argument(argument, context):
    """Parses a template tag argument within given context.

    Consider the tag:
    {% my_tag name='Toto' surname="Tata" age=32 size=1.70 person=object.get_person %}

    The values used above are interpreted as:
    - 'Toto' and "Tata" are converted to their string value (without quotes),
    respectively 'Toto' and 'Tata'
    - 32 is converted to an integer
    - 1.70 is converted to a float
    - object.get_person is interpreted as a variable and parsed within the context
    """
    if isinstance(argument, text_type) and argument:
        if argument[0] == argument[(-1)] and argument[0] in ('"', "'"):
            argument = argument[1:-1]
        else:
            m = re.match('(?P<int>\\d+)(\\.(?P<decimal>\\d+))?', argument)
            if m is not None:
                if m.group('decimal'):
                    argument = float(argument)
                else:
                    argument = int(argument)
            else:
                argument = template.Variable(argument).resolve(context)
    return argument


split_re = re.compile('(?P<left>[\\w-]+=)?(?P<right>"(?:[^"\\\\]*(?:\\\\.[^"\\\\]*)*)"|\'(?:[^\'\\\\]*(?:\\\\.[^\'\\\\]*)*)\'|[^\\s]+)')

def split_arguments(str):
    """
    Inspired by django.template.Token.split_contents(), except that arguments
    can be named.
    """
    str = force_text(str)
    str = str.split(' ', 1)
    if not len(str) > 1:
        return []
    str = str[1]
    arguments = []
    for match in split_re.finditer(str):
        left = match.group('left') or ''
        right = match.group('right') or ''
        if right[0] == '"' and right[(-1)] == '"':
            right = '"' + right[1:-1].replace('\\"', '"').replace('\\\\', '\\') + '"'
        elif right[0] == "'" and right[(-1)] == "'":
            right = "'" + right[1:-1].replace("\\'", "'").replace('\\\\', '\\') + "'"
        arguments.append(left + right)

    return arguments


def decode_tag_argument(argument):
    """Extracts argument name and value from the given string"""
    match = re.match('((?P<name>[\\w-]+)=)?(?P<value>.+)', argument)
    if match is None:
        raise template.TemplateSyntaxError("invalid tag argument syntax '%s'" % argument)
    else:
        return {'name': str(match.group('name')), 'value': match.group('value')}
    return


def decode_tag_arguments(token, default_arguments={}):
    """Returns a dictionnary of arguments that can be found in the given token.

    This can be useful to code template tags like this:
    {% my_tag name='Toto' surname="Tata" age=32 size=1.70 person=object.get_person %}
    In this syntax, arguments order is not important.

    You can provide default argument values with the parameter default_arguments.
    """
    arguments = {}
    args = split_arguments(token.contents)
    for arg_name, arg_value in iteritems(default_arguments):
        arguments[arg_name] = arg_value

    for arg in args:
        argument = decode_tag_argument(arg)
        arguments[argument['name']] = argument['value']

    return arguments