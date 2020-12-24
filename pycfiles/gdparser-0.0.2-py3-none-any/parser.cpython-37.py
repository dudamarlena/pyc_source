# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lxper/lxperservice/gdparser/gdparser/parser.py
# Compiled at: 2020-02-09 21:06:26
# Size of source mod 2**32: 10718 bytes
import re
from typing import List, Dict, Optional

def extract_enums(text):
    """Extract enums from text
    
    Choices should satisfy following conditions:
    - is surrouned by curly braces, 
    - able to evaluated as valid set
    
    Args:
        text (str): text to find choices
        
    Returns:
        Union[None, List]: None if choices are not found, else the List containing possible choices in sorted order
    """
    pat = '\\{[^\\{\\}]+\\}'
    out = None
    for m in re.finditer(pat, text):
        cb = m.group()
        try:
            out = eval(cb)
            assert isinstance(out, set)
            out = sorted(list(out))
        except:
            pass

    return out


test_text_1 = "Supported values are the one of {'ab', 'cd', 'ef'} {we want to}"
test_text_2 = 'Supported values are the one of {we want to find out}'
assert extract_enums(test_text_1) == ['ab', 'cd', 'ef']
assert extract_enums(test_text_2) is None

def extract_params(text: str, required: bool, javascript_type: bool) -> List[Dict[(str, Optional[str])]]:
    """Extract parameters from args/kwargs section body text.
    
    Args:
        text (str): Args/Kwargs 섹션의 바디 텍스트
        required (bool): 필수 파라미터라고 기록할지 여부
        javascript_type (bool): str -> string, int-> integer, float -> number, bool -> boolean 과 같이 자바스크립트 타입으로 변형할지
          만일 변환이 불가능한 데이터가 존재시 입력 타입을 그대로 반환
        
    Examples:
        [{'name': 'text', 
         'type': 'str', 
         'description': 'input text', 
         'required': True,
         'enum': ['a', 'b']}]
    """
    py_js_typemap = {'str':'string', 
     'int':'integer',  'bool':'boolean',  'float':'number'}
    pat = re.compile('\\s*([A-Za-z_]+)\\s*\\(([A-Za-z_\\.]+)\\)\\s*:\\s*')
    tmp = []
    for m in pat.finditer(text):
        s, e = m.span()
        name, type_ = m.group(1).strip(), m.group(2).strip()
        tmp.append((s, e, name, type_))

    tmp.append((len(text), None, None, None))
    out = []
    for cur, nxt in zip(tmp, tmp[1:]):
        _, s, n, t = cur
        e, _, _, _ = nxt
        d = text[s:e].strip()
        if javascript_type:
            t = py_js_typemap.get(t, t)
        o = {'name':n,  'type':t, 
         'description':d, 
         'required':required, 
         'enum':extract_enums(d)}
        out.append(o)

    return out


def clear_indent(text: str) -> str:
    """
    """
    lines = text.splitlines()
    n_lines = len(lines)
    effective_lines = []
    for idx, line in enumerate(lines, 1):
        if len(line.replace(' ', '')) == 0:
            effective_lines.append((True, line))
        else:
            effective_lines.append((False, line))

    i = 0
    while True:
        try:
            chars = [line[i] for should_skip, line in effective_lines if not should_skip]
            can_remove_char = all((c.isspace() for c in chars))
            if not can_remove_char:
                raise IndexError
            else:
                i += 1
        except IndexError:
            newlines = [line if should_skip else line[i:] for should_skip, line in effective_lines]
            return '\n'.join(newlines)


