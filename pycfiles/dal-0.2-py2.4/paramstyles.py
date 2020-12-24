# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dal/dbapi/paramstyles.py
# Compiled at: 2007-06-15 17:41:24
import string, re
PARAMSTYLES = {'all': ['qmark', 'numeric', 'named', 'format', 'pyformat'], 'sequence': ['qmark', 'numeric', 'format'], 'dict': ['named', 'pyformat'], 'token': ['qmark', 'format']}
QUOTE_CHARS = [
 '"', "'"]
ESCAPE_CHARS = [
 '\\']
PLACEHOLDER_TOKENS = {'qmark': '?', 'format': '%s'}
PLACEHOLDER_EXPS = {'qmark': re.compile('(\\?)'), 'numeric': re.compile('(:\\d+)'), 'named': re.compile('(:\\w+)'), 'format': re.compile('(%s)'), 'pyformat': re.compile('(%\\(\\w+\\)s)')}
PARAM_TYPES = {'qmark': lambda : [], 'numeric': lambda : [], 'named': lambda : {}, 'format': lambda : [], 'pyformat': lambda : {}}

def param_add(param_num, param_name, param, params):
    try:
        params.append(param)
    except AttributeError:
        params[param_name] = param

    return params


PARAMNAME_EXPS = {'named': re.compile(':(\\w+)'), 'pyformat': re.compile('%\\((\\w+)\\)s')}
PARAMNAME_GENS = {'qmark': lambda param_num, placeholder: 'param%d' % param_num, 
   'numeric': lambda param_num, placeholder: 'param%d' % param_num, 
   'named': lambda param_num, placeholder: PARAMNAME_EXPS['named'].findall(placeholder)[0], 
   'format': lambda param_num, placeholder: 'param%d' % param_num, 
   'pyformat': lambda param_num, placeholder: PARAMNAME_EXPS['pyformat'].findall(placeholder)[0]}
PARAMVALUE_GENS = {'qmark': lambda param_num, param_name, params: params[(param_num - 1)], 
   'numeric': lambda param_num, param_name, params: params[(param_num - 1)], 
   'named': lambda param_num, param_name, params: params[param_name], 
   'format': lambda param_num, param_name, params: params[(param_num - 1)], 
   'pyformat': lambda param_num, param_name, params: params[param_name]}
PLACEHOLDER_SUBS = {'qmark': lambda param_num, param_name: '?', 
   'numeric': lambda param_num, param_name: ':%d' % param_num, 
   'named': lambda param_num, param_name: ':%s' % param_name, 
   'format': lambda param_num, param_name: '%s', 
   'pyformat': lambda param_num, param_name: '%%(%s)s' % param_name}
CONVERSION_MATRIX = {'qmark': {'qmark': lambda query, params: (
                     query, params), 
             'numeric': lambda query, params: paramstyle_to_paramstyle('qmark', 'numeric', query, params), 
             'named': lambda query, params: paramstyle_to_paramstyle('qmark', 'named', query, params), 
             'format': lambda query, params: paramstyle_to_paramstyle('qmark', 'format', query, params), 
             'pyformat': lambda query, params: paramstyle_to_paramstyle('qmark', 'pyformat', query, params)}, 
   'numeric': {'qmark': lambda query, params: paramstyle_to_paramstyle('numeric', 'qmark', query, params), 
               'numeric': lambda query, params: (
                         query, params), 
               'named': lambda query, params: paramstyle_to_paramstyle('numeric', 'named', query, params), 
               'format': lambda query, params: paramstyle_to_paramstyle('numeric', 'format', query, params), 
               'pyformat': lambda query, params: paramstyle_to_paramstyle('numeric', 'pyformat', query, params)}, 
   'named': {'qmark': lambda query, params: paramstyle_to_paramstyle('named', 'qmark', query, params), 
             'numeric': lambda query, params: paramstyle_to_paramstyle('named', 'numeric', query, params), 
             'named': lambda query, params: (
                     query, params), 
             'format': lambda query, params: paramstyle_to_paramstyle('named', 'format', query, params), 
             'pyformat': lambda query, params: paramstyle_to_paramstyle('named', 'pyformat', query, params)}, 
   'format': {'qmark': lambda query, params: paramstyle_to_paramstyle('format', 'qmark', query, params), 
              'numeric': lambda query, params: paramstyle_to_paramstyle('format', 'numeric', query, params), 
              'named': lambda query, params: paramstyle_to_paramstyle('format', 'named', query, params), 
              'format': lambda query, params: (
                       query, params), 
              'pyformat': lambda query, params: paramstyle_to_paramstyle('format', 'pyformat', query, params)}, 
   'pyformat': {'qmark': lambda query, params: paramstyle_to_paramstyle('pyformat', 'qmark', query, params), 
                'numeric': lambda query, params: paramstyle_to_paramstyle('pyformat', 'numeric', query, params), 
                'named': lambda query, params: paramstyle_to_paramstyle('pyformat', 'named', query, params), 
                'format': lambda query, params: paramstyle_to_paramstyle('pyformat', 'format', query, params), 
                'pyformat': lambda query, params: (
                           query, params)}}

