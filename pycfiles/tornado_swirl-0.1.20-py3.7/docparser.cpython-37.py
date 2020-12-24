# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tornado_swirl/docparser.py
# Compiled at: 2019-12-17 19:30:30
# Size of source mod 2**32: 14174 bytes
"""Docstring line parser implementation.

Returns:
    [type] -- [description]
"""
import numbers, re
from tornado_swirl.openapi.types import Type
from tornado_swirl._parser_model import Param, PathSpec, SchemaSpec
_QUERY_HEADERS = 'query headers'
_PATH_HEADERS = 'path headers'
_BODY_HEADERS = 'body headers'
_COOKIE_HEADERS = 'cookies'
_HEADER_HEADERS = 'headers'
_ERROR_HEADERS = 'errors'
_RESPONSE_HEADERS = 'responses'
_PROPERTY_HEADERS = 'properties'
_TAGS_HEADERS = 'tags'
_DEPRECATED_HEADERS = 'deprecated'
_SECURITY_HEADERS = 'security'
QUERYSPEC_REGEX = '^(?P<name>[\\w][\\-\\[\\]\\w_0-9]*)(\\s+\\((?P<type>[\\w\\-, :/\\[\\]]+)\\)?)?\\s*(--(\\s+((?P<required>required|optional)\\.)?(?P<description>.*)?)?)?$'
PARAM_MATCHER = re.compile(QUERYSPEC_REGEX, re.IGNORECASE)
RESPONSE_REGEX = '^((http\\s+)?((?P<code>\\d+)\\s+))?response:$'
RESPONSE_MATCHER = re.compile(RESPONSE_REGEX, re.IGNORECASE)
ERRORSPEC_REGEX = '^(?P<code>\\d+)\\s*--\\s*(?P<description>.*)$'
ERRORSPEC_MATCHER = re.compile(ERRORSPEC_REGEX, re.IGNORECASE)

class Number(numbers.Number):
    __doc__ = 'Convenience type class to represent float or int'

    def __new__(cls, val):
        if str(val).find('.'):
            try:
                return float(val)
            except ValueError:
                return val

        try:
            return int(val)
        except ValueError:
            return val


class Boolean(object):
    __doc__ = 'Convenience type class to convert bool values'

    def __new__(cls, val):
        return val in ('True', 'true', '1', True)


_PROPS_TYPE_LOOKUP = {Boolean: ('exclusiveMinimum', 'exclusiveMaximum', 'uniqueItems', 'allowEmptyValue', 'deprecated',
 'readOnly', 'writeOnly'), 
 Number: ('minimum', 'maximum', 'multipleOf', 'minItems', 'maxItems', 'maxLength', 'minLength',
 'uniqueItems', 'minProperties', 'maxProperties')}

def _lookup_type_of(name):
    for typ, names in _PROPS_TYPE_LOOKUP.items():
        if name in names:
            return typ

    return str


def _process_security_params(fsm_obj, ptype):
    lines = fsm_obj.buffer.splitlines()
    cleaned_lines = _clean_lines(lines)
    params = {}
    for _, line in enumerate(cleaned_lines):
        matcher = PARAM_MATCHER.match(line.lstrip())
        if not matcher:
            continue
        name = matcher.group('name')
        spec = matcher.group('description')
        params[name] = spec.split(',') if spec else []

    return params


def _process_params(fsm_obj, ptype, required_func=None):
    if required_func is None:
        required_func = lambda x, y: x == y
    lines = fsm_obj.buffer.splitlines()
    cleaned_lines = _clean_lines(lines)
    params = {}
    for i, line in enumerate(cleaned_lines):
        matcher = PARAM_MATCHER.match(line.lstrip())
        if not matcher:
            continue
        open_type = matcher.group('type')
        param = Param(name=(matcher.group('name')), ptype=ptype,
          required=(required_func(str(matcher.group('required')).lower(), 'required')),
          order=i)
        description = str(matcher.group('description')).strip()
        desc, kwargs = _get_description_props(description)
        param.description = desc.strip()
        param.type = Type(open_type, **kwargs)
        params[param.name] = param

    return params


