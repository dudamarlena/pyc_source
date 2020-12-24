# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/strainer/xhtmlify.py
# Compiled at: 2011-03-21 01:30:30
"""An HTML to XHTML converter."""
import re, htmlentitydefs, codecs, encodings.aliases
__all__ = [
 'xhtmlify', 'xmldecl', 'fix_xmldecl', 'sniff_encoding', 'ValidationError']
DEBUG = False
NAME_RE = '(?:[A-Za-z_][A-Za-z0-9_.-]*(?::[A-Za-z_][A-Za-z0-9_.-]*)?)'
BAD_ATTR_RE = '[^> \\t\\r\\n]+'
ATTR_RE = '%s[ \\t\\r\\n]*(?:=[ \\t\\r\\n]*(?:"[^"]*"|\'[^\']*\'|%s))?[ \\t\\r\\n]*' % (NAME_RE, BAD_ATTR_RE)
CDATA_RE = '<!\\[CDATA\\[.*?\\]\\]>'
COMMENT_RE = '<!--.*?-->'
TAG_RE = '%s|%s|<((?:[^<>\'"]+|\'[^\']*\'|"[^"]*"|\'|")*)>|<' % (COMMENT_RE, CDATA_RE)
INNARDS_RE = '(%s(?:[ \\t\\r\\n]+%s)*[ \\t\\r\\n]*(/?)\\Z)|(/%s[ \\t\\r\\n]*\\Z)|(.*)' % (
 NAME_RE, ATTR_RE, NAME_RE)
SELF_CLOSING_TAGS = [
 'base', 'meta', 'link', 'hr', 'br', 'param', 'img', 'area',
 'input', 'col', 'isindex', 'basefont', 'frame']
CDATA_TAGS = [
 'script', 'style']
STRUCTURAL_TAGS = [
 'address', 'blockquote', 'dir', 'dl', 'fieldset', 'form',
 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'isindex', 'menu',
 'ol', 'p', 'pre', 'table', 'ul',
 'section', 'article', 'aside', 'header', 'footer', 'nav']

class StrainerError(Exception):
    pass


class ValidationError(StrainerError):

    def __init__(self, message, pos, line, offset, tags):
        message += ' at line %d, column %d (char %d)' % (line, offset, pos + 1)
        if DEBUG:
            message += '\n%r' % tags
        super(ValidationError, self).__init__(message)
        self.pos = pos
        self.line = line
        self.offset = offset


class XMLParsingError(StrainerError):
    pass


def ampfix(value):
    """Replaces ampersands in value that aren't part of an HTML entity.
    Adapted from <http://effbot.org/zone/re-sub.htm#unescape-html>.
    Also converts all entities to numeric form and replaces every
    "<" or ">" outside of any CDATA sections with "&lt;" or "&gt;"."""

    def fixup(m):
        text = m.group(0)
        if text == '&':
            pass
        elif text[:2] == '&#':
            try:
                if text[:3] in ('&#x', '&#X'):
                    c = unichr(int(text[3:-1], 16))
                else:
                    c = unichr(int(text[2:-1], 10))
            except ValueError:
                pass
            else:
                c = ord(c)
                if c in (9, 10, 13) or 32 <= c <= 55295 or 57344 <= c <= 65533 or 65536 <= c <= 1114111:
                    return text.lower()
        else:
            name = text[1:-1]
            if name in ('amp', 'lt', 'gt', 'quot', 'apos'):
                return text
            cp = htmlentitydefs.name2codepoint.get(name)
            if cp:
                return '&#x%x;' % cp
        return '&amp;' + text[1:]

    def fix2(m):
        g = m.group()
        if g.startswith('<!'):
            return g
        else:
            if g == '<':
                return '&lt;'
            if g == '>':
                return '&gt;'
            return re.sub('&#?\\w+;|&', fixup, g)

    R = re.compile('(<!\\[CDATA\\[.*?\\]\\]>)|<!--.*?-->|<|>|[^<>]+', re.DOTALL)
    return R.sub(fix2, value)