def parse_sections(text: str, supported_headers: Optional[List]=None) -> List[Dict[(str, str)]]:
    if supported_headers is None:
        supported_headers = [
         'Args', 'Arguments', 'Attention', 'Attributes', 'Caution', 'Danger',
         'Error', 'Example', 'Examples', 'Example Request', 'Hint', 'Important', 'Keyword Args',
         'Keyword Arguments', 'Kwargs', 'Methods', 'Note', 'Notes', 'Other Parameters',
         'Parameters', 'Return', 'Returns', 'Raises', 'References', 'See Also',
         'Tip', 'Todo', 'Warning', 'Warnings', 'Warns', 'Yield', 'Yields']
    sh = '|'.join(supported_headers)
    pat = re.compile('(?<=\\s)({supported_headers})\\s*:\\n'.format(supported_headers=sh), flags=(re.S))
    tmp = []
    tmp.append((None, 0, 'Overview'))
    for m in pat.finditer(text):
        s, e = m.span()
        section_header = m.group(0)[:-2]
        tmp.append((s, e, section_header))

    tmp.append((len(text), None, None))
    out = []
    for cur, nxt in zip(tmp, tmp[1:]):
        _, s, section_header = cur
        e, _, _ = nxt
        o = {'section_header':section_header,  'section_body':text[s:e]}
        out.append(o)

    return out


def parse_docstring(text: str, supported_headers=None, args_headers=None, kwargs_headers=None, remove_indent=True, javascript_type=True):
    """Parses Google-style Docstring.
    
    Args:
        text (str): docstring to parse written in Google-docstring format.
        
    Keyword Arguments:
        supported_headers (List[str] or None): list of text which can be recognized as the section headers, 
            if None, the values are
            ['Args', 'Arguments', 'Attention', 'Attributes', 'Caution', 'Danger',
             'Error', 'Example', 'Examples', 'Example Request', 'Hint', 'Important', 'Keyword Args',
             'Keyword Arguments', 'Kwargs', 'Methods', 'Note', 'Notes', 'Other Parameters',
             'Parameters', 'Return', 'Returns', 'Raises', 'References', 'See Also',
             'Tip', 'Todo', 'Warning', 'Warnings', 'Warns', 'Yield', 'Yields']
             
        args_headers (List[str] or None): list of text which can be recognized as the argument section headers. 
            Argument section headers is special which is parsed and fill the parameters of the final output.
            if None, the values are
            ['Args', 'Arguments', 'Parameters']
            
        kwargs_headers (List[str] or None): same as the args headers, except that the 'required' key of each parameter will become False.
            if None, the values are
            ['Kwargs', 'Keyword Args', 'Keyword Arguments']
            
        remove_indent (bool): whether indent is deleted or not. indent is defined as the 
            common whitespace length across the lines within same section.
            
        javascript_type (bool): whether the python type notation should be converted into javascript type.
            currently following four types are converted.
            'str'- 'string', 'int'- 'integer', 'bool'- 'boolean', 'float'- 'number'
            if the type is not in the among the supported types, returned as it is without conversion.
        
    Returns:
        dict: 
            - description (str) : function description
            - sections (List[Dict]) : the list of each section, each section is composed of two keys,
                 - section_header (str) 
                 - section_body (str)
            - parameters (List[Dict]) : the list of each parameter, each parameter is composed of five keys,
                 - name (str): parameter name
                 - type (str): parameter type
                 - description (str): parameter description
                 - required (bool) : when the parameter is found in the Args section, it becomes True. 
                      if found in Kwargs section, it become False
                 - enum (List or None) : You can make enum notation by using curly braces in the parameter description. 
                      if the curly brace notation can be evaluated as set, the set value is used.
                      e.g. {'ab', 'cd'} - ['ab', 'cd']
                           {10, 20, 30} - [10, 20, 30]

    
    """
    raw_sections = parse_sections(text, supported_headers=supported_headers)
    args_headers = args_headers or ['Args', 'Arguments', 'Parameters']
    kwargs_headers = kwargs_headers or ['Kwargs', 'Keyword Args', 'Keyword Arguments']
    parameters, sections = [], []
    description = None
    for section in raw_sections:
        if remove_indent:
            section['section_body'] = clear_indent(section['section_body'])
        if section['section_header'] in args_headers:
            params = extract_params((section['section_body']), True, javascript_type=javascript_type)
            parameters.extend(params)
        elif section['section_header'] in kwargs_headers:
            params = extract_params((section['section_body']), False, javascript_type=javascript_type)
            parameters.extend(params)
        elif section['section_header'] in ('Overview', ):
            description = section['section_body']
        else:
            sections.append(section)

    return {'description':description,  'sections':sections, 
     'parameters':parameters}