def escaped(string, pos):
    escape_chars = ESCAPE_CHARS
    count = 0
    if pos > 0:
        pos -= 1
        if string[pos] in escape_chars:
            escape_char = string[pos]
            while string[pos] == escape_char and pos >= 0:
                count += 1
                pos -= 1

    if count % 2 == 1:
        return True
    else:
        return False


def quoted(string):
    if string[0] in QUOTE_CHARS and string[(-1)] == string[0]:
        return True
    else:
        return False


class SegmentizeError(Exception):
    """
    Error associated with string segmentization.
    """
    __module__ = __name__


def segmentize(string):
    """
    Split a string into quoted and non-quoted segments.
    """
    quote_chars = QUOTE_CHARS
    segments = []
    current_segment = ''
    previous_char = None
    quote_char = None
    quoted = False
    pos = 0
    for char in string:
        if quoted:
            if char == quote_char and not escaped(string, pos):
                current_segment += char
                segments.append(current_segment)
                current_segment = ''
                previous_char = char
                quoted = False
            else:
                current_segment += char
                previous_char = char
        elif not quoted:
            if char in quote_chars and not escaped(string, pos):
                if current_segment != '':
                    segments.append(current_segment)
                    current_segment = ''
                quoted = True
                quote_char = char
                current_segment += char
                previous_char = char
            else:
                current_segment += char
                previous_char = char
        pos += 1

    if current_segment != '':
        segments.append(current_segment)
    if quoted:
        raise SegmentizeError, 'Unmatched quotes in string'
    return segments


def paramstyle_to_paramstyle(from_paramstyle, to_paramstyle, query, params):
    placeholder_exp = PLACEHOLDER_EXPS[from_paramstyle]
    placeholder_sub = PLACEHOLDER_SUBS[to_paramstyle]
    paramname_gen = PARAMNAME_GENS[from_paramstyle]
    paramvalue_gen = PARAMVALUE_GENS[from_paramstyle]
    new_query = ''
    segments = segmentize(query)
    new_params = PARAM_TYPES[to_paramstyle]()
    param_num = 0
    for segment in segments:
        if quoted(segment):
            new_query += segment
        else:
            pos = 0
            match = placeholder_exp.search(segment, pos)
            if match != None:
                while match != None:
                    new_query += segment[pos:match.start()]
                    placeholder = segment[match.start():match.end()]
                    if escaped(segment, match.start()):
                        new_query += placeholder
                    else:
                        param_num += 1
                        param_name = paramname_gen(param_num, placeholder)
                        param_value = paramvalue_gen(param_num, param_name, params)
                        new_placeholder = placeholder_sub(param_num, param_name)
                        new_query += new_placeholder
                        new_params = param_add(param_num, param_name, param_value, new_params)
                    pos = match.end()
                    match = placeholder_exp.search(segment, pos)

                if pos < len(segment):
                    new_query += segment[pos:]
            else:
                new_query += segment

    return (
     new_query, new_params)


def convert(from_paramstyle, to_paramstyle, query, params):
    try:
        convert_function = CONVERSION_MATRIX[from_paramstyle][to_paramstyle]
    except KeyError:
        raise NotImplementedError, 'Unsupported paramstyle conversion: %s to %s' % (from_paramstyle, to_paramstyle)

    (new_query, new_params) = convert_function(query, params)
    return (
     new_query, new_params)


if __name__ == '__main__':
    sequence_params = [
     'a', 'b', 'c', 'd']
    dict_params = {'foo': 'a', 'bar': 'b', 'baz': 'c', 'quux': 'd'}
    tests = {'qmark': ['SELECT * FROM ? WHERE ? > ? OR ? IS NOT NULL', sequence_params], 'numeric': ['SELECT * FROM :1 WHERE :2 > :3 OR :4 IS NOT NULL', sequence_params], 'named': ['SELECT * FROM :foo WHERE :bar > :baz OR :quux IS NOT NULL', dict_params], 'format': ['SELECT * FROM %s WHERE %s > %s OR %s IS NOT NULL', sequence_params], 'pyformat': ['SELECT * FROM %(foo)s WHERE %(bar)s > %(baz)s OR %(quux)s IS NOT NULL', dict_params]}
    indent = 4
    width = 16
    print ''
    print '[ PARAMSTYLE TRANSLATIONS ]'
    print ''
    for from_paramstyle in PARAMSTYLES['all']:
        query = tests[from_paramstyle][0]
        params = tests[from_paramstyle][1]
        print ''
        print '%s[ %s ]' % (' ' * indent, from_paramstyle.upper())
        print ''
        label = 'query'
        print '%s%s%s: %s' % (' ' * indent, label, '.' * (width + indent - len(label)), query)
        label = 'paramstyle'
        print '%s%s%s: %s' % (' ' * indent, label, '.' * (width + indent - len(label)), from_paramstyle)
        print ''
        for to_paramstyle in PARAMSTYLES['all']:
            (converted_query, converted_params) = convert(from_paramstyle, to_paramstyle, query, params)
            label = '%s_query' % to_paramstyle
            print '%s%s%s: %s' % (' ' * indent * 2, label, '.' * (width - len(label)), converted_query)
            label = '%s_params' % to_paramstyle
            print '%s%s%s: %s' % (' ' * indent * 2, label, '.' * (width - len(label)), converted_params)

        print ''