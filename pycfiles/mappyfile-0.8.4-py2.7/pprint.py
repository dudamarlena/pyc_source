# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mappyfile\pprint.py
# Compiled at: 2020-01-11 08:01:06
from __future__ import unicode_literals
import sys, logging, numbers
from mappyfile.tokens import COMPOSITE_NAMES, SINGLETON_COMPOSITE_NAMES, REPEATED_KEYS
from mappyfile.validator import Validator
log = logging.getLogger(b'mappyfile')
PY2 = sys.version_info[0] < 3
if PY2:
    str = unicode

class Quoter(object):
    """
    A class to handle adding and standardising quotes around strings
    """

    def __init__(self, quote=b'"'):
        assert quote == b"'" or quote == b'"'
        self.quote = quote
        if self.quote == b"'":
            self.altquote = b'"'
        else:
            self.altquote = b"'"

    def add_quotes(self, val):
        return self._add_quotes(val, self.quote)

    def add_altquotes(self, val):
        return self._add_quotes(val, self.altquote)

    def _add_quotes(self, val, quote):
        return (b'{}{}{}').format(quote, val, quote)

    def in_quotes(self, val):
        return self._in_quotes(val, self.quote) or self._in_quotes(val, self.altquote)

    def _in_quotes(self, val, char):
        return val.startswith(char) and val.endswith(char)

    def escape_quotes(self, val):
        """
        Escape any quotes in a value
        """
        if self.is_string(val) and self._in_quotes(val, self.quote):
            middle = self.remove_quotes(val).replace(b'\\' + self.quote, self.quote)
            middle = middle.replace(self.quote, b'\\' + self.quote)
            val = self.add_quotes(middle)
        return val

    def is_string(self, val):
        return isinstance(val, (bytes, str))

    def remove_quotes(self, val):
        if isinstance(val, list):
            return list(map(self.remove_quotes, val))
        else:
            if not self.is_string(val):
                return val
            if self.in_quotes(val):
                return val[1:-1]
            return val

    def in_brackets(self, val):
        val = val.strip()
        return val.startswith(b'[') and val.endswith(b']')

    def in_parenthesis(self, val):
        val = val.strip()
        return val.startswith(b'(') and val.endswith(b')')

    def in_braces(self, val):
        val = val.strip()
        return val.startswith(b'{') and val.endswith(b'}')

    def in_slashes(self, val):
        val = val.strip()
        return self._in_quotes(val, b'/')

    def standardise_quotes(self, val):
        """
        Change the quotes used to wrap a value to the pprint default
        E.g. "val" to 'val' or 'val' to "val"
        """
        if self._in_quotes(val, self.altquote):
            middle = self.remove_quotes(val)
            val = self.add_quotes(middle)
        return self.escape_quotes(val)


