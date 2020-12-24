# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\templ\templ.py
# Compiled at: 2013-07-26 13:23:14
"""
Copyright 2013 Brian Mearns

This file is part of templ.

templ is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

templ is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with templ.  If not, see <http://www.gnu.org/licenses/>.

"""
import teval, texec, types, ttypes, texceptions, tstreams, stack as tStack, io, os, filepos as tFilepos, tbuiltin, sys, errno, version, codecs
TOKEN_EOI = 0
TOKEN_SPACE = 1
TOKEN_OCUR = 2
TOKEN_CCUR = 3
TOKEN_SLASH = 4
TOKEN_QUOTE = 5
TOKEN_TEXT = 6
TOKEN_COMMENT = 7
TOKEN_OEMBED = 8
TOKEN_CEMBED = 9
STMT_EOI = 0
STMT_TEXT = 1
STMT_LIST = 2
STMT_CEMBED = 3
LINEBREAKS = ('\n', '\x0b', '\x0c', '\r', '\r\n', '\x85', '\u2028', '\u2029')

class TemplateProcessingError(texceptions.TemplateException):

    def __init__(self, cause, filepos=None):
        super(TemplateProcessingError, self).__init__(cause, filepos)

    def __str__(self):
        if self.filepos is None:
            filepos = ''
        else:
            filepos = ' ' + str(self.filepos)
        return 'Error%s: %s' % (filepos, self.message)


class TemplateSyntaxError(TemplateProcessingError):
    pass


def process(istream, ostream, scope=None, iname='<input-stream>', debug=False):
    stack = tStack.Stack(scope)
    processWithStack(istream, ostream, stack, iname, debug)


def processWithStack(istream, ostream, stack, iname='<input-stream>', debug=False):
    if not isinstance(istream, tstreams.TemplateInputStream):
        istream = tstreams.TemplateInputStream(istream, iname)
    try:
        while True:
            stmt, value, filepos = parse(istream)
            if stmt == STMT_EOI:
                return
            if stmt in (STMT_TEXT, STMT_CEMBED):
                if not isinstance(value, basestring):
                    raise AssertionError, repr(value)
                    value = isinstance(value, unicode) or unicode(value, 'latin1')
                try:
                    ostream.write(value)
                except UnicodeEncodeError as e:
                    raise texceptions.TemplateException(e, filepos)

            elif stmt == STMT_LIST:
                res = teval.evalExpression(value, ostream, stack)
                assert isinstance(res, ttypes.TType)
                if isinstance(res, ttypes.Null):
                    pass
                elif isinstance(res, ttypes.String):
                    string = res.str
                    if not isinstance(string, basestring):
                        raise AssertionError, repr(string)
                        string = isinstance(string, unicode) or unicode(string, 'latin1')
                    try:
                        ostream.write(string)
                    except UnicodeEncodeError as e:
                        raise texceptions.TemplateException(e, filepos)

                else:
                    raise texceptions.TemplateTypeException('Top level expression resulted in non-String value.', res.filepos, got=res)

    except texceptions.TemplateException as e:
        if debug:
            raise
        raise TemplateProcessingError(e, e.filepos)


def parse(istream):
    """
    Top level parser, handles both TEXT and LIST expressions (well, it delegates).
    """
    plaintext = None
    ptstart = None
    while True:
        token, text, filepos = lex(istream)
        if token == TOKEN_EOI:
            if plaintext is not None:
                longestEol = 0
                for eol in LINEBREAKS:
                    if plaintext.endswith(eol) and len(eol) > longestEol:
                        longestEol = len(eol)

                if longestEol > 0:
                    plaintext = plaintext[:-longestEol]
                return (STMT_TEXT, plaintext, ptstart)
            else:
                return (
                 STMT_EOI, None, filepos)

        elif token in (TOKEN_TEXT, TOKEN_SPACE, TOKEN_CCUR, TOKEN_QUOTE, TOKEN_COMMENT, TOKEN_OEMBED):
            if plaintext is None:
                plaintext = ''
                ptstart = filepos
            plaintext += text
        elif token == TOKEN_CEMBED:
            if plaintext is not None:
                istream.unget(text)
                return (
                 STMT_TEXT, plaintext, ptstart)
            else:
                return (
                 STMT_CEMBED, text, filepos)

        elif token == TOKEN_SLASH:
            content = ''
            token, text, dummy = lex(istream)
            while token == TOKEN_SLASH:
                content += '\\'
                token, text, dummy = lex(istream)

            if token in (TOKEN_OCUR, TOKEN_CCUR):
                content += text
            else:
                content += '\\' + text
            if plaintext is None:
                plaintext = ''
                ptstart = filepos
            plaintext += content
        elif token == TOKEN_OCUR:
            if plaintext is not None:
                istream.unget(text)
                return (
                 STMT_TEXT, plaintext, ptstart)
            expr = parseExpr(istream, filepos)
            if not isinstance(expr, ttypes.List):
                raise AssertionError
                return (
                 STMT_LIST, expr, filepos)

    return