def _process_path(fsm_obj, **kwargs):
    fsm_obj.spec.path_params = _process_params(fsm_obj, 'path', lambda x, y: True)
    _set_default_type(fsm_obj.spec.path_params, 'string')
    fsm_obj.buffer = ''


def _get_real_value(name, value):
    dtype = _lookup_type_of(name)
    return dtype(value)


def _get_description_props(description):
    """Returns description, kwargs"""
    kwargs = {}
    index = description.rfind(':')
    while index > -1:
        description, value = description[0:index], description[index + 1:]
        boundary = max(description.rfind(' '), description.rfind('\n'))
        description, name = description[0:boundary], description[boundary + 1:]
        kwargs[name] = _get_real_value(name, value.strip())
        index = description.rfind(':')

    return (description, kwargs)


def _set_default_type(dval, dtype):
    for name, param in dval.items():
        if param.type.name == 'None':
            dval[name].type = dtype


def _process_query(fsm_obj, **kwargs):
    fsm_obj.spec.query_params = _process_params(fsm_obj, 'query')
    _set_default_type(fsm_obj.spec.query_params, Type('string'))
    fsm_obj.buffer = ''


def _process_body(fsm_obj, **kwargs):
    fsm_obj.spec.body_params = _process_params(fsm_obj, 'body', lambda x, y: True)
    _set_default_type(fsm_obj.spec.body_params, Type('string'))
    fsm_obj.buffer = ''


def _process_cookie(fsm_obj, **kwargs):
    fsm_obj.spec.cookie_params = _process_params(fsm_obj, 'cookie')
    _set_default_type(fsm_obj.spec.cookie_params, Type('string'))
    fsm_obj.buffer = ''


def _process_header(fsm_obj, **kwargs):
    fsm_obj.spec.header_params = _process_params(fsm_obj, 'header')
    _set_default_type(fsm_obj.spec.header_params, Type('string'))
    fsm_obj.buffer = ''


def _process_response(fsm_obj, **kwargs):
    cur_code = kwargs.get('code', '200')
    res = _process_params(fsm_obj, 'response')
    if res:
        item = list(res.values())[0]
        item.name = cur_code
        fsm_obj.spec.responses.update({cur_code: item})
    fsm_obj.buffer = ''


def _process_properties(fsm_obj, **kwargs):
    fsm_obj.spec.properties = _process_params(fsm_obj, 'property')
    _set_default_type(fsm_obj.spec.properties, Type('string'))
    fsm_obj.buffer = ''


def _process_errors(fsm_obj, **kwargs):
    fsm_obj.spec.responses.update(_process_params(fsm_obj, 'response'))
    fsm_obj.buffer = ''


def _process_tags(fsm_obj, **kwargs):
    fsm_obj.spec.tags = _process_params(fsm_obj, 'tags')
    _set_default_type(fsm_obj.spec.tags, Type('string'))
    fsm_obj.buffer = ''


def _process_security(fsm_obj, **kwargs):
    fsm_obj.spec.security = _process_security_params(fsm_obj, 'security')
    fsm_obj.buffer = ''


def _process_deprecated(fsm_obj, **kwargs):
    fsm_obj.spec.deprecated = True
    fsm_obj.buffer = ''


def _clean_lines(lines):
    cleaned_lines, lines = [
     lines[0].strip()], lines[1:]
    while lines:
        cur_line, lines = lines[0], lines[1:]
        try:
            cur_line.lstrip().index(' -- ')
            cleaned_lines.append(cur_line.strip())
        except ValueError:
            cleaned_lines[-1] = cleaned_lines[(-1)] + ' ' + cur_line.strip()

    return cleaned_lines


