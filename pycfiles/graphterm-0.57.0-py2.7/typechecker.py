# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/graphterm/bin/svgwrite/data/typechecker.py
# Compiled at: 2012-08-15 03:48:07
import sys, re
from svgwrite.data import pattern
from svgwrite.data.colors import colornames
from svgwrite.data.svgparser import TransformListParser, PathDataParser, AnimationTimingParser
from svgwrite.utils import is_string

def iterflatlist(values):
    """ Flatten nested *values*, returns an *iterator*. """
    for element in values:
        if hasattr(element, '__iter__') and not is_string(element):
            for item in iterflatlist(element):
                yield item

        else:
            yield element


INVALID_NAME_CHARS = frozenset([' ', '\t', '\r', '\n', ',', '(', ')'])
WHITESPACE = frozenset([' ', '\t', '\r', '\n'])
SHAPE_PATTERN = re.compile('^rect\\((.*),(.*),(.*),(.*)\\)$')
FUNCIRI_PATTERN = re.compile('^url\\((.*)\\)$')
ICCCOLOR_PATTERN = re.compile('^icc-color\\((.*)\\)$')
COLOR_HEXDIGIT_PATTERN = re.compile('^#[a-fA-F0-9]{3}([a-fA-F0-9]{3})?$')
COLOR_RGB_INTEGER_PATTERN = re.compile('^rgb\\( *\\d+ *, *\\d+ *, *\\d+ *\\)$')
COLOR_RGB_PERCENTAGE_PATTERN = re.compile('^rgb\\( *\\d+% *, *\\d+% *, *\\d+% *\\)$')
NMTOKEN_PATTERN = re.compile('^[a-zA-Z_:][\\w\\-\\.:]*$')