def fix_attrs(tagname, attrs, ERROR=None):
    """Returns an XHTML-clean version of attrs, the attributes part
       of an (X)HTML tag. Tries to make as few changes as possible,
       but does convert all attribute names to lowercase."""
    if not attrs and tagname != 'html':
        return ''
    lastpos = 0
    result = []
    output = result.append
    seen = {}
    name_re = re.compile('(%s)' % NAME_RE + '([ \\t\\r\\n]*)\\Z')
    space_before = ' '
    for m in re.compile(ATTR_RE, re.DOTALL).finditer(attrs):
        assert re.match('[ \\t\\r\\n]*\\Z', attrs[lastpos:m.start()])
        output(attrs[lastpos:m.start()] or space_before)
        lastpos = m.end()
        attr = m.group()
        if attr[-1:] in ' \t\r\n':
            space_before = ''
        else:
            space_before = ' '
        if '=' not in attr:
            assert name_re.match(attr), repr(attr)
            output(re.sub('\\A(%s)' % NAME_RE, '\\1="\\1"', attr).lower())
        else:
            (name, value) = attr.split('=', 1)
            m2 = name_re.match(name)
            if m2:
                (name, postname) = m2.groups()
            else:
                ERROR('Invalid attribute name', m.start())
            name = name.lower()
            preval = re.match('[ \\t\\r\\n]*', value).group()
            value = value[len(preval):]
            value_end = re.search('[ \\t\\r\\n]*\\Z', value).start()
            value, postval = value[:value_end], value[value_end:]
            if name in seen:
                ERROR('Repeated attribute "%s"' % name, m.start())
            else:
                seen[name] = 1
            if len(value) > 1 and value[0] + value[(-1)] in ("''", '""'):
                if value[0] not in value[1:-1]:
                    value = ampfix(value)
                    output('%s%s=%s%s%s' % (name, postname, preval, value, postval))
                    continue
                value = value[1:-1]
            value = ampfix(value.replace('"', '&quot;'))
            output('%s%s=%s"%s"%s' % (name, postname, preval, value, postval))

    after = attrs[lastpos:]
    if re.match('[ \\t\\r\\n]*/?', after).end() == len(after):
        output(after)
    else:
        ERROR('Malformed tag contents', lastpos)
    if tagname == 'html' and 'xmlns' not in seen:
        output(space_before + 'xmlns="http://www.w3.org/1999/xhtml"')
    return ('').join(result)


def cdatafix(value):
    """Alters value, the body of a <script> or <style> tag, so that
       it will be parsed equivalently by the underlying language parser
       whether it is treated as containing CDATA (by an XHTML parser)
       or #PCDATA (by an HTML parser).
    """
    cdata_re = re.compile('(%s)' % CDATA_RE, re.DOTALL)
    result = []
    output = result.append
    outside_lexer = re.compile('((/\\*|"|\')|(<!\\[CDATA\\[)|(\\]\\]>)|\\]|(<)|(>)|(&))|/|[^/"\'<>&\\]]+')
    comment_lexer = re.compile('((\\*/)|(<!\\[CDATA\\[)|(\\]\\]>)|\\]|(<)|(>)|(&))|\\*|[^\\*<>&\\]]+')
    dqstring_lexer = re.compile('\\\\[^<>]|((")|(<!\\[CDATA\\[)|(\\]\\]>)|\\]|(\\\\<|<)|(\\\\>|>)|(\\\\&|&))|[^\\\\"<>&\\]]+', re.DOTALL)
    sqstring_lexer = re.compile("\\\\[^<>]|((')|(<!\\[CDATA\\[)|(\\]\\]>)|\\]|(\\\\<|<)|(\\\\>|>)|(\\\\&|&))|[^\\\\'<>&\\]]+", re.DOTALL)
    (Outside, Comment, DQString, SQString) = ([], [], [], [])
    Outside += (outside_lexer.match,
     '/*<![CDATA[*/ < /*]]>*/',
     '/*<![CDATA[*/ > /*]]>*/',
     '/*<![CDATA[*/ & /*]]>*/', {'/*': Comment, '"': DQString, "'": SQString})
    Comment += (comment_lexer.match,
     '<![CDATA[<]]>',
     '<![CDATA[>]]>',
     '<![CDATA[&]]>', {'*/': Outside})
    DQString += (dqstring_lexer.match,
     '\\x3c',
     '\\x3e',
     '\\x26', {'"': Outside})
    SQString += (sqstring_lexer.match,
     '\\x3c',
     '\\x3e',
     '\\x26', {"'": Outside})
    (lexer, lt_rep, gt_rep, amp_rep, next_state) = Outside
    pos = 0
    in_cdata = False
    while pos < len(value):
        m = lexer(value, pos)
        assert m.start() == pos
        pos = m.end()
        (interesting, state_changer, cdata_start, cdata_end, lt, gt, amp) = m.groups()
        if interesting:
            if cdata_start:
                output(m.group())
                in_cdata = True
            elif cdata_end:
                if in_cdata:
                    output(m.group())
                else:
                    output(']]')
                    pos = m.start() + 2
                in_cdata = False
            elif lt:
                output(in_cdata and m.group() or lt_rep)
            elif gt:
                output(in_cdata and m.group() or gt_rep)
            elif amp:
                output(in_cdata and m.group() or amp_rep)
            elif m.group() == ']':
                output(']')
            else:
                output(in_cdata and m.group() or state_changer)
                (lexer, lt_rep, gt_rep, amp_rep, next_state) = next_state[state_changer]
        else:
            output(m.group())

    assert not in_cdata
    return ('').join(result)