class PrettyPrinter(object):

    def __init__(self, indent=4, spacer=b' ', quote=b'"', newlinechar=b'\n', end_comment=False, **kwargs):
        """
        Option use "    " for spacer with an indent of 1
        """
        assert quote == b"'" or quote == b'"'
        self.indent = indent
        self.spacer = spacer * self.indent
        self.quoter = Quoter(quote)
        self.newlinechar = newlinechar
        self.end_comment = end_comment
        self.end = b'END'
        self.validator = Validator()

    def __is_metadata(self, key):
        """
        Check to see if the property is hidden metadata
        e.g. "__type__", "__comments__", "__position__"
        """
        if key.startswith(b'__') and key.endswith(b'__'):
            return True
        else:
            return False

    def whitespace(self, level, indent):
        return self.spacer * (level + indent)

    def singular(self, s):
        if s == b'points':
            return s
        if s.endswith(b'es'):
            return s[:-2]
        return s[:-1]

    def add_start_line(self, key, level):
        return self.whitespace(level, 1) + key.upper()

    def add_end_line(self, level, indent, key):
        end_line = self.whitespace(level, indent) + self.end
        if self.end_comment:
            end_line = (b'{} # {}').format(end_line, key.upper())
        return end_line

    def __format_line(self, spacer, key, value):
        tmpl = b'{spacer}{key} {value}'
        d = {b'spacer': spacer, 
           b'key': key, 
           b'value': value}
        return tmpl.format(**d)

    def process_key_dict(self, key, d, level):
        """
        Process key value dicts e.g. METADATA "key" "value"
        """
        comments = d.get(b'__comments__', {})
        lines = []
        self._add_type_comment(level, comments, lines)
        lines += [self.add_start_line(key, level)]
        lines += self.process_dict(d, level, comments)
        lines.append(self.add_end_line(level, 1, key))
        return lines

    def process_dict(self, d, level, comments):
        """
        Process keys and values within a block
        """
        lines = []
        for k, v in d.items():
            if not self.__is_metadata(k):
                qk = self.quoter.add_quotes(k)
                qv = self.quoter.add_quotes(v)
                line = self.__format_line(self.whitespace(level, 2), qk, qv)
                line += self.process_attribute_comment(comments, k)
                lines.append(line)

        return lines

    def process_config_dict(self, key, d, level):
        """
        Process the CONFIG block
        """
        lines = []
        for k, v in d.items():
            k = (b'CONFIG {}').format(self.quoter.add_quotes(k.upper()))
            v = self.quoter.add_quotes(v)
            lines.append(self.__format_line(self.whitespace(level, 1), k, v))

        return lines

    def process_repeated_list(self, key, lst, level):
        """
        Process blocks of repeated keys e.g. FORMATOPTION
        """
        lines = []
        for v in lst:
            k = key.upper()
            v = self.quoter.add_quotes(v)
            lines.append(self.__format_line(self.whitespace(level, 1), k, v))

        return lines

    def process_projection(self, key, lst, level):
        lines = [
         self.add_start_line(key, level)]
        if self.quoter.is_string(lst):
            val = self.quoter.add_quotes(lst)
            lines.append((b'{}{}').format(self.whitespace(level, 2), val))
        elif len(lst) == 1 and lst[0].upper() == b'AUTO':
            lines.append((b'{}{}').format(self.whitespace(level, 2), b'AUTO'))
        else:
            for v in lst:
                v = self.quoter.add_quotes(v)
                lines.append((b'{}{}').format(self.whitespace(level, 2), v))

        lines.append(self.add_end_line(level, 1, key))
        return lines

    def format_pair_list(self, key, pair_list, level):
        """
        Process lists of pairs (e.g. PATTERN block)
        """
        lines = [
         self.add_start_line(key, level)]
        list_spacer = self.spacer * (level + 2)
        pairs = [ (b'{}{} {}').format(list_spacer, p[0], p[1]) for p in pair_list ]
        lines += pairs
        lines.append(self.add_end_line(level, 1, key))
        return lines

    def format_repeated_pair_list(self, key, root_list, level):
        """
        Process (possibly) repeated lists of pairs e.g. POINTs blocks
        """
        lines = []

        def depth(L):
            return isinstance(L, (tuple, list)) and max(map(depth, L)) + 1

        if depth(root_list) == 2:
            root_list = [root_list]
        for pair_list in root_list:
            lines += self.format_pair_list(key, pair_list, level)

        return lines

    def is_composite(self, val):
        if isinstance(val, dict) and b'__type__' in val:
            return True
        else:
            return False

    def is_hidden_container(self, key, val):
        """
        The key is not one of the Mapfile keywords, and its
        values are a list
        """
        if key in ('layers', 'classes', 'styles', 'symbols', 'labels', 'outputformats',
                   'features', 'scaletokens', 'composites', 'joins') and isinstance(val, list):
            return True
        else:
            return False

    def pprint(self, composites):
        """
        Print out a nicely indented Mapfile
        """
        if composites and not isinstance(composites, list):
            composites = [
             composites]
        lines = []
        for composite in composites:
            type_ = composite[b'__type__']
            if type_ in ('metadata', 'validation'):
                lines += self.process_key_dict(type_, composite, level=0)
            else:
                lines += self._format(composite)

        result = str(self.newlinechar.join(lines))
        return result

    def get_attribute_properties(self, type_, attr):
        jsn_schema = self.validator.get_expanded_schema(type_)
        props = jsn_schema[b'properties']
        try:
            attr_props = props[attr]
        except KeyError as ex:
            log.error((b"The key '{}' was not found in the JSON schema for '{}'").format(attr, type_))
            log.error(ex)
            return {}

        return attr_props

    def is_expression(self, option):
        return b'description' in option and option[b'description'] == b'expression'

    def check_options_list(self, options_list, value):
        for option in options_list:
            if b'enum' in option and value.lower() in option[b'enum']:
                if value.lower() == b'end':
                    return self.quoter.add_quotes(value)
                else:
                    return value.upper()

            elif self.is_expression(option):
                if value.endswith(b"'i") or value.endswith(b'"i'):
                    return value

        if self.quoter.in_slashes(value):
            return value
        else:
            return self.quoter.add_quotes(value)

    def format_value(self, attr, attr_props, value):
        """
        TODO - refactor and add more specific tests (particularly for expressions)
        """
        if isinstance(value, bool):
            return str(value).upper()
        if any(i in ('enum', ) for i in attr_props):
            if not isinstance(value, numbers.Number):
                return value.upper()
            else:
                return value

        if b'type' in attr_props and attr_props[b'type'] == b'string':
            if self.is_expression(attr_props) and self.quoter.in_slashes(value):
                return value
            else:
                if self.is_expression(attr_props) and (value.endswith(b"'i") or value.endswith(b'"i')):
                    return value
                return self.quoter.add_quotes(value)

        if any(i in ('oneOf', 'anyOf') for i in attr_props):
            if b'oneOf' in attr_props:
                options_list = attr_props[b'oneOf']
            else:
                options_list = attr_props[b'anyOf']
            if self.quoter.is_string(value):
                if self.quoter.in_parenthesis(value):
                    pass
                elif attr == b'expression' and self.quoter.in_braces(value):
                    pass
                elif attr != b'text' and self.quoter.in_brackets(value):
                    pass
                elif value.startswith(b'NOT ') and self.quoter.in_parenthesis(value[4:]):
                    value = (b'NOT {}').format(value[4:])
                else:
                    value = self.check_options_list(options_list, value)
        if isinstance(value, list):
            new_values = []
            for v in value:
                if not isinstance(v, numbers.Number) and attr != b'polaroffset':
                    v = self.quoter.add_quotes(v)
                new_values.append(v)

            value = (b' ').join(list(map(str, new_values)))
        else:
            value = self.quoter.escape_quotes(value)
        return value

    def process_attribute(self, type_, attr, value, level):
        """
        Process one of the main composite types (see the type_ value)
        """
        attr_props = self.get_attribute_properties(type_, attr)
        value = self.format_value(attr, attr_props, value)
        line = self.__format_line(self.whitespace(level, 1), attr.upper(), value)
        return line

    def format_comment(self, spacer, value):
        return (b'{}{}').format(spacer, value)

    def process_composite_comment(self, level, comments, key):
        """
        Process comments for composites such as MAP, LAYER etc.
        """
        if key not in comments:
            comment = b''
        else:
            value = comments[key]
            spacer = self.whitespace(level, 0)
            if isinstance(value, list):
                comments = [ self.format_comment(spacer, v) for v in value ]
                comment = self.newlinechar.join(comments)
            else:
                comment = self.format_comment(spacer, value)
        return comment

    def process_attribute_comment(self, comments, key):
        if key not in comments:
            comment = b''
        else:
            value = comments[key]
            spacer = b' '
            if isinstance(value, list):
                value = (b' ').join(value)
            comment = self.format_comment(spacer, value)
        return comment

    def _add_type_comment(self, level, comments, lines):
        comment = self.process_composite_comment(level, comments, b'__type__')
        if comment:
            lines.append(str(comment))

    def _format(self, composite, level=0):
        lines = []
        comments = composite.get(b'__comments__', {})
        if isinstance(composite, dict) and b'__type__' in composite:
            type_ = composite[b'__type__']
            if not type_ in COMPOSITE_NAMES.union(SINGLETON_COMPOSITE_NAMES):
                raise AssertionError
                is_hidden = False
                self._add_type_comment(level, comments, lines)
                s = self.whitespace(level, 0) + type_.upper()
                lines.append(s)
            for attr, value in composite.items():
                if self.__is_metadata(attr):
                    continue
                elif self.is_hidden_container(attr, value):
                    for v in value:
                        lines += self._format(v, level + 1)

                elif attr == b'pattern':
                    lines += self.format_pair_list(attr, value, level)
                elif attr in ('metadata', 'validation', 'values'):
                    lines += self.process_key_dict(attr, value, level)
                elif attr == b'projection':
                    lines += self.process_projection(attr, value, level)
                elif attr in REPEATED_KEYS:
                    lines += self.process_repeated_list(attr, value, level)
                elif attr == b'points':
                    lines += self.format_repeated_pair_list(attr, value, level)
                elif attr == b'config':
                    lines += self.process_config_dict(attr, value, level)
                elif self.is_composite(value):
                    lines += self._format(value, level + 1)
                else:
                    line = self.process_attribute(type_, attr, value, level)
                    line += self.process_attribute_comment(comments, attr)
                    lines.append(line)

            is_hidden or lines.append(self.add_end_line(level, 0, type_))
        return lines