_HEADERS = {_QUERY_HEADERS: ('query param(s|eter(s)?)?:', _process_query), 
 _PATH_HEADERS: ('(path|url) param(s|eter(s)?)?:', _process_path), 
 _BODY_HEADERS: ('(request\\s*)? body:', _process_body), 
 _COOKIE_HEADERS: ('cookie(s|(\\s*param(s|eter(s)?)?)?)?:', _process_cookie), 
 _HEADER_HEADERS: ('(http\\s+)?(request\\s+)?header(s)?:', _process_header), 
 _ERROR_HEADERS: ('(error(s|\\s*response(s)?)?|default(\\s*response(s)?)):',
                  _process_errors), 
 
 _RESPONSE_HEADERS: ('(((http\\s+)?((?P<code>\\d+)\\s+))?response|return(s?)):',
                     _process_response), 
 
 _PROPERTY_HEADERS: ('(propert(y|ies):)', _process_properties), 
 _TAGS_HEADERS: ('tag(s?):', _process_tags), 
 _DEPRECATED_HEADERS: ('(deprecated|\\[deprecated\\])', _process_deprecated), 
 _SECURITY_HEADERS: ('security:', _process_security)}
_HEADERS_REGEX = {key:(re.compile('^' + val + '$', re.IGNORECASE), processor) for key, (val, processor) in _HEADERS.items()}
_ALL_HEADERS = '|'.join([rs for rs, _ in _HEADERS.values()])
_ALL_HEADERS_REGEX = re.compile('^(' + _ALL_HEADERS + ')$', re.IGNORECASE)
_SECTION_HEADER_REGEX = re.compile('^([\\w ]+):$')
_DEPRECATED_HEADER_REGEX = re.compile('^(deprecated|\\[deprecated\\])$', re.IGNORECASE)
S_START = 0
S_SUMMARY = 1
S_DESCRIPTION = 2
S_END = 3
S_BLANK = 4
S_SECTION = 5

def _get_header_type(section_header):
    for name, (regex, _) in _HEADERS_REGEX.items():
        matcher = regex.match(str(section_header))
        if matcher:
            if name == _RESPONSE_HEADERS:
                return (
                 name, {'code': matcher.group('code') or '200'})
            return (
             name, None)

    return (None, None)


def _transition_blank(fsm_obj):
    pass


def _transitionbuffer(fsm_obj):
    fsm_obj.buffer += fsm_obj.current_line.lstrip()


def _transition_section(fsm_obj):
    fsm_obj.cur_header = fsm_obj.current_line.strip()


def _transition_processbuffer(fsm_obj):
    htype, params = _get_header_type(fsm_obj.cur_header)
    _, processor = _HEADERS_REGEX.get(htype, (None, None))
    if not processor:
        return
    elif params:
        processor(fsm_obj, **params)
    else:
        processor(fsm_obj)
    fsm_obj.cur_header = None
    fsm_obj.buffer = ''


def _transition_processbuffer_new_section(fsm_obj):
    _transition_processbuffer(fsm_obj)
    _transition_section(fsm_obj)


def _transition_summary(fsm_obj):
    fsm_obj.spec.summary = fsm_obj.buffer
    fsm_obj.buffer = ''


def _transition_description(fsm_obj):
    fsm_obj.spec.description += fsm_obj.buffer
    fsm_obj.buffer = ''


def _is_generic_line(line):
    line = line.strip()
    if _SECTION_HEADER_REGEX.match(line):
        return False
    if _DEPRECATED_HEADER_REGEX.match(line):
        return False
    if line == '':
        return False
    if _is_end(line):
        return False
    return True


def _is_end(line):
    return line.strip() == '--THE END--'


def _is_blank_line(line):
    return line.strip() == ''


def _is_generic_line_or_blank(line):
    return _is_generic_line(line) or _is_blank_line(line)