def parseExpr(istream, filepos):
    """
    We've already read the opening curly brace, this has to parse the remainder of the expression
    up to an including the closing curly brace, and return a TType List it represents. Do NOT evaluate
    anything here, just build the expression tree.
    """
    elements = []
    myfilepos = filepos
    cur = None
    curstart = None
    while True:
        token, text, filepos = lex(istream)
        if token == TOKEN_EOI:
            raise TemplateSyntaxError('Input ended with expression unterminated.', myfilepos)
        elif token == TOKEN_SPACE:
            if cur is not None:
                elements.append(ttypes.String(cur, curstart))
                cur = None
                curstart = None
        elif token in (TOKEN_TEXT, TOKEN_SLASH):
            if cur is None:
                cur = ''
                curstart = filepos
            cur += text
        elif token == TOKEN_QUOTE:
            if cur is None:
                cur = ''
                curstart = filepos
            cur += parseStringLiteral(istream, filepos)
        elif token == TOKEN_COMMENT:
            if cur is not None:
                elements.append(ttypes.String(cur, curstart))
                cur = None
                curstart = None
            comment = text
            while True:
                c = istream.read(1)
                if len(c) == 0:
                    raise TemplateSyntaxError('Input ended with expression unterminated.', myfilepos)
                comment += c
                if any(comment.endswith(lb) for lb in LINEBREAKS):
                    unget = True
                    while any(comment.endswith(lb) for lb in LINEBREAKS):
                        c = istream.read(1)
                        if len(c) == 0:
                            unget = False
                            break
                        comment += c

                    if unget:
                        istream.unget(comment[(-1)])
                        comment = comment[:-1]
                    break

        elif token == TOKEN_OEMBED:
            if cur is not None:
                elements.append(ttypes.String(cur, curstart))
                cur = None
                curstart = None
            embedded = ["'"]
            embeddedStart = filepos
            while True:
                stmt, value, filepos = parse(istream)
                if stmt == STMT_EOI:
                    raise TemplateSyntaxError('Input ended with expression unterminated.', myfilepos)
                elif stmt == STMT_TEXT:
                    embedded.append(ttypes.String(value, filepos))
                elif stmt == STMT_CEMBED:
                    break
                elif stmt == STMT_LIST:
                    assert isinstance(value, ttypes.List)
                    embedded.append(value)

            elements.append(ttypes.List(embedded, embeddedStart))
        elif token == TOKEN_CEMBED:
            raise TemplateSyntaxError('Input >>> in expression. This is a reserved token inside expressions, to use it as a string, it must be quoted.', myfilepos)
        else:
            if token == TOKEN_CCUR:
                if cur is not None:
                    elements.append(ttypes.String(cur, curstart))
                return ttypes.List(elements, myfilepos)
            if token == TOKEN_OCUR:
                if cur is not None:
                    elements.append(ttypes.String(cur, curstart))
                    cur = None
                    curstart = None
                expr = parseExpr(istream, filepos)
                assert isinstance(expr, ttypes.List)
                elements.append(expr)
            else:
                raise AssertionError('Unknown token %d' % token)

    return