class Full11TypeChecker(object):

    def get_version(self):
        return ('1.1', 'full')

    def is_angle(self, value):
        if self.is_number(value):
            return True
        else:
            if is_string(value):
                return pattern.angle.match(value.strip()) is not None
            return False

    def is_anything(self, value):
        return bool(str(value).strip())

    is_string = is_anything
    is_content_type = is_anything

    def is_color(self, value):
        value = str(value).strip()
        if value.startswith('#'):
            if COLOR_HEXDIGIT_PATTERN.match(value):
                return True
            else:
                return False

        elif value.startswith('rgb('):
            if COLOR_RGB_INTEGER_PATTERN.match(value):
                return True
            if COLOR_RGB_PERCENTAGE_PATTERN.match(value):
                return True
            return False
        return self.is_color_keyword(value)

    def is_color_keyword(self, value):
        return value.strip() in colornames

    def is_frequency(self, value):
        if self.is_number(value):
            return True
        else:
            if is_string(value):
                return pattern.frequency.match(value.strip()) is not None
            return False

    def is_FuncIRI(self, value):
        res = FUNCIRI_PATTERN.match(str(value).strip())
        if res:
            return self.is_IRI(res.group(1))
        return False

    def is_icccolor(self, value):
        res = ICCCOLOR_PATTERN.match(str(value).strip())
        if res:
            return self.is_list_of_T(res.group(1), 'name')
        return False

    def is_integer(self, value):
        if isinstance(value, float):
            return False
        try:
            number = int(value)
            return True
        except:
            return False

    def is_IRI(self, value):
        if is_string(value):
            return bool(value.strip())
        else:
            return False

    def is_length(self, value):
        if value is None:
            return False
        else:
            if isinstance(value, (int, float)):
                return self.is_number(value)
            if is_string(value):
                result = pattern.length.match(value.strip())
                if result:
                    number, tmp, unit = result.groups()
                    return self.is_number(number)
            return False

    is_coordinate = is_length

    def is_list_of_T(self, value, t='string'):

        def split(value):
            if isinstance(value, (int, float)):
                return (value,)
            if is_string(value):
                return iterflatlist(v.split(',') for v in value.split(' '))
            return value

        checker = self.get_func_by_name(t)
        for v in split(value):
            if not checker(v):
                return False

        return True

    def is_four_numbers(self, value):

        def split(value):
            if is_string(value):
                values = iterflatlist(v.strip().split(' ') for v in value.split(','))
                return (v for v in values if v)
            else:
                return iterflatlist(value)

        values = list(split(value))
        if len(values) != 4:
            return False
        checker = self.get_func_by_name('number')
        for v in values:
            if not checker(v):
                return False

        return True

    def is_semicolon_list(self, value):
        return self.is_list_of_T(value.replace(';', ' '), 'number')

    def is_name(self, value):
        chars = frozenset(str(value).strip())
        if not chars or INVALID_NAME_CHARS.intersection(chars):
            return False
        return True

    def is_number(self, value):
        try:
            number = float(value)
            return True
        except:
            return False

    def is_number_optional_number(self, value):
        if is_string(value):
            values = re.split(' *,? *', value.strip())
            if 0 < len(values) < 3:
                for v in values:
                    if not self.is_number(v):
                        return False

                return True
        else:
            try:
                n1, n2 = value
                if self.is_number(n1) and self.is_number(n2):
                    return True
            except TypeError:
                return self.is_number(value)
            except ValueError:
                pass

        return False

    def is_paint(self, value):

        def split_values(value):
            try:
                funcIRI, value = value.split(')', 1)
                values = [funcIRI + ')']
                values.extend(split_values(value))
                return values
            except ValueError:
                return value.split()

        values = split_values(str(value).strip())
        for value in [ v.strip() for v in values ]:
            if value in ('none', 'currentColor', 'inherit'):
                continue
            elif self.is_color(value):
                continue
            elif self.is_icccolor(value):
                continue
            elif self.is_FuncIRI(value):
                continue
            return False

        return True

    def is_percentage(self, value):
        if self.is_number(value):
            return True
        else:
            if is_string(value):
                return pattern.percentage.match(value.strip()) is not None
            return False

    def is_time(self, value):
        if self.is_number(value):
            return True
        else:
            if is_string(value):
                return pattern.time.match(value.strip()) is not None
            return False

    def is_transform_list(self, value):
        if is_string(value):
            return TransformListParser.is_valid(value)
        else:
            return False

    def is_path_data(self, value):
        if is_string(value):
            return PathDataParser.is_valid(value)
        else:
            return False

    def is_XML_Name(self, value):
        return bool(NMTOKEN_PATTERN.match(str(value).strip()))

    def is_shape(self, value):
        res = SHAPE_PATTERN.match(value.strip())
        if res:
            for arg in res.groups():
                if arg.strip() == 'auto':
                    continue
                if not self.is_length(arg):
                    return False

        else:
            return False
        return True

    def is_timing_value_list(self, value):
        if is_string(value):
            return AnimationTimingParser.is_valid(value)
        else:
            return False

    def get_func_by_name(self, funcname):
        return getattr(self, 'is_' + funcname.replace('-', '_'), self.is_anything)

    def check(self, typename, value):
        if typename.startswith('list-of-'):
            t = typename[8:]
            return self.is_list_of_T(value, t)
        return self.get_func_by_name(typename)(value)


FOCUS_CONST = frozenset(['nav-next', 'nav-prev', 'nav-up', 'nav-down', 'nav-left',
 'nav-right', 'nav-up-left', 'nav-up-right', 'nav-down-left',
 'nav-down-right'])

class Tiny12TypeChecker(Full11TypeChecker):

    def get_version(self):
        return ('1.2', 'tiny')

    def is_boolean(self, value):
        if isinstance(value, bool):
            return True
        if is_string(value):
            return value.strip().lower() in ('true', 'false')
        return False

    def is_number(self, value):
        try:
            number = float(value)
            if -32767.9999 <= number <= 32767.9999:
                return True
            return False
        except:
            return False

    def is_focus(self, value):
        return str(value).strip() in FOCUS_CONST