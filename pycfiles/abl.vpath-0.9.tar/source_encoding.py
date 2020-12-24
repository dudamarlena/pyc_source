# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/errorreporter/util/source_encoding.py
# Compiled at: 2012-01-03 09:44:45
__doc__ = 'Parse a Python source code encoding string'
import codecs, re
PYTHON_MAGIC_COMMENT_re = re.compile('[ \\t\\f]* \\# .* coding[=:][ \\t]*([-\\w.]+)', re.VERBOSE)

def parse_encoding(lines):
    """Deduce the encoding of a source file from magic comment.

    It does this in the same way as the `Python interpreter`__

    .. __: http://docs.python.org/ref/encodings.html

    The ``lines`` argument should be a list of the first 2 lines of the
    source code.

    (From Jeff Dairiki)
    """
    try:
        line1 = lines[0]
        has_bom = line1.startswith(codecs.BOM_UTF8)
        if has_bom:
            line1 = line1[len(codecs.BOM_UTF8):]
        m = PYTHON_MAGIC_COMMENT_re.match(line1)
        if not m:
            try:
                import parser
                parser.suite(line1)
            except (ImportError, SyntaxError):
                pass
            else:
                line2 = lines[1]
                m = PYTHON_MAGIC_COMMENT_re.match(line2)
        if has_bom:
            if m:
                raise SyntaxError('python refuses to compile code with both a UTF8 byte-order-mark and a magic encoding comment')
            return 'utf_8'
        elif m:
            return m.group(1)
        else:
            return
    except:
        return

    return