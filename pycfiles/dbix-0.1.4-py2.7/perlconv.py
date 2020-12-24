# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dbix/perlconv.py
# Compiled at: 2017-10-18 08:52:26
from __future__ import print_function
import os, sys, re
header = '\nfrom dbix import builder\n\n'
footer = ''
re_comment = re.compile('(?P<nl>[\\r\\n])=\\S+(?P<comment>.*?)\\n=cut', re.UNICODE | re.DOTALL)
re_comment_tag = re.compile('^=\\S+', re.UNICODE | re.MULTILINE)
re_use = re.compile('^use.+$', re.UNICODE | re.MULTILINE)
re_our = re.compile('^our\\s+\\$(.+?);$', re.UNICODE | re.MULTILINE)
re_my = re.compile('^my\\s+(.+?)$', re.UNICODE | re.MULTILINE)
re_if = re.compile('^\\s*if\\s+(.+?);', re.UNICODE | re.MULTILINE)
re_qw = re.compile('qw\\s*\\((.+?)\\)', re.UNICODE | re.MULTILINE)
re_package = re.compile('^package\\s+(?P<package_name>.+?);$', re.UNICODE | re.MULTILINE)
re_package_invoke = re.compile('__PACKAGE__\\s*->\\s*', re.UNICODE | re.MULTILINE)
re_one = re.compile('^\\d\\s*;\\s*$', re.UNICODE | re.MULTILINE)
re_member = re.compile('=>', re.UNICODE | re.MULTILINE)
re_funcref = re.compile('\\\\\\&(\\S+)', re.UNICODE | re.MULTILINE)
re_array = re.compile('@(\\S+)', re.UNICODE | re.MULTILINE)
re_hash = re.compile('%(\\S+)', re.UNICODE | re.MULTILINE)
re_dict_only = re.compile('\\b(dict\\()', re.UNICODE)
re_dict_start = re.compile('{', re.UNICODE | re.MULTILINE)
dict_par = 'dict('
add_columns_par = 'add_columns('
re_dict_end = re.compile('}', re.UNICODE | re.MULTILINE)
re_add_columns = re.compile('add_columns\\s*?\\(', re.UNICODE | re.DOTALL)
re_add_columns_only = re.compile('\\b(add_columns\\()', re.UNICODE)
re_fix_kw = re.compile('(?P<func>has_many|belongs_to)\\s*\\(\\s*[\'"]?(?P<variable>\\S+?)[\'"]?\\s*=\\s*[\'"]?(?P<cls>.*?)[\'"]?\\s*,(?P<rem>.*?)\\);', re.UNICODE | re.DOTALL)
re_string_quoted = re.compile('"(?:\\\\.|[^"\\\\])*"', re.UNICODE | re.DOTALL)
re_string_aposed = re.compile("'(?:\\\\.|[^'\\\\])*'", re.UNICODE | re.DOTALL)
re_string_id = re.compile('[a-z_A-Z][a-z_A-Z0-9]*', re.UNICODE | re.DOTALL)
re_string_expr = re.compile('[^=,)]+?', re.UNICODE | re.DOTALL)
saved_words = [
 'class', 'type']
cls = None
__sourcepath__ = None
__load_namespaces__ = 1

def perlconvert(sourcepath, text, with_dict=False, in_tree=0):
    global __sourcepath__
    global cls
    global footer
    __sourcepath__ = sourcepath
    text = re.sub(re_comment, clean_comment, text)
    text = re.sub(re_add_columns, add_columns_par, text)
    text = re.sub(re_package, class_build, text)
    text = re.sub(re_use, '#\\g<0>', text)
    text = re.sub(re_our, '\\g<1>', text)
    text = re.sub(re_package_invoke, '%s.' % cls, text)
    text = re.sub(re_one, '', text)
    text = re.sub(re_funcref, '\\g<1>', text)
    text = re.sub(re_array, '\\g<1>', text)
    text = re.sub(re_hash, '\\g<1>', text)
    text = re.sub(re_member, '=', text)
    if with_dict:
        text = re.sub(re_dict_start, dict_par, text)
        text = re.sub(re_dict_end, ')', text)
        text = dict_parse(text, dict_par, re_dict_only)
        text = dict_parse(text, add_columns_par, re_add_columns_only, add_dict=True)
    text = re.sub(re_my, '\\g<1>', text)
    text = re.sub(re_if, '', text)
    text = re.sub(re_qw, qw_sub, text)
    text = re.sub(re_fix_kw, fix_kw, text)
    return text + '\n' + footer


def qw_sub(matchObj):
    return (', ').join([ '"%s"' % word.replace('"', '"') for word in matchObj.group(1).split() ])