def xmldecl(version='1.0', encoding=None, standalone=None):
    """Returns a valid <?xml ...?> declaration suitable for using
       at the start of a document. Note that no other characters are
       allowed before the declaration (other than byte-order markers).
       Only set standalone if you really know what you're doing.
       Raises a ValidationError if given invalid values."""
    if not re.match('1\\.[0-9]+\\Z', version):
        raise ValidationError('Bad version in XML declaration', 0, 1, 1, [])
    encodingdecl = ''
    if encoding is not None:
        EncName_re = re.compile('[A-Za-z][A-Za-z0-9._-]*\\Z')
        if isinstance(encoding, basestring) and EncName_re.match(encoding):
            encodingdecl = ' encoding="%s"' % encoding
        else:
            raise ValidationError('Bad encoding name in XML declaration', 0, 1, 1, [])
    sddecl = ''
    if standalone is not None:
        if standalone is True or standalone == 'yes':
            sddecl = ' standalone="yes"'
        elif standalone is False or standalone == 'no':
            sddecl = ' standalone="no"'
        else:
            raise ValidationError('Bad standalone value in XML declaration', 0, 1, 1, [])
    return '<?xml version="%s"%s%s ?>' % (version, encodingdecl, sddecl)


def fix_xmldecl(xml, encoding=None, add_encoding=False, default_version='1.0'):
    """Looks for an XML declaration near the start of xml, cleans it up,
       and returns the adjusted version of xml. Doesn't add a declaration
       if none was found."""
    EOS = '\\Z'
    starts_utf16_re = re.compile('utf[_-]?16', re.IGNORECASE)
    bomless_utf16_re = re.compile('utf[_-]?16[_-]?[bl]e\\Z', re.IGNORECASE)
    unicode_input = isinstance(xml, unicode)
    if not re.match('1\\.[0-9]+' + EOS, default_version):
        raise ValueError('Bad default XML declaration version')
    if encoding is not None:
        encoding = encodings.normalize_encoding(encoding)
        if encoding.lower() in encodings.aliases.aliases:
            encoding = encodings.aliases.aliases[encoding.lower()]
        if not re.match('[A-Za-z][A-Za-z0-9._-]*' + EOS, encoding):
            raise ValueError('Bad default XML declaration encoding')
        if starts_utf16_re.match(encoding):
            if not unicode_input and not (xml.startswith(codecs.BOM_UTF16_LE) or xml.startswith(codecs.BOM_UTF16_BE)):
                xml = ('\ufeff').encode(encoding) + xml
            elif unicode_input and bomless_utf16_re.match(encoding):
                xml = '\ufeff' + xml
    if unicode_input:
        if encoding:
            xmlstr = xml.encode(encoding)
        else:
            xmlstr = xml.encode('UTF-8')
    else:
        xmlstr = xml
    if encoding:
        enc = encoding
    else:
        enc = sniff_bom_encoding(xmlstr)
    if unicode_input:
        xml = xmlstr
    encode = codecs.lookup(enc).incrementalencoder().encode
    if bomless_utf16_re.match(enc):
        prefix = encode('\ufeff')
    else:
        prefix = encode('')
    chars_we_need = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-_ \t\r\n<?\'"[]:()+*>'
    assert encode(chars_we_need * 3) == encode(chars_we_need) * 3, enc
    L = lambda s: re.escape(encode(s))
    group = lambda s: '(%s)' % s
    optional = lambda s: '(?:%s)?' % s
    oneof = lambda opts: '(?:%s)' % ('|').join(opts)
    charset = lambda s: oneof([ L(c) for c in s ])
    all_until = lambda s: '(?:(?!%s).)*' % s
    caseless = lambda s: oneof([ L(c.lower()) for c in s ] + [ L(c.upper()) for c in s ])
    upper = charset('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    lower = charset('abcdefghijklmnopqrstuvwxyz')
    digits = charset('0123456789')
    punc = charset('._-')
    Name = '(?:%s%s*)' % (oneof([upper, lower]),
     oneof([upper, lower, digits, punc]))
    Ss = charset(' \t\r\n\x0c') + '*'
    Sp = charset(' \t\r\n\x0c') + '+'
    VERSION = encode('version')
    ENCODING = encode('encoding')
    STANDALONE = encode('standalone')
    StartDecl = ('').join([prefix, Ss, L('<'), Ss, L('?'), Ss,
     oneof([L('xml'), L('xmL'), L('xMl'), L('xML'),
      L('Xml'), L('XmL'), L('XMl'), L('XML')])])
    Attr = ('').join([group(Sp), group(Name), group(('').join([Ss, L('='), Ss])),
     oneof([
      group(L('"') + all_until(oneof([L('"'), L('<'), L('>')])) + L('"')),
      group(L("'") + all_until(oneof([L("'"), L('<'), L('>')])) + L("'")),
      group(all_until(oneof([Sp, L('?'), L('<'), L('>')])))])])
    Attr_re = re.compile(Attr, re.DOTALL)
    EndDecl = ('').join([group(Ss), oneof([('').join([L('?'), Ss, L('>')]), L('>')])])
    m = re.match(StartDecl, xml)
    if m:
        pos = m.end()
        attrs = {}
        while 1:
            m2 = Attr_re.match(xml, pos)
            if m2:
                (wspace, name, eq, dquoted, squoted, unquoted) = m2.groups()
                wspace = wspace.replace(encode('\x0c'), encode(' '))
                if dquoted is not None:
                    quotes = encode('"')
                    n = len(quotes)
                    value = dquoted[n:-n]
                elif squoted is not None:
                    quotes = encode("'")
                    n = len(quotes)
                    value = squoted[n:-n]
                else:
                    quotes = encode("'")
                    value = unquoted
                if name in attrs:
                    pass
                elif name == VERSION:
                    m3 = re.match(Ss + group(L('1.') + digits) + Ss + EOS, value)
                    if m3:
                        attrs[name] = wspace + name + eq + quotes + m3.group(1) + quotes
                elif name == ENCODING:
                    m3 = re.match(Ss + group(Name) + Ss + EOS, value)
                    if m3:
                        attrs[name] = wspace + name + eq + quotes + m3.group(1) + quotes
                elif name == STANDALONE:
                    m3 = re.match(Ss + oneof([group(oneof([L('yes'), L('yeS'), L('yEs'), L('yES'), L('Yes'), L('YeS'), L('YEs'), L('YES')])), group(oneof([L('no'), L('nO'), L('No'), L('NO')]))]) + Ss + EOS, value)
                    if m3:
                        (yes, no) = m3.groups()
                        if yes:
                            attrs[name] = wspace + name + eq + quotes + encode('yes') + quotes
                        else:
                            attrs[name] = wspace + name + eq + quotes + encode('no') + quotes
                pos = m2.end()
            else:
                break

        if add_encoding and ENCODING not in attrs:
            attrs[ENCODING] = encode(" encoding='%s'" % enc)
        m4 = re.compile(EndDecl).match(xml, pos)
        if m4:
            return prefix + encode('<?xml') + attrs.get(VERSION, encode(" version='%s'" % default_version)) + (attrs.get(ENCODING) if ENCODING in attrs else '') + (attrs.get(STANDALONE) if STANDALONE in attrs else '') + m4.group(1).replace(encode('\x0c'), encode(' ')) + encode('?>') + xml[m4.end():]
        m5 = re.compile(oneof([L('>'), L('<')])).search(xml, pos)
        if m5:
            if m5.group() == encode('>'):
                endpos = m5.end()
            else:
                endpos = m5.start()
            return xml[:m.start()] + xml[endpos:]
        return ''
    if unicode_input:
        xml = xml.decode(enc, 'strict')
    return xml


def fix_doctype(html):
    """    Searches for a doctype declaration at the start of html, after any
    XML declaration and white-space, and makes sure its syntax matches
    the "doctypedecl" rule in the XML spec, with a few minor exceptions
    (we disallow '<' and '>' in PUBLIC identifiers, allow any
    combination of plausible characters for ELEMENT grammar rules,
    and disallow nested comments and processing instructions).
    Returns (fixed_doctype, index) where fixed_doctype is a fixed
    version of everything up to the end of the doctype and index is the
    position within html of the end of the doctype (so html[index:]
    can be processed including positions relative to the original input).
    """
    S = '[ \t\r\n]+'
    Ss = '[ \t\r\n]*'
    opt = lambda *args: '(?:%s)?' % ('|').join(args)
    oneof = lambda *args: '(?:%s)' % ('|').join(args)
    any = lambda *args: '(?:%s)*' % ('|').join(args)
    some = lambda *args: '(?:%s)+' % ('|').join(args)
    named = lambda name, regexp: '(?P<%s>%s)' % (name, regexp)
    NameStartChar = '[:A-Z_a-zÀ-ÖØ-öø-˿Ͱ-ͽͿ-\u1fff\u200c-\u200d⁰-\u218fⰀ-\u2fef、-\ud7ff豈-\ufdcfﷰ-�]'
    if len('𐀀') == 1:
        NameStartChar = NameStartChar[:-1] + '𐀀-\U000effff]'
    NameChar = NameStartChar[:-1] + '0-9·̀-ͯ‿-⁀\\-]'
    Name = NameStartChar + any(NameChar)
    Nmtoken = some(NameChar)
    quoted = oneof('"[^<>"]*"', "'[^<>']*'")
    SystemLiteral = quoted
    PubidLiteral = oneof('"[-\\ \r\na-zA-Z0-9()+,./:=?;!*#@$_%\']*"', "'[-\\ \r\na-zA-Z0-9()+,./:=?;!*#@$_%]*'")
    ExternalID = oneof('SYSTEM' + S + SystemLiteral, 'PUBLIC' + S + quoted + S + SystemLiteral)
    Mixed = oneof('\\(' + Ss + '#PCDATA' + any(Ss + '\\|' + Ss + Name) + Ss + '\\)\\*', '\\(' + Ss + '#PCDATA' + Ss + '\\)')
    children = some(Name, '[?*+|,()]', S)
    contentspec = oneof('EMPTY', 'ANY', Mixed, children)
    elementdecl = '<!' + Ss + 'ELEMENT' + S + Name + S + contentspec + Ss + '>'
    NotationType = 'NOTATION' + S + '\\(' + Ss + Name + any(Ss + '\\|' + Ss + Name) + Ss + '\\)'
    Enumeration = '\\(' + Ss + Nmtoken + any(Ss + '\\|' + Ss + Nmtoken) + Ss + '\\)'
    AttType = oneof('CDATA', 'ID', 'IDREF', 'IDREFS', 'ENTITY', 'ENTITIES', 'NMTOKEN', 'NMTOKENS', NotationType, Enumeration)
    CharRef = oneof('&#[0-9]+;', '&#x[0-9a-fA-F]+;')
    EntityRef = '&' + Name + ';'
    PEReference = '%' + Name + ';'
    Reference = oneof(EntityRef, CharRef)
    EntityValue = oneof('"' + any('[^%&"]', PEReference, Reference) + '"', "'" + any("[^%&']", PEReference, Reference) + "'")
    AttValue = oneof('"' + any('[^<&"]', Reference) + '"', "'" + any("[^<&']", Reference) + "'")
    DefaultDecl = oneof('#REQUIRED', '#IMPLIED', opt('#FIXED' + S) + AttValue)
    AttDef = S + Name + S + AttType + S + DefaultDecl
    AttlistDecl = '<!' + Ss + 'ATTLIST' + S + Name + any(AttDef) + Ss + '>'
    NDataDecl = S + 'NDATA' + S + Name
    EntityDef = oneof(EntityValue, ExternalID + opt(NDataDecl))
    PEDef = oneof(EntityValue, ExternalID)
    GEDecl = '<!' + Ss + 'ENTITY' + S + Name + S + EntityDef + Ss + '>'
    PEDecl = '<!' + Ss + 'ENTITY' + S + '%' + S + Name + S + PEDef + Ss + '>'
    EntityDecl = oneof(GEDecl, PEDecl)
    PublicID = 'PUBLIC' + S + quoted
    NotationDecl = '<!' + Ss + 'NOTATION' + S + Name + S + oneof(ExternalID, PublicID) + Ss + '>'
    markupdecl = oneof(elementdecl, AttlistDecl, EntityDecl, NotationDecl)
    intSubset = any(markupdecl, PEReference, S)
    doctypedecl = named('doctype', '<!' + Ss + 'DOCTYPE' + S + Name) + named('body', named('extid', opt(S + ExternalID) + Ss) + named('subset', opt('\\[' + intSubset + '\\]' + Ss)) + '>')
    doctypedecl = re.compile(doctypedecl + '\\Z', flags=re.IGNORECASE)

    def ERROR(message, charpos=None):
        if charpos is None:
            charpos = pos
        line = html.count('\n', 0, charpos) + 1
        offset = charpos - html.rfind('\n', 0, charpos)
        raise ValidationError(message, charpos, line, offset, [])
        return

    m = re.compile('<!' + Ss + 'DOCTYPE' + S + '[^<>]*' + any('<![^<>]*>[^<>]*') + '>', re.IGNORECASE).search(html)
    if not m:
        return ('', 0)
    else:
        m2 = doctypedecl.match(html, m.start(), m.end())
        if not m2:
            raise ERROR('Invalid doctype', m.start())
        m = m2
        r = re.compile(S + 'PUBLIC' + S + '(%s)' % quoted, flags=re.IGNORECASE)
        for pubid in r.finditer(html, m.start(), m.end()):
            if not re.match(PubidLiteral + '\\Z', pubid.group(1)):
                raise ERROR('Bad characters in PUBLIC "..." identifier', pubid.start(1))

        def fix(m):
            g = m.group()
            if g[0] in '"\'':
                return g
            else:
                if g.startswith('<!'):
                    return '<!'
                return g.upper()

        (before, doctype, body, after) = (html[:m.start()], m.group('doctype'), m.group('body'), html[m.end():])
        doctype = re.sub('<!\\s*(\\S+)', lambda m: '<!' + m.group(1).upper(), doctype)
        body = re.sub(oneof('"[^"]*"', "'[^']*'", oneof('#', '!' + Ss) + '[a-zA-Z]+'), fix, body)
        return (before + doctype + body, m.end())


def xhtmlify(html, encoding=None, self_closing_tags=SELF_CLOSING_TAGS, cdata_tags=CDATA_TAGS, structural_tags=STRUCTURAL_TAGS):
    """
    Parses HTML and converts it to XHTML-style tags.
    Raises a ValidationError if the tags are badly nested or malformed.
    It is slightly stricter than normal HTML in some places and more lenient
    in others, but it generally tries to behave in a human-friendly way.
    It is intended to be idempotent, i.e. it should make no changes if fed
    its own output. It accepts XHTML-style self-closing tags.
    """
    html = fix_xmldecl(html, encoding=encoding, add_encoding=False)
    if not encoding:
        encoding = sniff_encoding(html)
    unicode_input = isinstance(html, unicode)
    if unicode_input:
        html = html.encode(encoding, 'strict')
    if not isinstance(html, str):
        raise TypeError('Expected string, got %s' % type(html))
    html = html.decode(encoding, 'replace')
    html = html.replace('\x0c', ' ')
    if len('𐀀') == 1:
        html = re.sub('[^\t\n\r -\ud7ff\ue000-�𐀀-\U0010ffff]', '�', html)
    else:
        html = re.sub('[^\t\n\r -\ud7ff\ue000-�]', '�', html)

    def ERROR(message, charpos=None):
        if charpos is None:
            charpos = pos
        line = html.count('\n', 0, charpos) + 1
        offset = charpos - html.rfind('\n', 0, charpos)
        raise ValidationError(message, charpos, line, offset, tags)
        return

    for tag in cdata_tags:
        assert tag not in self_closing_tags

    assert 'div' not in structural_tags
    assert 'span' not in structural_tags
    tags = []
    result = []
    output = result.append
    (doctype, lastpos) = fix_doctype(html)
    output(doctype)
    if html.startswith('<?xml') or html.startswith('\ufeff<?xml'):
        pos = html.find('>') + 1
        if not doctype:
            output(html[:pos])
            lastpos = pos
    tag_re = re.compile(TAG_RE, re.DOTALL | re.IGNORECASE)
    for tag_match in tag_re.finditer(html, lastpos):
        pos = tag_match.start()
        prevtag = tags and tags[(-1)][0].lower() or None
        innards = tag_match.group(1)
        if innards is None:
            whole_tag = tag_match.group()
            if whole_tag.startswith('<!'):
                if re.match('(?i)<!doctype[ \\t\\r\\n]', whole_tag):
                    text = html[lastpos:pos]
                    if re.match('[ \\t\\r\\n]*\\Z', text):
                        output(text)
                    output('<!DOCTYPE')
                    lastpos = tag_match.start() + len('<!doctype')
                continue
            assert whole_tag == '<'
            if prevtag in cdata_tags:
                continue
            else:
                ERROR('Unescaped "<" or unfinished tag')
        elif not innards:
            ERROR('Empty tag')
        text = html[lastpos:pos]
        if prevtag in cdata_tags:
            m = re.match('/(%s)[ \\t\\r\\n]*\\Z' % NAME_RE, innards)
            if not m or m.group(1).lower() != prevtag:
                continue
            output(cdatafix(text))
        else:
            output(ampfix(text))
        m = re.compile(INNARDS_RE, re.DOTALL).match(innards)
        if m.group(1):
            endslash = m.group(2)
            m = re.match(NAME_RE, innards)
            TagName, attrs = m.group(), innards[m.end():]
            tagname = TagName.lower()
            attrs = fix_attrs(tagname, attrs, ERROR=lambda msg, relpos: ERROR(msg, tag_match.start(1) + m.end() + relpos))
            if prevtag in self_closing_tags:
                tags.pop()
                prevtag = tags and tags[(-1)][0].lower() or None
            prohibitors_of = {'a': [
                   'a'], 
               'img': [
                     'pre'], 
               'object': ['pre'], 'big': ['pre'], 'small': [
                       'pre'], 
               'sub': ['pre'], 'sup': ['pre'], 'input': [
                       'button'], 
               'select': ['button'], 'textarea': [
                          'button'], 
               'button': [
                        'button'], 
               'form': ['button', 'form'], 'fieldset': [
                          'button'], 
               'iframe': ['button'], 'isindex': [
                         'button'], 
               'label': [
                       'button', 'label']}
            bad_parents = prohibitors_of.get(tagname, [])
            for (ancestor, _) in tags:
                if ancestor in bad_parents:
                    if tagname == ancestor:
                        other_text = 'other '
                    else:
                        other_text = ''
                    ERROR('XHTML <%s> elements must not contain %s<%s> elements' % (
                     ancestor, other_text, tagname))

            if tagname == prevtag and tagname not in ('div', 'span', 'fieldset', 'q',
                                                      'blockquote', 'ins', 'del',
                                                      'bdo', 'sub', 'sup', 'big',
                                                      'small') or prevtag == 'p' and tagname in structural_tags:
                tags.pop()
                output('</%s>' % prevtag)
            if endslash:
                output('<%s%s>' % (tagname, attrs))
            elif tagname in self_closing_tags:
                if attrs.rstrip() == attrs:
                    attrs += ' '
                output('<%s%s/>' % (tagname, attrs))
                tags.append((TagName, pos))
            else:
                output('<%s%s>' % (tagname, attrs))
                tags.append((TagName, pos))
        elif m.group(3):
            TagName = re.match('/(\\w+)', innards).group(1)
            tagname = TagName.lower()
            if prevtag in self_closing_tags:
                if prevtag == tagname:
                    if result[(-1)].strip():
                        ERROR('Self-closing tag <%s/> is not empty' % tags[(-1)][0], tags[(-1)][1])
                    else:
                        result.pop()
                else:
                    tags.pop()
                    prevtag = tags and tags[(-1)][0].lower() or None
                    assert prevtag not in self_closing_tags
            if prevtag != tagname and (prevtag == 'p' and tagname in structural_tags or prevtag == 'li' and tagname in ('ol',
                                                                                                                        'ul') or prevtag == 'dd' and tagname == 'dl' or prevtag == 'area' and tagname == 'map' or prevtag == 'td' and tagname == 'tr' or prevtag == 'th' and tagname == 'tr'):
                output('</%s>' % prevtag)
                tags.pop()
                prevtag = tags and tags[(-1)][0].lower() or None
            if prevtag == tagname:
                if tagname not in self_closing_tags:
                    output(tag_match.group().lower())
                    tags.pop()
            else:
                ERROR('Unexpected closing tag </%s>' % TagName)
        elif m.group(4):
            ERROR('Malformed tag')
        else:
            output(ampfix(tag_match.group()))
        lastpos = tag_match.end()

    prevtag = tags and tags[(-1)][0].lower() or None
    if prevtag in cdata_tags:
        output(cdatafix(html[lastpos:]))
    else:
        output(ampfix(html[lastpos:]))
    while tags:
        (TagName, pos) = tags.pop()
        tagname = TagName.lower()
        if tagname not in self_closing_tags:
            output('</%s>' % tagname)

    result = ('').join(result)
    if not unicode_input:
        result = result.encode(encoding)
    return result


def test(html=None):
    if html is None:
        import sys
        if len(sys.argv) == 2:
            if sys.argv[1] == '-':
                html = sys.stdin.read()
            else:
                html = open(sys.argv[1]).read()
        else:
            sys.exit('usage: %s HTMLFILE' % sys.argv[0])
    xhtml = xhtmlify(html)
    try:
        assert xhtml == xhtmlify(xhtml)
    except ValidationError:
        print xhtml
        raise

    xmlparse(re.sub('(?s)<!(?!\\[).*?>', '', xhtml))
    if len(sys.argv) == 2:
        sys.stdout.write(xhtml)
    return xhtml


def xmlparse(snippet, encoding=None, wrap=None):
    r"""Parse snippet as XML with ElementTree/expat.  By default it wraps the
       snippet in an outer <document> element before parsing (unless the
       snippet starts "<?xml" or u"\ufeff<?xml").  This can be suppressed by
       setting wrap to True or forced by setting wrap to False."""
    import xml.parsers.expat
    from xml.etree import ElementTree as ET
    if wrap is None:
        wrap = not snippet.startswith('<?xml') and not snippet.startswith('\ufeff<?xml')
    try:
        if encoding:
            try:
                parser = ET.XMLParser(encoding=encoding)
            except TypeError:
                parser = ET.XMLParser()

        else:
            parser = ET.XMLParser()
        if wrap:
            input = '<document>\n%s\n</document>' % snippet
        else:
            input = snippet
        if isinstance(snippet, unicode):
            if not encoding:
                encoding = sniff_encoding(snippet)
            input = input.encode(encoding)
        parser.feed(input)
        parser.close()
    except xml.parsers.expat.ExpatError, e:
        lineno, offset = e.lineno, e.offset
        lineno -= 1
        if lineno == input.count('\n'):
            lineno -= 1
            offset = len(snippet) - snippet.rfind('\n')
        message = re.sub('line \\d+', 'line %d' % lineno, e.message, count=1)
        message = re.sub('column \\d+', 'column %d' % offset, message, count=1)
        parse_error = xml.parsers.expat.ExpatError(message)
        parse_error.lineno = lineno
        parse_error.offset = offset
        parse_error.code = e.code
        raise parse_error

    return


def sniff_encoding(xml):
    """Detects the XML encoding as per XML 1.0 section F.1."""
    if isinstance(xml, str):
        xmlstr = xml
    elif isinstance(xml, basestring):
        xmlstr = xml.encode('utf-8')
    else:
        raise TypeError('Expected a string, got %r' % type(xml))
    enc = sniff_bom_encoding(xmlstr)
    encode = codecs.lookup(enc).incrementalencoder().encode
    prefix = encode('')
    if enc in ('utf_16_le', 'utf_16_be'):
        prefix = ('\ufeff').encode(enc)
    L = lambda s: re.escape(encode(s))
    optional = lambda s: '(?:%s)?' % s
    oneof = lambda opts: '(?:%s)' % ('|').join(opts)
    charset = lambda s: oneof([ L(c) for c in s ])
    upper = charset('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    lower = charset('abcdefghijklmnopqrstuvwxyz')
    digit = charset('0123456789')
    digits = digit + '+'
    punc = charset('._-')
    name = '(?:%s%s*)' % (oneof([upper, lower]),
     oneof([upper, lower, digit, punc]))
    Ss = charset(' \t\r\n') + '*'
    Sp = charset(' \t\r\n') + '+'
    Eq = ('').join([Ss, L('='), Ss])
    VersionInfo = ('').join([
     Sp, L('version'), Eq,
     oneof([L("'1.") + digits + L("'"),
      L('"1.') + digits + L('"')])])
    EncodingDecl = ('').join([
     Sp, L('encoding'), Eq,
     oneof([
      L("'") + '(?P<enc_dq>%s)' % name + L("'"),
      L('"') + '(?P<enc_sq>%s)' % name + L('"')])])
    SDDecl = ('').join([
     Sp, L('standalone'), Eq,
     oneof([
      L("'") + oneof([L('yes'), L('no')]) + L("'"),
      L('"') + oneof([L('yes'), L('no')]) + L('"')])])
    R = ('').join([prefix, L('<?xml'), VersionInfo, optional(EncodingDecl),
     optional(SDDecl), Ss, L('?>')])
    m = re.match(R, xml)
    if m:
        encvalue = m.group('enc_dq')
        if encvalue is None:
            encvalue = m.group('enc_sq')
            if encvalue is None:
                return enc
        decl_enc = encvalue.decode(enc).encode('ascii')
        bom_codec = None

        def get_codec(encoding):
            encoding = encoding.lower()
            if encoding == 'ebcdic':
                encoding = 'cp037'
            elif encoding in ('utf_16_le', 'utf_16_be'):
                encoding = 'utf_16'
            return codecs.lookup(encoding)

        try:
            bom_codec = get_codec(enc)
        except LookupError:
            pass

        try:
            if bom_codec and enc == enc.lower() and get_codec(decl_enc) != bom_codec:
                raise ValidationError('Multiply-specified encoding (BOM: %s, XML decl: %s)' % (
                 enc, decl_enc), 0, 1, 1, [])
        except LookupError:
            pass

        return decl_enc
    else:
        return 'UTF-8'
        return


def sniff_bom_encoding(xml):
    """Reads any byte-order marker. Returns the implied encoding.
       If the returned encoding is lowercase it means the BOM uniquely
       identified an encoding, so we don't need to parse the <?xml...?>
       to extract the encoding in theory."""
    if not isinstance(xml, str):
        raise TypeError('Expected str, got %r' % type(xml))
    enc = {b'\x00\x00\xfe\xff': 'utf_32', 
       b'\xff\xfe\x00\x00': 'utf_32', 
       b'\x00\x00\xff\xfe': 'undefined', 
       b'\xfe\xff\x00\x00': 'undefined', 
       '\x00\x00\x00<': 'UTF_32_BE', 
       '<\x00\x00\x00': 'UTF_32_LE', 
       '\x00\x00<\x00': 'undefined', 
       '\x00<\x00\x00': 'undefined', 
       '\x00<\x00?': 'UTF_16_BE', 
       '<\x00?\x00': 'UTF_16_LE', 
       '<?xm': 'ASCII', 
       b'Lo\xa7\x94': 'CP037'}.get(xml[:4])
    if enc and enc == enc.lower():
        return enc
    if not enc:
        if xml[:3] == '\ufeff':
            return 'utf_8_sig'
        if xml[:2] == b'\xff\xfe':
            return 'utf_16_le'
        if xml[:2] == b'\xfe\xff':
            return 'utf_16_be'
        enc = 'UTF-8'
    return enc


if __name__ == '__main__':
    test()