def parseStringLiteral(istream, filepos):
    string = ''
    while True:
        c = istream.read(1)
        if len(c) == 0:
            raise TemplateSyntaxError('Input ended with string-literal unterminated.', filepos)
        else:
            if c == '"':
                return string
            if c == '\\':
                c = istream.read(1)
                if len(c) == 0:
                    raise TemplateSyntaxError('Input ended with string-literal unterminated.', filepos)
                string += c
            else:
                string += c


def lex(istream):
    filepos = istream.getPosition()
    c = istream.read(1)
    if len(c) == 0:
        return (
         TOKEN_EOI, '', filepos)
    if c.isspace():
        space = c
        while True:
            c = istream.read(1)
            if len(c) == 0:
                break
            elif c.isspace():
                space += c
            else:
                istream.unget(c)
                break

        return (
         TOKEN_SPACE, space, filepos)
    if c == '{':
        return (
         TOKEN_OCUR, c, filepos)
    if c == '}':
        return (
         TOKEN_CCUR, c, filepos)
    if c == '\\':
        return (TOKEN_SLASH, c, filepos)
    if c == '"':
        return (TOKEN_QUOTE, c, filepos)
    if c == '%':
        return (TOKEN_COMMENT, c, filepos)
    if c == '<':
        text = '<'
        while True:
            c = istream.read(1)
            if len(c) == 0:
                return (
                 TOKEN_TEXT, text, filepos)
            if c == '<':
                text += c
                if text == '<<<':
                    return (
                     TOKEN_OEMBED, text, filepos)
            else:
                istream.unget(c)
                return (
                 TOKEN_TEXT, text, filepos)

    elif c == '>':
        text = '>'
        while True:
            c = istream.read(1)
            if len(c) == 0:
                return (
                 TOKEN_TEXT, text, filepos)
            if c == '>':
                text += c
                if text == '>>>':
                    return (
                     TOKEN_CEMBED, text, filepos)
            else:
                istream.unget(c)
                return (
                 TOKEN_TEXT, text, filepos)

    else:
        text = c
        while True:
            c = istream.read(1)
            if len(c) == 0:
                break
            elif c.isspace() or c in ('{', '}', '\\', '"', '%', '>'):
                istream.unget(c)
                break
            else:
                text += c

        return (
         TOKEN_TEXT, text, filepos)


def printVersion(ostream):
    ostream.write(('templ v{version} - {datestr}\n\n').format(version=version.string(), datestr=version.datestr()))


def printUsage(ostream, argv=sys.argv):
    ostream.write(('Usage: {PROG} [options] [TEMPLATE_FILE [OUTFILE]]\n   or: {PROG} [options] - [OUTFILE]\n\n').format(PROG=argv[0]))


def printHelp(ostream, argv=sys.argv):
    printVersion(ostream)
    printUsage(ostream, argv)
    ostream.write(('Processes TEMPLATE_FILE through the templ processor, writing the output to\nOUTFILE. In the second usage, the use of "-" as the TEMPLATE_FILE indicates\nthat the template should be read from STDIN. This is also the default if\nTEMPLATE_FILE is not specified. Likewise, a dash can be used for OUTFILE to\nindicate that output should be written to STDOUT, which is also the default if\nOUTFILE is not given.\n\nOptions:\n -s, --set NAME [VALUE]         Adds a symbol named NAME to the global scope\n                                with a String type value given by VALUE. If\n                                VALUE is not given, a NULL value is used.\n\n -b, --binary                   Opens the input and output files in binary\n                                mode, when possible. This is not possible for\n                                standard streams (STDIN or STDOUT).\n\n -e, --in-enc ENCODING          Specify the encoding to use when reading the \n                                input. Default is Latin-1 (one char per\n                                octet read). Other options include UTF-8,\n                                UTF-16, and UTF-32. Use --help-enc for more\n                                details on encoding.\n\n -E, --out-enc ENCODING         Specify the encoding to use when writing to\n                                the output. Default is Latin-1 (sometimes\n                                called "extended ASCII", this is one octet\n                                per char, chars with values greater than 255\n                                will cause an error). Other options include\n                                UTF-8, UTF-16, and UTF-32. Use --help-enc for\n                                more details on encoding.\n\nMisc Options:\n --debug                        Enable debug output.\n\n -V, --version                  Print the version string and exit.\n\n --usage                        Print a brief usage message and exit.\n\n --help-enc                     Print help on encoding.\n\n --help                         Print this help menu.\n\n\n\nCopyright {COPYRIGHT} Brian Mearns. Program licensed under GNU AGPLv3.\n\nFor more information about this product see:\n            <https://bitbucket.org/bmearns/templ/>.\n').format(COPYRIGHT=version.COPYRIGHT))


