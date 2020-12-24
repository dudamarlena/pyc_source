# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\i18n\pygettext\catalog.py
# Compiled at: 2011-03-26 09:19:59
import sys, os, codecs, pygettext
MESSAGES = []

def detect_unicode_encoding(bytes):
    encodings_map = [
     (
      3, codecs.BOM_UTF8, 'UTF-8'), (4, codecs.BOM_UTF32_LE, 'UTF-32LE'), (4, codecs.BOM_UTF32_BE, 'UTF-32BE'), (2, codecs.BOM_UTF16_LE, 'UTF-16LE'), (2, codecs.BOM_UTF16_BE, 'UTF-16BE')]
    for (offset, bom, name) in encodings_map:
        if bytes[:offset] == bom:
            return (
             name, offset)

    return ('UTF-8', 0)


class ParseError(ValueError):
    """Signals an error reading .po file."""
    __module__ = __name__


def merge(master_file, language_files):
    parsed_master_file = parse(master_file)
    for path in language_files:
        merging(parsed_master_file, path)


def merging(parsed_master_file, path):
    lang_file = parse(path)
    id_map = {}
    new_lang = []
    for msg in lang_file:
        message = msg['message']
        if message:
            id_map[msg['id']] = message

    for msg in parsed_master_file:
        msg['message'] = id_map.get(msg['id'])
        new_lang.append(msg)

    save(path, new_lang)


def items(path, sort_by, dir):
    po = parse(path)
    po = po[1:]
    if sort_by:
        return sort(po, sort_by, dir)
    return po


def sort(po, sort_by, dir):
    group = dict()
    sorted = list()
    col_map = dict(id='id', string='message', context='path')
    for message in po:
        group.setdefault(message[col_map[sort_by]], []).append(message)

    kg = group.keys()
    kg.sort()
    if dir == 'up':
        kg.reverse()
    for k in kg:
        sorted.extend(group[k])

    return sorted


def save(path, message_list):
    txt = []
    m = message_list[0]['message']
    txt.append(m)
    txt.append('\n\n')
    for p in message_list[1:]:
        message = p['message'] or ''
        context = p['context']
        id = p['id']
        txt.append('#: %s' % context)
        txt.append('msgid %s\n' % normalize(id))
        txt.append('msgstr %s\n\n' % normalize(message))

    txt = ('').join(txt)
    backup_name = path.replace('.po', '.back')
    try:
        os.remove(backup_name)
    except os.error:
        pass

    os.rename(path, backup_name)
    codecs.open(path, 'wb', 'utf-8').write(txt)


def update(path, msg_id, msg_text):
    message_list = parse(path)
    for p in message_list[1:]:
        if p['id'].strip() == msg_id.strip():
            p['message'] = msg_text

    save(path, message_list)


def quote(msg):
    return pygettext.escape_unicode(msg)


def normalize(s):
    lines = s.split('\n')
    if len(lines) == 1:
        s = '"' + quote(s) + '"'
    else:
        if not lines[(-1)]:
            del lines[-1]
            lines[-1] = lines[(-1)] + '\n'
        for i in range(len(lines)):
            lines[i] = quote(lines[i])

        lineterm = '\\n"\n"'
        s = '""\n"' + lineterm.join(lines) + '"'
    return s


def add(id, str, context, fuzzy, MESSAGES):
    """Add a non-fuzzy translation to the dictionary."""
    if fuzzy:
        return
    c = context.split(':')
    path = c[0]
    file = os.path.basename(path)
    line = c[(-1)].replace('\n', '')
    MESSAGES.append(dict(id=id, message=str, path=path, context=context, file=file, line=line))


def parse(infile):
    MESSAGES = list()
    ID = 1
    STR = 2
    header = list()
    fd = open(infile, 'rt')
    (encoding, offset) = detect_unicode_encoding(fd.read(4))
    fd.seek(offset)
    lines = [ line.decode(encoding) for line in fd.readlines() ]
    section = None
    fuzzy = 0
    lno = 0
    context = ''
    prev_context = ''
    heading = True
    for l in lines:
        if not l:
            continue
        lno += 1
        if heading:
            if l.startswith('#: '):
                heading = False
            if l.startswith('msgid "') and header and 'Generated-By:' in header[(-1)]:
                heading = False
            if l.strip() and heading:
                header.append(l)
        if l[0] == '#' and section == STR:
            add(msgid, msgstr, prev_context, fuzzy, MESSAGES)
            section = None
            fuzzy = 0
        if l[:2] == '#,' and l.find('fuzzy'):
            fuzzy = 1
        if l.startswith('#: '):
            context = l[len('#: '):]
        if l[0] == '#':
            continue
        if l.startswith('msgid'):
            if section == STR:
                add(msgid, msgstr, prev_context, fuzzy, MESSAGES)
            section = ID
            prev_context = context
            l = l[5:]
            msgid = msgstr = ''
        elif l.startswith('msgstr'):
            section = STR
            l = l[6:]
        l = l.strip()
        if not l:
            continue
        try:
            l = eval(l)
        except Exception, e:
            print >> sys.stderr, 'Escape error on %s: %d' % (infile, lno), 'before:', repr(l)
            raise ParseError(e)

        try:
            l = l.decode('utf8')
        except UnicodeDecodeError:
            print >> sys.stderr, 'Encoding error on %s: %d' % (infile, lno), 'before:', repr(l)
            raise ParseError(e)

        if section == ID:
            msgid += l
        elif section == STR:
            msgstr += l
        else:
            print >> sys.stderr, 'Syntax error on %s:%d' % (infile, lno), 'before:'
            print >> sys.stderr, l
            raise ParseError(e)

    if section == STR:
        add(msgid, msgstr, prev_context, fuzzy, MESSAGES)
    MESSAGES[0]['message'] = ('').join(header)
    return MESSAGES