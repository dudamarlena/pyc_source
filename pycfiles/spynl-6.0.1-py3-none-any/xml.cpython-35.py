# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/workspace/spynl-git/venv/src/spynl/spynl/main/serial/xml.py
# Compiled at: 2017-01-16 09:58:52
# Size of source mod 2**32: 3311 bytes
"""Handle XML content"""
from xml.etree.ElementTree import fromstring, ParseError
from xml.sax import saxutils
import re
from spynl.main.serial import objects
from spynl.main.serial.exceptions import MalformedRequestException
expression = re.compile('^\\s*\\<')

def loads(body, headers=None, context=None):
    """return body as XML"""
    try:
        root = fromstring(body)
    except ParseError as e:
        raise MalformedRequestException('application/xml', str(e))

    dic = __loads(root, True)
    return objects.SpynlDecoder(context=context)(dic)


def __loads(element, force_dict=False):
    """Recurse through etree node, return parsed structure"""
    if len(element) and element.get('type') != 'collection' or force_dict:
        result = {}
        for field in element:
            result[field.tag] = __loads(field)

    else:
        if element.get('type') == 'collection':
            result = [__loads(item) for item in element]
        else:
            result = None
    if element.text:
        result = element.text.strip()
    return result


def dumps(body, pretty=True):
    """return XML body as string"""
    result = __dumps(body)
    if pretty:
        result = prettify_xml(result)
    ustr = ''
    for item in result:
        ustr += str(item)

    return '<response>{}{}</response>'.format(pretty * '\n', ustr)


def __dumps(value):
    """Recurse through dict/list structure, returning XML text"""
    result = []
    if isinstance(value, (list, tuple, set)):
        for item in value:
            result.append('<item>')
            result.extend(__dumps(item))
            result.append('</item>')

    else:
        if isinstance(value, dict):
            for field, value in value.items():
                if field.startswith('$'):
                    field = field[1:]
                alpha = re.match('\\D', field)
                start_tag = '<' + (field if alpha else 'item')
                if not alpha:
                    start_tag += ' key="{}"'.format(field)
                if isinstance(value, (list, tuple)):
                    start_tag += ' type="collection"'
                start_tag += '>'
                end_tag = '</{}>' if alpha else '</item>'
                result.append(start_tag.format(field))
                result.extend(__dumps(value))
                result.append(end_tag.format(field))

        else:
            if isinstance(value, str):
                value = saxutils.escape(value)
            result.append(objects.encode(value))
    return result


def sniff(body):
    """sniff to see if body is xml"""
    return bool(re.match(expression, body))


def prettify_xml(xmlstr):
    """add indentation to create pretty xml"""
    indent = 1
    for i in range(len(xmlstr)):
        item = xmlstr[i]
        if item.startswith('</'):
            indent -= 1
            tag = xmlstr[(i - 1)].startswith('<')
            yield tag * ' ' * indent * 4 + item + '\n'
        else:
            if item.startswith('<'):
                tag = xmlstr[(i + 1)].startswith('<')
                yield ' ' * indent * 4 + item + tag * '\n'
                indent += 1
            else:
                yield item

    raise StopIteration()