def printEncodingHelp(ostream, argv=sys.argv):
    printVersion(ostream)
    ostream.write(('\nEncoding:\n\nFor most English-language templates, the default encoding, Latin-1, will work\nfine. ASCII is a subset of Latin-1 for codepoints 0-127, and Latin-1 adds a\nnumber of common accented characters in the range from 128 through 255.\n\nLatin-1 also works well if you plan to generate binary output, because octet\nvalues will not be changed by the output encoder. For instance in Latin-1, the\ntempl code...\n    {chr 144}\n...will produce a single octet of output, with octet value 0x90. On the other\nhand, if the output encoding is set to UTF-8, the same code will produce two\noctets of output, the first with value 0xC2, then second with value 0x90.\n\nFor input encoding, the default of Latin-1 is usually sufficient for most\ntemplates, including those stored in ASCII, Latin-1, or UTF-8. Even if the\ntemplate is stored in UTF-8, the Latin-1 input encoding will simply read each\nbyte as a single char and will not produce any encoding errors. Since all\ncharacters that are of significance to templ itself are in the ASCII subset\nanyway (a subset of both Latin-1 and UTF-8), templ will not have any trouble\nunderstanding the input.\n\nHowever, there are two likely sources of problems using Latin-1 input\nencoding for a UTF-8 template. First, the string length of text that\noriginated in the template may not be correct. For instance, if the template\nincludes a unicode inverted question mark (codepoint U+00BF), this will be\nstored as two octets in the UTF-8 encoded template file (0xC2 0xBF). The\nstring only contains one character (U+00BF) in UTF-8, but when read with\nLatin-1 input encoding, it will result in a string with two chracters (\\xC2\nand \\xBF).\n\nThe second potential issue depends on the output encoding used. If you use\nLatin-1 output encoding, it will work fine (other than as discussed above):\nthe exact octets that appeared in the input template will also appear in the\noutput, which will be interpretted correctly by a UTF-8 reader. However, if\nyou use any of the UTF encodings for output, then each octet in the input\ntemplate could be encoded to multiple octets in the output. For instance, if\nthe input template once again contains unicode character U+00BF (inverted\nquestion mark) in UTF-8, it will be read in Latin-1 as a two-character string,\nwith codepoint \\u00C2 and \\u00BF. If this is then written out using UTF-8\nencoding, it will produce four octets in total: the character \\u00C2 (Latin\ncapital letter A with circumflex) will be encoded as two octets as\n0xC3 0x82, and the character \\u00BF (inverted question mark) will once again\nbe encoded as two octets 0xC2 0xBF.\n\nThe best solution is to use the correct input encoding based on how the\ntemplate is stored. If it uses only ASCII characters and is stored using ASCII\nencoding, then the default will work fine. Likewise, if it is a binary file\nwhich contains non-textual binary octets, the default encoding will work well.\nBut if the file is stored in any other encoding (UTF-8 being common for\nnon-English language documents), then specify the same as the input encoding\nwhen invoking templ.\n\nThe output encoding is really just a matter of how you want to store the\noutput. If the output only contains ASCII characters, or if it contains\nnon-textual binary octets, the default encoding, Latin-1, should work fine.\nHowever, if you attempt to output any string which includes a codepoint\ngreater than 255, then Latin-1 encoding will not work and you will get an\nerror.\n\n\nCopyright {COPYRIGHT} Brian Mearns. Program licensed under GNU AGPLv3.\n\nFor more information about this product see:\n            <https://bitbucket.org/bmearns/templ/>.\n').format(COPYRIGHT=version.COPYRIGHT))


