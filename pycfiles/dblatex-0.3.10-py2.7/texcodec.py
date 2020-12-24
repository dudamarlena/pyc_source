# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dbtexmf/dblatex/texcodec.py
# Compiled at: 2017-04-03 18:58:57
import re, codecs, unient
tex_handler_installed = {}
tex_handler_counter = {}

def latex_char_replace(exc, pre, post, name):
    global tex_handler_counter
    if not isinstance(exc, UnicodeEncodeError):
        raise TypeError("don't know how to handle %r" % exc)
    l = []
    n = tex_handler_counter[name]
    for c in exc.object[exc.start:exc.end]:
        if pre:
            l.append(pre)
        try:
            l.append(unient.unicode_map[ord(c)])
        except KeyError:
            print 'Missing character &#x%x;' % ord(c)
            l.append('\\&\\#x%x;' % ord(c))

        if post:
            l.append(post)
        n = n + 1

    tex_handler_counter[name] = n
    return (('').join(l), exc.end)


class TexCodec:
    charmap = {b'\xa0': '~', 
       b'\xa5': '$\\yen$', 
       b'\xac': '\\ensuremath{\\lnot}', 
       b'\xb0': '\\textdegree{}', 
       b'\xb1': '\\ensuremath{\\pm}', 
       b'\xb2': '$^2$', 
       b'\xb3': '$^3$', 
       b'\xb5': '$\\mathrm{\\mu}$', 
       b'\xb9': '$^1$', 
       b'\xd7': '$\\times$', 
       b'\xf7': '$\\div$'}

    def __init__(self, input_encoding='utf8', output_encoding='latin-1', errors='latexcharreplace', pre='', post=''):
        self._errors = errors
        self._decode = codecs.getdecoder(input_encoding)
        self._encode = codecs.getencoder(output_encoding)
        if input_encoding == output_encoding:
            self.charmap = {}
            return
        if not tex_handler_installed.has_key(self._errors):
            f = self.build_error_func(pre, post, errors)
            codecs.register_error(self._errors, f)
            tex_handler_installed[self._errors] = f
            self.clear_errors()

    def clear_errors(self):
        tex_handler_counter[self._errors] = 0

    def get_errors(self):
        return tex_handler_counter[self._errors]

    def build_error_func(self, pre='', post='', errors='charrep'):
        return lambda exc: latex_char_replace(exc, pre, post, errors)

    def decode(self, text):
        return self._decode(text)[0]

    def encode(self, text):
        text = self._encode(text, self._errors)[0]
        for c, v in self.charmap.items():
            text = text.replace(c, v)

        return text


class LatexCodec(TexCodec):

    def __init__(self, input_encoding='utf8', output_encoding='latin-1'):
        TexCodec.__init__(self, input_encoding, output_encoding)
        self.texres = (
         (
          re.compile('^[\\s\n]*$'), ' '),
         (
          re.compile('([{}%_^$&#])'), '\\\\\\1'),
         (
          re.compile('([-^<>])'), '\\1{}'),
         (
          re.compile('`'), '\\\\`{}'),
         (
          re.compile('~'), '\\\\textasciitilde{}'))

    def _texescape(self, text):
        for r, s in self.texres:
            text = r.sub(s, text)

        return text

    def encode(self, text):
        text = text.replace('\\', '\\textbackslash')
        text = self._texescape(text)
        text = self._encode(text, self._errors)[0]
        for c, v in self.charmap.items():
            text = text.replace(c, v)

        text = text.replace('\\textbackslash', '\\textbackslash{}')
        return text


def main():
    import sys
    c = LatexCodec()
    f = open(sys.argv[1])
    text = ''
    for line in f:
        text += c.encode(c.decode(line))
        if text:
            sys.stdout.write(text)


if __name__ == '__main__':
    main()