def dict_parse(text, dict_par, spliter, add_dict=False):
    exprs = [
     (
      re_string_quoted, 2),
     (
      re_string_aposed, 2),
     (
      re_string_id, 0),
     (
      re_string_expr, 1)]
    blocks = {'[': (
           ']', [], ''), 
       '(': (
           ')', [], ''), 
       '{': (
           '}', [], ''), 
       dict_par: (
                ')', [dict_par, ')', '=', ','], '=,)')}
    dict_end, dict_skip, dict_popper = blocks[dict_par]
    dict_chunks = re.split(spliter, text)
    text1 = ''
    need_parse = True
    while need_parse:
        need_parse = 0
        dict_style = None
        for c, chunk in enumerate(dict_chunks):
            if chunk == dict_par and c + 1 < len(dict_chunks):
                chunk = dict_chunks[(c + 1)]
                dict_parts = list()
                offset = 0
                kv = list()
                kv_is_id = 0
                block_stack = [dict_par]
                parsed = False
                while offset < len(chunk):
                    if chunk[offset].isspace():
                        offset += 1
                        continue
                    ch = None
                    for d, (expr, is_id) in enumerate(exprs):
                        m = expr.match(chunk, offset)
                        if m is not None:
                            part = m.group(0)
                            offset += len(part)
                            part = part.strip()
                            if part in saved_words:
                                is_id = 1
                            ch = (
                             part, is_id)
                            parsed = ch[0] != dict_par
                            break
                    else:
                        if offset < len(chunk):
                            ch = (
                             chunk[offset], 1)
                            offset += 1
                        if ch[0] in blocks:
                            block_stack.append(ch[0])
                        blocks_top = block_stack[(-1)]
                        block_end, block_skip, block_popper = blocks[blocks_top]
                        if ch[0] not in block_skip:
                            kv.append(ch)
                        if kv and ch[0] in block_popper:
                            kv1 = list(kv[0])
                            for ch1 in kv[1:]:
                                kv1[0] += ch1[0]
                                if kv1[1] != ch1[1]:
                                    kv1[1] = 1

                            dict_parts.append(kv1)
                            kv = list()
                        if ch[0] == block_end:
                            block_stack.pop()
                        if not block_stack:
                            parsed = True
                            break

                if parsed:
                    try:
                        _dict = dict_render(dict_parts, dict_par, style=dict_style, add_dict=add_dict)
                        text1 += _dict + chunk[offset:]
                    except:
                        parsed = False

                if not parsed:
                    text1 += dict_par + chunk
                    need_parse += 1
                    dict_style = True
            elif c == 0:
                text1 += chunk

        if need_parse:
            dict_chunks = re.split(spliter, text1)
            text1 = ''

    return text1


def dict_render(dict_parts, dict_par, style=None, add_dict=False):
    _dict = [ (dict_parts[(c * 2)], dict_parts[(c * 2 + 1)]) for c, part in enumerate(dict_parts[::2])
            ]
    default_style = sum([ part[0][1] for part in _dict ])
    style = default_style if style is None else style

    def part_render(part):
        sep = ':' if style else '='
        formater = '%s%s%s'
        key = part[0][0]
        if style and part[0][1] < 2:
            formater = '"%s"%s%s'
            key = key.replace('"', '\\"')
        return formater % (key, sep, part[1][0])

    content = (',').join([ part_render(part) for part in _dict ])
    if style:
        if add_dict:
            return '%s\n**{\n%s\n}\n)' % (dict_par, content)
        else:
            return '{\n%s\n}' % content

    else:
        return '%s\n%s\n)' % (dict_par, content)
    return


def clean_comment(matchObj):
    text = matchObj.group('comment')
    text = re.sub(re_comment_tag, '', text)
    text = re.sub(re_dict_only, dict_par.upper(), text)
    return '"""%s"""' % text


def class_build(matchObj):
    global __load_namespaces__
    global cls
    text = matchObj.group('package_name')
    cls = text.split('::')[(-1)].strip()
    text = "class %s(builder.BuilderMixin):\n\t__name__ = '%s'\n\t__sourcepath__ = '%s'\n\t__load_namespaces__ = %d\n\tschema = schema\n\t" % (cls, cls, __sourcepath__, __load_namespaces__)
    return text


def fix_kw(matchObj):
    rep = dict(matchObj.groupdict())
    rep['cls'] = rep['cls'].split('::')[(-1)].strip()
    text = '%(func)s(\n\'%(variable)s\', "%(cls)s",%(rem)s)' % rep
    return text


def treeconv(path, exceptpath=None, with_dict=True):
    global __load_namespaces__
    all_text = list()
    __load_namespaces__ = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            fullpath = os.path.join(root, file)
            if fullpath.endswith('.pm'):
                text = open(fullpath, 'r').read()
                if exceptpath and fullpath in exceptpath:
                    continue
                text = perlconvert(fullpath, text, with_dict=with_dict)
                all_text.append(text)

    return header + ('\n\n').join(all_text)


def oneconv(sourcepath, with_dict=True):
    text = open(sourcepath, 'r').read()
    text = perlconvert(sourcepath, text, with_dict=with_dict)
    return header + text


def stdioconv(sourcepath, with_dict=True):
    text = sys.stdin.read()
    text = perlconvert(sourcepath, text, with_dict=with_dict)
    sys.stdout.write(header + text)


def schemaconv(sourcepath, schema, with_dict=True):
    if os.path.isdir(sourcepath):
        setup_pm = os.path.join(sourcepath, 'Setup.pm')
        if os.path.exists(setup_pm):
            text = oneconv(setup_pm, with_dict=with_dict)
        else:
            text = treeconv(sourcepath, exceptpath=None, with_dict=with_dict)
    else:
        text = oneconv(sourcepath, with_dict=with_dict)
    exec text in dict(schema=schema)
    return