def _is_section_header(line):
    stripped = line.strip()
    return _SECTION_HEADER_REGEX.match(stripped) or _DEPRECATED_HEADER_REGEX.match(stripped)


FSM_MAP = (
 {'src':S_START, 
  'dst':S_SUMMARY,  'condition':_is_generic_line,  'callback':_transitionbuffer},
 {'src':S_SUMMARY, 
  'dst':S_SUMMARY,  'condition':_is_generic_line, 
  'callback':_transitionbuffer},
 {'src':S_SUMMARY, 
  'dst':S_BLANK,  'condition':_is_blank_line, 
  'callback':_transition_summary},
 {'src':S_SUMMARY, 
  'dst':S_END,  'condition':_is_end, 
  'callback':_transition_summary},
 {'src':S_BLANK, 
  'dst':S_DESCRIPTION,  'condition':_is_generic_line,  'callback':_transitionbuffer},
 {'src':S_DESCRIPTION, 
  'dst':S_DESCRIPTION,  'condition':_is_generic_line, 
  'callback':_transitionbuffer},
 {'src':S_DESCRIPTION, 
  'dst':S_BLANK,  'condition':_is_blank_line, 
  'callback':_transition_description},
 {'src':S_START, 
  'dst':S_SECTION,  'condition':_is_section_header, 
  'callback':_transition_section},
 {'src':S_BLANK, 
  'dst':S_SECTION,  'condition':_is_section_header, 
  'callback':_transition_section},
 {'src':S_SECTION, 
  'dst':S_SECTION,  'condition':_is_generic_line_or_blank, 
  'callback':_transitionbuffer},
 {'src':S_SECTION, 
  'dst':S_SECTION,  'condition':_is_section_header, 
  'callback':_transition_processbuffer_new_section},
 {'src':S_SECTION, 
  'dst':S_END,  'condition':_is_end, 
  'callback':_transition_processbuffer},
 {'src':S_START, 
  'dst':S_END,  'condition':_is_end,  'callback':_transition_processbuffer},
 {'src':S_BLANK, 
  'dst':S_END,  'condition':_is_end,  'callback':_transition_processbuffer},
 {'src':S_DESCRIPTION, 
  'dst':S_END,  'condition':_is_end,  'callback':_transition_processbuffer})

class _ParseFSM:
    __doc__ = 'Internal line docstring parser'

    def __init__(self, fsm_map, lines, spec='operation'):
        self.input_lines = lines + ['--THE END--']
        self.current_state = S_START
        self.current_line = None
        if spec == 'operation':
            self.spec = PathSpec()
        else:
            self.spec = SchemaSpec()
        self._buffer = ''
        self._cur_code = None
        self._cur_header = None
        self.fsm_map = fsm_map

    @property
    def buffer(self):
        """Get the buffer"""
        return self._buffer

    @buffer.setter
    def buffer(self, val):
        self._buffer = val

    @property
    def cur_header(self):
        """Get current detected header"""
        return self._cur_header

    @cur_header.setter
    def cur_header(self, val):
        """Get current detected header"""
        self._cur_header = val

    def run(self):
        """Parser run"""
        for line in self.input_lines:
            if not self._process_next(line):
                print("skip '{}' in {}".format(line, self.current_state))

    def _process_next(self, line):
        self.current_line = line
        frozen_state = self.current_state
        for transition in FSM_MAP:
            if transition['src'] == frozen_state and self._iterate_re_evaluators(line, transition):
                return True

        return False

    def _iterate_re_evaluators(self, line, transition):
        condition = transition['condition']
        if condition(line):
            self._update_state(transition['dst'], transition['callback'])
            return True
        return False

    def _update_state(self, new_state, callback):
        self.current_state = new_state
        callback(self)


def parse_from_docstring(docstring, spec='operation'):
    """Returns path spec from docstring"""
    lines = docstring.splitlines(True)
    parser = _ParseFSM(FSM_MAP, lines, spec)
    parser.run()
    return parser.spec