def main():
    templates = []
    infile = None
    outfile = None
    globs = texec.getGlobalScope()
    debug = False
    binary = False
    in_enc = 'latin'
    out_enc = 'latin'
    i = 1
    argc = len(sys.argv)
    while i < argc:
        arg = sys.argv[i]
        i += 1
        if arg in ('-h', '-?', '/?', '--help'):
            printHelp(sys.stdout, sys.argv)
            return 0
        if arg in ('--help-enc', ):
            printEncodingHelp(sys.stdout, sys.argv)
            return 0
        if arg in ('-V', '--version'):
            printVersion(sys.stdout)
            return 0
        if arg in ('--usage', ):
            printUsage(sys.stdout, sys.argv)
            return 0
        if arg in ('--debug', ):
            debug = True
        elif arg in ('-b', '--binary'):
            binary = True
        elif arg in ('-s', '--set'):
            if i == argc:
                sys.stderr.write('%s: Error: Missing required parameter for option %s.\n' % (sys.argv[0], arg))
                sys.stderr.write('%s: Try `%s --help`\n' % (sys.argv[0], sys.argv[0]))
                return errno.EINVAL
            name = sys.argv[i]
            i += 1
            fp = tFilepos.CommandLineFilepos.new(i)
            if i < argc:
                value = sys.argv[i]
                value = ttypes.String(value, filepos=fp)
                i += 1
            else:
                value = ttypes.Null(filepos=fp)
            globs[name] = value
        elif arg in ('-e', '--in-enc'):
            if i == argc:
                sys.stderr.write('%s: Error: Missing required parameter for option %s.\n' % (sys.argv[0], arg))
                sys.stderr.write('%s: Try `%s --help`\n' % (sys.argv[0], sys.argv[0]))
                return errno.EINVAL
            in_enc = sys.argv[i]
            i += 1
        elif arg in ('-E', '--out-enc'):
            if i == argc:
                sys.stderr.write('%s: Error: Missing required parameter for option %s.\n' % (sys.argv[0], arg))
                sys.stderr.write('%s: Try `%s --help`\n' % (sys.argv[0], sys.argv[0]))
                return errno.EINVAL
            out_enc = sys.argv[i]
            i += 1
        elif infile is None:
            infile = arg
        elif outfile is None:
            outfile = arg
        else:
            sys.stderr.write('%s: Error: Unexpected argument "%s".\n' % (sys.argv[0], arg))
            sys.stderr.write('%s: Try `%s --help`\n' % (sys.argv[0], sys.argv[0]))
            return errno.EINVAL

    istream = None
    ostream = None
    try:
        if infile is None or infile == '-':
            iname = '<stdin>'
            istream = sys.stdin
        else:
            iname = infile
            mode = 'r'
            if binary:
                mode += 'b'
            istream = open(iname, mode)
        try:
            istream = codecs.getreader(in_enc)(istream)
        except LookupError as e:
            sys.stderr.write('Error: unknown encoding for --in-enc.\n')
            try:
                istream.close()
            except:
                pass

            return -1

        if outfile is None or outfile == '-':
            ostream = sys.stdout
        else:
            mode = 'w'
            if binary:
                mode += 'b'
            ostream = open(outfile, mode)
        try:
            ostream = codecs.getwriter(out_enc)(ostream)
        except LookupError as e:
            sys.stderr.write('Error: unknown encoding for --out-enc.\n')
            try:
                ostream.close()
            except:
                pass

            return -1

        ostream = tstreams.TemplateStreamOutputStream(ostream)
        try:
            process(istream, ostream, globs, iname, debug)
        except TemplateProcessingError as e:
            if debug:
                raise
            try:
                istream.close()
            except Exception:
                pass

            try:
                ostream.close()
            except Exception:
                pass

            sys.stderr.write(str(e) + '\n')
            return -1

        try:
            istream.close()
        except Exception:
            pass

        try:
            ostream.close()
        except Exception:
            pass

    except IOError as e:
        if debug:
            raise e
        if istream is not None:
            try:
                istream.close()
            except Exception:
                pass

        if ostream is not None:
            try:
                ostream.close()
            except Exception:
                pass

        sys.stderr.write('An IO Error occurred: %s\n' % str(e))
        return errno.EIO

    return


if __name__ == '__main__':
    ec = main()
    sys.exit(ec)